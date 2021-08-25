import requests
from bs4 import BeautifulSoup
from pprint import pprint
from pymongo import MongoClient
import pandas as pd



client = MongoClient('localhost', 27017)
data = client.products
collections = data.collections
# data.collections.delete_many({})


pprint([i for i in collections.find({})])