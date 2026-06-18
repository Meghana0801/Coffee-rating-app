from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('coffee.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS coffee (
            id INTEGER PRIMARY KEY,
            name TEXT,
            votes INTEGER
        )
    ''')

    cursor.execute("SELECT COUNT(*) FROM coffee")
    count = cursor.fetchone()[0]

    if count == 0:
        coffees = [
            ('Espresso', 0),
            ('Cappuccino', 0),
            ('Latte', 0)
        ]

        cursor.executemany(
            "INSERT INTO coffee(name, votes) VALUES (?, ?)",
            coffees
        )

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/coffees')
def get_coffees():
    conn = sqlite3.connect('coffee.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM coffee")
    coffees = cursor.fetchall()

    conn.close()

    return jsonify([
        {
            "id": c[0],
            "name": c[1],
            "votes": c[2]
        }
        for c in coffees
    ])

@app.route('/vote/<int:id>', methods=['POST'])
def vote(id):
    conn = sqlite3.connect('coffee.db')
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE coffee SET votes = votes + 1 WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Vote counted"})

if __name__ == '__main__':
    app.run(debug=True)