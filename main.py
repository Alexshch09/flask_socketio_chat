# Script for local html parsing. Parsing of questions
# Uses data from https://www.praktycznyegzamin.pl/inf03ee09e14/teoria/wszystko/

import psycopg2
from bs4 import BeautifulSoup

# Connection with database
conn = psycopg2.connect(
    dbname='egzamin',
    user='postgres',
    password='root',
    host='localhost'
)

# Initiate cursor for database
cursor = conn.cursor()

# Read HTML file with questions
with open('index.html', 'r', encoding='utf-8') as file:
    content = file.read()

# bs4 init
soup = BeautifulSoup(content, 'html.parser')

# Id for exam (1-INF03, 2-INF02, more examines in a future)
exam_id = 1

# Cicle for every question founded on page
for question_div in soup.find_all('div', class_='question'):
    question_text = question_div.find('div', class_='title').text.strip()
    image_url_tag = question_div.find('img')
    image_url = image_url_tag['src'] if image_url_tag else None
    options = [option.text.strip() for option in question_div.find_all('div', class_='answer')]
    correct_answer = question_div.find('div', class_='correct').text.strip()[0]  # Get only first letter of correct answer

    # Sql query for insert all questions to database
    sql_query = '''
        INSERT INTO questions (exam_id, text, image, a, b, c, d, correct_answer)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    '''
    
    # Launch query
    cursor.execute(sql_query, (exam_id, question_text, image_url, options[0], options[1], options[2], options[3], correct_answer))
    conn.commit()

# Close connection to database
conn.close()
