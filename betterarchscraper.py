from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import re
from item_dict import item_dict1


def scrapedata(iterations):

    if iterations == 0:
        scrape_url('https://www.realmeye.com/recent-offers')     
    pandaframe1 = [('offermade', offermade),
               ('qty', qty),
               ('names', names),
               ('selling_items', [str(i) for i in selling_items]),
               ('buying_items', [str(i) for i in buying_items]),
               ('selling_items_quantity', [str(i) for i in selling_items_quantity]),
               ('buying_items_quantity', [str(i) for i in buying_items_quantity]),
               #('servers', servers)
               ]
    df = pd.DataFrame.from_items(pandaframe1)
    return df

def scrape_url(url):
    servers = []
    offermade = []
    qty = []
    names = []
    selling_items = []
    buying_items = []
    selling_items_quantity = []
    buying_items_quantity = []
    
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'lxml')
    rows = soup.find_all('tr')

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
        
        #gets server names
        if len(cells) == 8:
            servers.append(row.findAll('td')[7].get_text())
        elif len(cells) == 7:
            servers.append('Hidden')
        else:
            servers.append('ERROR')

print(scrapedata(0))
                 
            
