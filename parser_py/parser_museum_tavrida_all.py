import requests
from bs4 import BeautifulSoup
import sqlite3
from urllib.parse import urljoin
import os
import time

DB_PATH = '../sql/expositions.db'

if not os.path.exists(os.path.dirname(DB_PATH)):
    os.makedirs(os.path.dirname(DB_PATH))

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS expositions')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS expositions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT UNIQUE,
        content TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        exposition_id INTEGER,
        image_url TEXT UNIQUE,
        caption TEXT,
        FOREIGN KEY (exposition_id) REFERENCES expositions(id)
    )
''')

conn.commit()

def fetch_soup(url, headers):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'lxml')

def extract_exposition_links(main_url, headers):
    soup = fetch_soup(main_url, headers)
    h3_tags = soup.find_all('h3', class_='p-4')
    links = []
    for h3 in h3_tags:
        a_tag = h3.find('a')
        if a_tag and 'href' in a_tag.attrs:
            link = urljoin(main_url, a_tag['href'])
            links.append(link)
    return links

def extract_content(expo_url, headers):
    soup = fetch_soup(expo_url, headers)
    title_tag = soup.find('h1', class_='news-page__title')
    title = title_tag.get_text(strip=True) if title_tag else 'No Title'
    content_div = soup.find('div', class_='entry-content')
    content_text = ''
    if content_div:
        text_tags = content_div.find_all(['p', 'h2', 'h3', 'h4', 'h5', 'h6'])
        content_parts = []
        for tag in text_tags:
            text = tag.get_text(strip=True)
            if text:
                content_parts.append(text)
        content_text = '\n\n'.join(content_parts)
    image_urls = []
    image_captions = []
    if content_div:
        imgs = content_div.find_all('img')
        for img in imgs:
            src = img.get('src') or img.get('data-src')
            if src:
                img_url = urljoin(expo_url, src)
                image_urls.append(img_url)
                caption = ''
                parent = img.parent
                if parent.name == 'a':
                    figcaption = parent.find_next_sibling('figcaption')
                    if figcaption:
                        caption = figcaption.get_text(strip=True)
                image_captions.append(caption)
        galleries = content_div.find_all('div', class_='gallery')
        for gallery in galleries:
            figures = gallery.find_all('figure', class_='gallery-item')
            for figure in figures:
                img_tag = figure.find('img')
                if img_tag:
                    src = img_tag.get('src') or img_tag.get('data-src')
                    if src:
                        img_url = urljoin(expo_url, src)
                        image_urls.append(img_url)
                figcaption = figure.find('figcaption', class_='gallery-caption')
                caption = figcaption.get_text(strip=True) if figcaption else ''
                image_captions.append(caption)
    return title, content_text, image_urls, image_captions

def save_to_database(title, content, image_urls, image_captions):
    try:
        cursor.execute('INSERT OR IGNORE INTO expositions (title, content) VALUES (?, ?)', (title, content))
        conn.commit()
        cursor.execute('SELECT id FROM expositions WHERE title = ?', (title,))
        result = cursor.fetchone()
        if result:
            exposition_id = result[0]
        else:
            return
        for img_url, caption in zip(image_urls, image_captions):
            cursor.execute('INSERT OR IGNORE INTO images (exposition_id, image_url, caption) VALUES (?, ?, ?)', (exposition_id, img_url, caption))
        conn.commit()
    except sqlite3.Error:
        pass

def scrape_tavrida_museum():
    main_url = 'https://tavrida-museum.ru/expositions/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' 
                      'AppleWebKit/537.36 (KHTML, like Gecko) ' 
                      'Chrome/58.0.3029.110 Safari/537.3'
    }
    exposition_links = extract_exposition_links(main_url, headers)
    print(f'Найдено {len(exposition_links)} ссылок на выставки.')
    for idx, link in enumerate(exposition_links, start=1):
        print(f'Обработка {idx}/{len(exposition_links)}: {link}')
        try:
            title, content, image_urls, image_captions = extract_content(link, headers)
            save_to_database(title, content, image_urls, image_captions)
            print(f"Сохранена выставка '{title}' с {len(image_urls)} изображениями.")
            time.sleep(1)
        except Exception:
            pass

    conn.close()
    print('Все данные сохранены в базу данных.')

if __name__ == '__main__':
    scrape_tavrida_museum()
