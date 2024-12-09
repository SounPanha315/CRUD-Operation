from flask import Flask, render_template, request, flash, redirect, url_for
import requests
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os

app = Flask(__name__)
app.secret_key = 'dont tell anyone'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123'
app.config['MYSQL_DB'] = 'pythonexam'

mysql = MySQL(app)

@app.route('/')
@app.route('/index')
def index():  # put application's code here
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM tblproduct')
    products = cursor.fetchall()
    cursor.close()
    return render_template('index.html', products=products)

@app.route('/delete_product/<int:item_id>', methods=['GET'])
def delete(item_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM tblproduct WHERE id = % s', (item_id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('index'))

@app.route('/addproduct', methods = ['POST'])
def addproduct():
    if request.method == "POST":
        flash("Product Added Successfully")
        name = request.form['name']
        cost = request.form['cost']
        price = request.form['price']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO tblproduct VALUES (NULL, % s, % s, % s)',
                       (name, cost, price, ))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('index'))

@app.route('/updateproduct/<int:item_id>', methods = ['POST', 'GET'])
def updateproduct(item_id):
    if request.method == "GET":
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tblproduct WHERE id = % s', (item_id,))
        products = cursor.fetchone()
        return redirect(url_for('index'), products=products)

    if request.method == "POST":
        item_id = request.form['id']
        name = request.form['name']
        cost = request.form['cost']
        price = request.form['price']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE tblproduct SET name=%s, cost=%s, price=%s WHERE id=%s',
                       (name, cost, price, item_id, ))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
