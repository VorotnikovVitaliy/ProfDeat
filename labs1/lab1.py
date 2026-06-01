import requests
from bs4 import BeautifulSoup

# 1. Ссылка на раздел продажи авто в Омске
url = "https://omsk.110km.ru/vybor/kupit-novie-omsk/"


def main():
    print("Начинаю скачивание...")

    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    block = soup.find_all('div', class_='sale-prev')

    with open("cars_omsk.txt", "w", encoding="utf-8") as file:
        file.write("Список из 20 последних объявлений о продаже авто в Омске:\n")
        file.write("=" * 50 + "\n\n")

        count = 0

        for data in block:
                # 1. Ищем ссылку и заголовок
                link_tag = data.find('a', 'sale-prev__header')
                if not link_tag:
                    continue
                
                title = link_tag.get_text()
                link = link_tag['href']

                price_tag = data.find('span', class_='sale-prev__price-cost')
                if not link_tag:
                    continue

                price = price_tag.get_text()
                
                count += 1
                file.write(f"{count}.\n")
                file.write(f"   Марка: {title}\n")
                file.write(f"   Цена: {price}\n")
                file.write(f"   Ссылка: {link}\n")
                file.write("-" * 30 + "\n")

    print(f"Готово! Сохранено {count} объявлений в файл 'cars_omsk.txt'")

if __name__ == "__main__":
    main()
