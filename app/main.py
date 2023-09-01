from bs4 import BeautifulSoup
import httpx
from database import save_urls_to_database, get_existing_urls,print_new_urls
from mytypes.urls import URL    
from threading import Timer
import os
from dotenv import load_dotenv
load_dotenv()
def get_urls_phishtank():
    url = os.getenv("PHISHTANK_URL")

    response = httpx.get(url)
    content = response.text
    soup = BeautifulSoup(content, "html.parser")
    rows = soup.find_all("tr")
    urls = []
    
    for row in rows:
        link = row.find("a")
        url_id = link.text if link is not None else None

        url_cell = row.find_all("td")
        url = url_cell[1].text if len(url_cell) >= 2 else None

        author_link = url_cell[2].find("a") if len(url_cell) >= 3 else None

        url_author = author_link.text if author_link is not None else None

        url_obj = URL(url_id=url_id, url=url, url_author=url_author, source="phishtank")
        urls.append(url_obj)
    existing_urls = get_existing_urls()
    new_urls = [url for url in urls if url.url not in existing_urls]
    save_urls_to_database(new_urls, "phishtank")
    print_new_urls(new_urls,"phistank")

def get_urls(url):
    response = httpx.get(url)
    content = response.text

    urls = content.split("\n")
    urls = [url.strip() for url in urls if url.strip() != ""]

    return urls

def get_urls_usom_openphis():
    # Get USOM URLs
    usom_url = os.getenv("USOM_URL")
    usom_urls = get_urls(usom_url)[:100]

    existing_urls = get_existing_urls()

    new_usom_urls = [URL(url=url, url_id=None, url_author=None, source='usom')
                     for url in usom_urls if url not in existing_urls][:100]

    save_urls_to_database(new_usom_urls, 'usom')
    print_new_urls(new_usom_urls,"Usom")
   
    openphish_url = os.getenv("OPENPHISH_URL")
    openphish_urls = get_urls(openphish_url)[:100]
    
    new_openphish_urls = [URL(url=url, url_id=None, url_author=None, source='openphis')
                            for url in openphish_urls if url not in existing_urls][:100]

    save_urls_to_database(new_openphish_urls, 'openphish')
    print_new_urls(new_usom_urls,"Openphis")

def loop_phishtank():
   
   
   get_urls_phishtank()
   timer1 = Timer(10, loop_phishtank)
   timer1.start()


def loop_usom_openphis():
    
   
   get_urls_usom_openphis()
   timer2 = Timer(10, loop_usom_openphis)
   timer2.start()

if __name__ == "__main__":
    
  
   loop_phishtank()
   loop_usom_openphis()

