#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
from datetime import datetime

#Initialize the app from Flask
app = Flask(__name__)
FLIGHT_NUM = 'None'

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
	redirect = ""
	return render_template('flight.html', posts=data, redirect = redirect, staff = [False, []])

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
	phone_num = request.form['phone_num']
	airline_name = request.form['airline_name']
	cursor = conn.cursor()
	query = 'SELECT * FROM airline_staff WHERE username = %s'
	cursor.execute(query, (username))
	data = cursor.fetchone()
	if(data):
		error = "You have an account, please login directly"
		return render_template('register.html', error = error)
	else:
		ins = 'INSERT INTO airline_staff VALUES(%s,%s,%s,%s,%s,%s)'
		cursor.execute(ins,(username,password,first_name,last_name,date_of_birth,phone_num))
		ins = 'INSERT INTO employment VALUES(%s,%s)'
		cursor.execute(ins,(airline_name,username))
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
		session['id'] = None
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
		return redirect(url_for('home_staff'))
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
		session['id'] = booking_agent_id
		return redirect(url_for('home_agent'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login.html', error=error)


@app.route('/home_agent', methods = ['GET', 'POST'])
def home_agent():
	username = session['username']
	ID = session['id']
	print(username)

	cursor = conn.cursor()
	auth = "SELECT * FROM booking_agent WHERE email = %s"
	cursor.execute(auth, (username))
	auth_result = cursor.fetchone()
	if auth_result == None:
		conn.commit()
		cursor.close()
		return render_template('unauthorized_warning.html')

	cursor1 = conn.cursor()
	query1 = 'SELECT buyer_email, order_info.flight_num flight_num, departure.airline_name airline_name, ticket_ID, purchase_date_time FROM booking_agent, purchases, order_info, departure WHERE booking_agent.booking_agent_ID = purchases.booking_agent_ID and purchases.order_ID = order_info.order_ID and order_info.flight_num = departure.flight_num and booking_agent.email = %s and departure.time >= NOW()'
	cursor1.execute(query1, (username))
	data1 = cursor1.fetchall()
	cursor1.close()

	# query for 30 day commissions
	cursor2 = conn.cursor()
	query2 = 'SELECT SUM(commission) tcom, AVG(commission) acom, COUNT(purchases.order_ID) ttickets FROM booking_agent, purchases, order_info WHERE booking_agent.booking_agent_ID = purchases.booking_agent_ID AND purchases.order_ID = order_info.order_ID AND booking_agent.booking_agent_ID = %s AND order_info.purchase_date_time >= DATE_ADD(NOW(), INTERVAL -30 DAY)'
	cursor2.execute(query2, (ID))
	data2 = cursor2.fetchall()

	# query for top customers
	cursor4 = conn.cursor()
	query4 = 'SELECT customer.email email, SUM(commission) total_commission_received, COUNT(order_info.order_ID) total_tickets FROM customer, purchases, booking_agent, order_info WHERE customer.email = purchases.buyer_email AND purchases.booking_agent_ID = booking_agent.booking_agent_ID AND order_info.order_id = purchases.order_id AND order_info.purchase_date_time >= DATE_ADD(NOW(), INTERVAL -6 MONTH) AND purchases.booking_agent_ID = %s GROUP BY purchases.buyer_email ORDER BY COUNT(order_info.order_ID) DESC LIMIT 5'
	cursor4.execute(query4, (ID))
	top_cus_6months = cursor4.fetchall()

	cursor5 = conn.cursor()
	query5 = 'SELECT customer.email email, SUM(commission) total_commission_received, COUNT(order_info.order_ID) total_tickets FROM customer, purchases, booking_agent, order_info WHERE customer.email = purchases.buyer_email AND purchases.booking_agent_ID = booking_agent.booking_agent_ID AND order_info.order_id = purchases.order_id AND order_info.purchase_date_time >= DATE_ADD(NOW(), INTERVAL -12 MONTH) AND purchases.booking_agent_ID = %s GROUP BY purchases.buyer_email ORDER BY COUNT(order_info.order_ID) DESC LIMIT 5'
	cursor5.execute(query5, (ID))
	top_cus_12months = cursor5.fetchall()


	if request.method == "POST":
		sdate = request.form['starting date']
		edate = request.form['end date']
		print("end date", edate)
		if edate == "":
			edate = datetime.now()
		cursor3 = conn.cursor()
		query3 = 'SELECT SUM(commission) tcom, AVG(commission) acom, COUNT(purchases.order_ID) ttickets FROM booking_agent, purchases, order_info WHERE booking_agent.booking_agent_ID = purchases.booking_agent_ID AND purchases.order_ID = order_info.order_ID AND booking_agent.booking_agent_ID = %s AND order_info.purchase_date_time >= %s AND order_info.purchase_date_time <= %s'
		cursor3.execute(query3, (ID, sdate, edate))
		# update the commssion results
		data3 = cursor3.fetchall()
		print((ID, sdate, edate))
		print(data3)
		return render_template('home_booking_agent.html', username=username, flight_info = data1, agent_info = data3, top_cus_6months=top_cus_6months, top_cus_12months=top_cus_12months)
	else:
		return render_template('home_booking_agent.html', username=username, flight_info = data1, agent_info = data2, top_cus_6months=top_cus_6months, top_cus_12months=top_cus_12months)

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
		print(source, destination, dtime + '%')
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
	return render_template('purchase.html', posts=data)

# Handle purchase information 
@app.route("/purchaseAuth", methods = ['POST', 'GET'])
def purchaseAuth():
	if request.method == "POST":
		#print(request.form["flight_num"])
		flight_num = request.form["flight_num"]
		#print("response:", flight_num)
	cursor = conn.cursor()
	query = 'SELECT flight.flight_num flight_num, flight.airline_name airline_name, departure.airport_name dairport, arrival.time atime, arrival.airport_name aairport, departure.time dtime, base_price bprice FROM flight, departure, arrival WHERE flight.flight_num = %s AND departure.flight_num = %s AND arrival.flight_num = %s'
	cursor.execute(query, (flight_num, flight_num, flight_num))
	data = cursor.fetchone()
	return render_template("purchaseAuth.html", data=data)

# After recording purchase information
@app.route('/purchaseComplete', methods = ['POST'])
def purchaseComplete():
	"""
	if request.method == "POST":
		print(request.form)
	#print(request.form)
	return render_template("login.html")
	"""
	global FLIGHT_NUM

	cursor = conn.cursor()
	if str(request.form.get('flight_num')) != 'None':
		FLIGHT_NUM = str(request.form.get('flight_num'))
	card_exp_date = request.form['card_exp_date']
	name_on_card = request.form['name_on_card']
	card_num = request.form['card_num']
	card_type = request.form['card_type']
	email = request.form['customer_email']
	query = "SELECT base_price FROM flight WHERE flight_num = %s"
	cursor.execute(query, FLIGHT_NUM)
	commission = float(cursor.fetchone()['base_price']) * 0.1


	query = 'SELECT airline_name FROM flight WHERE flight_num = %s'
	cursor.execute(query, (FLIGHT_NUM))
	airline_name = cursor.fetchone()['airline_name']

	query = 'SELECT MAX(order_id) FROM order_info'
	cursor.execute(query)
	latest_order = int(cursor.fetchone()['MAX(order_id)'])
	new_order_no = str(latest_order + 1).rjust(4,"0")

	query = 'SELECT base_price FROM flight WHERE flight_num = %s'
	cursor.execute(query, (FLIGHT_NUM))
	sold_price =  int(cursor.fetchone()['base_price']) + float(commission)

	purchase_time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

	print("sold_price:", sold_price)

	if(latest_order):
		ins = 'INSERT INTO order_info VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
		cursor.execute(ins,(new_order_no,FLIGHT_NUM,airline_name,purchase_time,card_exp_date,name_on_card,card_num,card_type,sold_price))
		
	else:
		new_order_no = "0001"
		ins = 'INSERT INTO order_info VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
		cursor.execute(ins,(new_order_no,FLIGHT_NUM,airline_name,purchase_time,card_exp_date,name_on_card,card_num,card_type,sold_price))

	query = 'SELECT ticket_ID FROM ticket WHERE ticket_ID like %s'
	cursor.execute(query, (FLIGHT_NUM + "%"))
	all_tickets = cursor.fetchall()
	

	if(all_tickets != ()):
		final_ticket = all_tickets[0]['ticket_ID']
		for dic in all_tickets:
			if dic['ticket_ID'] > final_ticket:
				final_ticket = dic['ticket_ID']
		new_ticket = final_ticket[:-2] + str(int(final_ticket[-2])+1) + final_ticket[-1]
		ins = 'INSERT INTO ticket VALUES(%s)'
		cursor.execute(ins, (new_ticket))
	else:
		new_ticket = FLIGHT_NUM + "-1A"
		ins = 'INSERT INTO ticket VALUES(%s)'
		cursor.execute(ins, (new_ticket))
 
	ins = 'INSERT INTO purchases VALUES (%s,%s,%s,%s,%s)'

	# For Customer 
	if session['id'] is None:
		cursor.execute(ins, (session['username'], "", new_order_no, new_ticket, ""))
		redirect = 'home_Customer'
	# For Booking Agent
	else:
		cursor.execute(ins, (email, session['id'], new_order_no, new_ticket, commission))
		redirect = 'home_agent'

	conn.commit()
	cursor.close()
	return render_template('success_purchase.html', redirect = redirect)


@app.route('/home_Customer', methods=['POST', 'GET'])
def home_Customer():
	username = session['username']
	cursor = conn.cursor()
	query = 'SELECT departure.flight_num flight_num, order_info.airline_name airline_name, departure.time dtime FROM purchases NATURAL JOIN order_info, departure, arrival WHERE buyer_email = %s AND departure.flight_num = order_info.flight_num AND arrival.flight_num = order_info.flight_num AND departure.time > CURRENT_TIMESTAMP'
	cursor.execute(query, (username))
	data = cursor.fetchall()

	# query for yearly sum of spending
	query = 'SELECT sum(sold_price) + sum(commission) yearly_spending FROM order_info, purchases WHERE order_info.order_id = purchases.order_id AND buyer_email = %s'
	cursor.execute(query, (username))
	spending = [cursor.fetchone()]

	if request.method == "POST":
		sdate = request.form['starting date']
		edate = request.form['end date']
		if  edate == '':
			query = 'SELECT sum(sold_price + commission) total, year(purchase_date_time) year, month(purchase_date_time) month FROM order_info NATURAL JOIN purchases WHERE buyer_email = %s AND purchase_date_time > %s GROUP BY year(purchase_date_time), month(purchase_date_time)' 
			cursor.execute(query, (username, sdate))
		else:
			query = 'SELECT sum(sold_price + commission) total, year(purchase_date_time) year, month(purchase_date_time) month FROM order_info NATURAL JOIN purchases WHERE buyer_email = %s AND purchase_date_time > %s AND purchase_date_time < %s GROUP BY year(purchase_date_time), month(purchase_date_time)' 
			cursor.execute(query, (username, sdate, edate))
		# update the commssion results
		y_m_spending = cursor.fetchall()
		for entry in y_m_spending:
			entry['ym'] = str(entry['year']) + "-" + str(entry['month'])
			del entry['year']
			del entry['month']
		spending.append(y_m_spending)
		cursor.close()
		return render_template('home_Customer.html', username=username, posts = data, spending = spending)
	else:
		# query for monthwise spending
		query = 'SELECT sum(sold_price + commission) total, year(purchase_date_time) year, month(purchase_date_time) month FROM order_info NATURAL JOIN purchases WHERE buyer_email = %s AND purchase_date_time > date_add(date(now()), INTERVAL -6 month) GROUP BY year(purchase_date_time), month(purchase_date_time)' 
		cursor.execute(query, (username))
		y_m_spending = cursor.fetchall()
		for entry in y_m_spending:
			entry['ym'] = str(entry['year']) + "-" + str(entry['month'])
			del entry['year']
			del entry['month']
		spending.append(y_m_spending)

		cursor.close()
		return render_template('home_Customer.html', username=username, posts = data, spending = spending)
		

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
	redirect = ""
	return render_template('flight.html', posts=data, redirect = redirect, staff = [False, []])

@app.route('/myFlights', methods=['GET', 'POST'])
def myFlights():
	#grabs information from the forms
	source = request.form['source'];
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
	redirect = ""
	return render_template('flight.html', posts=data, redirect = redirect, staff = [False, []])
		
@app.route('/post', methods=['GET', 'POST'])
def post():
	username = session['username']
	cursor = conn.cursor()
	blog = request.form['blog']
	query = 'INSERT INTO blog (blog_post, username) VALUES(%s, %s)'
	cursor.execute(query, (blog, username))
	conn.commit()
	cursor.close()
	return redirect(url_for('home'))

@app.route('/logout')
def logout():
	session.pop('username')
	return render_template('goodbye.html')

@app.route('/home_staff', methods=['GET', 'POST'])
def home_staff():
	username = session['username']
	cursor = conn.cursor()
	data = []

	auth = "SELECT airline_name FROM employment WHERE username = %s"
	cursor.execute(auth, (username))
	airline_name = cursor.fetchone()
	print("bug test", airline_name)
	if airline_name == None:
		conn.commit()
		cursor.close()
		return render_template('unauthorized_warning.html')
	airline_name = airline_name['airline_name']

	#--Use case 4. View my flights--
	query = 'SELECT departure.flight_num flight_num, flight.airline_name airline_name, departure.time dtime FROM employment, flight NATURAL JOIN departure, arrival WHERE employment.username = %s AND departure.flight_num = flight.flight_num AND arrival.flight_num = flight.flight_num AND departure.time > CURRENT_TIMESTAMP AND departure.time < date_add(date(now()), INTERVAL 30 day) AND flight.airline_name = employment.airline_name'
	cursor.execute(query, (username))
	data.append(cursor.fetchall())

	#--Use case 9. View all the booking agents--
	query = 'CREATE VIEW top_ticket_m (agent, orders) AS SELECT booking_agent_ID, COUNT(purchases.order_ID) FROM order_info, purchases WHERE purchases.order_ID = order_info.order_ID AND booking_agent_ID != "" AND purchase_date_time > date_add(date(now()), INTERVAL -1 month) AND order_info.airline_name = %s GROUP BY booking_agent_ID'
	cursor.execute(query, (airline_name))
	query = 'SELECT * FROM top_ticket_m ORDER BY orders DESC LIMIT 5'
	cursor.execute(query)
	data.append(cursor.fetchall())
	query = 'DROP VIEW top_ticket_m'
	cursor.execute(query)

	query = 'CREATE VIEW top_ticket_y (agent, orders) AS SELECT booking_agent_ID, COUNT(purchases.order_ID) FROM order_info, purchases WHERE purchases.order_ID = order_info.order_ID AND booking_agent_ID != "" AND purchase_date_time > date_add(date(now()), INTERVAL -1 year) AND order_info.airline_name = %s GROUP BY booking_agent_ID'
	cursor.execute(query, (airline_name))
	query = 'SELECT * FROM top_ticket_y ORDER BY orders DESC LIMIT 5'
	cursor.execute(query)
	data.append(cursor.fetchall())
	query = 'DROP VIEW top_ticket_y'
	cursor.execute(query)

	query = 'CREATE VIEW top_comm_y (agent, comm) AS SELECT booking_agent_ID, SUM(sold_price)*0.1 FROM order_info, purchases WHERE purchases.order_ID = order_info.order_ID AND booking_agent_ID != "" AND purchase_date_time > date_add(date(now()), INTERVAL -1 year) AND order_info.airline_name = %s GROUP BY booking_agent_ID'
	cursor.execute(query, (airline_name))
	query = 'SELECT * FROM top_comm_y ORDER BY comm DESC LIMIT 5'
	cursor.execute(query)
	data.append(cursor.fetchall())
	query = 'DROP VIEW top_comm_y'
	cursor.execute(query)

	#--Use case 10. View frequent customers--
	query = 'CREATE VIEW top_customer (customer, trips) AS SELECT buyer_email, COUNT(purchases.order_ID) FROM order_info, purchases WHERE purchases.order_ID = order_info.order_ID AND booking_agent_ID != "" AND purchase_date_time > date_add(date(now()), INTERVAL -1 year) AND order_info.airline_name = %s GROUP BY buyer_email'
	cursor.execute(query, (airline_name))
	query = 'SELECT * FROM top_customer ORDER BY trips DESC LIMIT 5'
	cursor.execute(query)
	data.append(cursor.fetchall())
	query = 'DROP VIEW top_customer'
	cursor.execute(query)

	#--Use case 13. View top destinations--
	query = 'CREATE VIEW top_destination_3m (destination, trips) AS SELECT city, COUNT(order_info.flight_num) FROM order_info, arrival WHERE order_info.flight_num = arrival.flight_num AND order_info.airline_name = %s AND purchase_date_time > date_add(date(now()), INTERVAL -3 month) GROUP BY city'
	cursor.execute(query, (airline_name))
	query = 'SELECT * FROM top_destination_3m ORDER BY trips DESC LIMIT 5'
	cursor.execute(query)
	data.append(cursor.fetchall())
	query = 'DROP VIEW top_destination_3m'
	cursor.execute(query)

	query = 'CREATE VIEW top_destination_y (destination, trips) AS SELECT city, COUNT(order_info.flight_num) FROM order_info, arrival WHERE order_info.flight_num = arrival.flight_num AND order_info.airline_name = %s AND purchase_date_time > date_add(date(now()), INTERVAL -1 year) GROUP BY city'
	cursor.execute(query, (airline_name))
	query = 'SELECT * FROM top_destination_y ORDER BY trips DESC LIMIT 5'
	cursor.execute(query)
	data.append(cursor.fetchall())
	query = 'DROP VIEW top_destination_y'
	cursor.execute(query)

	#--Use case 11. View reports--
	#query = 'SELECT sum(sold_price) + sum(commission) yearly_spending FROM order_info, purchases WHERE order_info.order_id = purchases.order_id AND buyer_email = %s'
	#cursor.execute(query, (username))
	#spending = [cursor.fetchone()]

	if request.method == "POST":
		sdate = request.form['starting date']
		edate = request.form['end date']
		if  edate == '':
			query = 'SELECT count(order_id) sum FROM order_info NATURAL JOIN purchases WHERE airline_name = %s AND purchase_date_time > %s'
			cursor.execute(query, (airline_name, sdate))
			spending = [cursor.fetchall()[0]]
			query = 'SELECT count(order_id) sum, year(purchase_date_time) year, month(purchase_date_time) month FROM order_info NATURAL JOIN purchases WHERE airline_name = %s AND purchase_date_time > %s GROUP BY year(purchase_date_time), month(purchase_date_time)' 
			cursor.execute(query, (airline_name, sdate))
			y_m_spending = cursor.fetchall()
		else:
			query = 'SELECT count(order_id) sum FROM order_info NATURAL JOIN purchases WHERE airline_name = %s AND purchase_date_time > %s AND purchase_date_time < %s'
			cursor.execute(query, (airline_name, sdate, edate))
			spending = [cursor.fetchall()[0]]
			query = 'SELECT count(order_id) sum, year(purchase_date_time) year, month(purchase_date_time) month FROM order_info NATURAL JOIN purchases WHERE airline_name = %s AND purchase_date_time > %s AND purchase_date_time < %s GROUP BY year(purchase_date_time), month(purchase_date_time)' 
			cursor.execute(query, (airline_name, sdate, edate))
			y_m_spending = cursor.fetchall()
		# update the commssion results
		for entry in y_m_spending:
			entry['ym'] = str(entry['year']) + "-" + str(entry['month'])
			del entry['year']
			del entry['month']
		spending.append(y_m_spending)
		print(spending, "aaaaa")
	else:
		# query for monthwise spending
		query = 'SELECT count(order_id) sum FROM order_info NATURAL JOIN purchases WHERE airline_name = %s AND purchase_date_time > DATE_ADD(NOW(), INTERVAL -6 MONTH)'
		cursor.execute(query, (airline_name))
		spending = [cursor.fetchall()[0]]
		query = 'SELECT count(order_id) sum, year(purchase_date_time) year, month(purchase_date_time) month FROM order_info NATURAL JOIN purchases WHERE airline_name = %s AND purchase_date_time > DATE_ADD(NOW(), INTERVAL -6 MONTH) GROUP BY year(purchase_date_time), month(purchase_date_time)' 
		cursor.execute(query, (airline_name))
		y_m_spending = cursor.fetchall()
		for entry in y_m_spending:
			entry['ym'] = str(entry['year']) + "-" + str(entry['month'])
			del entry['year']
			del entry['month']
		spending.append(y_m_spending)

	sale_12months = [{'total_sale':0},{'total_sale':0}]
	query = 'SELECT SUM(flight.base_price) total_sale FROM purchases, order_info, flight, airline_staff, employment where purchases.order_ID = order_info.order_ID AND order_info.flight_num = flight.flight_num AND employment.username = airline_staff.username AND flight.airline_name = employment.airline_name AND airline_staff.username = %s AND purchases.commission > 0 AND order_info.purchase_date_time >= DATE_ADD(NOW(), INTERVAL -12 MONTH)'
	cursor.execute(query, (username))
	ds = cursor.fetchone()
	if ds['total_sale'] != None:
		sale_12months[0]=ds
	query = 'SELECT SUM(flight.base_price) total_sale FROM purchases, order_info, flight, airline_staff, employment where purchases.order_ID = order_info.order_ID AND order_info.flight_num = flight.flight_num AND employment.username = airline_staff.username AND flight.airline_name = employment.airline_name AND airline_staff.username = %s AND purchases.commission in (0, NULL) AND order_info.purchase_date_time >= DATE_ADD(NOW(), INTERVAL -12 MONTH)'
	cursor.execute(query, (username))
	ids = cursor.fetchone()
	if ids['total_sale'] != None:
		sale_12months[1]=ids
	print("dsids", ds, ids)

	sale_1months = [{'total_sale':0},{'total_sale':0}]
	query = 'SELECT SUM(flight.base_price) total_sale FROM purchases, order_info, flight, airline_staff, employment where purchases.order_ID = order_info.order_ID AND order_info.flight_num = flight.flight_num AND employment.username = airline_staff.username AND flight.airline_name = employment.airline_name AND airline_staff.username = %s AND purchases.commission > 0 AND order_info.purchase_date_time >= DATE_ADD(NOW(), INTERVAL -12 MONTH)'
	cursor.execute(query, (username))
	ds = cursor.fetchone()
	if ds['total_sale'] != None:
		sale_1months[0]=ds
	query = 'SELECT SUM(flight.base_price) total_sale FROM purchases, order_info, flight, airline_staff, employment where purchases.order_ID = order_info.order_ID AND order_info.flight_num = flight.flight_num AND employment.username = airline_staff.username AND flight.airline_name = employment.airline_name AND airline_staff.username = %s AND purchases.commission in (0, NULL) AND order_info.purchase_date_time >= DATE_ADD(NOW(), INTERVAL -12 MONTH)'
	cursor.execute(query, (username))
	ids = cursor.fetchone()
	if ids['total_sale'] != None:
		sale_1months[1]=ids

	cursor.close()
	return render_template('home_staff.html', username=username, posts = data, sale_12months = sale_12months, sale_1months = sale_1months, tickets = spending)

@app.route('/search_staff', methods=['GET', 'POST'])
def search_staff():
	#grabs information from the forms
	username = session['username']
	sourcec = request.form['sourcec']
	destinationc = request.form['destinationc']
	sourcea = request.form['sourcea']
	destinationa = request.form['destinationa']
	dtime = request.form['departure date']
	atime = request.form['arrival date']
	if atime == "":
		atime = "3000-1-1"
	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT departure.flight_num flight_num, departure.time dtime, departure.airport_name dairport, arrival.time atime, arrival.airport_name aairport FROM employment, flight NATURAL JOIN departure, arrival WHERE employment.username = %s AND departure.flight_num = flight.flight_num AND arrival.flight_num = flight.flight_num AND flight.airline_name = employment.airline_name'
	query += " AND departure.time >= %s AND departure.time <= %s"
	query += " AND departure.airport_name like %s AND arrival.airport_name like %s"
	query += " AND departure.city like %s AND arrival.city like %s"
	cursor.execute(query, (username, dtime, atime, sourcea + "%", destinationa + "%", sourcec + "%", destinationc + "%"))
	data = cursor.fetchall()
	#print("data", data)
	customer_info = []
	for item in data:
		flight_num = item["flight_num"]
		query = "SELECT customer.name name, customer.passport_num passport, customer.email email, flight.flight_num flight_num FROM flight, customer, order_info, purchases WHERE order_info.order_ID = purchases.order_ID AND purchases.buyer_email = customer.email AND order_info.flight_num = flight.flight_num AND flight.flight_num = %s"
		cursor.execute(query, (flight_num))
		customer_info.append(cursor.fetchall())
	cursor.close()
	redirect = "home_staff"
	staff = (True, customer_info)
	return render_template('flight.html', posts=data, redirect = redirect, staff = staff)

@app.route('/flight')
def flight():

	return render_template('index.html', username=username, posts=data1)

@app.route('/create_flight', methods=['GET', 'POST'])
def create_flight():
	cursor = conn.cursor()

	airline_name = request.form['airline_name']
	flight_num = request.form['flight_num']
	bprice = request.form['bprice']
	airplane_id = request.form['airplane_id']
	status = request.form['status']
	dairport = request.form['dairport']
	aairport = request.form['aairport']
	dcity = request.form['dcity']
	acity = request.form['acity']
	dtime = request.form['ddate'] + " " + request.form['dtime']
	atime = request.form['adate'] + " " + request.form['atime']

	username = session['username']
	auth = "SELECT airline_name, username FROM employment WHERE username = %s"
	cursor.execute(auth, (username))
	auth_list = cursor.fetchone()

	if(auth_list == None):
		conn.commit()
		cursor.close()
		return render_template('unauthorized_warning.html')

	if(auth_list['airline_name'] == airline_name):
		ins = 'INSERT INTO flight VALUES(%s,%s,%s,%s,%s)'
		cursor.execute(ins, (airline_name, flight_num, bprice, airplane_id, status))

		ins = 'INSERT INTO departure VALUES(%s,%s,%s,%s,%s)'
		cursor.execute(ins, (airline_name, flight_num, dairport, dtime, dcity))

		ins = 'INSERT INTO arrival VALUES(%s,%s,%s,%s,%s)'
		cursor.execute(ins, (airline_name, flight_num, aairport, atime, acity))

		conn.commit()
		cursor.close()
		return redirect(url_for('home_staff'))
	
	else:
		conn.commit()
		cursor.close()
		return render_template('unauthorized_warning.html')
		# maybe show a warning webpage here

@app.route('/change_status', methods=['GET', 'POST'])
def change_status():
	cursor = conn.cursor()

	flight_num = request.form['flight_num']
	status = request.form['status']

	upd = 'UPDATE flight SET status = %s WHERE flight_num = %s'
	cursor.execute(upd, (status, flight_num))

	conn.commit()
	cursor.close()
	return redirect(url_for('home_staff'))


@app.route('/create_airplane', methods=['GET', 'POST'])
def create_airplane():
	cursor = conn.cursor()

	airline_name = request.form['airline_name']
	id = request.form['id']
	seats = request.form['seats']

	username = session['username']
	auth = "SELECT username, airline_name FROM employment WHERE username = %s"
	cursor.execute(auth, (username))
	auth_list = cursor.fetchone()

	if(auth_list == None):
		conn.commit()
		cursor.close()
		return render_template('unauthorized_warning.html')

	if(auth_list['airline_name'] == airline_name):
		ins = 'INSERT INTO airplane values(%s, %s, %s)'
		cursor.execute(ins, (airline_name, id, seats))

		query = 'SELECT airline_name, ID, seats FROM airplane where airline_name = %s'
		cursor.execute(query, (auth_list['airline_name']))
		data = cursor.fetchall()

		conn.commit()
		cursor.close()
		return render_template('airplane_list.html', posts = data)
	
	else:
		conn.commit()
		cursor.close()
		return render_template('unauthorized_warning.html')

@app.route('/create_airport', methods=['GET', 'POST'])
def create_airport():
	cursor = conn.cursor()

	name = request.form['name']
	city = request.form['city']

	username = session['username']
	auth = "SELECT username, airline_name FROM employment WHERE username = %s"
	cursor.execute(auth, (username))
	auth_list = cursor.fetchone()

	if(auth_list == None):
		conn.commit()
		cursor.close()
		return render_template('unauthorized_warning.html')

	else:
		ins = 'INSERT INTO airport values(%s, %s)'
		cursor.execute(ins, (name, city))

		conn.commit()
		cursor.close()
		return redirect(url_for('home_staff'))

@app.route('/customer_flight', methods=['GET', 'POST'])
def customer_flight():
	cursor = conn.cursor()

	username = session['username']
	auth = "SELECT airline_name FROM employment WHERE username = %s"
	cursor.execute(auth, (username))
	airline = cursor.fetchone()['airline_name']

	email = request.form['email']

	print("test customer", airline, email)

	query = 'SELECT DISTINCT buyer_email, flight_num FROM order_info, purchases WHERE purchases.order_ID = order_info.order_ID AND airline_name = %s and buyer_email = %s'
	cursor.execute(query, (airline, email))
	data = cursor.fetchall()

	conn.commit()
	cursor.close()
	return render_template('customer_flight_list.html', posts = data)
		
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	print("Runing flask server")
	app.run('127.0.0.1', port = 5050, debug = True)
