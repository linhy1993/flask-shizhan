# -*- coding: utf-8 -*-
import re

import requests
from bs4 import BeautifulSoup

from movies import db
from movies.models import MaoyanMovie, clean_db

headers = {
    'Cookie': '__mta=108942397.1569179242864.1569179595461.1569179600165.9; _lxsdk_cuid=16d5a5ebb94c8-0e804a28a9b404-38607501-fa000-16d5a5ebb94c8; uuid_n_v=v1; uuid=30A384E0DD6C11E9ACE10BB2E5F6D2609DAF34E90B7C434685BD961083A5259A; _csrf=e459ca46f7a8574c415857487f15b79ee072cf4d59cd607937cd758008bb9989; _lxsdk=30A384E0DD6C11E9ACE10BB2E5F6D2609DAF34E90B7C434685BD961083A5259A; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; _lxsdk_s=16d5a5ebb97-cd8-67f-0ed%7C%7C21',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
}


class MovieSpider(object):
    def __init__(self):
        self.results = []
        self.url = 'https://maoyan.com/board/4?offset='

    @staticmethod
    def clean_string(input_str):
        string = re.sub(r'\s+', ' ', input_str)
        output_str = string.strip()
        return output_str

    def get_html(self):
        for i in range(0, 100, 10):
            if i == 100:
                i -= 1
            try:
                response = requests.get(url=self.url + f'{i}', headers=headers)
                if response.status_code == 200:
                    print(self.url + f'{i}')
                    yield response.text
            except Exception:
                return None

    def parse_html(self, html):
        soup = BeautifulSoup(html, 'lxml')
        movies_info = soup.find_all(name='div', attrs={"class": "board-item-content"})
        for movie in movies_info:
            name = movie.find(name='p', attrs={'name'}).get_text()
            stars = movie.find(name='p', attrs={'star'}).get_text()[3:]
            time = movie.find(name='p', attrs={'releasetime'}).get_text()[5:]
            release_time = re.sub(u"\\(.*?\\)", "", time)
            score = movie.find(name='p', attrs={'score'}).get_text()

            yield {
                'name': self.clean_string(name),
                'stars': self.clean_string(stars),
                'release_time': release_time,
                'score': score
            }

    def run_spider(self):
        clean_db()
        for html in self.get_html():
            for movie_info in self.parse_html(html):
                item = MaoyanMovie()
                item.name = movie_info['name']
                item.stars = movie_info['stars']
                item.release_time = movie_info['release_time']
                item.score = movie_info['score']
                db.session.add(item)
        # commit after finish
        db.session.commit()


if __name__ == '__main__':
    spider = MovieSpider()
    spider.run_spider()