import requests
from bs4 import BeautifulSoup
import os
import time
from urllib.parse import urljoin
import sqlite3


output_dir = '../static/image_buildings_2'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

conn = sqlite3.connect('../sql/photo_gallery.db')
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS photos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        date TEXT,
        author TEXT,
        img_url TEXT,
        file_path TEXT
    )
''')
conn.commit()

base_url = 'https://russiainphoto.ru'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

start_page = 20
end_page = 35

session = requests.Session()

def get_photo_data(soup):
    photo_data = []
    for item in soup.find_all('a', class_='b-search-result__item'):
        img_tag = item.find('img')
        if img_tag:
            img_url = img_tag.get('src')
            if img_url:
                full_img_url = urljoin(base_url, img_url)

                desc_wrapper = item.find('div', class_='b-search-result__item-desc')
                if desc_wrapper:
                    title_tag = desc_wrapper.find('div', class_='b-search-result__item-title')
                    title = title_tag.get_text(strip=True) if title_tag else 'Нет названия'

                    date_tag = desc_wrapper.find('div', class_='b-search-result__item-years')
                    date = date_tag.get_text(strip=True) if date_tag else 'Неизвестная дата'

                    author_tag = desc_wrapper.find('div', class_='b-search-result__item-author')
                    author = author_tag.get_text(strip=True) if author_tag else 'Неизвестный автор'

                    print(f"Название: {title}, Дата: {date}, Автор: {author}, URL изображения: {full_img_url}")

                    photo_data.append({
                        'title': title,
                        'date': date,
                        'author': author,
                        'img_url': full_img_url
                    })

    return photo_data

def download_image(url, folder):
    try:
        response = session.get(url, headers=headers, stream=True)
        if response.status_code == 200:
            filename = os.path.join(folder, url.split('/')[-1].split('?')[0])
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f'Скачано: {filename}')
            return filename
        else:
            print(f'Не удалось скачать {url} - статус {response.status_code}')
            return None
    except Exception as e:
        print(f'Ошибка при скачивании {url}: {e}')
        return None

def save_photo_data_to_db(photo_data):
    for photo in photo_data:
        cursor.execute('''
            INSERT INTO photos (title, date, author, img_url, file_path)
            VALUES (?, ?, ?, ?, ?)
        ''', (photo['title'], photo['date'], photo['author'], photo['img_url'], photo.get('file_path')))
    conn.commit()

def main():
    for page in range(start_page, end_page + 1):
        current_url = f'https://russiainphoto.ru/search/years-1840-1999/?page={page}&query=крым'
        print(f'Обрабатывается страница {page}: {current_url}')

        try:
            response = session.get(current_url, headers=headers)
            if response.status_code != 200:
                print(f'Не удалось получить страницу: {current_url} - статус {response.status_code}')
                continue

            soup = BeautifulSoup(response.content, 'html.parser')
            photo_data = get_photo_data(soup)

            if not photo_data:
                print(f'Фотографии не найдены на странице {page}.')
                continue

            for photo in photo_data:
                file_path = download_image(photo['img_url'], output_dir)
                if file_path:
                    photo['file_path'] = file_path
                else:
                    photo['file_path'] = 'Ошибка при скачивании'
                time.sleep(0.5)

            save_photo_data_to_db(photo_data)

            time.sleep(2)

        except Exception as e:
            print(f'Ошибка при обработке страницы {page}: {e}')
            continue

if __name__ == "__main__":
    main()
    conn.close()
