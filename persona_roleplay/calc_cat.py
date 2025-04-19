import pandas as pd

df = pd.read_excel("cleaned_cat_MISTRAL.xlsx")

cats = pd.unique(df["labels"])

for c in cats:
    los = df.loc[df["labels"] == c]
    suc = len(los[los["rounds_persuaded"] != "NO"])
    all = len(df.loc[df["labels"] == c])

    print(c, suc/all)