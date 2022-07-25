import datetime
from bs4 import BeautifulSoup as BS
import requests


def logger(path):
    def decorator(foo):
        def new_foo(*args, **kwargs):
            time_now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
            result = foo(*args, **kwargs)
            logs = f'Функция: {foo.__name__} Время: {time_now} Аргументы: {args}, {kwargs} Результат: {result}\n'
            with open(path, 'w', encoding='UTF-8') as f:
                f.write(logs)
            return result
        return new_foo
    return decorator


@logger(path='logs.txt')
def habr_posts(keywords):
    responce = requests.get('https://habr.com/ru/all/')
    responce.raise_for_status()
    soup = BS(responce.text, 'html.parser')
    posts = soup.find_all('article', class_='tm-articles-list__item')
    count = 0

    for post in posts:
        post_title = post.find('a', class_='tm-article-snippet__title-link')
        link = f"https://habr.com{post_title.attrs.get('href')}"
        res_article = requests.get(link)
        soup_article = BS(res_article.text, 'html.parser')
        article = soup_article.find('div', id="post-content-body")
        if set(keywords) & set(post.text.lower().split(' ')) or set(keywords) & set(article.text.lower().split(' ')):
            post_time = post.find('time')
            print(f"{post_time.attrs.get('title')}, {post_title.text}, https://habr.com{post_title.attrs.get('href')}")
            count += 1
    return f'{count} статей найдено'


if __name__ == '__main__':
    habr_posts(['дизайн', 'фото', 'web', 'python'])
