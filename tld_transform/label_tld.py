import csv
import json

pairs = [
    ("TLD-binned/controversial_100-TLD-Data.csv", "../articles/controversial_100.json"),
    ("TLD-binned/controversial_200-TLD-Data.csv", "../articles/controversial_200.json"),
    ("TLD-binned/controversial_300-TLD-Data.csv", "../articles/controversial_300.json"),
    ("TLD-binned/controversial_400-TLD-Data.csv", "../articles/controversial_400.json"),
    ("TLD-binned/controversial_500-TLD-Data.csv", "../articles/controversial_500.json"),
    ("TLD-binned/controversial_600-TLD-Data.csv", "../articles/controversial_600.json"),
    ("TLD-binned/controversial_700-TLD-Data.csv", "../articles/controversial_700.json"),
    ("TLD-binned/controversial_800-TLD-Data.csv", "../articles/controversial_800.json"),
    ("TLD-binned/controversial_900-TLD-Data.csv", "../articles/controversial_900.json"),
    ("TLD-binned/controversial_1000-TLD-Data.csv", "../articles/controversial_1000.json"),
    ("TLD-binned/controversial_1100-TLD-Data.csv", "../articles/controversial_1100.json"),
    ("TLD-binned/controversial_1200-TLD-Data.csv", "../articles/controversial_1200.json"),
    ("TLD-binned/controversial_1300-TLD-Data.csv", "../articles/controversial_1300.json"),
    ("TLD-binned/controversial_last-TLD-Data.csv", "../articles/controversial_last.json"),
   
    ("TLD-binned/bin_0_final_unique-TLD-Data.csv", "../articles/bin_0_final_unique.json"),
    ("TLD-binned/bin_1_final_unique-TLD-Data.csv", "../articles/bin_1_final_unique.json"),
    ("TLD-binned/bin_2_final_unique-TLD-Data.csv", "../articles/bin_2_final_unique.json"),
    ("TLD-binned/bin_3_final_unique-TLD-Data.csv", "../articles/bin_3_final_unique.json"),
    ("TLD-binned/bin_4_final_unique-TLD-Data.csv", "../articles/bin_4_final_unique.json"),
    ("TLD-binned/bin_5_final_unique-TLD-Data.csv", "../articles/bin_5_final_unique.json"),
    ("TLD-binned/bin_6_final_unique-TLD-Data.csv", "../articles/bin_6_final_unique.json"),
    ("TLD-binned/bin_7_final_unique-TLD-Data.csv", "../articles/bin_7_final_unique.json"),
    ("TLD-binned/bin_8_final_unique-TLD-Data.csv", "../articles/bin_8_final_unique.json"),
    ("TLD-binned/bin_9_final_unique-TLD-Data.csv", "../articles/bin_9_final_unique.json"),
    ("TLD-binned/bin_10_final_unique-TLD-Data.csv", "../articles/bin_10_final_unique.json"),
    ("TLD-binned/bin_11_final_unique-TLD-Data.csv", "../articles/bin_11_final_unique.json"),
    ("TLD-binned/bin_12_final_unique-TLD-Data.csv", "../articles/bin_12_final_unique.json"),
    ("TLD-binned/bin_13_final_unique-TLD-Data.csv", "../articles/bin_13_final_unique.json"),
    ("TLD-binned/bin_14_final_unique-TLD-Data.csv", "../articles/bin_14_final_unique.json"),
]

output = "tld_binned.csv"

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
            

