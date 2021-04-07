SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+08:00";

--
-- Database: `esd_clinic`
--
CREATE DATABASE IF NOT EXISTS `appointment` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

USE `appointment`;


-- --------------------------------------------------------
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
  `appointment_date` varchar(20) NOT NULL,
  `appointment_time` varchar(9) NOT NULL,
  `did` int(5) DEFAULT NULL,
  `aid` int(11) DEFAULT NULL,
  `doctor_name` varchar(15) DEFAULT NULL,
  `status` varchar(10) NOT NULL DEFAULT 'booked',
  `room_no` varchar(10) NULL,
  PRIMARY KEY (`appointment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `appointment`
--

INSERT INTO `appointment` (`appointment_id`,`NRIC`, `patient_name`,`gender`,`contact_number`,`email`, `appointment_date`, `appointment_time`, `did`,`aid`, `doctor_name`, `status`, `room_no`) VALUES
(1, 'T0123456U', 'Leslie','M','82873618', 'leslie123@gmail.com', '2021-04-09', '1100', NULL , NULL , NULL, 'booked', NULL),
(2, 'T1234567I', 'Reuben','M','83476123', 'reuben234@yahoo.com', '2021-04-09', '1600', NULL , NULL , NULL, 'booked', NULL),
(3, 'S1234567J', 'Jasmine','F','98374986', 'jasmine345@hotmail.com', '2021-04-10', '1000', NULL , NULL , NULL, 'booked', NULL),
(4, 'S9234567I', 'Amelia','F','81097192', 'amelia456@abc.com', '2021-04-11', '1300', NULL , NULL , NULL, 'booked', NULL),
(5, 'S9743227O', 'John','M','98334556', 'john567@xyz.com', '2021-04-09', '1800', NULL , NULL , NULL, 'booked', NULL),
(6, 'T0188492K', 'Kelvin','M','89345782', 'kelvin557@xyz.com', '2021-04-08', '2000', NULL , NULL , NULL, 'booked', NULL),
(7, 'S3445023L', 'Melissa','F','88334569', 'melissa569@xyz.com', '2021-04-12', '1400', NULL , NULL , NULL, 'booked', NULL),
(8, 'S9543245P', 'Jolin','F','93458900', 'jolin234@xyz.com', '2021-04-12', '1600', NULL , NULL , NULL, 'booked', NULL);

COMMIT;





