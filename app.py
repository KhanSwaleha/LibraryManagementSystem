from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from datetime import date, timedelta
import logging

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_test'
 
mysql = MySQL(app)

def executeSelect(sql):
	cursor = mysql.connection.cursor()
	cursor.execute(sql)
	results = cursor.fetchall()
	return results

def executeIUD(sql):
	cursor = mysql.connection.cursor()
	if cursor.execute(sql):
		mysql.connection.commit()
		return True
	return False

@app.route('/')
def index():
	sql=''' SELECT * FROM BOOKS '''
	results = executeSelect(sql)
	return render_template('home.html', results=results)

@app.route('/issueBook/<id>', methods=['GET', 'POST'])
def issueBook(id):
	sql=''' SELECT TITLE, AUTHOR, AVERAGERATING FROM BOOKS WHERE BOOKID= '''+ id
	results = executeSelect(sql)
	insert=3
	debt=[]

	if request.method == 'POST':
		sql='SELECT DEBT FROM MEMBERS WHERE memberId='+ request.form['memberId']
		debt=executeSelect(sql)
		if debt:
			if debt[0][0] < 500:
				t=[]
				t.append(id)
				t.append(request.form['memberId'])
				t.append(date.today().strftime("%Y/%m/%d"))
				t.append((date.today()+timedelta(days=10)).strftime("%Y/%m/%d"))
				t.append(50)
				sql='INSERT INTO transactions(bookId,memberId,issueDate,expectedReturnDate,rent) VALUES {} '.format(tuple(t))
				sqlupdate='UPDATE BOOKS SET AVAILABLEQUANTITY=AVAILABLEQUANTITY-1 WHERE BOOKID='+id
				if (executeIUD(sql) and executeIUD(sqlupdate)):
					insert=0
				else:
					insert=1
			else:
				debt=True
		else:
			insert=2
	return render_template('issueBook.html', results=results, debt=debt, insert=insert)

@app.route('/returnBook', methods=['GET', 'POST'])
def returnBook():
	fine=0
	total=0
	results=[]
	update=2
	exist=True
	
	if request.method == 'POST':
		if 'form1' in request.form:
			sql='SELECT ID,TITLE,AUTHOR,NAME,ISSUEDATE,expectedReturnDate,rent,DEBT FROM books JOIN transactions ON books.bookId=transactions.bookId JOIN members ON transactions.memberId=members.memberId WHERE transactions.bookId='+ request.form['bookId'] +' AND transactions.memberId=' + request.form['memberId']
			results = executeSelect(sql)
			if results:
				if date.today() > results[0][5]:
					fineDays = date.today() - results[0][5]
					fine = int(fineDays.days)
				total = results[0][6] + fine + results[0][7]

				transId = results[0][0]
			else:
				exist=False

		if 'form2' in request.form:
			print('first')
			sql = 'SELECT MEMBERID, BOOKID FROM TRANSACTIONS WHERE ID='+request.form['transID']
			results = executeSelect(sql)
			sql = 'UPDATE TRANSACTIONS SET TOTALAMOUNTCOLLECTED = '+request.form['totalAmountCollected']+' ,RETURNDATE=\''+ date.today().strftime("%Y/%m/%d") +'\' WHERE ID='+request.form['transID']
			remDebt = int(request.form['totalA']) - int(request.form['totalAmountCollected'])
			sqlUpdateMem = 'UPDATE MEMBERS SET DEBT='+str(remDebt)+' ,AMOUNTPAID=AMOUNTPAID+'+ request.form['totalAmountCollected'] +' WHERE MEMBERID=' +str(results[0][0])
			sqlUpdateBook = 'UPDATE BOOKS SET AVAILABLEQUANTITY=AVAILABLEQUANTITY+1 WHERE BOOKID=' +str(results[0][1])
			if (executeIUD(sql) and executeIUD(sqlUpdateMem) and executeIUD(sqlUpdateBook)): #-----------
				update=True
			else:
				update=False
	return render_template('returnBook.html', results=results, fine=fine, total=total, update=update, exist=exist)

@app.route('/reports', methods = ['POST', 'GET'])
def reports():
	sql = 'SELECT TRANSACTIONS.BOOKID, COUNT(TRANSACTIONS.BOOKID) AS FREQUENCY, AVAILABLEQUANTITY FROM TRANSACTIONS JOIN BOOKS ON TRANSACTIONS.BOOKID=BOOKS.BOOKID GROUP BY TRANSACTIONS.BOOKID ORDER BY FREQUENCY DESC'
	results = executeSelect(sql)
	sqlMem = 'SELECT NAME,AMOUNTPAID FROM MEMBERS WHERE DEBT < 10 ORDER BY AMOUNTPAID DESC'
	resultsMem = executeSelect(sqlMem)
	return render_template('reports.html', results=results, resultsMem=resultsMem)

@app.route('/transactions')
def transactions():
	sql= 'SELECT ID,TITLE,AUTHOR,NAME,ISSUEDATE,RETURNDATE,EXPECTEDRETURNDATE,TOTALAMOUNTCOLLECTED FROM books JOIN transactions ON books.bookId=transactions.bookId JOIN members ON transactions.memberId=members.memberId'
	results = executeSelect(sql)
	return render_template('transactions.html', results=results)

if __name__ == '__main__':
	app.run(debug=True)