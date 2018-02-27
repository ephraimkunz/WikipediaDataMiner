import csv
import json

pairs = [
    ("TLD-output/controversial_100-TLD-Data.csv", "articles/controversial_100.json"),
    ("TLD-output/controversial_200-TLD-Data.csv", "articles/controversial_200.json"),
    ("TLD-output/controversial_300-TLD-Data.csv", "articles/controversial_300.json"),
    ("TLD-output/controversial_400-TLD-Data.csv", "articles/controversial_400.json"),
    ("TLD-output/controversial_500-TLD-Data.csv", "articles/controversial_500.json"),
    ("TLD-output/controversial_600-TLD-Data.csv", "articles/controversial_600.json"),
    ("TLD-output/controversial_700-TLD-Data.csv", "articles/controversial_700.json"),
    ("TLD-output/controversial_800-TLD-Data.csv", "articles/controversial_800.json"),
    ("TLD-output/controversial_900-TLD-Data.csv", "articles/controversial_900.json"),
    ("TLD-output/controversial_1000-TLD-Data.csv", "articles/controversial_1000.json"),
    ("TLD-output/controversial_1100-TLD-Data.csv", "articles/controversial_1100.json"),
    ("TLD-output/controversial_1200-TLD-Data.csv", "articles/controversial_1200.json"),
    ("TLD-output/controversial_1300-TLD-Data.csv", "articles/controversial_1300.json"),
    ("TLD-output/controversial_last-TLD-Data.csv", "articles/controversial_last.json"),
   
    ("TLD-output/normal_100-TLD-Data.csv", "articles/normal_100.json"),
    ("TLD-output/normal_200-TLD-Data.csv", "articles/normal_200.json"),
    ("TLD-output/normal_300-TLD-Data.csv", "articles/normal_300.json"),
    ("TLD-output/normal_400-TLD-Data.csv", "articles/normal_400.json"),
    ("TLD-output/normal_500-TLD-Data.csv", "articles/normal_500.json"),
    ("TLD-output/normal_600-TLD-Data.csv", "articles/normal_600.json"),
    ("TLD-output/normal_700-TLD-Data.csv", "articles/normal_700.json"),
    ("TLD-output/normal_800-TLD-Data.csv", "articles/normal_800.json"),
    ("TLD-output/normal_900-TLD-Data.csv", "articles/normal_900.json"),
    ("TLD-output/normal_1000-TLD-Data.csv", "articles/normal_1000.json"),
    ("TLD-output/normal_1100-TLD-Data.csv", "articles/normal_1100.json"),
    ("TLD-output/normal_1200-TLD-Data.csv", "articles/normal_1200.json"),
    ("TLD-output/normal_1300-TLD-Data.csv", "articles/normal_1300.json"),
    ("TLD-output/normal_last-TLD-Data.csv", "articles/normal_last.json"),
]

output = "tld.csv"

data = []
for pair in pairs:
    with open(pair[0], "r") as f_tld:
        with open(pair[1], "r") as f_orig:
            reader = csv.DictReader(f_tld, fieldnames=["com_percentage", "org_percentage", "gov_percentage", "net_percentage", "edu_percentage", "other_percentage"])
            
            text = f_orig.read()
            items = json.loads(text)
            articles = items["articles"]

            i = 0
            for line in reader:
                art = articles[i]
                line["pageid"] = art["pageid"]
                data.append(line)
                i += 1

with open(output, "w") as f:
    # pageid must come first
    orig_keys = list(data[0].keys())
    orig_keys.remove("pageid")
    keys = ["pageid"]
    keys.extend(orig_keys)

    w = csv.DictWriter(f, keys)
    w.writeheader()
    w.writerows(data)
            

