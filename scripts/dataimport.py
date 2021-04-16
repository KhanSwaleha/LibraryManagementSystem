import requests
import json
import pymysql

r = requests.get('https://frappe.io/api/method/frappe-library')
package_json=r.json()

con = pymysql.connect(host = 'localhost', user = 'root', passwd = '', db = 'flask_test')
cursor = con.cursor()

def validate_string(val):
	if val != None:
		if type(val) is int:
			return str(val).encode('utf-8')
		else:
			return val

for i in package_json['message']:
	t1=[]
	bookID = validate_string(i.get('bookID', None))
	title = validate_string(i.get('title', None))
	authors = validate_string(i.get('authors', None))
	average_rating = validate_string(i.get('average_rating', None))
	t1.append(bookID)
	t1.append(title)
	t1.append(authors)
	t1.append(average_rating)
	cursor.execute(""" INSERT INTO books(bookId,title,author,averageRating) VALUES {} """.format(tuple(t1)))
	print('inserted')

con.commit()
con.close()
