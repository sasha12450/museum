
import requests as rq
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sqlite3
import os

def init_db(db_path='../sql/expositions.db'):

    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
        print(f'Создана директория: {db_dir}')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exhibition_etnografica_all (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exhibition_images_etnografica_all (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exhibition_id INTEGER,
            image_url TEXT,
            FOREIGN KEY (exhibition_id) REFERENCES exhibition_etnografica_all(id)
        )
    ''')

    conn.commit()
    return conn, cursor

def save_exhibition(cursor, title, description):
    query = '''
        INSERT INTO exhibition_etnografica_all (title, description)
        VALUES (?, ?)
    '''
    cursor.execute(query, (title, description))
    return cursor.lastrowid

def save_image(cursor, exhibition_id, image_url):
    query = '''
        INSERT INTO exhibition_images_etnografica_all (exhibition_id, image_url)
        VALUES (?, ?)
    '''
    cursor.execute(query, (exhibition_id, image_url))

def main():
    base_url = 'https://ethnocrimea.ru'
    main_page = '/ru/postojannaja-ekspozitsija.html'
    full_url = urljoin(base_url, main_page)

    try:
        response = rq.get(full_url)
        response.raise_for_status()
    except rq.RequestException as e:
        print('Ошибка при запросе основной страницы:', e)
        return

    soup = BeautifulSoup(response.text, 'lxml')

    media_headings = soup.find_all('div', class_='media-heading')

    if not media_headings:
        print('Не найдено элементов с классом "media-heading". Проверьте структуру страницы.')
        return

    conn, cursor = init_db()

    for index, heading in enumerate(media_headings, start=1):
        a_tag = heading.find('a')
        if a_tag and 'href' in a_tag.attrs:
            title = a_tag.get_text(strip=True)
            relative_link = a_tag['href']
            exhibition_url = urljoin(base_url, relative_link)
        else:
            title = 'Без заголовка'
            exhibition_url = None

        media_body = heading.find_next_sibling('div', class_='media-body')
        description = media_body.get_text(strip=True) if media_body else 'Без описания'

        img_tag = heading.find('img') or (media_body.find('img') if media_body else None)
        if img_tag and 'src' in img_tag.attrs:
            image_url = urljoin(base_url, img_tag['src'])
        else:
            image_url = None

        exhibition_data = {
            'title': title,
            'description': description
        }
        exhibition_id = save_exhibition(cursor, title, description)
        print(f"Элемент {index}:")
        print(f"  Заголовок: {title}")
        print(f"  Описание: {description}")
        print(f"  URL изображения: {image_url}")
        print(f"  Ссылка на детали: {exhibition_url}\n")

        if image_url:
            save_image(cursor, exhibition_id, image_url)
            print(f"  Основное изображение добавлено: {image_url}")

        if exhibition_url:
            try:
                detail_response = rq.get(exhibition_url)
                detail_response.raise_for_status()
            except rq.RequestException as e:
                print(f'  Ошибка при запросе страницы деталей ({exhibition_url}):', e)
                continue

            detail_soup = BeautifulSoup(detail_response.text, 'lxml')

            detail_div = detail_soup.find('div', class_='col-md-9 col-md-push-3')
            if detail_div:
                title_tag = detail_div.find('h1', class_='title')
                detailed_title = title_tag.get_text(strip=True) if title_tag else 'Без заголовка'

                detailed_description = ''
                images = []
                for elem in detail_div.find_all(['p', 'img']):
                    if elem.name == 'p':
                        text = elem.get_text(separator=' ', strip=True)
                        if text:
                            detailed_description += text + '\n'
                    elif elem.name == 'img':
                        img_src = elem.get('src')
                        if img_src:
                            img_url = urljoin(base_url, img_src)
                            images.append(img_url)

                if detailed_description:
                    cursor.execute('''
                        UPDATE exhibition_etnografica_all
                        SET description = ?
                        WHERE id = ?
                    ''', (detailed_description, exhibition_id))
                    print(f"  Описание обновлено для элемента {index}.")

                for img_url in images:
                    save_image(cursor, exhibition_id, img_url)
                    print(f"  Изображение добавлено: {img_url}")
            else:
                print(f"  Не найден div с классом 'col-md-9 col-md-push-3' на странице {exhibition_url}.\n")

    conn.commit()
    conn.close()
    print('Все данные успешно сохранены в базу данных.')

if __name__ == '__main__':
    main()
