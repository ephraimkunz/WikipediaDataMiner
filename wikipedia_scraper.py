from __future__ import print_function
import wikipedia
import json
import os
import time
import requests

directory = "./articles"

# Skipped pages because of errors
skipped = []

# Array of dicts to serialize to json
articles = []

# Get array of controversial article names
def get_controversial_list():
    print("Getting list of controversial articles...")
    controversial = wikipedia.page("Wikipedia:List of controversial issues")
    links = controversial.links
    print("Found %d controversial articles" % len(links))
    return links

# Given a list of article names and a callback, lookup each name and apply the callback to it
def get_articles_in_list(names, callback):
    fetched = 0
    for link in names:
        page = None
        try:
            page = wikipedia.page(link)
        except Exception:
            try:
                page = wikipedia.page(link, auto_suggest=False) # Turning off autosuggest sometimes helps us.
            except Exception as e:
                skipped.append(link)
                print("Error fetching %s: %s, skipping" % (link, e))
                continue
            
        success = callback(page, fetched)
        if not success:
            continue

        if fetched % 1 == 0 and fetched != 0:
            print("Fetched %d of %d articles: %f%%" % (fetched, len(names), (float(fetched) / len(names) * 100)))

        fetched += 1

# Create a file with the file_prefix and count and dump json into it
def dump_data_to_file(file_prefix, count):
    structure = {}
    structure["articles"] = articles

    filename = file_prefix + "_" + str(count) + ".json"

    print("Dumping %d articles to file %s..." % (len(articles), filename))

    with open(directory + '/' + filename, "w+") as f:
        json.dump(structure, f, indent=4, sort_keys=True)

    # Clear data
    del articles[:]

# Return continuation if exists, else False. Continue param is specific to what type of query we are doing.
def get_continuation(data, continue_param):
    if 'continue' in data:
        continuation = data['continue'][continue_param]
        assert(continuation and 'batchcomplete' not in data)
        return continuation
    
    assert 'batchcomplete' in data
    return False

def get_inbound(data, pageid):
    linkshere = data['query']['pages'][pageid]['linkshere']
    return list(map(lambda x: x['title'], linkshere))

def get_edits(data, pageid):
    edits = data['query']['pages'][pageid]['revisions']
    return list(map(lambda x: x['timestamp'], edits))

# Returns array of revision timestamps of this page
def get_revisions(pageid):
    results = []
    raw_url = "https://en.wikipedia.org//w/api.php?action=query&format=json&prop=revisions&pageids={}&rvprop=timestamp&rvlimit=max"
    continue_param = 'rvcontinue'

    first_page = raw_url.format(pageid)
    resp = requests.get(first_page)
    data = json.loads(resp.text)

    results.extend(get_edits(data, pageid))

    continuation = get_continuation(data, continue_param)
    while continuation:
        next_page = raw_url + '&' + continue_param + '={}'
        next_page = next_page.format(pageid, continuation)

        resp = requests.get(next_page)
        data = json.loads(resp.text)
        results.extend(get_edits(data, pageid))
        continuation = get_continuation(data, continue_param)

    results.sort()
    return results

# Returns array of page titles inbound to this page
def get_inbound_links(pageid):
    results = []
    raw_url = "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=linkshere&pageids={}&lhprop=title&lhnamespace=0&lhlimit=max"
    continue_param = 'lhcontinue'
    
    first_page = raw_url.format(pageid)
    resp = requests.get(first_page)
    data = json.loads(resp.text)

    results.extend(get_inbound(data, pageid))

    continuation = get_continuation(data, continue_param)
    while continuation:
        next_page = raw_url + '&' + continue_param + '={}'
        next_page = next_page.format(pageid, continuation)

        resp = requests.get(next_page)
        data = json.loads(resp.text)
        results.extend(get_inbound(data, pageid))
        continuation = get_continuation(data, continue_param)

    results.sort()
    return results



# Callback for get_articles_in_list
def handle_article(file_prefix):
    def inner_handle_article(article, count):
        dic = {}
        try:
            dic["title"] = article.title
            dic["pageid"] = article.pageid
            dic["url"] = article.url
            dic["content"] = article.content
            dic["categories"] = article.categories
            dic["image_urls"] = article.images
            dic["links"] = article.links
            dic["references"] = article.references
            dic['inbound_links'] = get_inbound_links(article.pageid)
            dic['revisions'] = get_revisions(article.pageid)
            articles.append(dic)
        except Exception as e:
            print("Failure to parse %s: %s" % (article.title, e))
            skipped.append(article.title)
            return False

        if count > 0 and count % 100 == 0:
            dump_data_to_file(file_prefix, count)
        
        return True

    return inner_handle_article

# Get a random list of wikipedia articles about count big, avoiding articles found in avoid
def get_random_list(count, avoid):
    result = []

    print("Building list of random pages...")
    while len(result) < count:
        pages = wikipedia.random(10)
        pages = [page for page in pages if page not in avoid and page not in result]
        result.extend(pages)
    return result

# Dumps list of skipped articles to file
def dump_skipped_to_file(postfix):
    structure = {}
    structure["skipped"] = skipped

    filename = "skipped_" + postfix + ".json"

    print("Dumping %d skipped names to file %s..." % (len(skipped), filename))

    with open(directory + '/' + filename, "w+") as f:
            json.dump(structure, f, indent=4, sort_keys=True)

    # Clear data
    del articles[:]

if __name__ == "__main__":
    # Set up scraper responsibly
    start = time.time()
    wikipedia.set_rate_limiting(True)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Get controversial articles
    cont = get_controversial_list()
    get_articles_in_list(cont, handle_article("controversial"))

    # Dump anything left to a file
    dump_data_to_file("controversial", "last")

    # Get non-controversial articles
    normal = get_random_list(1500, cont)
    get_articles_in_list(normal, handle_article("normal"))
    dump_data_to_file("normal", "last")

    dump_skipped_to_file("all")

    end = time.time()
    print("Scrape took %f seconds" % (end - start))
    print("Done")
