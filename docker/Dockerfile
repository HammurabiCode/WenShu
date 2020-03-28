FROM registry.cn-shanghai.aliyuncs.com/hammurabi/wenshu:0.0.1

WORKDIR /hammurabi/WenShu

COPY WenShu.tar.gz /hammurabi/WenShu

RUN tar xzf WenShu.tar.gz


CMD python etc/uwsgi.py |  uwsgi --ini - 