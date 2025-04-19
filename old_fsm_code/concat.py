from pandas import DataFrame, read_excel, concat
import os

dfs = []
df3 = []
dfm = []

for f in os.listdir("eval_results"):
    if f[:25] == "storytelling_test_1008_4o":
        df = read_excel("eval_results/" + f)
        dfs.append(df)
    elif f[:25] == "storytelling_test_1008_3.":
        df = read_excel("eval_results/" + f)
        df3.append(df)
    elif f[:25] == "storytelling_test_1008_MI":
        df = read_excel("eval_results/" + f)
        dfm.append(df)
    else: 
        continue

df_a = concat(dfs)
df_3 = concat(df3)
df_m = concat(dfm)

df_a.to_excel("full_4o_eval.xlsx")
df_3.to_excel("full_3.5_eval.xlsx")
df_m.to_excel("full_MISTRAL_eval.xlsx")