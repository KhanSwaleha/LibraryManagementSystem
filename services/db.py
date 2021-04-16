from flask_mysqldb import MySQL
from app import *

def executeSelect(sql, params):
	cursor = mysql.connection.cursor()
	cursor.execute(sql, params)
	results = cursor.fetchall()
	return results

def executeIUD(sql, params):
	cursor = mysql.connection.cursor()
	if cursor.execute(sql, params):
		mysql.connection.commit()
		return True
	return False
