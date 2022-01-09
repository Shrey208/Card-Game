import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from kaggle.api.kaggle_api_extended import KaggleApi
api = KaggleApi()
api.authenticate()
cnames = []

glink = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'
usr = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive' }

def getimg(data, n):
    imgname = "p" + str(n) +".png"
    if os.path.exists(imgname):
        os.remove(imgname)
    url = glink + 'q=' + data + " Marvel Comics"
    response = requests.get(url, headers = usr)
    html = response.text
    bs = BeautifulSoup(html, 'html.parser')
    results = bs.findAll('img', {'class': 'rg_i Q4LuWd'})
    imagelinks = []
    for res in results:
        try:
            link = res['data-src']
            imagelinks.append(link)
            break
        except KeyError:
            continue
    for i,imagelink in enumerate(imagelinks):
        response = requests.get(imagelink)
        with open(imgname, 'wb') as file:
            file.write(response.content)

def getsts(n) :
    pname = "p" + str(n) + ".csv"
    if os.path.exists(pname):
        os.remove(pname)
    rand = sdf.sample()
    for cname in rand.Name :
        cnames.append(cname)
        abdf = adf.loc[adf['Name'] == cname]
        getimg(cname,n)
        abidf = abdf.loc[:,[(abdf[col] == True).all() for col in abdf.columns]]
        rand['Abilities'] = ", ".join(abidf)
        tr = rand.transpose()
        tr.to_csv("cs.csv")
    with open("cs.csv",'r') as f:
        with open(pname,'w') as f1:
            next(f)
            for line in f:
                f1.write(line)
    os.remove("cs.csv")

def getviz(cnames):
    if os.path.exists("comp.png") :
        os.remove("comp.png")
    p1 = sdf.loc[sdf['Name'] == cnames[0]]
    p1 = p1[["Name", "Intelligence", "Strength", "Speed", "Durability", "Power", "Combat", "Total"]].copy()
    p2 = sdf.loc[sdf['Name'] == cnames[1]]
    p2 = p2[["Name", "Intelligence", "Strength", "Speed", "Durability", "Power", "Combat", "Total"]].copy()
    p3 = pd.DataFrame({cnames[0] : [p1.iat[0,1], p1.iat[0,2], p1.iat[0,3], p1.iat[0,4], p1.iat[0,5], p1.iat[0,6], p1.iat[0,7]],
                        cnames[1]: [p2.iat[0,1], p2.iat[0,2], p2.iat[0,3], p2.iat[0,4], p2.iat[0,5], p2.iat[0,6], p2.iat[0,7]]},
                        index=[0, 1, 2, 3, 4, 5, 6])
    p3 = p3.div(p3.sum(axis=1), axis=0)
    p3["NOA"] = ["Intelligence", "Strength", "Speed", "Durability", "Power", "Combat", "Total"]
    plot = p3.plot( x = 'NOA', kind = 'barh', stacked = True, title = cnames[0] + " vs " + cnames[1], mark_right = True)
    fig = plot.get_figure()
    fig.savefig("comp.png")

api.dataset_download_file('dannielr/marvel-superheroes', 'charcters_stats.csv')
api.dataset_download_file('dannielr/marvel-superheroes', 'superheroes_power_matrix.csv')
os.rename("charcters_stats.csv", "stats.csv")
os.rename("superheroes_power_matrix.csv", "abilities.csv")

stats = pd.read_csv("stats.csv")
stats = stats[stats['Total'] > 5]
abilities = pd.read_csv("abilities.csv")
df = stats.merge(abilities, on=['Name'])
sdf = stats[stats.Name.isin(df.Name)]
adf = abilities[abilities.Name.isin(df.Name)]

# n = int(input("Enter no. of Characters : "))
n = 2
for i in range(1,n+1):
    getsts(i)

if n == 2:
    getviz(cnames)

os.remove("stats.csv")
os.remove("abilities.csv")