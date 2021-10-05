import celery
import requests
from bs4 import BeautifulSoup


class Task(celery.Task):

    def run(self, domain):

        response = requests.get(domain)
        response.encoding = 'utf-8'
        return self.soup_parcer(response)

    def soup_parcer(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')

        for tag_a in soup.find_all(target='_blank'):
            link = tag_a.get('href')

            if link is not None and link.startswith('/epz/order/notice/printForm/'):
                domain = 'https://zakupki.gov.ru' + link.replace('view.html', 'viewXml.html')
                response = requests.get(domain)
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.text, 'xml')

                print('{} - {}'.format(domain, soup.find('docPublishDate')))


myTask = Task()
myTask.run('https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber=1')
myTask.run('https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber=2')