from __future__ import print_function
import wikipedia
import json
import os
import requests
import sys
import datetime

directory = "./binned_articles"

# Each bin is start, end, count
bins = [
    (0, 7346, 78),
    (7347, 14626, 131),
    (14627, 21905, 336),
    (21906, 29185, 142), 
    (29186, 36465, 131), 
    (36466, 43745, 115), 
    (43746, 51025, 108), 
    (51026, 58304, 113),
    (58305, 65584, 76), 
    (65585, 72864, 61), 
    (72865, 80144, 61),
    (80145, 87424, 37),
    (87425, 94703, 38),
    (94704, 101983, 22),
    (101984, sys.maxint, 41)]

# Array of dicts to serialize to json
articles = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

# Cache articles needed for each bin so we don't have to do so many len checks
articles_needed = [bin[2] for bin in bins]

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
                print("Error fetching %s: %s, skipping" % (link, e))
                continue
            
        success = callback(page, fetched)
        if not success:
            continue

        if fetched % 1 == 0 and fetched != 0:
            print("Fetched %d of %d articles: %f%%" % (fetched, len(names), (float(fetched) / len(names) * 100)))

        fetched += 1

# Create a file with the file_prefix and count and dump json into it
def dump_data_to_file():
    for i in range(len(articles)):
        structure = {}
        structure["articles"] = articles[i]

        filename = "bin_" + str(i) + ".json"

        print("Dumping %d articles to file %s..." % (len(articles[i]), filename))

        with open(directory + '/' + filename, "w+") as f:
            json.dump(structure, f, indent=4, sort_keys=True)

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
def handle_article(article, count):
    content = article.content
    len_content = len(content)
    
    for i in range(len(bins)):
        bin = bins[i]
        if articles_needed[i] > 0 and len_content >= bin[0] and len_content <= bin[1]:
            try:
                dic = {}
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
                articles[i].append(dic)
                articles_needed[i] -= 1
            except Exception as e:
                print("Failure to parse %s: %s" % (article.title, e))
                return False
    return True

if __name__ == "__main__":   
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Get random articles and fill bins
    current = datetime.datetime.now()
    dump_time = current + datetime.timedelta(minutes = 10)

    while True:
        arts = wikipedia.random(10)
        get_articles_in_list(arts, handle_article)

        current = datetime.datetime.now()
        if current >= dump_time:
            dump_time = current + datetime.timedelta(minutes = 10)
            dump_data_to_file()

    print("Done")
