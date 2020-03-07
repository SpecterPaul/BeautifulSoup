import pandas as pd
import requests
from requests import get
from bs4 import BeautifulSoup
import time
from time import sleep
from random import randint
from IPython.display import clear_output
from warnings import warn

names = []
prices = []

start_time = time.time()
requests = 0
pages = [str(i) for i in range(1, 5)]

for page in pages:
    response = get('https://www.jumia.co.ke/catalog/?q=earphones&page=' + page)

    sleep(randint(8, 15))

    # monitoring the request
    requests += 1
    elapsed_time = time.time() - start_time
    print('Request:{}; Frequency: {} requests/s'.format(requests, response.status_code))
    clear_output(wait=True)

    # Throw a warning for a non-200 status codes
    if response.status_code != 200:
        warn('Request{}; Status code: {}'.format(requests, response.status_code))

    # Break the loop if the number of requets is greater than expected
    if requests > 25:
        warn('The number of the request seem to be greater that the expected')
        break

    # parse the content of the request with BeautifulSoup

    page_html = BeautifulSoup(response.text, 'html.parser')

    # select the the 40 div container

    itemsSection = page_html.find('section', class_='products -mabaya')
    cartDivs = itemsSection.find_all('a', class_='link')
    for cartDiv in cartDivs:
        name = cartDiv.find('span', class_='name')
        price = cartDiv.find('span', class_='price')
        price = price.find('span', dir='ltr')
        prices.append(price.text)
        names.append(name.text)

test_df= pd.DataFrame({
    'price': prices,
    'name': names
})

