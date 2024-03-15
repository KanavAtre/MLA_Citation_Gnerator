# Importing BeautifulSoup and
# it is in the bs4 module
import pandas.core.dtypes.astype
from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://www.space.com/15421-black-holes-facts-formation-discovery-sdcmp.html'
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}
response = requests.get(url, headers = headers)
soup = BeautifulSoup(response.content, "html.parser")

title = str(soup.find('title').contents[0])

titles = title.split("|")
title = titles[0]

x = soup.findAll('a')

for i in x:
    if "author" or "authors" in str(i["class"]):
        print(i.contents)
#author = str(soup.findAll('a'))


'''
if len(titles)>1:
    author = titles[1]
'''


if title == "None" or title == '403 Forbidden':
    title = str(soup.find('h1').contents[0])
    titles = title.split("|")
    title = titles[0]

print(title)
#print(author)
#print(soup.prettify())