import sys
import os
import re
import dateutil.parser
import datetime

sys.path.append('..')

from transformer.transformer import Transformer

def word_bias(data, count):
    if count % 20 == 0:
        print(count)

    output = {}
    num_pos_words = 0;
    num_neg_words = 0;
    num_controversial_words = 0;
    for word in data["content"].split(): #iterate all the words in the content section
        """
        for char in word:
            if(char == '(' or char == ')' or char== ','):
                word.remove(char)
        """
        if word in positive_words:
            num_pos_words += 1
        if word in negative_words:
            num_neg_words += 1

        """
        # because controversial words can be phrases, use regular expressions instead
        for controv_word in controversial_words:
            regex = re.compile(" %s " % controv_word)
            match = regex.findall(controv_word)
            if(len(match) > 0):
                num_controversial_words += 1;
        """

        if word in controversial_words:
            num_controversial_words += 1


        print(word)
    print("Positive Words: ", num_pos_words)
    print("Negative Words: ", num_neg_words)
    print("Controversial Words: ", num_controversial_words)
    #print(data["content"])
    """
    output["pageid"] = data["pageid"]

    revision_strings = data["revisions"]
    revisions = map(lambda x: dateutil.parser.parse(x), revision_strings)

    oldest = min(revisions)

    output["article_age_in_days"] = (datetime.datetime.now(datetime.timezone.utc) - oldest).days
    output["avg_revs_per_day"] = len(revision_strings) / output["article_age_in_days"]
    return output
    """

def load_words(file):
    # Check for valid paths
    content = set();
    if not os.path.exists(file):
        raise ValueError("Input path {} does not exist".format(file))

    #followed stack overflow https://stackoverflow.com/questions/3277503/how-do-i-read-a-file-line-by-line-into-a-list
    with open(file) as f:
        next(f) # skip first line of file
        next(f) # skip second line of file
        content = f.readlines(); #read the rest of the files

    content = [x.strip() for x in content] # get rid of all whitespace
    content = [x.lower() for x in content] # make all lowercase for easy checking

    return content



positive_words = load_words("positive_words.txt")
negative_words = load_words("negative_words.txt")
controversial_words = load_words("controversial_topics_mod.txt")
print(positive_words)
print(negative_words)
print(controversial_words)


trans = Transformer("../raw_data/", "./word_bias.csv", word_bias)
trans.run()
