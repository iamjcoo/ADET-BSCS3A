-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 04, 2024 at 04:12 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `adet`
--

-- --------------------------------------------------------

--
-- Table structure for table `adet_user`
--

CREATE TABLE `adet_user` (
  `ID` int(11) NOT NULL,
  `FirstName` varchar(50) NOT NULL,
  `MiddleName` varchar(50) NOT NULL,
  `LastName` varchar(50) NOT NULL,
  `ContactNumber` varchar(11) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `Address` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `adet_user`
--

INSERT INTO `adet_user` (`ID`, `FirstName`, `MiddleName`, `LastName`, `ContactNumber`, `Email`, `Password`, `Address`) VALUES
(1, 'Jayp', 'Surara', 'Bazar', '09123456789', 'jabazar@my.cspc.edu.ph', 'b03ddf3ca2e714a6548e7495e2a03f5e824eaac9837cd7f159c67b90fb4b7342', 'Naga City, Camarines Sur');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `adet_user`
--
ALTER TABLE `adet_user`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `adet_user`
--
ALTER TABLE `adet_user`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
