-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jan 14, 2019 at 06:42 AM
-- Server version: 5.7.19
-- PHP Version: 7.1.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `book`
--
CREATE DATABASE IF NOT EXISTS `doctor` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `doctor`;

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `doctor`;
CREATE TABLE IF NOT EXISTS `doctor` (
  `did` INT NOT NULL,
  `name` CHAR(26) NOT NULL,
  `date` DATE NOT NULL,
  `availability` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`did`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `doctor`
--

INSERT INTO `doctor` 
(`did`, `name`, `date`, `availability`) VALUES
(1, 'Dr. Marcus', '2021-03-21', '0900, 1000, 1100, 1300, 1400, 1500'),
(2, 'Dr. John', '2021-03-22', '1200, 1300, 1400, 1500, 1600, 1700'),
(3, 'Dr. Kenny', '2021-03-23', '1600, 1700, 1800, 1900, 2000, 2100');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
