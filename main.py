import requests
import re
from bs4 import BeautifulSoup


KEYWORDS = ['дизайн', 'фото', 'web', 'python']
URL = 'https://habr.com'

response = requests.get(URL + '/ru/all/')

response.raise_for_status()

soup = BeautifulSoup(response.text, features='html.parser')

articles = soup.find_all('article', class_='tm-articles-list__item')
for article in articles:
    link = article.find('a', class_='tm-article-snippet__title-link')
    href = link.attrs.get('href')
    response_inner = requests.get(URL + href)
    response_inner.raise_for_status()
    soup_inner = BeautifulSoup(response_inner.text, features='html.parser')
    inner_text_html = BeautifulSoup(soup_inner.find('div', class_='article-formatted-body').text, 'html.parser').text
    words = [word.group() for word in re.finditer(r'[a-zа-яё]{2,}', inner_text_html.lower())]
    for word in words:
        if any([keyword in word for keyword in KEYWORDS]):
            print(f'Дата: {article.find("span", class_="tm-article-snippet__datetime-published").text} - {link.text} - '
                  f'{URL + href}')
            break
