import csv

fileList = ["dumb_counter/dumb_counts.csv", "output_classes/output_classes.csv", "revisions/revisions.csv", "word_bias/word_bias.csv", "tld_transform/tld.csv"]
output = "combined.arff"

datasets = [] # array of dicts that look like this: {pageId: {attributes}, pageId: {attributes}}

for filename in fileList:
    data = {}
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for item in reader:
            deletedPageId = dict(item) # Copy it so we can modify it
            del deletedPageId["pageid"]
            data[item["pageid"]] = deletedPageId
    a = len(data)
    datasets.append(data)

# Join on pageid across all datasets

# Make sure all datasets are the same length
length = len(datasets[1])
for ds in datasets:
    assert len(ds) == length

final_set = []
for key in datasets[0].keys():
    merged_data = {}
    for ds in datasets:
        merged_data.update(ds[key])
    merged_data["pageid"] = key
    final_set.append(merged_data)

with open(output, "w") as f:
    # Arrange the order of the keys
    orig_keys = list(final_set[0].keys())
    orig_keys.remove("pageid") # First item
    orig_keys.remove("class") # Want to be the last column in final dataset
    keys = ['pageid']
    keys.extend(orig_keys)
    keys.append("class")
    writer = csv.DictWriter(f, keys)
    writer.writeheader()
    writer.writerows(final_set)