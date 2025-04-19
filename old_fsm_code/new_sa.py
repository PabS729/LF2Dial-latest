import pandas as pd
fi = pd.read_excel("classification_results/okk_all.xlsx", index_col=None)
# from sklearn.utils import shuffle


fks = []
kdd = [k for k in fi.keys() if k not in ["sentences", "chats"]]


fi_1 = fi.drop_duplicates(["sentences"])
print(len(fi_1["sentences"]))
fi2 = pd.read_excel("classification_results/okk_all_2.xlsx")
comb = pd.concat([fi_1, fi2], axis=0)

for k in kdd:
    # comb[k] = comb[k].str.replace(r'yes*|Yes*', "yes")
    # comb[k] = comb[k].str.replace(r'no*|No*', "no")
    fks.append(comb[k].values.tolist())

for (ar, k) in zip(fks, kdd):
    ct = 0 
    for (j,st) in zip(ar, comb["sentences"]):
        # print(j)
        if str(j) != None and "yes" in str(j)[:5].lower():
            comb[k][ct] = "yes"
        else:
            comb[k][ct] = "no"
        ct += 1

comb.to_excel("processed_o3.xlsx")