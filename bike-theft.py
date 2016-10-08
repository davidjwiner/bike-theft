import requests
import json
import unicodecsv as csv
import datetime
import math
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


start = 1262419199 #Epoch timestamp for 1/1/2010
end = 1451635199 #Epoch timestamp for 12/31/2015
# proximity = 'San Francisco, CA'
# proximity_square = 20

#url = """https://bikeindex.org:443/api/v2/bikes_search/stolen?page={0}&per_page=25&proximity=San%20Francisco%2C%20CA&proximity_square=20&stolen_before=1451635199&stolen_after=1262419199"""
#
#r = requests.get('https://bikeindex.org:443/api/v2/bikes_search/stolen?proximity=San%20Francisco%2C%20CA&proximity_square=20&stolen_before=1451635199&stolen_after=1262419199')
#per_page = 25;
#num_bikes = int(r.headers['Total'])
#num_pages = int(math.ceil(num_bikes/per_page))
#
#for i in range(num_pages + 1): # would like to make this dynamic
#    url_page = url.format(i+1)
#    r = requests.get(url_page.format(i))
#    j = r.json()
#    with open('./api-output/{0}.json'.format(i), 'w') as outfile:
#        json.dump(j, outfile)
#
writer = csv.writer(open('bike-data.csv', 'wb+'), dialect='excel', encoding='utf-8')

def convert_time(timestamp):
    value = datetime.datetime.fromtimestamp(timestamp)
    val = value.strftime('%Y-%m-%d')
    return val.encode('utf-8')

writer.writerow(['id', 'title', 'serial', 'manufacturer_name', 'frame_model', 'year', 'frame_colors', 'stolen', 'stolen_location', 'date_stolen'])

for i in range(145):
    json_file = open('./api-output/{0}.json'.format(i), "r")
    x = json.load(json_file)
    bikes = x['bikes']
    for b in bikes:
        writer.writerow([
            b['id'],
            b['title'],
            b['serial'],
            b['manufacturer_name'],
            b['frame_model'],
            b['year'],
            b['frame_colors'],
            b['stolen'],
            b['stolen_location'], 
            b['date_stolen']
        ])

# Plotting—keep in mind only looks like this because bike index gained traction

b_data = pd.read_csv("bike-data.csv", header=0)
b_data['date_stolen'] = pd.to_datetime(b_data['date_stolen'], utc=True, unit='s')
b_data = b_data.set_index('date_stolen')

monthly = pd.groupby(b_data, pd.TimeGrouper(freq='M')).count()
monthly = b_data.resample('M').count()

yearly = pd.groupby(b_data, pd.TimeGrouper(freq='12M')).count()
yearly = b_data.resample('12M').count()

fig, ax = plt.subplots(1, 1)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))
ax.bar(monthly.index, monthly['id'], width=10, align='center')
locs, labels = plt.xticks()
plt.setp(labels, rotation=40)

fig, ax = plt.subplots(1, 1)
chart = ax.bar(yearly.index, yearly['id'], width=200, align='center', alpha=0.4)