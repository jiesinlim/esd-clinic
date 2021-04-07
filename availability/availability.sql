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
SET time_zone = "+08:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `esd_clinic`
--
CREATE DATABASE IF NOT EXISTS `availability` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

USE `availability`;

-- --------------------------------------------------------

--
-- Table structure for table `availability`
--

DROP TABLE IF EXISTS `availability`;
CREATE TABLE IF NOT EXISTS `availability` (
  `aid` int(11) NOT NULL AUTO_INCREMENT,
  `did` int(11) NOT NULL,
  `doctor_name` char(26) NOT NULL,
  `date` date NOT NULL,
  `availability` varchar(1000) DEFAULT NULL,
  CONSTRAINT `availability_pk` PRIMARY KEY (`aid`, `did`, `doctor_name`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


--
-- Dumping data for table `availability`
--

INSERT INTO `availability` (`aid`, `did`, `doctor_name`, `date`, `availability`) VALUES
(1, 1, 'Dr. Marcus', '2021-04-08', '0900, 1000, 1100, 1300, 1400, 1500'),
(2, 2, 'Dr. Alan', '2021-04-08', '1600, 1700, 1800, 1900, 2000, 2100'),
(3, 3, 'Dr. Hong Seng', '2021-04-09', '0900, 1000, 1100, 1300, 1400, 1500'),
(4, 4, 'Dr. Strange', '2021-04-09', '1600, 1700, 1800, 1900, 2000, 2100'),
(5, 5, 'Dr. Oz', '2021-04-10', '0900, 1000, 1100, 1300, 1400, 1500'),
(6, 6, 'Dr. Phil', '2021-04-11', '0900, 1000, 1100, 1300, 1400, 1500'),
(7, 3, 'Dr. Hong Seng', '2021-04-12', '0900, 1000, 1100, 1300, 1400, 1500'),
(8, 2, 'Dr. Alan', '2021-04-12', '1600, 1700, 1800, 1900, 2000, 2100');

COMMIT;
-- --------------------------------------------------------