import os
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi
api = KaggleApi()
api.authenticate()

if os.path.exists("cs.csv"):
    os.remove("cs.csv")
if os.path.exists("final.csv"):
    os.remove("final.csv")
if os.path.exists("stats.csv"):
    os.remove("stats.csv")
if os.path.exists("abilities.csv"):
    os.remove("abilities.csv")

api.dataset_download_file('dannielr/marvel-superheroes', 'charcters_stats.csv')
api.dataset_download_file('dannielr/marvel-superheroes', 'superheroes_power_matrix.csv')
os.rename("charcters_stats.csv", "stats.csv")
os.rename("superheroes_power_matrix.csv", "abilities.csv")

stats = pd.read_csv("stats.csv")
abilities = pd.read_csv("abilities.csv")
df = stats.merge(abilities, on=['Name'])
sdf = stats[stats.Name.isin(df.Name)]
adf = abilities[abilities.Name.isin(df.Name)]

rand1 = sdf.sample()
for i in rand1.Name :
    abdf = adf.loc[adf['Name'] == i]
    abidf = abdf.loc[:,[(abdf[col] == True).all() for col in abdf.columns]]
    rand1['Abilities'] = ", ".join(abidf)
    tr = rand1.transpose()
    tr.to_csv('cs.csv')

with open("cs.csv",'r') as f:
    with open("final.csv",'w') as f1:
        next(f)
        for line in f:
            f1.write(line)

os.remove("cs.csv")
os.remove("stats.csv")
os.remove("abilities.csv")
