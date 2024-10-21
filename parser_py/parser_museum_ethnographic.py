import requests as rq
from bs4 import BeautifulSoup
import sqlite3
from urllib.parse import urljoin
import os

def main():
    url = 'https://ethnocrimea.ru/ru/postojannaja-ekspozitsija.html'
    base_url = 'https://ethnocrimea.ru/ru/postojannaja-ekspozitsija.html'

    try:
        response = rq.get(url)
        response.raise_for_status()
    except rq.RequestException as e:
        print('Ошибка при запросе страницы:', e)
        return

    soup = BeautifulSoup(response.text, 'lxml')
    media_items = soup.find_all('div', class_='media')

    if not media_items:
        print('Не найдено элементов с классом "media".')
        return

    db_path = '../sql/expositions.db'
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expositions_etnografica (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            image_url TEXT
        )
    ''')

    for index, media in enumerate(media_items, start=1):
        heading = media.find('div', class_='media-heading')
        title = heading.get_text(strip=True) if heading else 'Без заголовка'

        body = media.find('div', class_='media-body')
        description = body.get_text(strip=True) if body else 'Без описания'

        img_tag = media.find('img')
        image_url = urljoin(base_url, img_tag['src']) if img_tag and 'src' in img_tag.attrs else None

        cursor.execute('''
            INSERT INTO expositions_etnografica (title, description, image_url)
            VALUES (?, ?, ?)
        ''', (title, description, image_url))

        print(f"Элемент {index}:")
        print(f"  Заголовок: {title}")
        print(f"  Описание: {description}")
        print(f"  URL изображения: {image_url}\n")

    conn.commit()
    conn.close()
    print('Данные успешно сохранены в базу данных.')

if __name__ == '__main__':
    main()
