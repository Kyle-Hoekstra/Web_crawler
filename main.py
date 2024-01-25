import requests
from bs4 import BeautifulSoup
import sys


print("Importing modules...")

modules = ['requests', 'bs4']
for name in modules:
    if name not in sys.modules:
        print('You have not imported the {} module'.format(name))

print("Docker is magic")
