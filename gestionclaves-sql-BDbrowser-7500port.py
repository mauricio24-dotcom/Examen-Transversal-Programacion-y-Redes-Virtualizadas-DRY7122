# Gestión de usuarios con hash, SQLite y sitio web en Flask (puerto 7500).

import sqlite3
import hashlib
from flask import Flask, request

app = Flask(__name__)


db_name = 'users.db'
@app.route('/')
def index():
    return 'hola bienvenido a base de datos sql'
######################################### Password Hashing #########################################################

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS USER_HASH
       (USERNAME  TEXT    PRIMARY KEY NOT NULL,
        HASH      TEXT    NOT NULL);''')
    conn.commit()
    try:
        hash_value = hashlib.sha256(request.form['password'].encode()).hexdigest()
        c.execute("INSERT INTO USER_HASH (USERNAME, HASH) "
              "VALUES ('{0}', '{1}')".format(request.form['username'], hash_value))
        conn.commit()
    except sqlite3.IntegrityError:
        return "El usuario ha sido registrado."
    print('username: ', request.form['username'], ' password: ', request.form['password'], ' hash: ', hash_value)
    return "Registro exitoso."
def verify_hash(username, password):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    query = "SELECT HASH FROM USER_HASH WHERE USERNAME = '{0}'".format(username)
    c.execute(query)
    records = c.fetchone()
    conn.close()
    if not records:
        return False
    return records[0] == hashlib.sha256(password.encode()).hexdigest()
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if verify_hash(request.form['username'], request.form['password']):
            error = 'Registro exitoso.'
        else:
            error = 'usuario/contraseña inválido.'
    else:
        error = 'Método inválido'
    return error
if __name__ == '__main__':
        app.run(host='0.0.0.0', port=7500, ssl_context='adhoc')
                                                        