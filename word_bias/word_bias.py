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
    content = data["content"]
    for word in content.split(): #iterate all the words in the content section
        """
        for char in word:
            if(char == '(' or char == ')' or char== ','):
                word.remove(char)
        """
        if word in positive_words:
            num_pos_words += 1
        if word in negative_words:
            num_neg_words += 1

        """ find if a word is in the phrase at all, then count it
        for controv_phrase in controversial_words:
            split = controv_phrase.split()
            if(word in split):
                num_controversial_words +=1
                """
        """ dumb counter, will only count if the word matches the controversial phrase exactly, which is very rare
        if word in controversial_words:
            num_controversial_words += 1
        """

    # use regular expression to see if the controversial phrase is found in the entire article
    # may be intractable, will have to see when running on the whole dataset
    for controversial_phrase in controversial_words:
        regex = re.compile("%s" % controversial_phrase)
        match = regex.findall(content)
        num_controversial_words += len(match)

    output["pageid"] = data["pageid"] # put the page id in here so that it can create the right csv
    output["num_positive_words"] = num_pos_words
    output["num_negative_words"] = num_neg_words
    output["num_controversial_words"] = num_controversial_words

    print("Positive Words: ", num_pos_words)
    print("Negative Words: ", num_neg_words)
    print("Controversial Words: ", num_controversial_words)

    return output;

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
