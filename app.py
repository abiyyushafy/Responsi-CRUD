from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    "host": "alzxv.h.filess.io",
    "database": "dbkuliah_brassdayus",
    "user": "dbkuliah_brassdayus",
    "password": "95e02140996050006c5dd4579274eec907831e19",
    "port": "3305"
}

# Function to get database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return None

# Home page
@app.route('/')
def index():
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM tbl_mahasiswa")
            mahasiswa = cursor.fetchall()
            cursor.close()
            connection.close()
            return render_template('index.html', mahasiswa=mahasiswa)
        else:
            return "Database connection error", 500
    except Error as e:
        print(f"Error: {e}")
        return "Database error", 500

# Tambah data
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        try:
            connection = get_db_connection()
            if connection:
                cursor = connection.cursor()
                nim = request.form['nim']
                nama = request.form['nama']
                asal = request.form['asal']
                
                cursor.execute("INSERT INTO tbl_mahasiswa (nim, nama, asal) VALUES (%s, %s, %s)", 
                             (nim, nama, asal))
                connection.commit()
                cursor.close()
                connection.close()
                return redirect(url_for('index'))
            else:
                return "Database connection error", 500
        except Error as e:
            print(f"Error: {e}")
            return "Database error", 500
    return render_template('add.html')

# Edit data
@app.route('/edit/<nim>', methods=['GET', 'POST'])
def edit(nim):
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            
            if request.method == 'POST':
                nama = request.form['nama']
                asal = request.form['asal']
                cursor.execute("UPDATE tbl_mahasiswa SET nama = %s, asal = %s WHERE nim = %s", 
                             (nama, asal, nim))
                connection.commit()
                cursor.close()
                connection.close()
                return redirect(url_for('index'))
            
            cursor.execute("SELECT * FROM tbl_mahasiswa WHERE nim = %s", (nim,))
            mahasiswa = cursor.fetchone()
            cursor.close()
            connection.close()
            return render_template('edit.html', mahasiswa=mahasiswa)
        else:
            return "Database connection error", 500
    except Error as e:
        print(f"Error: {e}")
        return "Database error", 500

# Hapus data
@app.route('/delete/<nim>')
def delete(nim):
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM tbl_mahasiswa WHERE nim = %s", (nim,))
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('index'))
        else:
            return "Database connection error", 500
    except Error as e:
        print(f"Error: {e}")
        return "Database error", 500

if __name__ == '__main__':
    app.run(debug=True)