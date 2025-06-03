import os
from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import re
import sqlite3


url_list = 'https://pokemondb.net/pokedex/all'
list_response = requests.get(url_list)
if list_response:
    list_soup = BeautifulSoup(list_response.text, 'html')

pokenombre = list_soup.find_all('a', class_= 'ent-name')
pokelista = [name.get_text().strip() for name in pokenombre]
pokeset = set(pokelista)

ds = []

for n in pokeset:
    resourece_url = f'https://pokemondb.net/pokedex/{n}'

    response = requests.get(resourece_url)
    
    if response:
        soup = BeautifulSoup(response.text, 'html')

    number_element = soup.find("th", string="National №").find_next_sibling("td")
    number = int(number_element.text.strip())
    name = n
    height_element = soup.find(string="Height").find_next()
    height = re.search(r"\d+\.\d+", height_element.text).group()
    weight_element = soup.find(string="Weight").find_next()
    weight = re.search(r"\d+\.\d+", weight_element.text).group()
    type_elements = soup.find("th", string="Type").find_next_sibling("td").find_all("a")
    types = [t.text for t in type_elements]
    types_str = ", ".join(types)  # Para mostrarlo como cadena
    abilities_element = soup.find("th", string="Abilities").find_next_sibling("td").find("a")
    first_ability = abilities_element.text.strip()
    ds.append({'Name': n, 
               'Number' : number, 
               'Height (m)' : height, 
               'Weight (Kg)': weight, 
               'Types' : types_str, 
               'Ability' : first_ability})

df = pd.DataFrame(ds)
df = df.sort_values(by = ['Number'])
df.set_index('Number', drop = False, inplace = True)

# print(df)

conn = sqlite3.connect('pokedex.db')
df.to_sql('pokedex', conn, if_exists = 'replace', index = False)
conn.commit()
conn.close()