import pandas as pd

df = pd.read_excel("cleaned_cat_MISTRAL.xlsx")

sc = df["sentence"].values.tolist()

rp = df["rounds_persuaded"].values.tolist()

cat = df["labels"].values.tolist()

prof = df["profile"].values.tolist()

pers_list = ["inventive and curious", "consistent and cautious", "efficient and organized", 
             "extravagant and careless", "outgoing and energetic", "solitary and reserved", 
             "friendly and compassionate", "critical and judgmental", "sensitive and nervous", "resilient and confident"]
ed = ["Toddler", "Elementary", "High School", "Associate", "Bachelor", "PHD"]
edu_levels = []
comp_p = []

for j in range(len(sc)):
    persona = ""
    edu = ""
    for p in pers_list:
        if p in prof[j].lower():
            persona += p + " "
    for e in ed:
        if e.lower() in prof[j].lower():
            edu += e
    comp_p.append(persona)
    edu_levels.append(edu)

data_dict = {
    "sentence": sc,
    "rounds_persuaded": rp,
    "labels": cat,
    "profile": prof,
    "personality": comp_p,
    "edu_level": edu_levels

}

new_df = pd.DataFrame.from_dict(data_dict)

c = 0
for q in new_df["personality"].unique():
    df_all_p = new_df.loc[new_df['personality'] == q]
    df_succ = new_df.loc[new_df['rounds_persuaded'] != "NO"]
    df_succ = df_succ.loc[df_succ['personality'] == q]
    ct = df_succ.shape[0]/ df_all_p.shape[0]

    print(q, ct, c, df_succ.shape[0], df_all_p.shape[0])
    c += 1

for q in new_df["edu_level"].unique():
    df_all_p = new_df.loc[new_df['edu_level'] == q]
    df_succ = new_df.loc[new_df['rounds_persuaded'] != "NO"]
    df_succ = df_succ.loc[df_succ['edu_level'] == q]
    ct = df_succ.shape[0]/ df_all_p.shape[0]

    print(q, ct, c, df_succ.shape[0], df_all_p.shape[0])
    c += 1



# new_df.to_excel("detail_MISTRAL.xlsx")