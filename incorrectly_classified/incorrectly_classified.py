import glob
import csv
import wikipedia

filenames = glob.glob("/Users/ephraimkunz/Desktop/WikipediaDataMiner/incorrectly_classified/*.txt")
wrong = {}

for filename in filenames:
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=",")
        on_header = True
        for row in reader:
            if len(row) == 0:
                continue
            if on_header:
                on_header = False
                continue
            
            pageid = row[5]
            confidence = float(row[4])
            actual = row[1]
            predicted = row[2]

            if predicted != actual:
                false_pos = actual == "2:no"
                if pageid not in wrong.keys():
                    wrong[pageid] = [("false_pos" if false_pos else "false_neg", confidence)]
                else:
                    wrong[pageid].append(("false_pos" if false_pos else "false_neg", confidence))


# Lookup pageids for the mostly wrong
item_list = []
for k, v in wrong.iteritems():
    item_list.append((k, v[0][0], v[0][1]))

item_list.sort(key=lambda x: x[2], reverse=True)

top = [x for x in item_list if x[2] >= 0.9]

print()
for item in top:
    page = wikipedia.page(pageid=item[0])
    print("%s (%0.1f%%): %s" % (page.title, item[2] * 100, item[1]))