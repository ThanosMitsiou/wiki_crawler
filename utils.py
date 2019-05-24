import requests
from bs4 import BeautifulSoup, SoupStrainer


def get_wiki_sublinks(url: str):
    prefix = '/wiki'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml', parse_only=SoupStrainer('a'))
    links = list()

    for link in soup.find_all(['a'], href=True):
        wiki_link = link.get('href')
        if wiki_link.startswith(prefix):
            links.append(wiki_link)

    return links