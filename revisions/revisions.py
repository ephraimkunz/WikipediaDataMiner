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

    revision_strings = data["revisions"]
    revisions = map(lambda x: dateutil.parser.parse(x), revision_strings)

    oldest = min(revisions)
    
    output["article_age_in_days"] = (datetime.datetime.now(datetime.timezone.utc) - oldest).days
    output["avg_revs_per_day"] = len(revision_strings) / output["article_age_in_days"]
    return output

trans = Transformer("../articles/", "./revisions-binned.csv", revisions)
trans.run()