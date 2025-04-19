import pandas as pd

df = pd.read_csv("pos_train_set.csv")
df_k = pd.read_csv("full_speeches_new.csv")
df_k['year'] = pd.DatetimeIndex(df_k['date']).year
df = df[df["Label"] != "Slogans"]

df["length"] = [len(i.split(" ")) for i in df["Context"]]

# df_short = df[df["length"] <= 35]
df_long = df[df["length"] >= 35]
df_long = df_long[df_long["Subcategory"] != "Flag waving"]
# df_short_s = df_short["Context"].values.tolist()
# df_y = df_short["Date"].values.tolist()
# for k in range(len(df_y)):
#     matched = df_k[df_k["year"] == df_y[k]]
#     st = matched["concatenated_speech"].values.tolist()
#     for s in st:
#         if df_short_s[k] in s:
#             sp_before = s.split(df_short_s[k])
#             print("found")
#             prev_st = sp_before[0].split(".")
#             print(prev_st)
#             os = prev_st[-1]
#             if os not in ["", " "]:
#                 df_short_s[k] = prev_st[-1] + "." + df_short_s[k]
#             elif len(prev_st) >= 2:
#                 df_short_s[k] = prev_st[-2] + "." + df_short_s[k]

        
# df_short["Context"] = df_short_s
# df_full = pd.concat([df_short,df_long])

df_long.to_csv("filtered_train.csv")