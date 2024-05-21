import re

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


class KufarParser:
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': '*/*'
    }

    @classmethod
    def get_soup(cls, url: str) -> BeautifulSoup | None:
        response = requests.get(url, headers=cls.HEADERS)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            return soup
        else:
            print(f'{response.status_code} | {url}')

    def get_notebook_list(self, soup: BeautifulSoup) -> list:
        links = []
        sections = soup.find_all('section')
        for section in sections:
            link = section.find('a', href=True)['href'].split('?')[0]
            price = section.find('p', class_='styles_price__G3lbO')
            if not price:
                price = section.find('span', class_='styles_price__vIwzP')
            price = price.text
            price = re.sub(r'[^0-9]', '', price)
            if price.isdigit():
                links.append(link)

        return links

    def get_notebook_data(self, soup: BeautifulSoup):
        title = soup.find('h1', class_='styles_brief_wrapper__title__Ksuxa')
        if title:
            title = title.text

        price = soup.find('span', class_='styles_main__eFbJH')
        if not price:
            price = soup.find('div', class_='styles_discountPrice__WuQiu')

        price = price.text.replace(' ', '').replace('р.', '')
        price = float(price)

        description = soup.find('div', itemprop="description")
        if description:
            description = description.text

        params = soup.find('div', class_="styles_parameter_block__6HwcY").find_all('div',
                                                                                   class_='styles_parameter_wrapper__L7UfK')
        for param in params:
            key = param.find('div', class_='styles_parameter_label__i_OkS').text
            if key == 'Производитель':

    def run(self):
        url = 'https://www.kufar.by/l/r~minsk/noutbuki'
        links = self.get_notebook_list(self.get_soup(url))
        for link in tqdm(links):
            soup = self.get_soup(link)
            notebook = self.get_notebook_data(soup)


parse = KufarParser()
parse.run()
