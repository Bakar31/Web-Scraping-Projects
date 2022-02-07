# required libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# destination url
url = 'https://www.espn.com/nfl/standings/_/season/2020/group/league'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')

# accessing only table html
table = soup.find('div', class_ = 'standings__table')

# header elements
headers = table.find_all('th')

# text headers
headers = [th.text for th in headers][1:]

# creating new dataset
df = pd.DataFrame(columns = headers)

# team names
first_col = table.find('tbody', class_ = 'Table__TBODY')
rows = first_col.find_all('tr')

entities = []
for row in rows:
    data = row.find('td')
    data = data.text
    data = data[4:]
    entities.append(data)

# other entites
value_table = table.find('div', class_ = 'Table__Scroller')
value_table_rows = value_table.find_all('tr')[1:]
for row in value_table_rows:
    single_row = row.find_all('td')
    single_row = [td.text for td in single_row]
    length = len(df)
    df.loc[length] = single_row

# insert team name as the first column
df.insert(loc=0, column='', value = entities)
print(df.head())

# Output as a csv file.
df.to_csv('NFL Standings 2020.csv', index = False)