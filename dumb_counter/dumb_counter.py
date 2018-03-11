import sys

sys.path.append('..')

from transformer.transformer import Transformer

def dumb_counter(data, count):
    output = {}
    output["pageid"] = data["pageid"]
    output["num_categories"] = len(data["categories"])
    output["num_words"] = len(data["content"])
    output["num_images"] = len(data["image_urls"])
    output["num_links_in"] = len(data["inbound_links"])
    output["num_links_out"] = len(data["links"])
    output["num_references"] = len(data["references"])
    return output

trans = Transformer("../articles/", "./dumb_counts_binned.csv", dumb_counter)
trans.run()