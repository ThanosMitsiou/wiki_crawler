import requests
from time import time,sleep
from collections import deque
from threading import Thread
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup, SoupStrainer


class Crawler:

    def __init__(self, starting_url, ending_url):
        self.ending_url = ending_url
        self.queue = deque()
        self.queue.append(starting_url)
        self.queue.append('level')
        self.session = requests.Session()
        self.pool = ThreadPoolExecutor(max_workers=5)

    def crawl(self, depth):
        seen = set()
        level = 0
        t1 = time()
        links_crawled = 0

        while True:
            url = self.queue.popleft()
            if level > depth:
                return False

            print(url, level)
            if url == self.ending_url:
                return True

            if url == 'level':
                level += 1
                self.queue.append('level')
                sleep(5)
                continue

            # Check if already visited
            if url in seen:
                continue

            self.pool.submit(self.get_wiki_links, url)
            # self.get_wiki_links(url=url)

            links_crawled += 1

            if links_crawled % 100 == 0:
                print(f'for the {links_crawled} required {time() - t1}')

        return

    def get_wiki_links(self, url: str):
        """
        Given a wiki url, put all the wiki sun links in the wue
        :param url:
        :return:
        """
        prefix = '/wiki'
        page = self.session.get('https://en.wikipedia.org' + url)
        soup = BeautifulSoup(page.text, 'lxml', parse_only=SoupStrainer('a'))

        for link in soup.find_all(['a'], href=True):
            wiki_link = link.get('href')
            if ':' in wiki_link or '.png' in wiki_link:
                continue
            if wiki_link.startswith(prefix):
                self.queue.append(wiki_link)

        return


crawler = Crawler(starting_url='/wiki/Computer_science', ending_url='/wiki/fsdfsfs')

crawler.crawl(depth=100)
