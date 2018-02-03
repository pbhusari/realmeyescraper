from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime
import re
from item_dict import item_dict1
import sys


sys.setrecursionlimit(10000000) #   *nervous laughter*

#realmeye frequency is EXACTLY an hour
url = 'https://www.realmeye.com/recent-offers'
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html, 'lxml')
#rows = soup.findall('tbody')

def find_number_of_iterations(soup):
    if int(soup.findAll('a')[(len(soup.findAll('a')) - 2)].get_text()[:1]) > 1:
        return int(soup.findAll('a')[(len(soup.findAll('a')) - 2)].get_text()[:1])
    else:
        return 0

it = find_number_of_iterations(soup)
rows = soup.find_all('tr')

servers = []
offermade = []
qty = []
names = []
selling_items = []
buying_items = []
selling_items_quantity = []
buying_items_quantity = []

for row in rows:
    #finds server
    
    #finds offer times
    times = []
    try:
        times += row.find_all(class_='timeago')
    except TypeError:
        times += 'Hidden'

    try:
        offermade += times[0]
    except IndexError:
        offermade += times

    #finds quantities

    try:
        if len(row.findAll('strong')) > 0:
            qty.append(re.sub("\D", '', str(row.findAll('strong')[0])))
        qty.append(re.sub("\D", '',str(row.findAll(class_='muted')[0])))
        
    except IndexError:
        pass
    
    #finds player names
    try:
        name = row.find_all('a')
    except TypeError:
        pass
    try:
        names.append(name[0].get_text())
    except IndexError:
        pass

    #finds items
    cells = row.findAll('td')
    try:
        
        #finds selling item ids
        selling_items_temp = []
        selling_items_temp += (cells[0].findAll(class_="item"))
        strlist = []
        selling_item_ids = []
        for item in selling_items_temp:
            strlist.append(str(item))
        for item in strlist:
            short = item[30:]
            shorter = short[:(short.index('"'))]
            selling_item_ids.append(shorter)
        selling_items.append(selling_item_ids)

        #finds buying item ids
        buying_items_temp = []
        buying_items_temp += (cells[1].findAll(class_="item"))
        strlist = []
        buying_item_ids = []
        for item in buying_items_temp:
            strlist.append(str(item))
        for item in strlist:
            short = item[30:]
            shorter = short[:(short.index('"'))]
            buying_item_ids.append(shorter)
        buying_items.append(buying_item_ids)

        selling_items_quantity_soup = (cells[0].findAll(class_="item-quantity-static"))
        buying_items_quantity_soup = (cells[1].findAll(class_="item-quantity-static"))

        strlist = []
        for item in selling_items_quantity_soup:
            strlist.append(item.get_text())
        selling_items_quantity.append(strlist)
        
        strlist = []
        for item in buying_items_quantity_soup:
            strlist.append(item.get_text())
        buying_items_quantity.append(strlist)

    except IndexError:
        pass
    
    

for i in range (1, it + 1):
    url = 'https://www.realmeye.com/recent-offers/' + str(i*100+1)
    print(url)
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'lxml')

    rows = soup.find_all('tr')

    for row in rows:
        times = []
        try:
            times += row.find_all(class_='timeago')
        except TypeError:
            times += 'Hidden'

        try:
            offermade += times[0]
        except IndexError:
            offermade += times

        #finds quantities

        try:
            if len(row.findAll('strong')) > 0:
                qty.append(re.sub("\D", '', str(row.findAll('strong')[0])))
            qty.append(re.sub("\D", '',str(row.findAll(class_='muted')[0])))
            
        except IndexError:
            pass
        
        #finds player names
        try:
            name = row.find_all('a')
        except TypeError:
            pass
        try:
            names.append(name[0].get_text())
        except IndexError:
            pass

        #finds items
        cells = row.findAll('td')
        try:
            
            #finds selling item ids
            selling_items_temp = []
            selling_items_temp += (cells[0].findAll(class_="item"))
            strlist = []
            selling_item_ids = []
            for item in selling_items_temp:
                strlist.append(str(item))
            for item in strlist:
                short = item[30:]
                shorter = short[:(short.index('"'))]
                selling_item_ids.append(shorter)
            selling_items.append(selling_item_ids)

            #finds buying item ids
            buying_items_temp = []
            buying_items_temp += (cells[1].findAll(class_="item"))
            strlist = []
            buying_item_ids = []
            for item in buying_items_temp:
                strlist.append(str(item))
            for item in strlist:
                short = item[30:]
                shorter = short[:(short.index('"'))]
                buying_item_ids.append(shorter)
            buying_items.append(buying_item_ids)

            selling_items_quantity_soup = (cells[0].findAll(class_="item-quantity-static"))
            buying_items_quantity_soup = (cells[1].findAll(class_="item-quantity-static"))

            strlist = []
            for item in selling_items_quantity_soup:
                strlist.append(item.get_text())
            selling_items_quantity.append(strlist)
            
            strlist = []
            for item in buying_items_quantity_soup:
                strlist.append(item.get_text())
            buying_items_quantity.append(strlist)

        except IndexError:
            pass    #gets server names

unknown_ids = []

# Think of nixing this block to save on data space
#revises item ids
for offer in buying_items:
	for item in offer:
		if int(item) in item_dict1:
			a = offer.index(item)
			offer.pop(a)
			offer.insert(a, item_dict1[int(item)])
		else:
			unknown_ids.append(item)

#revises item ids
for offer in selling_items:
	for item in offer:
		if int(item) in item_dict1:
			a = offer.index(item)
			offer.pop(a)
			offer.insert(a, item_dict1[int(item)])
		else:
			unknown_ids.append(item)
			



pandaframe1 = [('offermade', offermade),
               ('qty', qty),
               ('names', names),
               ('selling_items', selling_items),
               ('buying_items', buying_items),
               ('selling_items_quantity', selling_items_quantity),
               ('buying_items_quantity', buying_items_quantity),
               ]

timestamp = str(datetime.datetime.now())
df_rotmg = pd.DataFrame.from_items(pandaframe1)
df_rotmg.to_pickle(timestamp, 'gzip')

del df_rotmg

#str(datetime.datetime.now())
#df.to_csv('scrapetest/Data/', str(datetime.datetime.now()) + '.csv', sep='\t')

print(len(offermade))
