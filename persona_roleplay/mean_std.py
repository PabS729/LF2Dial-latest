import pandas as pd

df = pd.read_excel("full_MISTRAL.xlsx")
print(df.columns)

df = df.loc[df["rounds_persuaded"] != "NO"]
df = df.loc[df["rounds_persuaded"] != 0]["rounds_persuaded"]

avg = df.sum() / len(df.values.tolist())

STD = df.std()

print(avg, STD)

df = pd.read_excel("full_MISTRAL_eval.xlsx")



for c in df.columns:
    if c == "sentences":
        continue
    s = df[c]

    avg = s.sum() / len(s.values.tolist())

    std = s.std()

    print(c, avg, std)
