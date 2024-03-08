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
products = []

# Gather links to players' pages
link_elements = soup.select("a[href]")
for link_element in link_elements:
    url = link_element['href']
    if ("/players/" in url) and (".html" in url) and (url not in visited):
        urls.append(url)
        visited.append(url)

# Scrape through player urls

player_url = "https://www.basketball-reference.com" + visited[0]
page2 = requests.get(player_url)
soup2 = BeautifulSoup(page2.text, 'html.parser')

print('Classes of each table')
table = soup2.find('table', class_='stats_table sortable row_summable')
print(table.get('class'))

#extract data from individual player page
for row in table.tbody.find_all('tr'):
    columns = row.find_all('td')




#Extract specific data from products and store it
player_data = {}
player_data["url"] = (player_url)
player_data["age"] = (columns[0].text.strip())
player_data["pos"] = columns[3].text.strip()
player_data["games"] = columns[4].text.strip()
player_data["games_started"] = columns[5].text.strip()
player_data["minutes pg"] = columns[6].text.strip()

products.append(player_data)



#CSV output
with open('player_stats.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)

    #Fill CSV file
    for player in products:
        writer.writerow(player.values())
