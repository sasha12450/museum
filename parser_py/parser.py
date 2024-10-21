import requests as rq
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import sqlite3

conn = sqlite3.connect('../sql/news.db')
c = conn.cursor()

def create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS News (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    full_text TEXT NOT NULL,
    publication_time TEXT NOT NULL,
    article_url TEXT NOT NULL UNIQUE,
    image TEXT NOT NULL) 
    ''')
    conn.commit()

def article_exists(article_url):
    c.execute("SELECT 1 FROM News WHERE article_url = ?", (article_url,))
    return c.fetchone() is not None

def insert_article(title, description, full_text, publication_time, article_url, image):
    if not article_exists(article_url):
        c.execute('''INSERT INTO News (title, description, full_text, publication_time, article_url, image)
                     VALUES (?, ?, ?, ?, ?, ?)''', (title, description, full_text, publication_time, article_url, image))
        conn.commit()
    else:
        print(f"Статья с URL '{article_url}' уже существует, пропускаем.")

def get_full_article(article_url):
    try:
        full_url = f'https://travelcrimea.com{article_url}'
        response = rq.get(full_url)
        response.raise_for_status()

        bs = BeautifulSoup(response.text, 'lxml')

        article_body = bs.find('section', class_='article-body')

        publication_time_tag = bs.find('time')
        if publication_time_tag and 'datetime' in publication_time_tag.attrs:
            publication_time = publication_time_tag['datetime'].split('T')[0]
        else:
            publication_time = "Неизвестно"

        if article_body:
            paragraphs = article_body.find_all('p')
            full_text = ''

            for paragraph in paragraphs:
                paragraph_text = paragraph.get_text(strip=True)

                if (
                        paragraph.find('a', class_='inject-article__media-caption') or
                        paragraph.find('figure', class_='inject-mega') or
                        paragraph.find('em', class_='article-body') or
                        'Читайте также' in paragraph_text or
                        'Фото предоставлено' in paragraph_text
                ):
                    continue

                full_text += paragraph_text + "\n"

            return full_text.strip(), publication_time
        else:
            return "Основной текст статьи не найден.", publication_time
    except rq.RequestException as e:
        print(f'Ошибка HTTP при получении статьи: {e}')
        return None, None
    except Exception as e:
        print(f'Произошла ошибка при извлечении текста статьи: {e}')
        return None, None

def get_articles(date):
    try:
        url = f'https://travelcrimea.com/ajax/rubric/get.html?list_sid=novosti&date={date}&count=11'
        response = rq.get(url)
        response.raise_for_status()

        bs = BeautifulSoup(response.text, 'lxml')

        articles = bs.find_all('article', class_='rubric-list__article')

        if not articles:
            print(f"Статей не найдено на дату {date}")
            return

        for article in articles:
            title = article.find('div', class_='rubric-list__article-title').get_text(strip=True)
            description = article.find('p', class_='rubric-list__article-announce').get_text(strip=True)
            article_link = article.find('div', class_='rubric-list__article-title').a['href']

            picture_tag = article.find('picture')
            if picture_tag:
                img_tag = picture_tag.find('img')
                if img_tag and 'src' in img_tag.attrs:
                    image = 'https://travelcrimea.com' + img_tag['src']
                    print(f"Извлечённый URL изображения: {image}")
                else:
                    image = 'default_image.jpg'
                    print("Изображение не найдено, используется изображение по умолчанию.")
            else:
                image = 'default_image.jpg'
                print("Тег <picture> не найден, используется изображение по умолчанию.")

            full_text, publication_time = get_full_article(article_link)

            insert_article(title, description, full_text, publication_time, article_link, image)

            print(f"Заголовок: {title}")
            print(f"Описание: {description}")
            print(f"Полный текст: {full_text}")
            print(f"Время публикации: {publication_time}")
            print(f"URL статьи: {article_link}\n")

    except rq.RequestException as e:
        print(f'Ошибка HTTP: {e}')
    except Exception as e:
        print(f'Произошла ошибка: {e}')


def scrape_articles(start_date, end_date):
    current_date = start_date

    while current_date <= end_date:
        date_str = current_date.strftime('%Y%m%dT%H%M%S')
        print(f"Парсинг данных за {current_date.strftime('%Y-%m-%d')}")
        get_articles(date_str)

        current_date += timedelta(days=1)

start_date = datetime(2024, 8, 15)

end_date = datetime.now()

if __name__ == '__main__':
    create_table()
    scrape_articles(start_date, end_date)

conn.close()
