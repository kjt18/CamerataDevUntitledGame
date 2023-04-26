-- MySQL dump 10.13  Distrib 8.0.29, for Win64 (x86_64)
--
-- Host: capstone-server.mysql.database.azure.com    Database: capstone
-- ------------------------------------------------------
-- Server version	5.7.40-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `accounts`
--

DROP TABLE IF EXISTS `accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(45) NOT NULL,
  `phash` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=83 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts`
--

LOCK TABLES `accounts` WRITE;
/*!40000 ALTER TABLE `accounts` DISABLE KEYS */;
INSERT INTO `accounts` VALUES (62,'test123','$2b$12$hpXZFYIus4xpaFlwfhPtK.ikeFcSKXcasrAELqKnFIDgJYdNoqBHu'),(63,'test1','$2b$12$BosMUKG2P6EtWFLdr71BJOsgjghTqaHMWNThZIXKppmO265z8AM1S'),(64,'jacob1','$2b$12$twYkw8KGjN5DFeagKa/WqOSy6OIF.tVYy8aVJgkm4MDaVaXNJWvda'),(65,'testin123','$2b$12$lKA80ZW8oaRuGq43sCI0AuvLCvAu1QvmSUq6DoA0Exi/68FapDRpC'),(72,'testinglogin1','$2b$12$bG.fbZ1DG1peFShfzOPQ0.E9enG0i1E0Lk4UO3/s3QH/f2RqSDvLy'),(73,'testinglogin2','$2b$12$RhXyt/EBi2qoHVKNGC3v9.yqYnnN8h4bV9GdRrLdJf0sXZ8Bg3t3S'),(74,'flb_test','$2b$12$/2/ohacGLziTtVDH92Y0j.v5iOw1eu3zu8PDXdYlu22iOpLL1u2MC'),(76,'test','$2b$12$XL0PyQEKkDPBV3vsMehTu..jxpexhuqBLsyxalgHTWyaGBnTPeR5a'),(79,'configtest','$2b$12$TkE7uOXxbNP8Vg7bHd3FRevYsApXA7RbMv7Ok8.c3o7m0vrAkg1FK'),(80,'jcaole','$2b$12$9ybXSHZFPiyQ/KI4OhXfOu1l0xM8tZ/w8L1NL99tG19NpUq/n/.5S'),(81,'imregistering','$2b$12$rfstl7hP4XVsfC4R76llq.u9M2nNno379VBKuBCNi0NuqeEyLZX7K'),(82,'register','$2b$12$t4bxdQ/Wx5VOllpBfYWz5.28Q4Tf3N/oipnPpBo0VVGY81w4A6eVq');
/*!40000 ALTER TABLE `accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lobby`
--

DROP TABLE IF EXISTS `lobby`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lobby` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lobby_name` varchar(45) NOT NULL,
  `owner_name` varchar(45) NOT NULL,
  `game_type` varchar(45) NOT NULL,
  `num_players` int(2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `owner_name_idx` (`owner_name`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lobby`
--

LOCK TABLES `lobby` WRITE;
/*!40000 ALTER TABLE `lobby` DISABLE KEYS */;
/*!40000 ALTER TABLE `lobby` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lobby_players`
--

DROP TABLE IF EXISTS `lobby_players`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lobby_players` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lobby_id` int(11) DEFAULT NULL,
  `username` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `lobby_id_idx` (`lobby_id`),
  KEY `username` (`username`),
  CONSTRAINT `lobby_id` FOREIGN KEY (`lobby_id`) REFERENCES `lobby` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lobby_players`
--

LOCK TABLES `lobby_players` WRITE;
/*!40000 ALTER TABLE `lobby_players` DISABLE KEYS */;
/*!40000 ALTER TABLE `lobby_players` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `matchhistory`
--

DROP TABLE IF EXISTS `matchhistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `matchhistory` (
  `matchid` int(11) NOT NULL AUTO_INCREMENT,
  `matchtime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `p1ID` int(11) NOT NULL,
  `p2ID` int(11) NOT NULL,
  `p1Score` int(11) NOT NULL,
  `p2Score` int(11) NOT NULL,
  `Round` int(11) NOT NULL,
  PRIMARY KEY (`matchid`),
  KEY `p1FK_idx` (`p1ID`),
  KEY `p2FK_idx` (`p2ID`),
  CONSTRAINT `p1FK` FOREIGN KEY (`p1ID`) REFERENCES `accounts` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `p2FK` FOREIGN KEY (`p2ID`) REFERENCES `accounts` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `matchhistory`
--

LOCK TABLES `matchhistory` WRITE;
/*!40000 ALTER TABLE `matchhistory` DISABLE KEYS */;
INSERT INTO `matchhistory` VALUES (1,'2023-03-22 17:39:59',62,63,53000,15,1),(2,'2023-03-22 17:39:59',63,64,5700,63000,1),(3,'2023-03-22 17:39:59',65,64,12,13,1),(4,'2023-03-22 17:39:59',65,62,17,16,1),(5,'2023-03-22 17:40:55',63,65,345,987,16),(6,'2023-03-23 22:00:15',62,65,35,865,16),(7,'2023-03-23 22:00:15',62,64,546,865,1),(8,'2023-03-23 22:00:15',62,64,547,457,1),(9,'2023-03-23 22:00:15',63,62,457,57,1),(10,'2023-03-23 22:00:15',62,65,3456,74634,16),(11,'2023-03-23 22:00:15',62,64,35678,5655,1),(12,'2023-03-23 22:00:15',62,64,6689,5555,1),(13,'2023-03-23 22:00:15',63,62,23578,8654,1),(14,'2023-03-23 22:00:15',62,65,11,22,16),(15,'2023-03-23 22:00:15',62,64,33,44,1),(16,'2023-03-23 22:00:15',62,64,55,66,1),(17,'2023-03-23 22:00:15',63,62,77,88,1),(18,'2023-03-23 22:00:15',62,65,999,28882,16),(19,'2023-03-23 22:00:15',62,64,666,777,1),(20,'2023-03-23 22:00:15',62,64,555,444,1),(21,'2023-03-23 22:00:16',63,62,222,333,1),(22,'2023-03-23 22:02:54',62,65,1,1,16);
/*!40000 ALTER TABLE `matchhistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `matchhistoryview`
--

DROP TABLE IF EXISTS `matchhistoryview`;
/*!50001 DROP VIEW IF EXISTS `matchhistoryview`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `matchhistoryview` AS SELECT 
 1 AS `id`,
 1 AS `matchid`,
 1 AS `matchtime`,
 1 AS `Player Name`,
 1 AS `Opponent Name`,
 1 AS `Player Score`,
 1 AS `Opponent Score`,
 1 AS `Round`,
 1 AS `Result`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `playerstatsview`
--

DROP TABLE IF EXISTS `playerstatsview`;
/*!50001 DROP VIEW IF EXISTS `playerstatsview`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `playerstatsview` AS SELECT 
 1 AS `id`,
 1 AS `High Score`,
 1 AS `Highest Round`,
 1 AS `Won`,
 1 AS `Lost`,
 1 AS `Tied`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `sessions`
--

DROP TABLE IF EXISTS `sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sessions` (
  `sid` varchar(255) NOT NULL,
  `data` blob NOT NULL,
  `expiration` datetime NOT NULL,
  PRIMARY KEY (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sessions`
--

LOCK TABLES `sessions` WRITE;
/*!40000 ALTER TABLE `sessions` DISABLE KEYS */;
/*!40000 ALTER TABLE `sessions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_sessions`
--

DROP TABLE IF EXISTS `user_sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_sessions` (
  `user_id` int(11) NOT NULL,
  `session_id` varchar(255) NOT NULL,
  PRIMARY KEY (`user_id`,`session_id`),
  KEY `session_id_idx` (`session_id`),
  CONSTRAINT `session_id` FOREIGN KEY (`session_id`) REFERENCES `sessions` (`sid`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_sessions`
--

LOCK TABLES `user_sessions` WRITE;
/*!40000 ALTER TABLE `user_sessions` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_sessions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'capstone'
--

--
-- Dumping routines for database 'capstone'
--

--
-- Final view structure for view `matchhistoryview`
--

/*!50001 DROP VIEW IF EXISTS `matchhistoryview`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`capstonesa`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `matchhistoryview` AS select `allmatches`.`id` AS `id`,`allmatches`.`matchid` AS `matchid`,`allmatches`.`matchtime` AS `matchtime`,`allmatches`.`Player Name` AS `Player Name`,`allmatches`.`Opponent Name` AS `Opponent Name`,`allmatches`.`Player Score` AS `Player Score`,`allmatches`.`Opponent Score` AS `Opponent Score`,`allmatches`.`Round` AS `Round`,(case when (`allmatches`.`Player Score` > `allmatches`.`Opponent Score`) then 'Won' when (`allmatches`.`Player Score` < `allmatches`.`Opponent Score`) then 'Lost' when (`allmatches`.`Player Score` = `allmatches`.`Opponent Score`) then 'Tied' end) AS `Result` from (select `a`.`id` AS `id`,`m`.`matchid` AS `matchid`,`m`.`matchtime` AS `matchtime`,`a`.`username` AS `Player Name`,`o`.`username` AS `Opponent Name`,`m`.`p2Score` AS `Player Score`,`m`.`p1Score` AS `Opponent Score`,`m`.`Round` AS `Round` from ((`capstone`.`accounts` `a` left join `capstone`.`matchhistory` `m` on((`a`.`id` = `m`.`p2ID`))) join `capstone`.`accounts` `o` on((`o`.`id` = `m`.`p1ID`))) union all select `a`.`id` AS `id`,`m`.`matchid` AS `matchid`,`m`.`matchtime` AS `matchtime`,`a`.`username` AS `Player Name`,`o`.`username` AS `Opponent Name`,`m`.`p1Score` AS `Player Score`,`m`.`p2Score` AS `Opponent Score`,`m`.`Round` AS `Round` from ((`capstone`.`accounts` `a` left join `capstone`.`matchhistory` `m` on((`a`.`id` = `m`.`p1ID`))) join `capstone`.`accounts` `o` on((`o`.`id` = `m`.`p2ID`)))) `allmatches` order by `allmatches`.`matchtime` desc */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `playerstatsview`
--

/*!50001 DROP VIEW IF EXISTS `playerstatsview`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`capstonesa`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `playerstatsview` AS select `tbla`.`id` AS `id`,`tbla`.`High Score` AS `High Score`,`tbla`.`Highest Round` AS `Highest Round`,`tblb`.`Won` AS `Won`,`tblb`.`Lost` AS `Lost`,`tblb`.`Tied` AS `Tied` from (((select `matchhistoryview`.`id` AS `id`,max(`matchhistoryview`.`Player Score`) AS `High Score`,max(`matchhistoryview`.`Round`) AS `Highest Round` from `capstone`.`matchhistoryview` group by `matchhistoryview`.`id`)) `tbla` left join (select `matchhistoryview`.`id` AS `id`,count((case when (`matchhistoryview`.`Player Score` > `matchhistoryview`.`Opponent Score`) then 1 else NULL end)) AS `Won`,count((case when (`matchhistoryview`.`Player Score` < `matchhistoryview`.`Opponent Score`) then 1 else NULL end)) AS `Lost`,count((case when (`matchhistoryview`.`Player Score` = `matchhistoryview`.`Opponent Score`) then 1 else NULL end)) AS `Tied` from `capstone`.`matchhistoryview` group by `matchhistoryview`.`id`) `tblb` on((`tbla`.`id` = `tblb`.`id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-04-26 11:51:49
