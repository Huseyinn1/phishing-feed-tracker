from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, URL

engine = create_engine("sqlite:///urls.db")
#engine = create_engine("postgresql://myuser:password@localhost/fastapi_database")
#engine = create_engine("postgresql://myuser:password@localhost/fastapi_database")
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(bind=engine)


def save_urls_to_database(urls, source):
    for url in urls:
        url_obj = URL(url=url.url, url_id=url.url_id, url_author=url.url_author, source=source)
        session.add(url_obj)
    session.commit()


def get_existing_urls():
    return [result[0] for result in session.query(URL.url).all()]

def print_new_urls(new_urls,source):
 
    if len(new_urls) > 0:
        print(f"{len(new_urls)} new {source} URLs added.")
     
    else:
        print(f"No new Urls From {source} found.")
