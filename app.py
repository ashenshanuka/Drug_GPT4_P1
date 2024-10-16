from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database configuration
db_config = {
    'user': 'root',
    'password': '1234',
    'host': '127.0.0.1',
    'database': 'pharmacy_gpt4_db'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM drugs')
    drugs = cursor.fetchall()
    conn.close()
    return render_template('index.html', drugs=drugs)

@app.route('/add', methods=('GET', 'POST'))
def add_drug():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        expiration_date = request.form['expiration_date']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO drugs (name, quantity, price, expiration_date) VALUES (%s, %s, %s, %s)',
                       (name, quantity, price, expiration_date))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_drug.html')

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit_drug(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM drugs WHERE id = %s', (id,))
    drug = cursor.fetchone()

    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        expiration_date = request.form['expiration_date']

        cursor.execute('UPDATE drugs SET name=%s, quantity=%s, price=%s, expiration_date=%s WHERE id=%s',
                       (name, quantity, price, expiration_date, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('edit_drug.html', drug=drug)

@app.route('/delete/<int:id>', methods=('POST',))
def delete_drug(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM drugs WHERE id = %s', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)