import requests as rq
from bs4 import BeautifulSoup
import re
import sqlite3

conn = sqlite3.connect('../sql/expositions.db')
cursor = conn.cursor()

# Создаем таблицу, если она еще не существует
cursor.execute('''
CREATE TABLE IF NOT EXISTS temporary_exhibitions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    date TEXT,
    museum TEXT
)
''')
conn.commit()

def save_event_to_db(title, description, date, museum):
    cursor.execute('''
    INSERT INTO temporary_exhibitions (title, description, date, museum) 
    VALUES (?, ?, ?, ?)
    ''', (title, description, date, museum))
    conn.commit()

cookies = {
    'app_demo': '2895d1d7eb47a7c4f4a3b6f934fce2a8',
    '_csrf-app_demo': 'b9e57364eb33818e97b1e7df1bc9a57879b6271fbbcbebb1eccc582261018c0fa%3A2%3A%7Bi%3A0%3Bs%3A14%3A%22_csrf-app_demo%22%3Bi%3A1%3Bs%3A32%3A%220WNL2Gs8TLiwewYDl5dNnS6J2BFQyNwL%22%3B%7D',
    '_ym_uid': '1729322712448195585',
    '_ym_d': '1729322712',
    '_ym_isad': '2',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru,en;q=0.9',
    'cache-control': 'max-age=0',
    'referer': 'https://yandex.ru/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "YaBrowser";v="24.7", "Yowser";v="2.5"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 YaBrowser/24.7.0.0 Safari/537.36',
}

response = rq.get('https://afisha7.ru/simferopol/vystavki?page=2&per-page=10', headers=headers, cookies=cookies)
soup = BeautifulSoup(response.text, 'lxml')

events = soup.find_all('h2', class_='mt-5 mb-15 event-title title-line-left')

for event in events:
    link = event.find('a')
    if link:
        event_title = link.text.strip()
        event_url = f'https://afisha7.ru{link.get("href")}'
        print(f'Парсим событие: {event_title} ({event_url})')

        response_2 = rq.get(event_url, headers=headers, cookies=cookies)
        soup_2 = BeautifulSoup(response_2.text, 'lxml')

        event_details = soup_2.find('div', class_='event-desc col-md-12')

        event_date = soup_2.find('span', class_='date')
        if event_date:
            event_date = event_date.text.replace('\xa0', '').strip()
        else:
            event_date = 'Дата не найдена'

        museum_container = soup_2.find('div', class_='place-block pb-20 pt-20 col-md-12')
        museum_name = None
        if museum_container:
            museum_link = museum_container.find('span', class_='place bb-dotted').find('a')
            if museum_link:
                museum_name = museum_link.text.strip()

        if not museum_name:
            museum_name = 'Музей не найден'

        if event_details:
            event_description = event_details.text.strip()

            cleaned_description = re.sub(r'Автор:.*|Источник:.*|‹|›', '', event_description)
            cleaned_description = re.sub(r'\n\s*\n', '\n', cleaned_description).strip()

            print(f'Описание события: {cleaned_description}')
        else:
            cleaned_description = 'Описание не найдено'

        save_event_to_db(event_title, cleaned_description, event_date, museum_name)

        print(f'Дата события: {event_date}')
        print(f'Музей: {museum_name}')
        print('-' * 40)

conn.close()

