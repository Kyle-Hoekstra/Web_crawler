import requests
from bs4 import BeautifulSoup
import csv
import time
import random
import pandas as pd
from fake_useragent import UserAgent
from IPython.core.display import clear_output
from urllib.request import Request, urlopen


# helper functions

def my_delay():
    # random generates float between 0 and 1
    delay_time = random.uniform(3, 4)
    time.sleep(delay_time)


'''
Make proxies and random_proxy provided by user on StackOverflow
https://stackoverflow.com/questions/38785877/spoofing-ip-address-when-web-scraping-python
'''
# Here I provide some proxies for not getting caught while scraping
ua = UserAgent() # From here we generate a random user agent
proxies = [] # Will contain proxies [ip, port]

def make_proxies():
    # Retrieve latest proxies
    proxies_req = Request('https://www.sslproxies.org/')
    proxies_req.add_header('User-Agent', ua.random)
    proxies_doc = urlopen(proxies_req).read().decode('utf8')

    soup = BeautifulSoup(proxies_doc, 'html.parser')
    proxies_table = soup.find('table', class_= 'table table-striped table-bordered')

    # Save proxies in the array
    for row in proxies_table.tbody.find_all('tr'):
        proxies.append({
            'ip':   row.find_all('td')[0].string,
            'port': row.find_all('td')[1].string
        })

    # Choose a random proxy
    proxy_index = random_proxy()
    proxy = proxies[proxy_index]

    for n in range(1, 20):
        req = Request('http://icanhazip.com')
        req.set_proxy(proxy['ip'] + ':' + proxy['port'], 'http')

        # Every 5 requests, generate a new proxy
        if n % 5 == 0:
            proxy_index = random_proxy()
            proxy = proxies[proxy_index]

        # Make the call
        try:
            my_ip = urlopen(req).read().decode('utf8')
            print('#' + str(n) + ': ' + my_ip)
            clear_output(wait = True)
        except: # If error, delete this proxy and find another one
            del proxies[proxy_index]
            print('Proxy ' + proxy['ip'] + ':' + proxy['port'] + ' deleted.')
            proxy_index = random_proxy()
            proxy = proxies[proxy_index]

# Retrieve a random index proxy (we need the index to delete it if not working)
def random_proxy():
    return random.randint(0, len(proxies) - 1)

user_agent_list = (
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
)




# Run make proxies
make_proxies()

###########################################################

#generate new proxy 
user_agent = random.choice(user_agent_list)
headers= {'User-Agent': user_agent, "Accept-Language": "en-US, en;q=0.5"}
proxy = random.choice(proxies)

# initialize the list of discovered urls
# with the first page to visit
start_url = "https://www.basketball-reference.com/leagues/NBA_2017_totals.html"
page = requests.get(start_url, headers=headers, proxies=proxy)
soup = BeautifulSoup(page.text, 'html.parser')

urls = []
products = []
visited = []

initial_row = {'url': "URL", 'name': "Name", 'age': "Age", 'pos': "Position", 'games': "Games Played", 'games_started': "Games Started", 'minutes pg': "MPG"}
products.append(initial_row)



# Gather links to players' pages
link_elements = soup.select("a[href]")
print("Extracting player links...")
for link_element in link_elements:
    url = link_element['href']

    if ("/players/" in url) and (".html" in url) and url not in visited:
        urls.append(url)
        visited.append(url)

print(str(len(urls)) + " players to extract.\n")
# Scrape through player urls
print("Extracting player data...")
tables_not_found = 0
num_players = 0



for link in urls:
    '''
    Basketball-reference.com's bot policy
    Currently we will block users sending requests to:
        our sites more often than twenty requests in a minute.
        This is regardless of bot type and construction and pages accessed.
        If you violate this rule your session will be in jail for an hour.
    '''
    # Delay of 3 to 4 seconds to comply with bot policy to limit to <20 requests per minute
    my_delay()
    # urls should already be unique as copies were filtered out above
    player_url = "https://www.basketball-reference.com" + link


    #generate new proxy 
    user_agent = random.choice(user_agent_list)
    headers= {'User-Agent': user_agent, "Accept-Language": "en-US, en;q=0.5"}
    proxy = random.choice(proxies)

    #access the players page with the proxy
    player_page = requests.get(player_url, headers=headers, proxies=proxy)
    soup2 = BeautifulSoup(player_page.text, 'html.parser')

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

    # url for the players page
    player_data["url"] = (player_url)

    #name of the player
    player_name = soup2.find('h1').text.strip()
    player_data["name"] = player_name

    #age of the player
    player_data["age"] = (columns[0].text.strip())

    #Stats of the player{position, games played, games started, mpg}
    try:
        player_data["pos"] = columns[3].text.strip()
    except:
        player_data["pos"] = "x"
    try:
        player_data["games"] = columns[4].text.strip()
    except:
        player_data["games"] = "x"
    try:
        player_data["games_started"] = columns[5].text.strip()
    except:
        player_data["games_started"] = "x"
    try:
        player_data["minutes pg"] = columns[6].text.strip()
    except:
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
