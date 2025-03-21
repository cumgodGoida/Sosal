from flask import Flask, request, jsonify
import bcrypt
import sqlite3

app = Flask(__name__)

def create_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

create_table()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password'].encode('utf-8')

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()

    if result and bcrypt.checkpw(password, result[0]):
        return jsonify({'message': 'Вход выполнен успешно'}), 200
    else:
        return jsonify({'message': 'Неверный логин или пароль'}), 401

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password'].encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
      c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
      conn.commit()
      conn.close()
      return jsonify({'message': 'Пользователь успешно зарегистрирован'}), 201
    except sqlite3.IntegrityError:
      return jsonify({'message': 'Пользователь уже существует'}), 400

if __name__ == '__main__':
    app.run(debug=True)
