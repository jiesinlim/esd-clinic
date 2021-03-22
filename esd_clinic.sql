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
CREATE DATABASE IF NOT EXISTS `esd_clinic` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

USE `esd_clinic`;

-- --------------------------------------------------------

--
-- Table structure for table `doctor`
--

DROP TABLE IF EXISTS `doctor`;
CREATE TABLE IF NOT EXISTS `doctor` (
  `aid` int(11) NOT NULL AUTO_INCREMENT,
  `did` int(11) NOT NULL,
  `name` char(26) NOT NULL,
  `date` date NOT NULL,
  `availability` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`aid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `doctor`
--

INSERT INTO `doctor` (`aid`, `did`, `name`, `date`, `availability`) VALUES
(1, 1, 'Dr. Marcus', '2021-03-21', '0900, 1000, 1100, 1300, 1400, 1500'),
(2, 2, 'Dr. Alan', '2021-03-22', '1200, 1300, 1400, 1500, 1600, 1700'),
(3, 3, 'Dr. Hong Seng', '2021-03-23', '1600, 1700, 1800, 1900, 2000, 2100'),
(4, 4, 'Dr. Strange', '2021-03-24', '0900, 1000, 1500, 1800, 2000, 2100'),
(5, 5, 'Dr. Oz', '2021-03-25', '1100, 1300, 1400, 1900, 2000, 2100'),
(6, 6, 'Dr. Phil', '2021-03-26', '0800, 0900, 1000, 1100, 1200, 1300');

-- --------------------------------------------------------

--
-- Table structure for table `patient`
--

DROP TABLE IF EXISTS `patient`;
CREATE TABLE IF NOT EXISTS `patient` (
  `NRIC` varchar(9) NOT NULL,
  `patient_name` varchar(15) NOT NULL,
  `gender` varchar(15) NOT NULL,
  `contact_number` int(8) NOT NULL,
  `email` varchar(15) NOT NULL,
  PRIMARY KEY (`NRIC`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `patient`
--

INSERT INTO `patient` (`NRIC`, `patient_name`, `gender`, `contact_number`, `email`) VALUES
('T0123456U', 'Leslie', 'M', '82873618', 'leslie123@gmail.com'),
('T1234567I', 'Reuben', 'M', '83476123', 'reuben234@yahoo.com'),
('S1234567J', 'Jasmine', 'F', '98374986', 'jasmine345@hotmail.com'),
('J1234567I', 'Amelia', 'F', '81097192', 'amelia456@abc.com'),
('P1234567I', 'Jack', 'M', '98683274', 'jack567@xyz.com');

--
-- Table structure for table `appointment`
--

DROP TABLE IF EXISTS `appointment`;
CREATE TABLE IF NOT EXISTS `appointment` (
  `aid` int(5) NOT NULL AUTO_INCREMENT,
  `NRIC` varchar(9) NOT NULL,
  `appointment_date` date NOT NULL,
  `appointment_time` varchar(15) NOT NULL,
  `did` int(5) DEFAULT NULL,
  `doctor_name` varchar(15) DEFAULT NULL,
  `status` varchar(10) NOT NULL DEFAULT 'booked',
  `room_no` varchar(10) NULL,
  PRIMARY KEY (`aid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `appointment`
--

INSERT INTO `appointment` (`aid`, `NRIC`, `appointment_date`, `appointment_time`, `did`, `doctor_name`, `status`, `room_no`) VALUES
(1, 'T0123456U', '2021-03-22', '1000', NULL, NULL, 'booked', NULL),
(2, 'T1234567I', '2021-03-21', '1300', NULL, NULL, 'booked', NULL),
(3, 'S1234567J', '2021-03-23', '1500', NULL, NULL, 'booked', NULL),
(4, 'J1234567I', '2021-03-23', '1900', NULL, NULL, 'booked', NULL),
(5, 'P1234567I', '2021-03-22', '1400', NULL, NULL, 'booked', NULL);


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

DROP TABLE IF EXISTS `patientlogin`;
CREATE TABLE IF NOT EXISTS `patientlogin` (
  `Name` char(50),
  `NRIC` varchar(9) NOT NULL,
  PRIMARY KEY (`Name`)
);

INSERT INTO `patientlogin` (`Name`, `NRIC`) VALUES
('Leslie', 'T0123456U'),
('Reuben', 'T1234567I'),
('Jasmine', 'S1234567J'),
('Amelia', 'J1234567I'),
('Jack', 'P1234567I');
COMMIT;



