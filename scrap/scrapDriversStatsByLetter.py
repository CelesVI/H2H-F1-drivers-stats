import requests
import re
import string
import csv
import json
import pandas as pd
from bs4 import BeautifulSoup

'''Saves a part of url to append later.
    Only use for testing new functions. 
    Get the main page and turno into soup object to scrap
    Testing for drivers with the same first letter in their surnames.
    Not the definite version'''

base_url = "https://www.statsf1.com"
page = requests.get("https://www.statsf1.com/en/pilotes-f.aspx")
soup = BeautifulSoup(page.content, 'html.parser')

#To parse dictionaries.
lista_dict = []

#Get drivers name form the title tag.
def getDriverName(soup):

    #Formating driver name from title tag.
    name = soup.find("title")

    name_string = name.get_text()

    name_string_striped = " ".join(name_string.split())

    name_string_splited = name_string_striped.split(str('•'))[0]

    name_formatted = " ".join([i.capitalize() for i in name_string_splited.split()])

    return name_formatted

def getDriverChampionships(soup):
    #Param is a url with driver's stats.
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

#Get stats form a url.
def getDriverStats(soup):
    #To create a dictonary from driver's stats.
    stats_dict = {}
    lista = []
    
    #Name from previous function parse to dictionary.
    stats_dict['Nombre'] = getDriverName(soup)
    #Get championships if he has.
    stats_dict['Championships'] = getDriverChampionships(soup)
    #Stats are in class piloteitem. 4 rows of data.
    stats = soup.find_all("div", class_='piloteitem')
    cont = 0
    for stat in stats:
        stat_text = stat.get_text()

        stat_text_striped = " ".join(stat_text.split())

        stat_text_splited = stat_text_striped.split()

        #print(stat_text_splited)

        #Append all the data in a list to format later.
        lista.append(stat_text_striped)
        cont += 1
        if cont == 2:
            break
    print(lista)
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

#Driver's link are in a table div. Usefull links are those without year and the word victorie. 
tabla = soup.select("table a")

#Looking for all href label.
links = [link['href'] for link in tabla]

#Filter usefull links and save it.
actual_links = []
for i in links:
    if not contains_digits(i) and 'victoire' not in i:
        actual_links.append(base_url+i)


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
df.to_csv('scrap/scrapDriversStatsByLetter.csv')
df.to_excel('scrap/scrapDriversStatsByLetter.xlsx')

#Print to check if everything went well.
print(df.head(50))
