import requests
import re
import string
import csv
import pandas as pd
from bs4 import BeautifulSoup

#Main page to want to scrap. Save the usefull links in the list below.
base_url = "https://www.statsf1.com"
actual_links = []

#To parse dictionaries.
lista_dict = []

#Getting all the drives by surname first letter.
def getDriversLinks():
    #Checking for table tag who contains links to each driver.
    for i in string.ascii_lowercase:
        page = requests.get("https://www.statsf1.com/en/pilotes-"+i+".aspx")
        soup = BeautifulSoup(page.content, 'html.parser')
        tabla = soup.select("table a")
        links = [link['href'] for link in tabla]

        #Cleaning the data keeping those links are usefull.
        for i in links:
            if not contains_digits(i) and 'victoire' not in i:
                actual_links.append(base_url+i)

#Formating driver name from title tag.
def getDriverName(soup):
    
    name = soup.find("title")

    name_string = name.get_text()

    name_string_striped = " ".join(name_string.split())

    name_string_splited = name_string_striped.split(str('•'))[0]

    name_formatted = " ".join([i.capitalize() for i in name_string_splited.split()])

    return name_formatted

#Get driver championships if they have. 
def getDriverChampionships(soup):
    
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
    
    #Name from previous function parse to dictionary.
    stats_dict['Nombre'] = getDriverName(soup)
    #Get championships if he has.
    stats_dict['Championships'] = getDriverChampionships(soup)
    #Stats are in class piloteitem. 4 rows of data.
    stats = soup.find_all("div", class_='piloteitem')
    for stat in stats:
        stat_text = stat.get_text()

        stat_text_striped = " ".join(stat_text.split())

        stat_text_splited = stat_text_striped.split()

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

#Check if string has any digits.
def contains_digits(s):
    return any(char.isdigit() for char in s)

#Iterating over links and write the stats in a file.
for i in actual_links:
    page = requests.get(i)
    soup = BeautifulSoup(page.content, 'html.parser')

    #Soup object as param.
    full_stat = getDriverStats(soup)
    lista_dict.append(full_stat)

#Create a dataframe from list of dictionaries.
df = pd.DataFrame.from_dict(lista_dict)

#Save the just-created dataframe.
df.to_csv('scrap/scrapDriversStatsAll.csv')
df.to_excel('scrap/scrapDriversStatsAll.xlsx')

#Print to check if everything went well.
print(df.head(100))

