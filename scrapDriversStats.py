import requests
import re
import string
import csv
import pandas as pd
import json
from bs4 import BeautifulSoup

page = requests.get("https://www.statsf1.com/en/juan-manuel-fangio.aspx")
soup = BeautifulSoup(page.content, 'html.parser')

stats_dict = {}

def contains_digits(s):
    return any(char.isdigit() for char in s)

name = soup.find("title")
stats = soup.find_all("div", class_='piloteitem')

name_string = name.get_text()

name_string_striped = " ".join(name_string.split())

name_string_splited = name_string_striped.split(str('•'))[0]

name_formatted = " ".join([i.capitalize() for i in name_string_splited.split()])

'''with open('stats.txt', 'a+') as f:
    f.write('\n'+name_formatted+'\n')
    f.close()
'''
stats_dict['Nombre'] = name_formatted

champ = []

#Return championship for a driver if he has.
for champion in soup.find_all("div", class_='pilotechp'):
    championship = champion.get_text()
    if re.search(r'\bWorld Champion\b', championship):
        champ.append(championship)

champ_years = re.findall(r'\d+', str(champ))
#print(len([i for i in champ_years if len(i)==4]))

#print(champ_striped)
#print(championships)
stats_dict['Championships'] = str(len([i for i in champ_years if len(i)==4]))


#print(len([i for i in champ_years if len(i)==4]))

#print(champ_striped)
#print(championships)



lista = []
cont = 0
for stat in stats:
    stat_text = stat.get_text()

    stat_text_striped = " ".join(stat_text.split())
    print(stat_text_striped)
    stat_text_splited = stat_text_striped.split()

    print(stat_text_splited)

    lista.append(stat_text_striped)
    cont += 1
    if cont == 2:
        break

for i in lista:
    print(i +'\n')
    lista_stats = re.findall(r'[A-Za-z]+|\d+', i)
    print(lista_stats)
    lista_final = []
    for i in range(0, len(lista_stats)+1):
        try:
            type(int(lista_stats[i])) == int
            stat = lista_stats[i]+' '+lista_stats[i+1]
            lista_final.append(stat)
            stats_dict[lista_stats[i+1]] = lista_stats[i]
        except:
            continue
    

with open('statsOneDriver.json', 'a+') as f:
    json.dump(stats_dict, f)
    f.write("\n")
    f.close()

'''with open('stats.csv', 'a+') as csvfile:
        writer = csv.DictWriter(csvfile)
        writer.writeheader()
        for data in dict:
            writer.writerow(data)
'''
'''with open('stats.csv', 'a+') as f:
    for key in stats_dict.keys():
        f.write("%s,%s\n"%(key,stats_dict[key]))'''