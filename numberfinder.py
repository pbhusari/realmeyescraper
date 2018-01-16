from bs4 import BeautifulSoup
import requests

url = 'https://www.realmeye.com/recent-offers'
response = requests.get(url)
html = response.content
soup = BeautifulSoup(html, 'lxml')


if int(soup.findAll('a')[(len(soup.findAll('a')) - 2)].get_text()[:1]) < 1:
    return int(soup.findAll('a')[(len(soup.findAll('a')) - 2)].get_text()[:1])
else:
    return 0
