import logging

from src.connection.conn_web import WebLoader
from src.connection.conn_redis import get_proxy_redis_conn


def get_proxy(page_cnt=10):
    connection = WebLoader('https://www.xicidaili.com', time_gap=5)
    res = []
    for i in range(1, page_cnt + 1):
        url = 'https://www.xicidaili.com/wn/{}'.format(i)
        soup = connection.get(url)
        tr_list = soup.find_all('tr')[1:]
        for tr in tr_list:
            td_list = tr.find_all('td')
            host = '{}:{}'.format(td_list[1].string.strip(), td_list[2].string.strip())
            if all([float(x['title'][:-1]) < 0.5 for x in tr.find_all('div', class_='bar')]):
                yield host
    # return res


def flush_proxy():
    redis_client = get_proxy_redis_conn()
    # redis_client.set('ip_proxy', )
    for p in get_proxy(10):
        logging.info('add proxy to redis: {}.'.format(p))
        redis_client.append('ip_proxy', p)
