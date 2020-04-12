import re
import logging
from queue import Queue
from threading import Thread

from src.connection.conn_web import WebLoader
from src.connection.conn_mongo import quota_coll


class DoubanBookQuotaSpider(object):
    def __init__(self, book_id, time_gap=10, writer=None, sort='page_num'):
        super().__init__()
        self.connection = WebLoader('http://www.douban.com', time_gap=time_gap)
        self.book_id = book_id
        self.sort = sort
        self.book_home_url = 'http://book.douban.com/subject/{}/blockquotes?sort={}'.format(self.book_id, self.sort)
        self.writer = writer

        self.result = []
        self.book_home_soup = None
        self.book_name = None
        self._init_name()

    def _init_name(self):
        self.book_home_soup = self.connection.get(self.book_home_url)
        name_tag = self.book_home_soup.find('h1')
        if name_tag:
            raw_name = name_tag.string.strip()
            if '《' in raw_name and '》' in raw_name:
                self.book_name = raw_name[raw_name.index('《') + 1:raw_name.index('》')]
            else:
                self.book_name = raw_name

    def get_all(self, start=0):
        while True:
            logging.info('run {}, {}, {}.'.format(self.book_id, self.book_name, start))
            soup = self.connection.get(self.book_home_url, params={'start': start})
            yuanwen_list = soup.find_all('a', string='查看原文')
            cnt = 0
            for x in yuanwen_list:
                one_quota = self._parse_quota_from_a_tag(x)
                self.result.append(one_quota)
                self.writer.write(one_quota)
                cnt += 1
            print(start, cnt)
            start += cnt
            if not cnt:
                break

    def _parse_quota_from_a_tag(self, a_tag):
        quota = a_tag.previous_sibling[:-1].replace('\n', '').strip()
        if quota.endswith('...'):
            url = a_tag['href']
            soup = self.connection.get(url)
            figcaption = soup.find('figcaption')
            if figcaption:
                page = soup.find('span', class_='page-num')
                if page:
                    page = int(page.string.strip()[1:-1])
                quota = figcaption.previous_sibling.string.replace('\n', '').strip()
                return a_tag['href'], page, quota
        page = 0
        figcaption = a_tag.next_sibling.next_sibling.find('figcaption')
        if figcaption:
            page_strs = re.findall(r'\d+', figcaption.string.strip())
            if page_strs:
                page = int(page_strs[0])
        return a_tag['href'], page, quota


def get_quota(book_id):
    res_queue = Queue()
    queue_writer = QueueWriter(res_queue)
    spider = DoubanBookQuotaSpider(book_id, time_gap=10, writer=queue_writer)

    def _down():
        spider.get_all()
        res_queue.put(None)
    Thread(target=_down).start()
    quota = res_queue.get()
    while quota is not None:
        print(quota)
        quota_coll.update_one(
            {'href': quota[0]},
            {'$set': {'book_id': int(book_id), 'page': int(quota[1]), 'quota': quota[2]}},
            upsert=True,
        )
        quota = res_queue.get()


class MongoBucketWriter(object):
    def write(self, doc):
        pass


class QueueWriter(object):

    def __init__(self, q):
        self.queue = q
        pass

    def write(self, item):
        self.queue.put(item)
