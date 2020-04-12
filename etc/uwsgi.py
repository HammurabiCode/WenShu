if __name__ == "__main__":
    cfg = """[uwsgi]
http=:8080
wsgi-file=web_service/web_main.py 
callable=web_app 
"""
    print(cfg)
