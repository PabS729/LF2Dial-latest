import pandas as pd

df = pd.read_excel("full_4o.xlsx")

sc = df["sentence_sample"].values.tolist()

rp = df["rounds_persuaded"].values.tolist()

cat = df["labels"].values.tolist()

prof = df["profile"].values.tolist()

new_sc = []
new_rp = []
new_cat = []
new_prof = []

for j in range(len(sc)):
    if str(sc[j]) != "nan":
        new_sc.append(sc[j])
        new_cat.append(cat[j])
        new_prof.append(prof[j])
    if str(rp[j]) != "0":
        new_rp.append(rp[j])


data_dict = {
    "sentence": new_sc,
    "labels": new_cat,
    "rounds_persuaded": new_rp,
    "profile": new_prof
}

dfn = pd.DataFrame.from_dict(data_dict)
dfn.to_excel("cleaned_cat_4o.xlsx")

    



