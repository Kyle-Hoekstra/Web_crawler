import requests
from bs4 import BeautifulSoup
import csv

# initialize the list of discovered urls
# with the first page to visit
urls = ["https://scrapeme.live/shop/"]
#Array to store dict entries of products and their data
products = []

# until all pages have been visited
while len(urls) != 0:
    # get the page to visit from the list
    current_url = urls.pop()
    
    # crawling logic
    response = requests.get(current_url)
    soup = BeautifulSoup(response.content, "html.parser")

    link_elements = soup.select("a[href]")
    for link_element in link_elements:
        url = link_element['href']
        if "https://scrapeme.live/shop" in url:
            urls.append(url)

    print("Number of Urls remaining: " + str(len(urls)))

    #Extract specific data from products and store it
    product = {}
    product["url"] = current_url 
    product["image"] = soup.select_one(".wp-post-image")["src"]
    #product["title"] = soup.select_one(".product_title").text() 
    product["price"] = soup.select_one(".price")

    #place product in products array for CSV to read through
    products.append(product)

#CSV output
with open('products.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)

    #Fill CSV file
    for product in products:
        writer.writerow(product.values())

