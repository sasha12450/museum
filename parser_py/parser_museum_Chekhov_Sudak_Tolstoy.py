import requests
import os
import sqlite3


# -------------------------------------------------------------
# Универсальный скрипт для веб-скрапинга и сохранения изображений
# Используется для сбора данных о выставках Судак, Чехова и Толстого
# Менял ссылку чтобы получать сбор данных
# -------------------------------------------------------------
url = ('https://ar.culture.ru/ru/facets/Subject?s=48&l=24&owner=5c5843ec34b6ed2f7e452a00&isCatalogue=true&o=%7B%22title.ru%22%3A%201%7D&sel=title%20topImage%20label%20organization%20authors%20locales%20activities%20nsfw%20publicSubjectsCount%20slug%20subjects%20projects%20organizations%20authors%20gallery%20audio&totals=true')

headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru,en;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': '_ym_uid=1727012468197293475; _ym_d=1727012468; _ym_isad=2; _ym_visorc=b; adtech_uid=08c22272-cdd5-490e-a372-55f1e7a0e89e%3Aculture.ru; top100_id=t1.7672653.1017546806.1728455908820; t3_sid_7672653=s1.1148285629.1728455908822.1728458303186.1.192',
    'Referer': 'https://ar.culture.ru/ru/museum-catalog/dom-muzey-a-p-chehova-v-yalte',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 YaBrowser/24.7.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "YaBrowser";v="24.7", "Yowser";v="2.5"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

output_folder = '../static/image_Sudak_fortress'
os.makedirs(output_folder, exist_ok=True)

conn = sqlite3.connect('../sql/Sudak_fortress.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS fortress_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title_ru TEXT,
        image_path TEXT
    )
''')
conn.commit()

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()

    for item in data.get('data', []):
        title_ru = item.get('title', {}).get('ru', '')

        image_info = item.get('topImage', {}).get('attachment', {})

        listing_info = image_info.get('listing', {})
        if listing_info:
            image_url = listing_info.get('defaultUrl')
            if image_url:
                full_image_url = f"https://ar.culture.ru/attachments/{image_url}"
                image_name = f"listing_{os.path.basename(image_url)}"
                image_path = os.path.join(output_folder, image_name)

                try:
                    img_response = requests.get(full_image_url, timeout=10)
                    img_response.raise_for_status()
                    with open(image_path, 'wb') as img_file:
                        img_file.write(img_response.content)
                    print(f"Изображение сохранено: {image_path}")

                    cursor.execute('''
                        INSERT OR REPLACE INTO fortress_items (title_ru, image_path)
                        VALUES (?, ?)
                    ''', (title_ru, image_path))
                    conn.commit()
                except requests.RequestException as e:
                    print(f"Ошибка при загрузке изображения: {full_image_url} - {e}")
else:
    print(f"Ошибка при получении данных: {response.status_code}")

conn.close()
