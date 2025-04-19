import pandas as pd

df = pd.read_excel("classification_results/fd_terms.xlsx")

rk = pd.read_excel("okk_all_gpt.xlsx")
sts = rk["sentences"].values.tolist()
small_k = []
for s in df["sentences"]:
    filt_s = rk[rk["sentences"] == s]
    small_k.append(filt_s)
smk = pd.concat(small_k)
smk.to_excel("hh_terms.xlsx")