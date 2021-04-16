from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from datetime import date, timedelta
from services.businessLogic import *
from settings import *
import logging

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_DB'] = 'flask_test'

mysql = MySQL(app)

@app.route('/')
def index():
	results = indexLogic()
	return render_template('home.html', results=results)

@app.route('/issueBook/<id>', methods = ['GET', 'POST'])
def issueBook(id):
	sql = 'SELECT TITLE, AUTHOR, AVERAGERATING FROM BOOKS WHERE BOOKID=%(id)s'
	results = executeSelect(sql, {'id': id})

	insert = 4
	debt = []
	
	if request.method == 'POST':
		debt, insert = issueBookLogic(id)
	return render_template('issueBook.html', results=results, debt=debt, insert=insert)

@app.route('/returnBook', methods = ['GET', 'POST'])
def returnBook():
	fine = 0
	total = 0
	results = []
	update = 2
	exist = True
	
	if request.method == 'POST':
		results, fine, total, update, exist = returnBookLogic()
	return render_template('returnBook.html', results=results, fine=fine, total=total, update=update, exist=exist)

@app.route('/reports', methods = ['POST', 'GET'])
def reports():
	results, resultsMem, exist = reportsLogic()
	return render_template('reports.html', results=results, resultsMem=resultsMem, exist=exist)

@app.route('/transactions')
def transactions():
	results, exist = transactionsLogic()
	return render_template('transactions.html', results=results, exist=exist)

if __name__ == '__main__':
	app.run(debug=True)