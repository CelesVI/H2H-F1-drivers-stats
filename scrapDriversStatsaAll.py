import requests
import re
import string
import csv
import pandas as pd
from bs4 import BeautifulSoup

base_url = "https://www.statsf1.com"
actual_links = []

#To parse dictionaries.
lista_dict = []

def getDriversLinks():
    for i in string.ascii_lowercase:
        page = requests.get("https://www.statsf1.com/en/pilotes-"+i+".aspx")
        soup = BeautifulSoup(page.content, 'html.parser')
        tabla = soup.select("table a")
        links = [link['href'] for link in tabla]

        for i in links:
            if not contains_digits(i) and 'victoire' not in i:
                actual_links.append(base_url+i)

def getDriverName(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    name = soup.find("title")

    name_string = name.get_text()

    name_string_striped = " ".join(name_string.split())

    name_string_splited = name_string_striped.split(str('•'))[0]

    name_formatted = " ".join([i.capitalize() for i in name_string_splited.split()])

    return name_formatted

def getDriverChampionships(url):
    #Param is a url with driver's stats.
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    champ = []
    #Championships are in pilotechp class
    for champion in soup.find_all("div", class_='pilotechp'):
        #Add bad results.
        championship = champion.get_text()
        if re.search(r'\bWorld Champion\b', championship):
            champ.append(championship)
    print(champ)
    #Get all digits in the get_text()
    champ_years = re.findall(r'\d+', str(champ))
    
    return str(len([i for i in champ_years if len(i)==4]))

def getDriverStats(url):
    #To create a dictonary from driver's stats.
    stats_dict = {}
    lista = []
    #Param is a url with driver's stats.
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    #Name from previous function parse to dictionary.
    stats_dict['Nombre'] = getDriverName(url)
    #Get championships if he has.
    stats_dict['Championships'] = getDriverChampionships(url)
    #Stats are in class piloteitem. 4 rows of data.
    stats = soup.find_all("div", class_='piloteitem')
    for stat in stats:
        stat_text = stat.get_text()

        stat_text_striped = " ".join(stat_text.split())

        stat_text_splited = stat_text_striped.split()

        #print(stat_text_splited)

        #Append all the data in a list to format later.
        lista.append(stat_text_striped)

    #Finding a string-int pair to create a key,value item and parse into dictionary.
    for i in lista:
        lista_stats = re.findall(r'[A-Za-z]+|\d+', i)
        for i in range(0, len(lista_stats)+1):
            try:
                type(int(lista_stats[i])) == int
                stats_dict[lista_stats[i+1]] = lista_stats[i]
            except:
                continue
    return stats_dict
    '''with open('stats.txt', 'a+') as f:
        print(stats_dict, file=f)
        f.close()'''


def contains_digits(s):
    return any(char.isdigit() for char in s)
 
#print(actual_links)

getDriversLinks()

for i in actual_links:
    full_stat = getDriverStats(i)
    '''with open('statsDriversByLetters.txt', 'a+') as f:
        print(full_stat, file=f)
        f.close()'''
    '''with open('statsDriversByLetters.json', 'a+') as f:
        json.dump(full_stat, f)
        f.write('\n')
        f.close()'''
    lista_dict.append(full_stat)

df = pd.DataFrame.from_dict(lista_dict)

df.to_csv('scrapDriversStatsAll.csv')
df.to_excel('scrapDriversStatsAll.xlsx')
print(df.head(100))

'''with open('stats.txt', 'a+') as f:
    print(stats_dict, file=f)
    f.close()
'''
'''with open('stats.csv', 'a+') as csvfile:
        writer = csv.DictWriter(csvfile)
        writer.writeheader()
        for data in dict:
            writer.writerow(data)
'''
'''with open('stats.csv', 'a+') as f:
    for key in stats_dict.keys():
        f.write("%s,%s\n"%(key,stats_dict[key]))'''