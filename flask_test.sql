-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 10, 2021 at 01:41 PM
-- Server version: 10.4.18-MariaDB
-- PHP Version: 8.0.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `flask_test`
--

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

CREATE TABLE `books` (
  `bookId` int(8) NOT NULL,
  `title` varchar(200) NOT NULL,
  `author` varchar(200) NOT NULL,
  `averageRating` varchar(10) NOT NULL,
  `availableQuantity` int(100) NOT NULL,
  `noOfTimesIssued` int(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `books`
--

INSERT INTO `books` (`bookId`, `title`, `author`, `averageRating`, `availableQuantity`, `noOfTimesIssued`) VALUES
(1226, 'Life of Pi', 'Yann Martel', '3.91', 1, 0),
(2123, 'The 36-Hour Day: A Family Guide to Caring for Persons with Alzheimer Disease  Related Dementing Illnesses  and Memory Loss in Later Life', 'Nancy L. Mace/Peter V. Rabins', '4.24', 0, 0),
(2543, 'Las intermitencias de la muerte', 'José Saramago/Pilar del Río', '4.00', 4, 0),
(2912, 'Escape from Fire Mountain (World of Adventure  #3)', 'Gary Paulsen/Steve Chorney', '3.67', 2, 0),
(8598, 'Eats  Shoots & Leaves: Why  Commas Really Do Make a Difference!', 'Lynne Truss/Bonnie Timmons', '4.15', 1, 0),
(9742, 'The Audacity of Hope: Thoughts on Reclaiming the American Dream', 'Barack Obama', '3.75', 9, 0),
(10767, 'Merde!: The Real French You Were Never Taught at School', 'Geneviève/Michael    Heath', '3.96', 4, 0),
(10970, 'Outlander', 'Matt Keefe', '3.85', 10, 0),
(14258, 'English Passengers', 'Matthew Kneale', '4.06', 2, 0),
(15004, 'First Love: A Gothic Tale', 'Joyce Carol Oates/Barry Moser/Erhan Sunar', '3.19', 5, 0),
(17946, 'Seven Nights', 'Jorge Luis Borges/Eliot Weinberger', '4.33', 8, 0),
(25257, 'Mein Urgroßvater  die Helden und ich', 'James Krüss', '4.30', 10, 0),
(28869, 'Pégate un tiro para sobrevivir: un viaje personal por la América de los mitos', 'Chuck Klosterman', '3.81', 9, 0),
(29680, 'The Coen Brothers: Interviews', 'William Rodney Allen', '3.82', 7, 0),
(32637, 'Imajica: The Reconciliation', 'Clive Barker', '4.42', 6, 0),
(32816, 'The Canterbury Tales: Fifteen Tales and the General Prologue', 'Geoffrey Chaucer/V.A. Kolve/Glending Olson', '3.95', 1, 0),
(33308, 'There\'s No Toilet Paper . . . on the Road Less Traveled: The Best of Travel Humor and Misadventure', 'Doug Lansky', '3.38', 0, 0),
(39763, 'The Mystical Poems of Rumi 1: First Selection  Poems 1-200', 'Rumi/A.J. Arberry', '4.28', 0, 0),
(44145, 'The Bar on the Seine', 'Georges Simenon/David Watson', '3.69', 0, 0),
(44229, 'The Silver Pigs (Marcus Didius Falco  #1)', 'Lindsey Davis', '3.94', 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `members`
--

CREATE TABLE `members` (
  `memberId` int(8) NOT NULL,
  `name` varchar(100) NOT NULL,
  `debt` int(100) NOT NULL,
  `amountPaid` int(100) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `members`
--

INSERT INTO `members` (`memberId`, `name`, `debt`, `amountPaid`) VALUES
(101, 'SWALEHA', 19, 100),
(102, 'KANIZ', 9, 0),
(103, 'FALISHA', 9, 0),
(104, 'ALIZA', 0, 0),
(105, 'KARAN', 8, 50),
(106, 'ARJUN', 0, 0),
(107, 'PRANAY', 7, 101),
(108, 'SALMAN', 0, 0),
(109, 'ASHWINI', 0, 0),
(110, 'GAURI', 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `id` int(8) NOT NULL,
  `bookId` int(8) NOT NULL,
  `memberId` int(8) NOT NULL,
  `issueDate` date NOT NULL,
  `returnDate` date NOT NULL,
  `expectedReturnDate` date NOT NULL,
  `rent` int(100) NOT NULL,
  `totalAmountCollected` int(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `transactions`
--

INSERT INTO `transactions` (`id`, `bookId`, `memberId`, `issueDate`, `returnDate`, `expectedReturnDate`, `rent`, `totalAmountCollected`) VALUES
(3, 1226, 101, '2021-03-21', '2021-01-01', '2021-03-21', 50, 70),
(4, 2543, 102, '2021-03-21', '0000-00-00', '2021-03-31', 50, 1),
(5, 2543, 103, '2021-03-21', '2021-04-09', '2021-03-31', 50, 50),
(6, 1226, 104, '2021-03-23', '0000-00-00', '2021-04-02', 50, 0),
(7, 1226, 105, '2021-03-23', '2021-04-10', '2021-04-02', 50, 50),
(9, 1226, 107, '2021-03-23', '2021-04-10', '2021-04-02', 50, 50),
(11, 2123, 107, '2021-04-10', '2021-04-10', '2021-04-20', 50, 51),
(12, 15004, 102, '2021-04-10', '0000-00-00', '2021-04-20', 50, 0),
(14, 32816, 101, '2021-04-10', '2021-04-10', '2021-04-20', 50, 100);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`bookId`);

--
-- Indexes for table `members`
--
ALTER TABLE `members`
  ADD PRIMARY KEY (`memberId`);

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `bookId_fk` (`bookId`),
  ADD KEY `memberId_fk` (`memberId`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `id` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `transactions`
--
ALTER TABLE `transactions`
  ADD CONSTRAINT `memberId_fk` FOREIGN KEY (`memberId`) REFERENCES `members` (`memberId`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
