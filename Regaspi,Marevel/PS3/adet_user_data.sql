-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: adet
-- ------------------------------------------------------
-- Server version	10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `adet_user`
--

DROP TABLE IF EXISTS `adet_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `adet_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) NOT NULL,
  `middle_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) NOT NULL,
  `contact_number` varchar(15) NOT NULL,
  `email_address` varchar(100) NOT NULL,
  `address` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adet_user`
--

LOCK TABLES `adet_user` WRITE;
/*!40000 ALTER TABLE `adet_user` DISABLE KEYS */;
INSERT INTO `adet_user` VALUES (1,'Marevel','Abinal','Regaspi','09301840869','regaspimarevel@gmail.com','Zone 3, Bustrac Nabua Camarines Sur'),(2,'Marevel','Abinal','Regaspi','09301840869','regaspimarevel@gmail.com','Zone 3, bustrac nabua camarines sur'),(3,'Kate','Cabigayan','Balang','09890976578','balangjerson@gmail.com','Zone 2, Bustrac Nabua Camarines Sur'),(4,'John','Doe','Smith','12345678901','john.doe@example.com','123 Main St, City, Country'),(5,'Kate','Cabigayan','Balang','09890976578','balangjerson@gmail.com','Zone 2, Bustrac Nabua Camarines Sur'),(6,'Kate','Cabigayan','Balang','09890976578','balangjerson@gmail.com','Zone 2, Bustrac Nabua Camarines Sur'),(7,'Marevel','Abinal','Regaspi','09301840869','regaspimarevel@gmail.com','Zone 3, bustrac nabua camarines sur'),(8,'Marevel','Abinal','Regaspi','09301840869','regaspimarevel@gmail.com','Zone 3, bustrac nabua camarines sur'),(9,'Marevel','Abinal','Regaspi','09301840869','regaspimarevel@gmail.com','Zone 3, bustrac nabua camarines sur'),(10,'Kate','Cabigayan','Balang','09890976578','balangjerson@gmail.com','Zone 2, Bustrac Nabua Camarines Sur'),(11,'Marevel','Abinal','Regaspi','09301840869','regaspimarevel@gmail.com','Zone 3, bustrac nabua camarines sur'),(12,'Marevel','Abinal','Regaspi','09301840869','regaspimarevel@gmail.com','Zone 3, bustrac nabua camarines sur'),(13,'Marevel','Abinal','Regaspi','09301840869','regaspimarevel@gmail.com','Zone 3, bustrac nabua camarines sur'),(14,'Marevel','Abinal','Regaspi','09301840869','regaspimarevel@gmail.com','Zone 3, bustrac nabua camarines sur'),(15,'Jose','Abinal','Regaspi','09301840869','regaspimarevel@gmail.com','Zone 3, bustrac nabua camarines sur'),(16,'Gina','Abinal','Arbaja','09301840869','regaspimarevel@gmail.com','Zone 3, bustrac nabua camarines sur'),(17,'Chiry','Llaban','Azon','09876875462','chiryazon@gmail.com','Zone 3, Bustrac Nabua Camarines Sur'),(18,'Gina','Salles','Arbaja','09301840869','ginaarbaja@gmail.com','Zone 2, Bustrac Nabua Camarines Sur'),(19,'James','Abinal','Abanes','09301840869','jamesabanes@gmail.com','Zone 5, Bustrac Nabua Camarines Sur'),(20,'James','Abinal','Abanes','09301840869','jamesabanes@gmail.com','Zone 5, Bustrac Nabua Camarines Sur'),(21,'James','Abinal','Abanes','09301840869','jamesabanes@gmail.com','Zone 5, Bustrac Nabua Camarines Sur');
/*!40000 ALTER TABLE `adet_user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-09-29 20:01:14
