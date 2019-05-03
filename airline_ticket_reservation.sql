-- phpMyAdmin SQL Dump
-- version 4.8.4
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: May 01, 2019 at 10:16 AM
-- Server version: 10.1.37-MariaDB
-- PHP Version: 7.3.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `airline_ticket_reservation`
--

-- --------------------------------------------------------

--
-- Table structure for table `airline`
--

CREATE TABLE `airline` (
  `name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `airline`
--

INSERT INTO `airline` (`name`) VALUES
('China Eastern');

-- --------------------------------------------------------

--
-- Table structure for table `airline_staff`
--

CREATE TABLE `airline_staff` (
  `username` varchar(20) DEFAULT NULL,
  `user_password` varchar(20) NOT NULL,
  `first_name` varchar(20) DEFAULT NULL,
  `last_name` varchar(20) DEFAULT NULL,
  `date_of_birt` date DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `airline_staff`
--

INSERT INTO `airline_staff` (`username`, `user_password`, `first_name`, `last_name`, `date_of_birt`, `phone_number`) VALUES
('Fischer', 'password', 'Jinyu', 'Zhao', '1997-04-02', '13552865605');

-- --------------------------------------------------------

--
-- Table structure for table `airplane`
--

CREATE TABLE `airplane` (
  `airline_name` varchar(20) NOT NULL,
  `ID` char(20) NOT NULL,
  `seats` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `airplane`
--

INSERT INTO `airplane` (`airline_name`, `ID`, `seats`) VALUES
('China Eastern', '233', 600),
('China Eastern', '666', 500);

-- --------------------------------------------------------

--
-- Table structure for table `airport`
--

CREATE TABLE `airport` (
  `name` varchar(20) NOT NULL,
  `city` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `airport`
--

INSERT INTO `airport` (`name`, `city`) VALUES
('JFK', 'New York'),
('PVG', 'Shanghai');

-- --------------------------------------------------------

--
-- Table structure for table `arrival`
--

CREATE TABLE `arrival` (
  `airline_name` varchar(20) NOT NULL,
  `flight_num` varchar(20) NOT NULL,
  `airport_name` varchar(20) NOT NULL,
  `time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `arrival`
--

INSERT INTO `arrival` (`airline_name`, `flight_num`, `airport_name`, `time`) VALUES
('China Eastern', 'MU-2333', 'JFK', '2019-04-30 07:00:00'),
('China Eastern', 'MU-666', 'PVG', '2019-04-30 22:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `booking_agent`
--

CREATE TABLE `booking_agent` (
  `email` varchar(50) NOT NULL,
  `booking_agent_ID` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `commission_30d` int(11) DEFAULT NULL,
  `average_commission` int(11) DEFAULT NULL,
  `total_tickets` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `booking_agent`
--

INSERT INTO `booking_agent` (`email`, `booking_agent_ID`, `password`, `commission_30d`, `average_commission`, `total_tickets`) VALUES
('jz2194@nyu.edu', '6666', 'bossman69', 20000, 200, 200),
('zz@nyu.edu', '8888', 'password', NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `email` varchar(50) NOT NULL,
  `password` varchar(20) NOT NULL,
  `name` varchar(20) DEFAULT NULL,
  `building_num` int(11) DEFAULT NULL,
  `street` varchar(20) DEFAULT NULL,
  `city` varchar(20) DEFAULT NULL,
  `state` varchar(20) DEFAULT NULL,
  `phone_num` varchar(20) DEFAULT NULL,
  `passport_num` varchar(20) DEFAULT NULL,
  `passport_expiration` datetime DEFAULT NULL,
  `passport_country` varchar(20) DEFAULT NULL,
  `date_of_birth` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`email`, `password`, `name`, `building_num`, `street`, `city`, `state`, `phone_num`, `passport_num`, `passport_expiration`, `passport_country`, `date_of_birth`) VALUES
('CaptainAmerica@gmail.com', 'hailhydra', 'Steve Rogers', 310, '3rd Avenue', 'New York City', 'NY', '678-136-7092', 'A1234567', '2025-07-03 00:00:00', 'USA', '1918-07-04 00:00:00'),
('jz2170@nyu.edu', 'lovedaye', 'Jingyi Zhang', 10, 'Tianshan Rd.', 'Lianyungang', 'Jiangsu', '13888866886', 'E88866888', '2026-10-01 00:00:00', 'China', '1998-04-09 00:00:00'),
('yn656@nyu.edu', 'lovesheshe', 'Yibin Ni', 2, 'Yangtai Rd.', 'Shanghai', 'Shanghai', '15921536001', 'E1234567', '2026-08-01 00:00:00', 'China', '1997-05-19 00:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `departure`
--

CREATE TABLE `departure` (
  `airline_name` varchar(20) NOT NULL,
  `flight_num` varchar(20) NOT NULL,
  `airport_name` varchar(20) NOT NULL,
  `time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `departure`
--

INSERT INTO `departure` (`airline_name`, `flight_num`, `airport_name`, `time`) VALUES
('China Eastern', 'MU-2333', 'PVG', '2019-04-29 19:00:00'),
('China Eastern', 'MU-666', 'JFK', '2019-04-30 10:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `employment`
--

CREATE TABLE `employment` (
  `name` varchar(20) DEFAULT NULL,
  `username` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `flight`
--

CREATE TABLE `flight` (
  `airline_name` varchar(20) NOT NULL,
  `flight_num` varchar(20) NOT NULL,
  `base_price` int(5) DEFAULT NULL,
  `airplane_id` varchar(20) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `flight`
--

INSERT INTO `flight` (`airline_name`, `flight_num`, `base_price`, `airplane_id`, `status`) VALUES
('China Eastern', 'MU-2333', 1500, '233', 'delayed'),
('China Eastern', 'MU-666', 3500, '666', 'on-time');

-- --------------------------------------------------------

--
-- Table structure for table `order_info`
--

CREATE TABLE `order_info` (
  `order_ID` varchar(20) NOT NULL,
  `flight_num` varchar(20) DEFAULT NULL,
  `airline_name` varchar(20) DEFAULT NULL,
  `purchase_date_time` datetime DEFAULT NULL,
  `card_exp_date` datetime DEFAULT NULL,
  `name_on_card` varchar(20) DEFAULT NULL,
  `card_num` varchar(20) DEFAULT NULL,
  `card_type` varchar(20) DEFAULT NULL,
  `sold_price` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `order_info`
--

INSERT INTO `order_info` (`order_ID`, `flight_num`, `airline_name`, `purchase_date_time`, `card_exp_date`, `name_on_card`, `card_num`, `card_type`, `sold_price`) VALUES
('0001', 'MU-666', 'China Eastern', '2019-04-11 20:48:01', '2026-08-01 00:00:00', 'Jingyi Zhang', '4392268389918888', 'Visa', 1700);

-- --------------------------------------------------------

--
-- Table structure for table `purchases`
--

CREATE TABLE `purchases` (
  `email` varchar(50) NOT NULL,
  `booking_agent_ID` varchar(20) NOT NULL,
  `order_ID` varchar(20) NOT NULL,
  `ticket_ID` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `purchases`
--

INSERT INTO `purchases` (`email`, `booking_agent_ID`, `order_ID`, `ticket_ID`) VALUES
('jz2170@nyu.edu', '6666', '0001', 'MU-666-1A');

-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

CREATE TABLE `ticket` (
  `ticket_ID` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`ticket_ID`) VALUES
('MU-233-1A'),
('MU-233-1B'),
('MU-666-1A'),
('MU-666-1B'),
('MU-666-1C');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `airline`
--
ALTER TABLE `airline`
  ADD PRIMARY KEY (`name`);

--
-- Indexes for table `airplane`
--
ALTER TABLE `airplane`
  ADD PRIMARY KEY (`airline_name`,`ID`);

--
-- Indexes for table `airport`
--
ALTER TABLE `airport`
  ADD PRIMARY KEY (`name`);

--
-- Indexes for table `arrival`
--
ALTER TABLE `arrival`
  ADD PRIMARY KEY (`airline_name`,`flight_num`,`airport_name`);

--
-- Indexes for table `booking_agent`
--
ALTER TABLE `booking_agent`
  ADD PRIMARY KEY (`email`,`booking_agent_ID`),
  ADD UNIQUE KEY `booking_agent_ID` (`booking_agent_ID`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `departure`
--
ALTER TABLE `departure`
  ADD PRIMARY KEY (`airline_name`,`flight_num`,`airport_name`);

--
-- Indexes for table `flight`
--
ALTER TABLE `flight`
  ADD PRIMARY KEY (`airline_name`,`flight_num`);

--
-- Indexes for table `order_info`
--
ALTER TABLE `order_info`
  ADD PRIMARY KEY (`order_ID`);

--
-- Indexes for table `purchases`
--
ALTER TABLE `purchases`
  ADD PRIMARY KEY (`email`,`booking_agent_ID`,`order_ID`,`ticket_ID`);

--
-- Indexes for table `ticket`
--
ALTER TABLE `ticket`
  ADD PRIMARY KEY (`ticket_ID`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `airplane`
--
ALTER TABLE `airplane`
  ADD CONSTRAINT `airplane_ibfk_1` FOREIGN KEY (`airline_name`) REFERENCES `airline` (`name`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
