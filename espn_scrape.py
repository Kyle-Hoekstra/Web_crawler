import requests
from bs4 import BeautifulSoup
import csv
import time
import random

# initialize the list of discovered urls
# with the first page to visit
start_url = "https://www.basketball-reference.com/leagues/NBA_2017_totals.html"
page = requests.get(start_url)
soup = BeautifulSoup(page.text, 'html.parser')

urls = []
products = []
visited = []

def my_delay():
    # random generates float between 0 and 1
    delay_time = random.random()
    time.sleep(delay_time)


# Gather links to players' pages
link_elements = soup.select("a[href]")
print("Extracting player links...")
for link_element in link_elements:
    url = link_element['href']

    if ("/players/" in url) and (".html" in url):
        urls.append(url)

for link in urls:
    print(link)
# Scrape through player urls
print("Extracting player data...")
tables_not_found = 0


for link in urls:
    if link not in visited:
        visited.append(link)
    else:
        continue
    # Delay for a random amount of time
    my_delay()
    # Goto page for player
    player_url = "https://www.basketball-reference.com" + link
    page2 = requests.get(player_url)
    soup2 = BeautifulSoup(page2.text, 'html.parser')
    #Extract table of player stats data
    table = soup2.find('table', class_='stats_table sortable row_summable')
    
    if type(table) == type(None):
        # If player doesn't have a table, ignore for now
        # TODO
        tables_not_found += 1
        print("no table" + str(tables_not_found))
        continue

    #extract data from individual player table
    for row in table.tbody.find_all('tr'):
        columns = row.find_all('td')

    #Extract specific data from player table and store it
    player_data = {}
    player_data["url"] = (player_url)
    player_data["age"] = (columns[0].text.strip())

    if 3 <= len(columns):
        player_data["pos"] = columns[3].text.strip()
    else:
        player_data["pos"] = "x"
    if 4 <= len(columns):
        player_data["games"] = columns[4].text.strip()
    else:
        player_data["games"] = "x"
    if 5 <= len(columns):
        player_data["games_started"] = columns[5].text.strip()
    else:
        player_data["games_started"] = "x"
    if 6 <= len(columns):
        player_data["minutes pg"] = columns[6].text.strip()
    else:
        player_data["minutes pg"] = "x"

    products.append(player_data)



#CSV output
print(str(tables_not_found) + " tables not found.")
print("Writing to csv...")
with open('player_stats.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)

    #Fill CSV file
    for player in products:
        writer.writerow(player.values())
