from config import *
from bs4 import BeautifulSoup
import requests

def get_yahoo_articles():
    yahoo_url = 'https://finance.yahoo.com'
    page = requests.get(yahoo_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    selector_list = [
        '#Col1-0-ThreeAmigos-Proxy > div > div:nth-child(1) > div.Pos\(r\).dustyImage.W\(\$ntkLeadWidth\).Fl\(start\).article-cluster-boundary > a', 
        '#Col1-0-ThreeAmigos-Proxy > div > div:nth-child(1) > div.Mstart\(67\%\) > ul > li:nth-child(1) > a', 
        '#Col1-0-ThreeAmigos-Proxy > div > div:nth-child(1) > div.Mstart\(67\%\) > ul > li:nth-child(2) > a', 
        '#Col1-0-ThreeAmigos-Proxy > div > div:nth-child(1) > div.Mstart\(67\%\) > ul > li:nth-child(3) > a', 
        '#Col1-0-ThreeAmigos-Proxy > div > div:nth-child(2) > div:nth-child(2) > ul > li:nth-child(1) > a', 
        '#Col1-0-ThreeAmigos-Proxy > div > div:nth-child(2) > div:nth-child(2) > ul > li:nth-child(2) > a', 
        '#Col1-0-ThreeAmigos-Proxy > div > div:nth-child(3) > ul > li:nth-child(1) > a', 
        '#Col1-0-ThreeAmigos-Proxy > div > div:nth-child(3) > ul > li:nth-child(2) > a', 
        '#Col1-0-ThreeAmigos-Proxy > div > div:nth-child(3) > ul > li:nth-child(3) > a'
    ]

    url_list = [
        [article['href'] for article in soup.select(url)] 
        for url in selector_list
    ]

    return url_list