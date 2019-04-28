#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='192.168.64.2',
#					   port=8080,
                       user='zjy',
                       password='19970402zjy',
                       db='airline_ticket_reservation',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
	#username = session['username']
	cursor = conn.cursor()
	query = 'SELECT flight_num, status FROM flight'
	cursor.execute(query)
	data1 = cursor.fetchall() 
	cursor.close()
	return render_template('index.html', posts=data1)

@app.route('/searchAuth', methods=['GET', 'POST'])
def searchAuth():
	#grabs information from the forms
	source = request.form['source']
	destination = request.form['destination']
	dtime = request.form['departure date']
	atime = request.form['arrival date']
	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	if atime == '':
		query = 'SELECT departure.flight_num flight_num, departure.time dtime, arrival.time atime FROM departure, arrival WHERE departure.flight_num = arrival.flight_num AND departure.airport_name = %s AND arrival.airport_name = %s AND departure.time like %s'
		cursor.execute(query, (source, destination, dtime + '%'))
	else:
		query = 'SELECT departure.flight_num flight_num, departure.time dtime, arrival.time atime FROM departure, arrival WHERE departure.flight_num = arrival.flight_num AND departure.airport_name = %s AND arrival.airport_name = %s AND departure.time like %s'
		query += 'UNION '
		query += 'SELECT departure.flight_num flight_num, departure.time dtime, arrival.time atime FROM departure, arrival WHERE departure.flight_num = arrival.flight_num AND departure.airport_name = %s AND arrival.airport_name = %s AND departure.time like %s'
		cursor.execute(query, (source, destination, dtime + '%',destination, source, atime + '%'))
	print(query)
	#stores the results in a variable
	data = cursor.fetchall()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	print(data)
	return render_template('flight.html', posts=data)

# ============================================================================================ #

#Define route for login
@app.route('/login')
def login():
	return render_template('login.html')

#Define route for register
@app.route('/register')
def register():
	return render_template('register.html')

#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM user WHERE username = %s and password = %s'
	cursor.execute(query, (username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		return redirect(url_for('home'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login.html', error=error)

#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM user WHERE username = %s'
	cursor.execute(query, (username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register.html', error = error)
	else:
		ins = 'INSERT INTO user VALUES(%s, %s)'
		cursor.execute(ins, (username, password))
		conn.commit()
		cursor.close()
		return render_template('index.html')

@app.route('/home')
def home():
    
    username = session['username']
    cursor = conn.cursor();
    query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    cursor.execute(query, (username))
    data1 = cursor.fetchall() 
    for each in data1:
        print(each['blog_post'])
    cursor.close()
    return render_template('home.html', username=username, posts=data1)

		
@app.route('/post', methods=['GET', 'POST'])
def post():
	username = session['username']
	cursor = conn.cursor();
	blog = request.form['blog']
	query = 'INSERT INTO blog (blog_post, username) VALUES(%s, %s)'
	cursor.execute(query, (blog, username))
	conn.commit()
	cursor.close()
	return redirect(url_for('home'))

@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')

@app.route('/flight')
def flight():

	return render_template('index.html', username=username, posts=data1)
		
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	print("Runing flask server")
	app.run('127.0.0.1', port = 5050, debug = True)
