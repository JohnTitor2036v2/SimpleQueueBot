from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2, logging

from config import SQLALCHEMY_URL, SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['DATABASE_URI'] = SQLALCHEMY_URL

ACCOUNT = []

def get_conn():
    # Connect to the database
    conn = psycopg2.connect(app.config['DATABASE_URI'])
    return conn

@app.route("/")
def index():
    ACCOUNT.clear()
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    ACCOUNT.clear()
    if request.method == "POST":
        user_details = request.form
        column2_value = 0
        username = user_details["username"]

        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM users WHERE nickname = '{username}'")
        result = cursor.fetchall()
        for row in result:
            column2_value = row[1]  # Access the second column value

        cursor.close()
        conn.close()

        if column2_value == username:
            ACCOUNT.append(username)
            return redirect(url_for("account"))
        else:
            flash("No such user.", "error")

    return render_template("login.html" )

@app.route("/account")
def account():
    username = ACCOUNT[0]
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM users WHERE nickname = '{username}'")
    users = cursor.fetchall()
    cursor.fetchall()

    user_id = 0
    for row in users:
        user_id = row[0]

    cursor.execute(f"SELECT * FROM follows WHERE following_user_id = {user_id}")
    follows = cursor.fetchall()
    cursor.fetchall()

    following_queue_id = []
    position = []
    for row in follows:
        following_queue_id.append(row[2])
        position.append(row[3])

    queues = []
    for queue_id in following_queue_id:
        cursor.execute(f"SELECT * FROM queues WHERE id = {queue_id}")
        row = cursor.fetchall()
        queues.append(row[0])
        cursor.fetchall()

    queue_name = []
    chat_id = []
    size = []
    for row in queues:
        queue_name.append(row[1])
        chat_id.append(row[2])
        size.append(row[3])

    chat_name = []
    for id in chat_id:
        cursor.execute(f"SELECT * FROM groups WHERE chat_id = {id}")
        groups = cursor.fetchall()
        cursor.fetchall()

        for row in groups:
            chat_name.append(row[1])

    data = list(zip(chat_name, queue_name, size, position))
    ordered_data = sorted(data, key=lambda x: x[0])

    cursor.close()
    conn.close()

    return render_template("account.html", username=username, ordered_data=ordered_data)
    


if __name__ == '__main__':
    app.run(debug=True)
