from pprint import pprint
import requests
from bs4 import BeautifulSoup

from parsers.utils import SushiSet


def east():
    url = 'https://sushivostok.com/products/sety/'
    response = requests.get(url)
    list_set = []
    # Проверяем успешность запроса
    if response.status_code == 200:
        # Создаем объект BeautifulSoup, передавая HTML-контент страницы
        soup = BeautifulSoup(response.content, 'html.parser')

        product_divs = soup.select('section.catalogPage div.item')
        # Обрабатываем найденные элементы
        for div in product_divs:
            quantity = 0
            url = div.find('a').get('href')
            img_tag = div.find('img')
            image_url = img_tag['src']
            print(image_url)
            price_div_t = div.find('div', class_='price1')
            price_div = price_div_t.find('div', class_='price')
            price = int(price_div.text.strip().split()[0])
            weight_div = div.find('div', class_='weight')
            if weight_div.text.strip().replace(',', '.').split()[2] == 'кг':
                weight = int(float(weight_div.text.strip().replace(',', '.').split()[1]) * 1000)
            else:
                weight = int(float(weight_div.text.strip().replace(',', '.').split()[1]))
            coefficient = round(price / weight, 3)
            name = div.find('div', class_='heading').text.strip()
            list_set.append(SushiSet(name, price, weight, quantity, url, coefficient, image_url))
    # list_set = sorted(list_set, key=lambda x: x[5], reverse=False)
    return list_set


if __name__ == '__main__':
    east()
