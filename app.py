from flask import Flask, render_template, request, jsonify
import sqlite3
from flask_cors import CORS


def dic_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def init_sqlite_db():
    connection = sqlite3.connect('database.db')
    print("Successfully open a database")
    connection.execute('CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, fname TEXT, uname TEXT, passw Text, email TEXT)')
    print("Successfully created the table")
    connection.execute
    ('CREATE TABLE IF NOT EXISTS admin (id INTEGER PRIMARY KEY AUTOINCREMENT,uname TEXT,passw TEXT')
    print("Successfully created the table")
    connection.close()


init_sqlite_db()


app = Flask(__name__)
CORS(app)


@app.route('/add-new/', methods=['POST'])
def add_new():
    msg = None
    if request.method == "POST":
        try:
            post_data = request.get_json()
            fname = post_data['fname']
            uname = post_data['uname']
            passw = post_data['passw']
            email = post_data['email']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO accounts (fname, uname , passq, email) VALUES (?, ?, ?, ?)",(fname,uname,passw, email))
                cur.execute("INSERT INTO admin (uname, passw) VALUES ('admin','admin')",
                (uname, passw))
                con.commit()
                msg = fname + "Successfully created account"
        except Exception as e:
            con.rollback()
            msg = "Error occurred in insert operation:" + str(e)
        finally:
            con.close()
            return jsonify(msg)


@app.route('/login-account/', methods=["GET"])
def login_account():
    records = {}
    if request.method == "POST":
        msg = None

        try:
            post_data = request.get_json()
            uname = post_data['uname']
            passw = post_data['passw']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                sql = "SELECT * FROM accounts WHERE uname = ? and passw = ?"
                cur.execute(sql,[uname, passw])
                records = cur.fetchall()
        except Exception as e:
            con.rollback()
            msg = "Error occurred while fetching data from db: " + str(e)
        finally:
            con.close()
            return jsonify(records)


@app.route('/accounts/', methods=["GET"])
def get_accounts():
    records = []
    msg = None
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            sql = "SELECT * FROM accounts"
            cur.execute(sql)
            records = cur.fetchall()
    except Exception as e:
        con.rollback()
        msg = "Error occurred while fetching data from db: " + str(e)
    finally:
        con.close()
        return jsonify(records)

@app.route('/show-admin/', methods=["GET"])
def show_admin():
    records = []
    try:
            with sqlite3.connect('database.db') as con:
                con.row_factory = dic_factory
                cur = con.cursor()
                cur.execute("SELECT * FROM admin")
                records = cur.fetchall()
    except Exception as e:
            con.rollback()
            print("There was am error fetching accounts from the database." + str(e))
    finally:
            con.close()
            return jsonify(records)

def admin():
    msg = None
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()

            cur.execute("INSERT INTO admin (uname, passw) VALUES ('admin','1234')",
                        )
            con.commit()
            msg = " Aadmin succefully created."
    except Exception as e:
        con.rollback()
        msg = "Error occurred in insert operation: " + str(e)
    finally:
        con.close()
        print(msg)
admin()