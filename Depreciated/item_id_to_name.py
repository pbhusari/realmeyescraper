from bs4 import BeautifulSoup
import requests
from Scraptest import unknown_ids

urls = []
for item in unknown_ids:
    urls.append('https://www.realmeye.com/offers-to/sell/' + item)

fh = open("Item Dictionary", "w")

fh.write('item_dict1 = {')
urls = list(set(urls))
url_num = 0
for item in urls:
    url_num += 1
    print(str(url_num) +  '/' + str(len(urls)) + '(' + item + ')')
    url = item
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'lxml')

    fh.write(item[40:] + ':"' + soup.findAll('strong')[3].get_text() + '"' + '\n' + ',')

fh.write('}')
fh.close()
