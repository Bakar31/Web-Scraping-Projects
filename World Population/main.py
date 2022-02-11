import requests
from bs4 import BeautifulSoup
import pandas as pd

# destination url
url = 'https://www.worldometers.info/world-population/population-by-country/'
page  = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')

# getting the headers
table = soup.find('thead')
headers = table.find_all('th')
headers = [th.text for th in headers]

# empty dataframe with header as column name
df = pd.DataFrame(columns= headers)

# get the table bpdy
table_body = soup.find('tbody')

# all the rows
rows = table_body.find_all('tr')

# Separately access row texts and add to the dataframe 
for row in rows:
    single_row = row.find_all('td')
    single_row = [td.text for td in single_row]
    length = len(df)
    df.loc[length] = single_row

print(df.head())

# output as csv file
df.to_csv('Word Population.csv', index = False)