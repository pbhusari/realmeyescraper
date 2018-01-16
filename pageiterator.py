from bs4 import BeautifulSoup
import requests

url = 'https://www.realmeye.com/recent-offers'
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html, 'lxml')
#rows = soup.findall('tbody')

rows = soup.find_all('tr')

offermade = []
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

for i in range (1, 10):
    url = 'https://www.realmeye.com/recent-offers/' + str(i*100+1)
    response = requests.get(url)
    html = response.content

    soup = BeautifulSoup(html, 'lxml')
    #rows = soup.findall('tbody')

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
