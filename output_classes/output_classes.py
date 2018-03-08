import sys
import dateutil.parser
import datetime

sys.path.append('..')

from transformer.transformer import Transformer

def revisions(data, count):
    if count % 20 == 0:
        print(count)

    output = {}
    output["pageid"] = data["pageid"]

    output["class"] = "yes"
    return output

trans = Transformer("../articles/", "./output_classes_binned_yes.csv", revisions)
trans.run()