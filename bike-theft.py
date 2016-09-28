import requests
import json
import unicodecsv as csv
import datetime
from dateutil import parser
import math
import pandas as pd
import matplotlib.pyplot as plt

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
        try:
            parser.parse(str(b['date_stolen']))
        except ValueError:
            continue
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
            parser.parse(str(b['date_stolen']))
        ])

#b_data = pd.read_csv("bike-data.csv", parse_dates=['date_stolen'])
b_data = pd.read_csv("bike-data.csv")
b_data.head()
b_data = b_data.set_index('date_stolen')
b_data.index = pd.to_datetime(b_data['date_stolen'])
#print(b_data)

#monthly = pd.groupby(b_data, pd.TimeGrouper(freq='M')).count()
#print(monthly.sum())
#monthly = b_data.resample('M', how='count')
#plot = monthly.plot(kind='bar', title="Bike thefts by month", legend=None)
##plot = b_data.plot(title="Bike thefts by month", legend=None)

#figure = plot.get_figure()
#plt.show(block=True)
#date_group = b_data.groupby('date_stolen')
#print(date_group.size())

#b_data.describe()

#ax = a.plot(x=['Iteration'], kind='line', title='Cost of batch vs. stochastic gradient descent')
#ax.set_ylabel('Cost')
#ax.set_xlabel('Iteration')
#ax.show()
