# -*- coding: utf-8 -*-
import os
import re
import time
from hashlib import md5

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

from movies import db
from movies.models import MaoyanMovie, clean_db, init_db
from movies.settings import Config

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

    def get_movie_intro(self, movie_intro_url):
        print(movie_intro_url)
        time.sleep(2)
        try:
            response = requests.get(url=movie_intro_url, headers=headers)
            print(response.status_code)
            if response.status_code == 200:
                # parse html
                html = response.text
                soup = BeautifulSoup(html, 'lxml')
                movie_info = soup.find(name='div', attrs={'mod-content'}).get_text().strip()
                category = soup.find(name='li', attrs={'ellipsis'}).get_text().strip()
                return movie_info, category
        except Exception:
            return None

    def parse_html(self, html):
        soup = BeautifulSoup(html, 'lxml')
        movies_info = soup.find_all(name='dd')
        for movie in movies_info:
            name = movie.find(name='p', attrs={'name'}).get_text()
            stars = movie.find(name='p', attrs={'star'}).get_text()[3:]
            time = movie.find(name='p', attrs={'releasetime'}).get_text()[5:]
            release_time = re.sub(u"\\(.*?\\)", "", time)
            img_url = movie.find(name='img', attrs={'board-img'}).get('data-src')
            score = movie.find(name='p', attrs={'score'}).get_text()
            movie_intro_url = 'https://maoyan.com' + movie.find(name='a').get('href')
            movie_info, category = self.get_movie_intro(movie_intro_url)
            yield {
                'name': self.clean_string(name),
                'stars': self.clean_string(stars),
                'release_time': release_time,
                'score': score,
                'img_url': img_url,
                'info': movie_info,
                'category': category
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
                item.img_url = movie_info['img_url']
                item.info = movie_info['info']
                item.category = movie_info['category']
                db.session.add(item)
            # commit after finish
            db.session.commit()
        db.session.close()


def download_img(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            save_image(response.content)
        return None
    except RequestException:
        return None


def save_image(content):
    file_path = os.path.join(Config.BASEDIR, 'img', f'{md5(content).hexdigest()}.jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()


if __name__ == '__main__':
    init_db()
    spider = MovieSpider()
    spider.run_spider()
