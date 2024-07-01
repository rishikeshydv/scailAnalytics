import requests
from bs4 import BeautifulSoup
import json
import os
import time
import random
import re
import csv
import pandas as pd

#URL of the website
URL = "https://press.essexregister.com/prodpress/clerk/ShowDetails.aspx"

#sending #POST request to the website
#postReq = requests.post(URL)

#sending GET request to the website
getReq = requests.get(URL)
getRes = getReq.content
soup = BeautifulSoup(getRes, 'html.parser')
print(soup.prettify())