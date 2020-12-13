#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import urllib.request
import time 
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd 
from urllib.request import urlopen


# In[2]:


url = 'https://en.wikipedia.org/wiki/Epidemiology_of_depression'


# In[3]:


html = urlopen(url)


# In[4]:


soup = BeautifulSoup(html, 'html.parser')    


# In[5]:


tables = soup.find_all('table')


# In[6]:


# convert number as string to integer 
# re.sub() returns the substring that match the regrex 

import re 
def process_num(num):
    return float(re.sub(r'[^\w\s.]','',num))


# In[7]:


num1 = re.sub(r'[^\w\s.]','','1,156.30')
num1


# In[15]:


ranks = []
rates = []
countries  = []
links = []

for table in tables:
    rows = table.find_all('tr')
    
    for row in rows:
        cells = row.find_all('td')
        
        if len(cells) > 1:
            rank = cells[0]
            ranks.append(int(rank.text))
            
            country = cells[1]
            countries.append(country.text.strip())
            
            rate = cells[2]
            rates.append(process_num(rate.text.strip()))
            
            link = cells[1].find('a').get('href')
            links.append('https://en.wikipedia.org/' + link)
            

df1 = pd.DataFrame(ranks, index = countries, columns = ['Rank'])
df1['DAILY rate'] = rates

df1.head(10)


# In[17]:


sun_url = urlopen('https://en.wikipedia.org/wiki/List_of_cities_by_sunshine_duration')
sun = BeautifulSoup(sun_url, 'html.parser')
tables = sun.find_all('table')

# Dictionary to hold the name of the country and its corresponding temperature 
country_suns = {}

# Dictionary to hold the country and its freqency in the table 
count = {}
for table in tables:
    rows = table.find_all('tr')
    
    #Skip the first row, which is the name of the columns 
    for row in rows[1:]:
        cells = row.find_all('td')
        country = cells[0].text.strip()
        
        if country in countries:
            
            sun = cells[-2].text.strip()
            sun = process_num(sun)/10
            
            if country in country_suns:
                count[country] +=1
                country_suns[country] += sun
            
            else:
                count[country] = 1
                country_suns[country] = sun
                
# Find the average temperature of each country 
for country in country_suns:
    print(country_suns[country], count[country])
    country_suns[country] = round(country_suns[country]/count[country],2)
    print('Country: {}, Sunshine Hours: {}'. format(country,country_suns[country]))


# In[18]:


df2 = pd.DataFrame.from_dict(country_suns,orient='index', columns = ['Sunshine Hours/Year'])

df = df1.join(df2)

df.info()


# In[20]:


df.dropna(inplace=True)


# In[24]:


df.info()

import matplotlib.pyplot as plt
import seaborn as sns

sns.scatterplot('Rank', 'Sunshine Hours/Year', data=df)


# In[22]:

df.corr()
