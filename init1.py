#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
from datetime import datetime

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
	#stores the results in a variable
	data = cursor.fetchall()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	return render_template('flight.html', posts=data)

@app.route('/flight_status', methods=['GET', 'POST'])
def searchStatus():
	airline = request.form['airline']
	flight_num = request.form['flight_num']
	cursor = conn.cursor()
	query = 'SELECT airline_name, flight_num, status FROM flight WHERE airline_name = %s AND flight_num = %s'
	cursor.execute(query, (airline, flight_num))
	data = cursor.fetchall()
	cursor.close()
	return render_template('flight_status.html', posts=data)

# ============================================================================================ #

#Define route for login
@app.route('/login')
def login():
	return render_template('login.html')

#Define route for register
@app.route('/register')
def register():
	return render_template('register.html')

@app.route('/register_Customer', methods=['GET', 'POST'])
def register_Customer():
	username = request.form['username']
	password = request.form['password']
	name = request.form['name']
	phone = request.form['phone']
	date_of_birth = request.form['date_of_birth']
	building_number = request.form['building_number']
	street = request.form['street']
	city = request.form['city']
	state = request.form['state']
	passport_number = request.form['passport_number']
	passport_expiration = request.form['passport_expiration']
	passport_country = request.form['passport_country']
	cursor = conn.cursor()
	query = 'SELECT * FROM customer WHERE email = %s'
	cursor.execute(query, (username))
	data = cursor.fetchone()
	if(data):
		error = "You have an account, please login directly"
		return render_template('register.html', error = error)
	else:
		ins = 'INSERT INTO customer VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
		cursor.execute(ins,(username,password,name,building_number,street,city,state,phone,passport_number,passport_expiration,passport_country,date_of_birth))
		conn.commit()
		cursor.close()
		return render_template('index.html')

@app.route('/register_Staff', methods=['GET', 'POST'])
def register_Staff():
	username = request.form['username']
	password = request.form['password']
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	date_of_birth = request.form['date_of_birth']
	airline_name = request.form['airline_name']
	cursor = conn.cursor()
	query = 'SELECT * FROM airline_staff WHERE username = %s'
	cursor.execute(query, (username))
	data = cursor.fetchone()
	if(data):
		error = "You have an account, please login directly"
		return render_template('register.html', error = error)
	else:
		ins = 'INSERT INTO airline_staff VALUES(%s,%s,%s,%s,%s,%s,)'
		cursor.execute(ins,(username,password,first_name,last_name,date_of_birth,airline_name))
		conn.commit()
		cursor.close()
		return render_template('index.html')

@app.route('/register_Agent', methods=['GET', 'POST'])
def register_Agent():
	email = request.form['email']
	password = request.form['password']
	booking_agent_id = request.form['booking_agent_id']
	cursor = conn.cursor()
	query = 'SELECT * FROM booking_agent WHERE booking_agent_ID = %s'
	cursor.execute(query, (booking_agent_id))
	data = cursor.fetchone()
	if(data):
		error = "You have an account, please login directly"
		return render_template('register.html', error = error)
	else:
		ins = 'INSERT INTO booking_agent VALUES(%s,%s,%s,NULL,NULL,NULL)'
		cursor.execute(ins,(email,booking_agent_id,password))
		conn.commit()
		cursor.close()
		return render_template('index.html')


@app.route('/login_Customer', methods=['GET', 'POST'])
def login_Customer():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM customer WHERE email = %s and password = %s'
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
		return redirect(url_for('home_Customer'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login.html', error=error)

#Authenticates the login
@app.route('/login_Staff', methods=['GET', 'POST'])
def login_Staff():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM airline_staff WHERE username = %s and user_password = %s'
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

@app.route('/login_Agent', methods=['GET', 'POST'])
def login_Agent():
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']
	booking_agent_id = request.form['booking_agent_id']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM booking_agent WHERE email = %s and password = %s and booking_agent_id = %s'
	cursor.execute(query, (email, password, booking_agent_id))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = email
		return redirect(url_for('home_agent'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login.html', error=error)


@app.route('/home_agent')
def home_agent():
	username = session['username']
	cursor = conn.cursor();
	query = 'SELECT order_info.flight_num flight_num, departure.airline_name airline_name, ticket_ID, time FROM booking_agent, purchases, order_info, departure WHERE booking_agent.booking_agent_ID = purchases.booking_agent_ID and purchases.order_ID = order_info.order_ID and order_info.flight_num = departure.flight_num and email = %s and departure.time >= NOW()'
	cursor.execute(query, (username))
	data = cursor.fetchall()
	print(data)
	cursor.close()
	return render_template('home_booking_agent.html', username=username, posts = data)

# Handle purchasing in /home, record flight_num information for further activities
@app.route('/purchase', methods = ['POST','GET'])
def purchase():
	source = request.form['source']
	destination = request.form['destination']
	dtime = request.form['departure date']
	atime = request.form['arrival date']
	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	if atime == '':
		query = 'SELECT departure.flight_num flight_num, departure.time dtime, arrival.time atime, flight.base_price bprice FROM departure, arrival, flight WHERE departure.flight_num = arrival.flight_num AND departure.flight_num = flight.flight_num AND departure.airport_name = %s AND arrival.airport_name = %s AND departure.time like %s'
		cursor.execute(query, (source, destination, dtime + '%'))
	else:
		query = 'SELECT departure.flight_num flight_num, departure.time dtime, arrival.time atime, flight.base_price bprice FROM departure, arrival, flight WHERE departure.flight_num = arrival.flight_num AND departure.flight_num = flight.flight_num AND departure.airport_name = %s AND arrival.airport_name = %s AND departure.time like %s'
		query += 'UNION '
		query += 'SELECT departure.flight_num flight_num, departure.time dtime, arrival.time atime, flight.base_price bprice FROM departure, arrival, flight WHERE departure.flight_num = arrival.flight_num AND arrival.flight_num = flight.flight_num AND departure.airport_name = %s AND arrival.airport_name = %s AND departure.time like %s'
		cursor.execute(query, (source, destination, dtime + '%',destination, source, atime + '%'))
	#stores the results in a variable
	data = cursor.fetchall()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	return render_template('purchase_agent.html', posts=data)

# Handle purchase information 
@app.route("/purchaseAuth", methods = ['POST', 'GET'])
def purchaseAuth():
	if request.method == "POST":
		print(request.form["flight_num"])
		flight_num = request.form["flight_num"]
		print("response:", flight_num)
	cursor = conn.cursor()
	query = 'SELECT flight.flight_num flight_num, flight.airline_name airline_name, departure.airport_name dairport, arrival.time atime, arrival.airport_name aairport, departure.time dtime, base_price bprice FROM flight, departure, arrival WHERE flight.flight_num = %s AND departure.flight_num = %s AND arrival.flight_num = %s'
	cursor.execute(query, (flight_num, flight_num, flight_num))
	data = cursor.fetchone()
	return render_template("purchaseAuth.html", data=data)

# After recording purchase information
@app.route('/purchaseComplete', methods = ['POST'])
def purchaseComplete1():
	"""
	if request.method == "POST":
		print(request.form)
	#print(request.form)
	return render_template("login.html")
	"""

	# 蛇蛇 这里的问题是purchaseAuth.html会post两次内容 所以整个function会跑两次 然后第二次的flight_num就会变成None 我还没想好怎么解决
	# 另一个bug是时间老是0000-00-00 00：00：00 我也不知道为啥 print出来明明是对的
	# 目前这个功能的其他东西都已经好了 你可以跑跑看 然后order_info这个表也会被更新
	# purchases这个表的更新我还没写 包括ticket怎么算也还没写 先休息一下hhh

	print("Form type ", type(request.form))
	flight_num = str(request.form.get('flight_num'))
	print("original flight_num", flight_num)
	card_exp_date = request.form['card_exp_date']
	name_on_card = request.form['name_on_card']
	card_num = request.form['card_num']
	card_type = request.form['card_type']

	print("current flight_num", flight_num)

	cursor = conn.cursor()
	query = 'SELECT airline_name FROM flight WHERE flight_num = %s'
	cursor.execute(query, (flight_num))
	airline_name = cursor.fetchone()

	#cursor = conn.cursor()
	query = 'SELECT MAX(order_id) FROM order_info'
	cursor.execute(query)
	latest_order = int(cursor.fetchone()['MAX(order_id)'])
	new_order_no = str(latest_order + 1).rjust(4,"0")
	#print("New Order No. ", new_order_no)

	#cursor = conn.cursor()
	query = 'SELECT base_price FROM flight WHERE flight_num = %s'
	cursor.execute(query, (flight_num))
	sold_price = str(cursor.fetchone())

	purchase_time = str(datetime.now().strftime('%H:%M:%S'))
	print("current time", purchase_time)

	if(latest_order):
		ins = 'INSERT INTO order_info VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
		cursor.execute(ins,(new_order_no,flight_num,airline_name,purchase_time,card_exp_date,name_on_card,card_num,card_type,sold_price))
		conn.commit()
		cursor.close()
		return render_template('success_purchase.html')
	else:
		ins = 'INSERT INTO order_info VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
		cursor.execute(ins,("0001",flight_num,airline_name,purchase_time,card_exp_date,name_on_card,card_num,card_type,sold_price))
		conn.commit()
		cursor.close()
		return render_template('success_purchase.html')



@app.route('/home')
def home():
    
    username = session['username']
    cursor = conn.cursor()

    return render_template('home.html', username=username)

@app.route('/home_Customer')
def home_Customer():
	username = session['username']
	cursor = conn.cursor()
	query = 'SELECT departure.flight_num flight_num, order_info.airline_name airline_name, departure.time dtime FROM purchases NATURAL JOIN order_info, departure, arrival WHERE buyer_email = %s AND departure.flight_num = order_info.flight_num AND arrival.flight_num = order_info.flight_num AND departure.time > CURRENT_TIMESTAMP'
	cursor.execute(query, (username))
	data = cursor.fetchall()
	print(data)
	cursor.close()
	return render_template('home_Customer.html', username=username, posts = data)


@app.route('/myFutureFlights', methods=['GET', 'POST'])
def myFutureFlights():
	#cursor used to send queries
	cursor = conn.cursor()
	#specifies username
	username = session['username']
	#executes query
	query = 'SELECT departure.flight_num flight_num, departure.time dtime, arrival.time atime FROM purchases NATURAL JOIN order_info, departure, arrival WHERE buyer_email = %s AND departure.flight_num = order_info.flight_num AND arrival.flight_num = order_info.flight_num'
	cursor.execute(query, username)
	#stores the results in a variable
	data = cursor.fetchall()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	return render_template('flight.html', posts=data)

@app.route('/myFlights', methods=['GET', 'POST'])
def myFlights():
	#grabs information from the forms
	source = request.form['source']
	destination = request.form['destination']
	dtime = request.form['departure date']
	atime = request.form['arrival date']
	#cursor used to send queries
	cursor = conn.cursor()
	#specifies username
	username = session['username']
	#executes query
	if atime == '':
		query = 'SELECT departure.flight_num flight_num, departure.time dtime, arrival.time atime FROM purchases NATURAL JOIN order_info, departure, arrival WHERE buyer_email = %s AND departure.flight_num = order_info.flight_num AND arrival.flight_num = order_info.flight_num AND departure.airport_name = %s AND arrival.airport_name = %s AND departure.time like %s'
		cursor.execute(query, (username, source, destination, dtime + '%'))
	else:
		query = 'SELECT departure.flight_num flight_num, departure.time dtime, arrival.time atime FROM departure, arrival WHERE departure.flight_num = arrival.flight_num AND departure.airport_name = %s AND arrival.airport_name = %s AND departure.time like %s'
		query += 'UNION '
		query += 'SELECT departure.flight_num flight_num, departure.time dtime, arrival.time atime FROM departure, arrival WHERE departure.flight_num = arrival.flight_num AND departure.airport_name = %s AND arrival.airport_name = %s AND departure.time like %s'
		cursor.execute(query, (source, destination, dtime + '%',destination, source, atime + '%'))
	#stores the results in a variable
	data = cursor.fetchall()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	return render_template('flight.html', posts=data)
		
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
