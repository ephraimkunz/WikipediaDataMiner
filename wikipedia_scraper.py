from __future__ import print_function
import wikipedia
import json
import os
import time

directory = "./articles"

# Skipped pages because of errors
skipped = []

# Array of dicts to serialize to json
articles = []

# Get controversial articles
def get_controversial_list():
    print("Getting list of controversial articles...")
    controversial = wikipedia.page("Wikipedia:List of controversial issues")
    links = controversial.links
    print("Found %d controversial articles" % len(links))
    return links

def get_articles_in_list(names, callback):
    fetched = 0
    for link in names:
        page = None
        try:
            page = wikipedia.page(link, auto_suggest=False)
        except Exception as e:
            skipped.append(link)
            print("Error fetching %s, skipping" % link)
            continue
            
        callback(page, fetched)

        if fetched % 20 == 0:
            print("Fetched %d of %d articles: %f%%" % (fetched, len(names), (float(fetched) / len(names) * 100)))

        fetched += 1

def dump_data_to_file(file_prefix, count):
    structure = {}
    structure["skipped"] = skipped
    structure["controversial"] = articles

    filename = file_prefix + "_" + str(count) + ".json"

    print("Dumping %d articles and %d skipped to file %s..." % (len(articles), len(skipped), filename))

    with open(directory + '/' + filename, "w+") as f:
        json.dump(structure, f, indent=4, sort_keys=True)

    # Clear data
    del skipped[:]
    del articles[:]

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
            articles.append(dic)
        except Exception as e:
            print("Failure to parse %s" % article.title)
            skipped.append(article.title)

        if count > 0 and count % 100 == 0:
            dump_data_to_file(file_prefix, count)

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

if __name__ == "__main__":
    # Set up scraper responsibly
    start = time.time()
    wikipedia.set_rate_limiting(True)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Get controversial articles
    cont = get_controversial_list()
    #get_articles_in_list(cont, handle_article("controversial"))

    # Dump anything left to a file
    #dump_data_to_file("controversial", "last")



    # Get non-controversial articles
    normal = get_random_list(len(cont), cont)
    get_articles_in_list(normal, handle_article("normal"))
    dump_data_to_file("controversial", "last")

    end = time.time()
    print("Scrape took %f seconds" % (end - start))
    print("Done")
