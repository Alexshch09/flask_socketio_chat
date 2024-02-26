from flask_socketio import SocketIO, emit
import psycopg2

socketio = SocketIO()

# PostgreSQL connection configuration
conn = psycopg2.connect(
    host='localhost',
    user='postgres',
    password='root',
    database='egzamin'
)