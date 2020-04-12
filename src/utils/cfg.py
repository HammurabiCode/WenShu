import configparser


_conf_file = 'etc/wenshu.conf'
_parser = configparser.ConfigParser()

_parser.read(_conf_file)

proxy_redis_host = _parser.get('proxy_redis', 'host', fallback='')
proxy_redis_auth = _parser.get('proxy_redis', 'auth', fallback='')
proxy_redis_db = _parser.get('proxy_redis', 'db', fallback='')

mongo_uri = _parser.get('mongo', 'uri', fallback='')



