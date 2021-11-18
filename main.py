import requests
from bs4 import BeautifulSoup


class Scrapper(object):
    keywords = []
    all_articles = []
    url = 'https://habr.com/ru/all/'
    results = []

    def __init__(self, *keywords):
        self.keywords = []
        self.all_articles = []
        self.results = []
        for keyword in keywords:
            self.keywords.append(keyword)

    def get_page(self):

        response = requests.get(
            url=self.url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
            }
        )
        if response.status_code == 200:

            return response.text
        else:
            print(f'Сервер вернул {response.status_code}. Контент не загружен')
            return None

    def get_soup(self):

        if page := self.get_page():
            return BeautifulSoup(page, 'html.parser')
        else:
            return None

    def get_all_articles(self):

        if soup := self.get_soup():
            article_list_soup = soup.find_all('article')
            all_articles = []

            for article_soup in article_list_soup:
                article_info = {
                    'date': article_soup.find('time').get('title'),
                    'title': article_soup.find('h2').text,
                    'hubs': article_soup.find('div', {'class': 'tm-article-snippet__hubs'}).text,
                    'link': 'https://habr.com' + article_soup.find('h2').find('a').get('href'),
                    'preview': article_soup.find('div', {'class': 'article-formatted-body'}).text
                }

                all_articles.append(article_info)

            return all_articles

    def get_articles_by_keywords(self):

        if self.all_articles:
            articles_by_kw = []
            for article in self.all_articles:
                text_to_search_in = f"{article['title']} {article['hubs']} {article['preview']}"
                if any([keyword in text_to_search_in.lower() for keyword in self.keywords]):
                    articles_by_kw.append(article)
            return articles_by_kw
        else:
            return None

    def print_search_results(self):

        if self.results:
            for result in self.results:
                print(
                    f'{result["date"]} - {result["title"]} - {result["link"]}')

    def run(self):

        self.all_articles = self.get_all_articles()
        if self.keywords:
            self.results = self.get_articles_by_keywords()
        else:
            self.results = self.all_articles
        self.print_search_results()


print('Запрос с фильтрацией по ключевым словам.')
scrapper = Scrapper('обзор', 'хэш', 'unity')
scrapper.run()

print('Запрос без ключевых слов.')
scrapper_wo_kw = Scrapper()
scrapper_wo_kw.run()
