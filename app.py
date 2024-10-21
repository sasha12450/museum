import flask
from flask import Flask, render_template, url_for, request, redirect
import sqlite3
import os


app = Flask(__name__)

def get_db_connection_news():
    conn = sqlite3.connect('sql/news.db')
    conn.row_factory = sqlite3.Row
    return conn

def read_text_sql():
    try:
        conn = get_db_connection_news()
        cursor = conn.cursor()
        cursor.execute('''
                   SELECT title, description, publication_time, image 
                   FROM News 
                   ORDER BY 
                        CASE 
                            WHEN publication_time == 'Неизвестно' THEN 1
                            ELSE 0
                        END,
                        publication_time DESC
               ''')
        news_items = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Ошибка при работе с SQLite: {e}")
        news_items = []
    finally:
        conn.close()
    return news_items

@app.route('/', methods=['GET'])
def render_index():
    return render_template('index.html')

@app.route('/history_crimea', methods=['GET'])
def render_history_crimea():
    return render_template('index_history_crimea.html')

@app.route('/middle_ages', methods=['GET'])
def render_middle_ages():
    return render_template('index_middle_ages.html')

@app.route('/modern', methods=['GET'])
def render_modern():
    news_items = read_text_sql()
    return render_template('index_modern.html', news_items=news_items)

@app.route('/famous_personalities', methods=['GET'])
def render_famous():
    from jinj_py.famous_personalities_jinj import famous_people
    events = famous_people()
    return render_template('famous_personalities.html', events=events)


def get_photos_from_db():
    conn = sqlite3.connect('sql/photo_gallery.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT title, date, author, img_url, file_path FROM photos')
    photos = cursor.fetchall()
    conn.close()
    filtered_photos = [photo for photo in photos if "ошибка" not in photo['file_path'].lower()]
    for photo in filtered_photos:
        print(photo)

    return filtered_photos


def get_text_exposition():
    conn = sqlite3.connect('sql/expositions.db')
    cursor = conn.cursor()
    cursor.execute('SELECT title, description FROM exhibition_etnografica_all')
    text = cursor.fetchall()
    conn.close()
    return text

def get_text_tavrida():
    conn = sqlite3.connect('sql/expositions.db')
    cursor = conn.cursor()
    cursor.execute('SELECT title, content FROM expositions')
    text_tavrida = cursor.fetchall()
    conn.close()
    return text_tavrida

@app.route('/photo_gallery', methods=['POST', 'GET'])
def render_photo_gallery():
    photos = get_photos_from_db()
    return render_template('index_history_photo.html', photos=photos)

@app.route('/exposition', methods=['POST', 'GET'])
def render_exposition():
    text = get_text_exposition()
    text_tavrida = get_text_tavrida()
    return render_template('index_exposition.html', text=text, text_tavrida = text_tavrida)

def get_infromation_about_artifacts_musium():
    conn = sqlite3.connect('sql/museum_data.db')
    cursor_ = conn.cursor()
    cursor_.execute('SELECT title_ru, image_path FROM museum_items')
    information = cursor_.fetchall()
    conn.close()
    return information

def get_infromation_about_artifacts_library():
    conn = sqlite3.connect('sql/museum_data.db')
    cursor_ = conn.cursor()
    cursor_.execute('SELECT title_ru, image_path FROM library_items')
    library = cursor_.fetchall()
    conn.close()
    return library

@app.route('/cultural_artifacts', methods=['POST', 'GET'])
def render_cultural_artifacts():
    artifact = get_infromation_about_artifacts_musium()
    artifacts_library = get_infromation_about_artifacts_library()
    return render_template('index_cultural_artifacts.html', artifact=artifact, artifacts_library = artifacts_library)

def get_information_archaeological_finds():
    conn = sqlite3.connect('sql/Sudak_fortress.db')
    cursor_ = conn.cursor()
    cursor_.execute('SELECT title_ru, image_path FROM fortress_items')
    archeologica = cursor_.fetchall()
    conn.close()
    return archeologica

@app.route('/archaeological_finds', methods=['POST', 'GET'])
def render_archaeological_finds():
    archeologica = get_information_archaeological_finds()
    return render_template('index_archaeological_finds.html', archeologica=archeologica)

@app.route('/historical_map', methods = ['POST', 'GET'])
def render_historical_map():
    return render_template('index_historical_map.html')

@app.route('/timeline', methods=['POST', 'GET'])
def render_timelina():
    from jinj_py.chronology_jinj import timeline
    events = timeline()
    return render_template('index_timeline.html', events=events)

@app.route('/about', methods = ['POST', 'GET'])
def render_about():
    return render_template('index_about_project.html')


def get_info_text_temporary_exhibitions():
    conn = sqlite3.connect('sql/expositions.db')
    c = conn.cursor()
    c.execute('SELECT title, description, date, museum FROM temporary_exhibitions')
    exhibitions = c.fetchall()
    conn.close()
    return exhibitions

@app.route('/temporary_exhibitions', methods= ['POST', 'GET'])
def render_temporary_exhibition():
    exhibitions = get_info_text_temporary_exhibitions()
    return render_template('index_temporary_exhibitions.html', exhibitions=exhibitions)

def create_table_subscribe():
    conn = sqlite3.connect('sql/subscriptions.db')  # Подключение к базе данных
    c = conn.cursor()  # Создание курсора
    c.execute('''
        CREATE TABLE IF NOT EXISTS email_subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            subscription_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')  # Запрос на создание таблицы
    conn.commit()  # Применение изменений
    conn.close()  # Закрытие соединения


def save_email_to_db(email):
    create_table_subscribe()
    try:
        conn = sqlite3.connect('sql/subscriptions.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO email_subscriptions (email)
            VALUES (?)
        ''', (email,))
        conn.commit()
    except sqlite3.Error as e:
        print(f'Ошибка: {e}')
    finally:
        conn.close()

@app.route('/subscribe', methods=['POST'])
def subscribe():
    if 'email' in request.form:
        email = request.form['email']
        save_email_to_db(email)  # Сохранение email в базу данных
    return redirect(request.referrer or url_for('/'))  # Перенаправление обратно на исходную страницу




if __name__ == '__main__':
    app.run(debug=True)

