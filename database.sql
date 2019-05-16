CREATE TABLE airline_staff(
	username	varchar(20),
	user_password	varchar(20) NOT NULL,
	first_name	varchar(20),
	last_name	varchar(20),
	date_of_birth date,
	phone_number varchar(20)
);

ALTER TABLE `airline_staff` ADD INDEX( `username`);


CREATE TABLE airline(
	name    varchar(20),
	PRIMARY KEY (name)
);

ALTER TABLE `airline` ADD INDEX( `name`);

INSERT INTO `airline` (`name`) VALUES
('Air China');

CREATE TABLE airplane(
	airline_name    varchar(20),
	ID      varchar(20),
	seats   int,
	PRIMARY KEY (airline_name, ID),
	FOREIGN KEY (airline_name) REFERENCES airline(name)
	on delete cascade
	on update cascade
);
ALTER TABLE `airplane` ADD INDEX( `ID`);


CREATE TABLE flight( 
	airline_name varchar(20), 
	flight_num varchar(20), 
	base_price int(5), 
	airplane_id varchar(20), 
	status varchar(20), 
	PRIMARY KEY (airline_name, flight_num),
	FOREIGN KEY (airline_name) REFERENCES airline(name),
	FOREIGN KEY (airplane_id) REFERENCES airplane(ID)
);

ALTER TABLE `flight` ADD INDEX( `flight_num`);



CREATE TABLE employment( 
	airline_name varchar(20), 
	username varchar(20),
	PRIMARY KEY (username),
	FOREIGN KEY (airline_name) REFERENCES airline(name)
	on delete cascade
	on update cascade,
	FOREIGN KEY (username) REFERENCES airline_staff(username)
);




CREATE TABLE airport(
	name varchar(20),
	city varchar(20),
	PRIMARY KEY (name)
);
ALTER TABLE `airport` ADD INDEX( `name`);




CREATE TABLE departure(
	 airline_name varchar(20),
	 flight_num varchar(20),
	 airport_name varchar(20),
	 time datetime,
	 city varchar(20) DEFAULT NULL,
	 PRIMARY KEY (airline_name, flight_num, airport_name),
	 FOREIGN KEY (airline_name) REFERENCES airline(name)
	 on delete cascade
	 on update cascade,
	 FOREIGN KEY (flight_num) REFERENCES flight(flight_num)
	 on delete cascade
	 on update cascade,
	 FOREIGN KEY (airport_name) REFERENCES airport(name)
	 on delete cascade
	 on update cascade
);





CREATE TABLE arrival(
	 airline_name varchar(20),
	 flight_num varchar(20),
	 airport_name varchar(20),
	 time datetime,
	 `city` varchar(20) DEFAULT NULL,
	 PRIMARY KEY (airline_name, flight_num, airport_name),
	 FOREIGN KEY (airline_name) REFERENCES airline(name)
	 on delete cascade
	 on update cascade,
	 FOREIGN KEY (flight_num) REFERENCES flight(flight_num)
	 on delete cascade
	 on update cascade,
	 FOREIGN KEY (airport_name) REFERENCES airport(name)
	 on delete cascade
	 on update cascade
);



CREATE TABLE booking_agent(
	 email varchar(50),
	 booking_agent_ID varchar(20) UNIQUE,
	 password varchar(20) NOT NULL,
	 commission_30d int,
	 average_commission int,
	 total_tickets int,
	 PRIMARY KEY (email, booking_agent_ID)
);


CREATE TABLE customer(
	 email varchar(50),
	 password varchar(20) NOT NULL,
	 name varchar(20),
	 building_num int,
	 street varchar(20),
	 city varchar(20),
	 state varchar(20),
	 phone_num varchar(20),
	 passport_num varchar(20),
	 passport_expiration datetime,
	 passport_country varchar(20),
	 date_of_birth datetime,
	 PRIMARY KEY (email)
);





CREATE TABLE ticket(
	 ticket_ID varchar(20),
	 PRIMARY KEY (ticket_ID)
);


ALTER TABLE `ticket` ADD INDEX( `ticket_ID`);

CREATE TABLE order_info(
	 order_ID varchar(20),
	 flight_num varchar(20),
	 airline_name varchar(20),
	 purchase_date_time datetime,
	 card_exp_date datetime,
	 name_on_card varchar(20),
	 card_num varchar(20),
	 card_type varchar(20),
	 sold_price int,
	 PRIMARY KEY (order_ID),
	 FOREIGN KEY (flight_num) REFERENCES flight(flight_num)
	 on delete cascade
	 on update cascade,
	 FOREIGN KEY (airline_name) REFERENCES airline(name)
	 on delete cascade
	 on update cascade
);

ALTER TABLE `order_info` ADD INDEX( `order_ID`);




CREATE TABLE purchases(
	 buyer_email varchar(50),
	 booking_agent_ID varchar(20) DEFAULT NULL,
	 order_ID varchar(20),
	 ticket_ID varchar(20),
	 commission int(11) DEFAULT NULL,
	 PRIMARY KEY (buyer_email, booking_agent_ID, order_ID, ticket_ID),
	 FOREIGN KEY (order_ID) REFERENCES order_info(order_ID)
	 on delete cascade
	 on update cascade,
	 FOREIGN KEY (ticket_ID) REFERENCES ticket(ticket_ID)
	 on delete cascade
	 on update cascade
);















