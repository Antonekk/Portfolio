#Antoni Strasz

import urllib.request
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urljoin
import queue
from threading import Thread
from threading import Lock


#Sprawdzamy czy link jest prawidłowy
def check_if_url_valid(url):
    parsed_url = urlparse(url)
    return bool(parsed_url.netloc) and bool(parsed_url.scheme)


#Wyszukujemy i generujemy poprawne linki
def get_all_links(soup,url):
    links = []
    for link in soup.find_all('a'):
        l = link.attrs.get("href")
        #jeżeli link jest odnośnikiem na podstronę strony którą sprawdzamy to odpowiednio smieniamy link
        if not check_if_url_valid(link.get('href')):
            l = urljoin(url, l)
        links.append(l)
    return links


def crawl_main(crawl_queue: queue.Queue, action,all_urls_visited,list_of_actions):
    global lock
    page,distance = crawl_queue.get()
    try:
        with urllib.request.urlopen(page) as web_page:
            tekst = web_page.read().decode('utf-8')
    except:
        print("Cant't read webside content")
        return

    try:
        action_on_page = action(tekst)
        lock.acquire()
        list_of_actions.append((page,action_on_page))
        lock.release()
    except:
        print("Cant't apply function to webside content")
        return

    try:
        soup = BeautifulSoup(requests.get(page).content, "html.parser")
    except:
        print("Cant't parse website content")
        return


    if distance >= 1:
        links = get_all_links(soup,page)
        for link in links:
            lock.acquire()
            if link not in all_urls_visited :
                all_urls_visited.add(link)
                crawl_queue.put((link,distance-1))
            lock.release()
    return (page,action_on_page)






def crawl(start_page,distance,action):
    global lock
    lock = Lock()
    crawl_queue = queue.Queue()
    crawl_queue.put((start_page,distance))
    all_urls_visited = set()
    all_urls_visited.add(start_page)

    list_of_actions = []

    while not crawl_queue.empty():
        ths = [Thread(target=crawl_main,args=(crawl_queue,action,all_urls_visited,list_of_actions)) for _ in range(crawl_queue.qsize())]
        [th.start() for th in ths]
        [th.join() for th in ths]

    return list_of_actions






c = crawl("https://skos.ii.uni.wroc.pl/my/",2 ,lambda tekst : 'kursy' in tekst)
for i in c:
    print(i)

