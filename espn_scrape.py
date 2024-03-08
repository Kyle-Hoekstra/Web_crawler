import requests
from bs4 import BeautifulSoup
import csv

# initialize the list of discovered urls
# with the first page to visit
start_url = "https://www.basketball-reference.com/leagues/NBA_2017_totals.html"
page = requests.get(start_url)
soup = BeautifulSoup(page.text, 'html.parser')

urls = []
visited = []


# Gather links to players' pages
link_elements = soup.select("a[href]")
print("before loop\n")
for link_element in link_elements:
    print("inside")
    url = link_element['href']
    if ("/players/" in url) and (".html" in url) and (url not in visited):
        urls.append(url)
        visited.append(url)

for link in visited:
    print(link)


page2 = requests.get(visited[0])
soup2 = BeautifulSoup(page2.text, 'html.parser')


