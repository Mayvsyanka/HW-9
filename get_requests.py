import requests
from bs4 import BeautifulSoup
import json

authors_urls = []

def parse_pages_query(base_url):


    n = 0

    while True:

        n = n+ 1

        url = base_url + f'page/{n}/'
        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')
        quotes_div = soup.find_all('div', {'class': 'quote'})

        if soup.find('small', attrs={'class': 'author'}) == None:
            break

        for quote_info in quotes_div:

                authors_name = quote_info.find(
                    'small', attrs={'class': 'author'}).string
                quote = quote_info.find('span', {'class': 'text'}).string
                tags = quote_info.find('meta')['content'].split(',')

                json_dictionary = {"tags": tags,
                               "author": authors_name, "quote": quote}

                with open("quotes.json") as fh:
                    file_in = fh.read().strip()

                    if not file_in:
                        with open('quotes.json', "w", encoding='utf-8', errors='replace') as fh:
                            json.dump([json_dictionary], fh)

                    else:
                        with open('quotes.json', "r") as fh:
                            data = json.load(fh)
                            data.append(json_dictionary)

                        with open('quotes.json', "w", encoding='utf-8', errors='replace') as fh:
                            json.dump(data, fh)


def parse_authors(base_url):

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

        for author in authors_divs:

            author_name = author.find("h3").text.split("\n")[0]
            authors_bd = author.find(
                'span', attrs={'class': 'author-born-date'}).string
            authors_bp = author.find(
                'span', attrs={'class': 'author-born-location'}).string
            authors_description = author.find(
                'div').text


            author_json = {"fullname": author_name, "born_date": authors_bd,
                           "born_location": authors_bp, "description": authors_description}

            authors_list.append(author_json)

            with open("authors.json", "w") as fh:
                json.dump(authors_list, fh)


if __name__ == '__main__':

    with open("quotes.json", "w") as fh:
        pass

    base_url = "http://quotes.toscrape.com/"


    parse_pages_query(base_url)
    parse_authors(base_url)






