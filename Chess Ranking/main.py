import requests
from bs4 import BeautifulSoup
import pandas as pd

# destination url
url = 'https://www.chess.com/ratings'
page  = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')

# getting the headers
table = soup.find('thead')
headers = table.find_all('th')
headers = [(th.text).strip() for th in headers]

# empty dataframe with header as column name
df = pd.DataFrame(columns= headers)

counter = 0

# loop through all available pages
while True:  
    # get the table bpdy
    table_body = soup.find('tbody')

    # all the rows
    rows = table_body.find_all('tr')

    # Separately access row texts and add to the dataframe 
    for row in rows:
        single_row = row.find_all('td')
        single_row = [(td.text).strip() for td in single_row]
        single_row[1] = ' '.join(single_row[1].split())
        length = len(df)
        df.loc[length] = single_row

    # go to next page and grab the html
    try:
        next_page = soup.find('a', {'aria-label': 'Next Page'}).get('href')
    except:
        break
    page = requests.get(next_page)
    soup = BeautifulSoup(page.text, 'lxml')

    counter += 1
    print('Page No. {} done.'.format(counter))

print(df.head())
df.to_csv('Chess Ranking.csv', index = False)