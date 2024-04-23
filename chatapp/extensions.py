import psycopg2
from flask_login import LoginManager


login_manager = LoginManager()

# PostgreSQL global connection configuration
conn = psycopg2.connect(
    host='localhost', # 192.168.0.185
    user='postgres',
    password='root',
    database='egzamin'
)

"""
Main Database Script

-- Exams (if03, inf02)
CREATE TABLE Exams (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- Users
CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    login VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    nickname VARCHAR(50) NOT NULL,
    invited_by INTEGER REFERENCES Users(id),
    invite_code VARCHAR(20),
    current_exam INTEGER REFERENCES Exams(id),
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_admin BOOLEAN DEFAULT FALSE,
    profile_image BYTEA,
    premium BOOLEAN DEFAULT FALSE
);

-- Settings 1 to 1
CREATE TABLE Settings (
    user_id INTEGER PRIMARY KEY REFERENCES Users(id),
    beta_enable BOOLEAN DEFAULT FALSE,
    color_scheme VARCHAR(20)
);

-- Stats for 1 question exam
CREATE TABLE Stats (
    user_id INTEGER REFERENCES Users(id),
    exam_id INTEGER REFERENCES Exams(id),
    quest_id INTEGER,
    answer VARCHAR(1),
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Stats for 40 questions exam
CREATE TABLE Stats40 (
    user_id INTEGER REFERENCES Users(id),
    exam_id INTEGER REFERENCES Exams(id),
    question_id INTEGER,
    answer VARCHAR(1),
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Questions (all) exam_id - INF03/ INF02
CREATE TABLE Questions (
    id SERIAL PRIMARY KEY,
    exam_id INTEGER REFERENCES Exams(id),
    text TEXT,
    image BYTEA,
    a TEXT,
    b TEXT,
    c TEXT,
    d TEXT,
    correct_answer VARCHAR(1)
);

-- Ready exams. Users can create ready exams from questions in database. In questions are stored questions id`s
CREATE TABLE Ready_exams (
    id SERIAL PRIMARY KEY,
    exam_id INTEGER REFERENCES Exams(id),
    name VARCHAR(100),
    questions INTEGER[],
    author VARCHAR(50)
);

-- Guides. Admins and users can create an guides for every questions. In future will be added guides check and rating
CREATE TABLE Guides (
    question_id INTEGER REFERENCES Questions(id),
    title VARCHAR(100),
    text TEXT,
    author VARCHAR(50)
);

"""