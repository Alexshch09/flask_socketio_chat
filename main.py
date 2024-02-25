import psycopg2
from bs4 import BeautifulSoup

# Устанавливаем соединение с базой данных
conn = psycopg2.connect(
    dbname='egzamin',
    user='postgres',
    password='root',
    host='localhost'
)
cursor = conn.cursor()

# Читаем HTML файл
with open('index.html', 'r', encoding='utf-8') as file:
    content = file.read()

# Используем BeautifulSoup для парсинга HTML
soup = BeautifulSoup(content, 'html.parser')

# Идентификатор экзамена, куда будут вставляться вопросы
exam_id = 1

# Итерируемся по каждому вопросу
for question_div in soup.find_all('div', class_='question'):
    question_text = question_div.find('div', class_='title').text.strip()
    image_url_tag = question_div.find('img')
    image_url = image_url_tag['src'] if image_url_tag else None
    options = [option.text.strip() for option in question_div.find_all('div', class_='answer')]
    correct_answer = question_div.find('div', class_='correct').text.strip()[0]  # Получаем только первую букву

    # Формируем SQL-запрос для вставки данных
    sql_query = '''
        INSERT INTO questions (exam_id, text, image, a, b, c, d, correct_answer)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    '''
    
    # Выполняем SQL-запрос
    cursor.execute(sql_query, (exam_id, question_text, image_url, options[0], options[1], options[2], options[3], correct_answer))
    conn.commit()

# Закрываем соединение с базой данных
conn.close()
