import sys

sys.path.append('..')

from transformer.transformer import Transformer

def dumb_counter(data):
    output = {}
    output["pageid"] = data["pageid"]
    return output

trans = Transformer("../articles/", "./dumb_counts.csv", dumb_counter)
trans.run()