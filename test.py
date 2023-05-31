import requests
from bs4 import BeautifulSoup
import json

base_url = "http://quotes.toscrape.com/"

response = requests.get(base_url)

soup = BeautifulSoup(response.text, 'html.parser')
quotes_divs = soup.find_all('div', {'class': 'quote'})

author_urls = []

authors_list = []

n = 0

while True:

    n = n + 1

    url = base_url + f'page/{n}/'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    quotes_div = soup.find_all('div', {'class': 'quote'})

    if soup.find('small', attrs={'class': 'author'}) == None:
        break

    for div in quotes_div:

        author_url = base_url + div.find('a')['href']

        author_urls.append(author_url)


for url in list(set(author_urls)):

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    authors_divs = soup.find_all('div', {'class': 'author-details'})

    # print(authors_divs)

    for author in authors_divs:

        author_name = author.find("h3").text.split("\n")[0]
        authors_bd = author.find(
            'span', attrs={'class': 'author-born-date'}).string
        authors_bp = author.find(
            'span', attrs={'class': 'author-born-location'}).string
        authors_description = author.find('div').text

        author_json = {"fullname": author_name, "born_date": authors_bd,
                       "born_location": authors_bp, "description": authors_description}

        authors_list.append(author_json)

        with open("authors.json", "w") as fh:
            json.dump(authors_list, fh)
