import sys
import requests
import re
import time

from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote


class SiteParser(object):
    SITE = ''
    HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

    @classmethod
    def get_parser(cls, **kwargs):
        engine = kwargs.pop('engine', 'google').lower().title()+'Parser'
        parcer_class = getattr(sys.modules[__name__], engine)
        return parcer_class(**kwargs)

    def __init__(self, url='', text='', limit=10, depth=0):
        url = url or self.SITE

        self._soup = None

        self.uri = urlparse(url)
        self.text = text
        self.limit = limit
        self.depth = depth

        params = self.get_request_params()
        try:
            response_text = requests.get(url, params, headers=self.HEADERS).text
            self._soup = BeautifulSoup(response_text, features="html.parser")
        except Exception as e:
            print('!!! %s' % e)

    def get_request_params(self):
        return {}

    def parse_url(self, elem):
        ref = elem['href']
        if not ref.startswith('http'):
            ref = '{uri.scheme}://{uri.netloc}{ref}'.format(uri=self.uri, ref=ref)
        return elem.text.strip(), unquote(ref)

    def find_urls(self):
        return self._soup.find_all('a', href=re.compile(r'[/]([a-z]|[A-Z])\w+'),
                                   text=True, limit=self.limit) if self._soup else None

    def parse(self, t=0):
        urls = self.find_urls()
        if urls:
            for i, url in enumerate(urls):
                text, ref = self.parse_url(url)
                print('%s%s: %s\n%s%s' % ('\t' * t, i + 1, text, '\t' * (t + 1), ref))

                if self.depth > 0:
                    SiteParser(ref, limit=self.limit, depth=self.depth - 1).parse(t + 1)
        elif self._soup:
            print('%s! Nothing found. Captcha may be required !' % ('\t'*t))


class YandexParser(SiteParser):
    SITE = 'https://yandex.ru/search/'

    def get_request_params(self):
        return {'text': self.text, 'numdoc': self.limit + 5}

    def parse_url(self, elem):
        text = elem.find('div', {'class': 'organic__url-text'}).text
        ref = elem.find('a').get('href')
        if ref.startswith('//'):
            ref = '{uri.scheme}:{ref}'.format(uri=self.uri, ref=ref)
        return text, unquote(ref)

    def find_urls(self):
        return self._soup.find_all('div',
                                   {'class': 'organic organic_with-related_yes typo typo_text_m typo_line_s i-bem'},
                                   limit=self.limit)


class GoogleParser(SiteParser):
    SITE = 'https://www.google.com/search'

    def get_request_params(self):
        return {'q': self.text, 'num': self.limit + 5}

    def parse_url(self, elem):
        text = elem.find('h3', {'class': 'LC20lb'}).text
        ref = elem.find('a').get('href')
        return text, unquote(ref)

    def find_urls(self):
        return self._soup.find_all('div', {'class': 'r'}, limit=self.limit)


