# library section
import requests
from bs4 import BeautifulSoup
import pandas as pd

# destination url
url = 'https://ev-database.org/?fbclid=IwAR3LkjdJIXW3Sgyr7XmFT1N15dxOgwfL9-i0H2attrrG9WTO1_HfKk_vR5w#sort:path~type~order=.rank~number~desc|range-slider-range:prev~next=0~1200|range-slider-acceleration:prev~next=2~23|range-slider-topspeed:prev~next=110~450|range-slider-battery:prev~next=10~200|range-slider-towweight:prev~next=0~2500|range-slider-fastcharge:prev~next=0~1500|paging:currentPage=0|paging:number=all'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')

# store html of all the postings
postings = soup.find_all('div', class_ = 'list-item')

# blank csv file
df = pd.DataFrame()

# empty list to store values
titles = []
subtitles = []
batteries = []
weights = []
plug_types = []
sizes = []
number_of_seats_all = []
acceleration_all = []
topspeed_all = []
car_range_all = []
efficiency_all = []
fastcharge_all = []

# loop through each posting to get desired text or number
for posting in postings:
    title = posting.find('a', class_ = 'title').text
    subtitle_full = posting.find('div', class_ = 'subtitle').text.strip().split('|')
    subtitle = subtitle_full[0]
    battery = subtitle_full[-1].strip()

    # weights of some car were missing. To avoid error try, except block was implemented
    try:
        weight = posting.find('span', class_ = 'towweight').text
    except:
        weight = 'N/A'

    # plug_type of some car were missing. To avoid error try, except block was implemented
    try:
        plug_type = posting.find('span', class_ = 'plug-type2-ccs hidden').text
    except:
        plug_type = 'N/A'

    size = posting.find('span', {'title':'Market Segment'}).text
    number_of_seats = posting.find_all('span', {'title':'Number of seats'})[-1].text
    acceleration = posting.find('span', class_ = 'acceleration').text
    topspeed = posting.find('span', class_ = 'topspeed').text
    car_range = posting.find('span', class_ = 'erange_real').text
    efficiency = posting.find('span', class_ = 'efficiency').text
    fastcharge = posting.find('span', class_ = 'fastcharge_speed_print').text

    # founded values adding to empty lists
    titles.append(title)
    subtitles.append(subtitle)
    batteries.append(battery)
    weights.append(weight)
    plug_types.append(plug_type)
    sizes.append(size)
    number_of_seats_all.append(number_of_seats)
    acceleration_all.append(acceleration)
    topspeed_all.append(topspeed)
    car_range_all.append(car_range)
    efficiency_all.append(efficiency)
    fastcharge_all.append(fastcharge)
    
    # check all values for each iteration
    print(title, subtitle, battery, weight, plug_type, size, number_of_seats, acceleration, car_range, topspeed, efficiency, fastcharge)

# double check by checking the length of each list
# print(len(titles))
# print(len(subtitles))
# print(len(batteries))
# print(len(weights))
# print(len(plug_types))
# print(len(number_of_seats_all))
# print(len(acceleration_all))
# print(len(topspeed_all))
# print(len(car_range_all))
# print(len(efficiency_all))
# print(len(fastcharge_all))

# columns of the dataframe
df['Title'] = titles
df['Subtitle'] = subtitles
df['Battery'] = batteries
df['Weight'] = weights
df['Plug Type'] = plug_types
df['Number of Seats'] = number_of_seats_all
df['Acceleration'] = acceleration_all
df['Top Speed'] = topspeed_all
df['Car Range'] = car_range_all
df['Efficiency'] = efficiency_all
df['Fastcharge'] = fastcharge_all

# convert to csv file
df.to_csv('Electronics vehicles.csv', index=False)