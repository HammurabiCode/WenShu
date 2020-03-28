

if __name__ == "__main__":
    cfg = """[uwsgi]
http=:5000
wsgi-file=web_service/__init__.py 
callable=web_app 
"""
    print(cfg)
    

