import requests
from bs4 import BeautifulSoup
import csv

# initialize the list of discovered urls
# with the first page to visit
urls = ["https://www.espn.com/nba/stats/player/"]
visited = []
#Array to store dict entries of products and their data
products = []

# until all pages have been visited
while len(urls) != 0:
    # get the page to visit from the list
    current_url = urls.pop()
    
    # crawling logic
    response = requests.get(current_url)
    soup = BeautifulSoup(response.content, "html.parser")

    link_elements = soup.select('.AnchorLink')
    print("here")
    for link_element in link_elements:
        url = link_element['href']
        if ("https://www.espn.com/nba/player/_/id" in url) and (url not in visited):
            urls.append(url)
            visited.append(url)
    
    print("Number of Urls remaining: " + str(len(urls)))

for link in visited:
    print(link)
