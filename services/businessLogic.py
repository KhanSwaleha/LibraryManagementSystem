from services.db import *

def indexLogic():
	sql = ' SELECT * FROM BOOKS '
	results = executeSelect(sql, {})
	return results

def issueBookLogic(id):

	insert = 4
	debt = []
	sqlCheck = 'SELECT * FROM TRANSACTIONS WHERE BOOKID=%(id)s AND MEMBERID=%(memId)s AND RETURNDATE=\'0000-00-00\''
	resultsCheck = executeSelect(sqlCheck, {'id': id, 'memId': request.form['memberId']})
	if resultsCheck:
		insert = 3
	else:
		sql = 'SELECT DEBT FROM MEMBERS WHERE memberId=%(memId)s'
		debt = executeSelect(sql, {'memId': request.form['memberId']})
		if debt:
			if debt[0][0] < 500:
				t = []
				t.append(id)
				t.append(request.form['memberId'])
				t.append(date.today().strftime("%Y/%m/%d"))
				t.append((date.today()+timedelta(days=10)).strftime("%Y/%m/%d"))
				t.append(50)
				sql = 'INSERT INTO transactions(bookId,memberId,issueDate,expectedReturnDate,rent) VALUES {} '.format(tuple(t))
				sqlUpdate = 'UPDATE BOOKS SET AVAILABLEQUANTITY=AVAILABLEQUANTITY-1 WHERE BOOKID=%(id)s'
				if (executeIUD(sql, {}) and executeIUD(sqlUpdate, {'id': id})):
					insert = 0
				else:
					insert = 1
			else:
				debt = True
		else:
			insert = 2
	return debt, insert

def returnBookLogic():

	fine = 0
	total = 0
	results = []
	update = 2
	exist = True

	if 'form1' in request.form:
		sql = 'SELECT ID,TITLE,AUTHOR,NAME,ISSUEDATE,expectedReturnDate,rent,DEBT FROM books JOIN transactions ON books.bookId=transactions.bookId JOIN members ON transactions.memberId=members.memberId WHERE transactions.bookId=%(bId)s AND transactions.memberId=%(memId)s AND RETURNDATE=\'0000-00-00\''
		results = executeSelect(sql, {'bId': request.form['bookId'], 'memId': request.form['memberId']})
		if results:
			if date.today() > results[0][5]:
				fineDays = date.today() - results[0][5]
				fine = int(fineDays.days)
			total = results[0][6] + fine + results[0][7]

			transId = results[0][0]
		else:
			exist = False

	if 'form2' in request.form:
		sql = 'SELECT MEMBERID, BOOKID FROM TRANSACTIONS WHERE ID=%(trId)s'
		results = executeSelect(sql, {'trId': request.form['transID']})
		sql = 'UPDATE TRANSACTIONS SET TOTALAMOUNTCOLLECTED = %(totAmountCol)s ,RETURNDATE=\''+ date.today().strftime("%Y/%m/%d") +'\' WHERE ID=%(trId)s'
		remDebt = int(request.form['totalA']) - int(request.form['totalAmountCollected'])
		sqlUpdateMem = 'UPDATE MEMBERS SET DEBT='+str(remDebt)+' ,AMOUNTPAID=AMOUNTPAID+%(totAmountCol)s WHERE MEMBERID=' +str(results[0][0])
		sqlUpdateBook = 'UPDATE BOOKS SET AVAILABLEQUANTITY=AVAILABLEQUANTITY+1 WHERE BOOKID=' +str(results[0][1])
		if (executeIUD(sql, {'totAmountCol': request.form['totalAmountCollected'], 'trId': request.form['transID']}) and executeIUD(sqlUpdateMem, {'totAmountCol': request.form['totalAmountCollected']}) and executeIUD(sqlUpdateBook, {})): 
			update = True
		else:
			update = False

	return results, fine, total, update, exist

def transactionsLogic():
	sql = 'SELECT ID,TITLE,AUTHOR,NAME,ISSUEDATE,RETURNDATE,EXPECTEDRETURNDATE,TOTALAMOUNTCOLLECTED FROM books JOIN transactions ON books.bookId=transactions.bookId JOIN members ON transactions.memberId=members.memberId'
	results = executeSelect(sql, {})
	if results:
		exist = True

	return results, exist

def reportsLogic():
	exist = False
	sql = 'SELECT TRANSACTIONS.BOOKID, COUNT(TRANSACTIONS.BOOKID) AS FREQUENCY, AVAILABLEQUANTITY FROM TRANSACTIONS JOIN BOOKS ON TRANSACTIONS.BOOKID=BOOKS.BOOKID GROUP BY TRANSACTIONS.BOOKID ORDER BY FREQUENCY DESC'
	results = executeSelect(sql, {})
	sqlMem = 'SELECT NAME,AMOUNTPAID FROM MEMBERS WHERE DEBT < 10 ORDER BY AMOUNTPAID DESC'
	resultsMem = executeSelect(sqlMem, {})
	if (results and resultsMem):
		exist = True

	return results, resultsMem, exist