-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 18, 2021 at 05:18 PM
-- Server version: 8.0.18
-- PHP Version: 7.4.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `esd_clinic`
--
CREATE DATABASE IF NOT EXISTS `appointment` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

USE `appointment`;


-- --------------------------------------------------------

--
-- Table structure for table `patient`
--

-- DROP TABLE IF EXISTS `patient`;
-- CREATE TABLE IF NOT EXISTS `patient` (
--   `NRIC` varchar(9) NOT NULL,
--   `patient_name` varchar(15) NOT NULL,
--   `gender` varchar(15) NOT NULL,
--   `contact_number` int(8) NOT NULL,
--   `email` varchar(50) NOT NULL,
--   PRIMARY KEY (`NRIC`)
-- ) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- --
-- -- Dumping data for table `patient`
-- --

-- INSERT INTO `patient` (`NRIC`, `patient_name`, `gender`, `contact_number`, `email`) VALUES
-- ('T0123456U', 'Leslie', 'M', '82873618', 'leslie123@gmail.com'),
-- ('T1234567I', 'Reuben', 'M', '83476123', 'reuben234@yahoo.com'),
-- ('S1234567J', 'Jasmine', 'F', '98374986', 'jasmine345@hotmail.com'),
-- ('J1234567I', 'Amelia', 'F', '81097192', 'amelia456@abc.com'),
-- ('P1234567I', 'Jack', 'M', '98683274', 'jack567@xyz.com');

--
-- Table structure for table `appointment`
--

DROP TABLE IF EXISTS `appointment`;
CREATE TABLE IF NOT EXISTS `appointment` (
  `appointment_id` int(5) NOT NULL AUTO_INCREMENT,
  `NRIC` varchar(9) NOT NULL,
  `patient_name` varchar(15) NOT NULL,
  `gender` varchar(15) NOT NULL,
  `contact_number` int(8) NOT NULL,
  `email` varchar(50) NOT NULL,
  `appointment_date` date NOT NULL,
  `appointment_time` varchar(9) NOT NULL,
  `did` int(5) DEFAULT NULL,
  `aid` int(11) DEFAULT NULL,
  `doctor_name` varchar(15) DEFAULT NULL,
  `status` varchar(10) NOT NULL DEFAULT 'booked',
  `room_no` varchar(10) NULL,
  PRIMARY KEY (`appointment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `appointment`
--

INSERT INTO `appointment` (`appointment_id`,`NRIC`, `patient_name`,`gender`,`contact_number`,`email`, `appointment_date`, `appointment_time`, `did`,`aid`, `doctor_name`, `status`, `room_no`) VALUES
(1, 'T0123456U', 'Leslie','M','82873618', 'leslie123@gmail.com', '2021-03-22', '1200', NULL , NULL , NULL, 'booked', NULL),
(2, 'T1234567I', 'Reuben','M','83476123', 'reuben234@yahoo.com', '2021-03-21', '0900', NULL , NULL , NULL, 'booked', NULL),
(3, 'S1234567J', 'Jasmine','F','98374986', 'jasmine345@hotmail.com', '2021-03-23', '1600', NULL , NULL , NULL, 'booked', NULL),
(4, 'S9234567I', 'Amelia','F','81097192', 'amelia456@abc.com', '2021-03-24', '0900', NULL , NULL , NULL, 'booked', NULL),
(5, 'S8745120I', 'Jack','M','98683274', 'jack567@xyz.com', '2021-03-25', '1100', NULL , NULL , NULL, 'booked', NULL);

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;




