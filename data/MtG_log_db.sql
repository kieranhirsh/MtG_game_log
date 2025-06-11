-- MySQL dump 10.13  Distrib 8.0.37, for Linux (x86_64)
--
-- Host: localhost    Database: MtG_log
-- ------------------------------------------------------
-- Server version	8.0.37-0ubuntu0.20.04.3

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Colour_Identities`
--

DROP TABLE IF EXISTS `Colour_Identities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Colour_Identities` (
  `id` varchar(64) NOT NULL,
  `ci_name` varchar(128) NOT NULL,
  `colours` varchar(128) NOT NULL,
  `num_colours` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Colour_Identities`
--

LOCK TABLES `Colour_Identities` WRITE;
/*!40000 ALTER TABLE `Colour_Identities` DISABLE KEYS */;
INSERT INTO `Colour_Identities` VALUES ('018240aa-1533-4c89-9a7e-8f7d57d849a4','Colourless','c',0),('04f42ef3-d4be-45ea-a289-031b7261ab38','Mono-white','w',1),('1447712e-0fb2-4a08-a23e-9345923f3be1','Mono-blue','u',1),('218a0838-cbe1-4308-aabb-8de17cc5873b','Mono-black','b',1),('26842c69-c93d-4ad2-8627-cbe100b600f7','Mono-red','r',1),('302f8628-53b7-44e1-8d77-2aaf65538ba8','Mono-green','g',1),('3256d58c-f465-46ff-94f7-435625da0a3a','Azorius','wu',2),('3b391a97-4c58-4132-8200-68bc2898aef9','Dimir','ub',2),('3de61941-7ac0-4230-aa3b-a8f079e64472','Rakdos','br',2),('532de6fb-59c1-487b-8931-47e70d5cefb2','Gruul','rg',2),('59cb4e07-0520-4b9e-b59c-96088df32978','Selesnya','gw',2),('5d5f6800-e325-4507-a1d5-d8689cd714b9','Orzhov','wb',2),('62eb1f23-0289-46f6-8d3e-ed016a341945','Golgari','bg',2),('702360b8-7181-41a6-b8ac-662eeace3cf2','Simic','gu',2),('71f2e91c-12aa-4358-ae0b-affd4f823cb2','Izzet','ur',2),('7aa24b49-5e15-4fef-8e2a-8f8ee2984cc9','Boros','rw',2),('7c705ad4-f0c3-467e-b480-63a9a809871c','Bant','gwu',3),('7eda5111-5c65-493c-bc32-92a6261ce547','Esper','wub',3),('880393b9-3191-4a6b-a4c5-42f97a659e2c','Grixis','ubr',3),('8a0eed82-6019-46e7-9683-21b622c859b4','Jund','brg',3),('9aa54b57-e5f0-44b6-9c26-09b357a4d54f','Naya','rgw',3),('9fb8539e-2258-4239-bc87-de29d55565e0','Mardu','rwb',3),('a3dec342-cc95-49ec-8dae-4f966da95624','Temur','gur',3),('ad5cec7a-e866-493a-a39c-a0bff8d46eef','Abzan','wbg',3),('b2f7fcf3-ce9f-4898-8d6b-d667de484db2','Jeskai','urw',3),('b5fa6356-25a5-48d5-b2dc-c08a7df6ebe9','Sultai','bgu',3),('b6092dea-04b5-4c40-a089-6d297fb86cfb','Glint-Eye','ubrg',4),('c3daee5a-4ce2-4ccd-bec1-43953ee105c5','Dune-Brood','brgw',4),('cf77b2f2-70ea-432b-8af0-46bfae139e50','Ink-Treader','rgwu',4),('d37e8574-23c4-4dd1-a017-d0b9209bac69','Witch-Maw','gwub',4),('ee1465f8-e828-4a00-baf7-adf39653c678','Yore-Tiller','wubr',4),('ff8bc843-3aa7-4cd4-9db6-c378a69f57b7','Rainbow','wubrg',5);
/*!40000 ALTER TABLE `Colour_Identities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Decks`
--

DROP TABLE IF EXISTS `Decks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Decks` (
  `id` varchar(64) NOT NULL,
  `deck_name` varchar(128) NOT NULL,
  `player_id` varchar(64) NOT NULL,
  `colour_identity_id` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `player_id` (`player_id`),
  KEY `colour_identity_id` (`colour_identity_id`),
  CONSTRAINT `decks_ibfk_1` FOREIGN KEY (`player_id`) REFERENCES `Players` (`id`),
  CONSTRAINT `decks_ibfk_2` FOREIGN KEY (`colour_identity_id`) REFERENCES `Colour_Identities` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Decks`
--

LOCK TABLES `Decks` WRITE;
/*!40000 ALTER TABLE `Decks` DISABLE KEYS */;
INSERT INTO `Decks` VALUES ('0bef737c-68ef-4f15-81e2-49d0477d7e13','Gut / Agent','f73a2cf1-38a2-4ae6-b4d5-ea3c68f10db5','3de61941-7ac0-4230-aa3b-a8f079e64472'),('15dec003-5456-43ea-a6da-cf981333f6a5','Xyris, Hedron Grinder','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26','a3dec342-cc95-49ec-8dae-4f966da95624'),('238370d5-306e-4cde-a891-849b365ee683','Obeka, Brute Chronologist','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26','880393b9-3191-4a6b-a4c5-42f97a659e2c'),('25fa61be-722d-4a60-b7bc-d374310469ac','Bruse, Kamahl Herder','7c847407-d519-479c-99bd-b57d01a98670','9aa54b57-e5f0-44b6-9c26-09b357a4d54f'),('442a348e-0a25-460e-9b1f-0804fb716f93','Extus, suzerain de l\'Oriq','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26','5d5f6800-e325-4507-a1d5-d8689cd714b9'),('4872bbe1-39b7-4b48-b983-bf06f56c660c','Bhaal','7c847407-d519-479c-99bd-b57d01a98670','8a0eed82-6019-46e7-9683-21b622c859b4'),('49f2b076-a321-4123-92b5-ab2e81a5f451','Atraxa, Unifier','18f2bada-2f3c-419e-921c-0fac96324e41','d37e8574-23c4-4dd1-a017-d0b9209bac69'),('55966c99-36e5-48a1-855c-227d114223b3','Raffine','f73a2cf1-38a2-4ae6-b4d5-ea3c68f10db5','7eda5111-5c65-493c-bc32-92a6261ce547'),('59f538d7-3159-41bf-884a-49010663c67a','Rashmi & Ragavan','7c847407-d519-479c-99bd-b57d01a98670','a3dec342-cc95-49ec-8dae-4f966da95624'),('66c75202-6a2b-45cc-b4d4-08585053e0ef','Réveiller l\'Avatar de sang','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26','3de61941-7ac0-4230-aa3b-a8f079e64472'),('69393a02-7e5c-499f-8005-108740dee92f','General Ferrous Rokiric','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26','7aa24b49-5e15-4fef-8e2a-8f8ee2984cc9'),('77fc2f5f-4551-484c-9551-e493f4828747','Nethroi, Apex of Death','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26','ad5cec7a-e866-493a-a39c-a0bff8d46eef'),('839b690f-adcf-4901-92d1-1e87ea6393cc','Myrel','18f2bada-2f3c-419e-921c-0fac96324e41','04f42ef3-d4be-45ea-a289-031b7261ab38'),('8ad26608-ed95-4b9e-ab80-e8b2b1a5ed11','Ratadrabik of Urborg','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26','5d5f6800-e325-4507-a1d5-d8689cd714b9'),('8fa9c10a-9a9a-4c75-bdd7-cc95d9591850','Michael, Bone Manager','7c847407-d519-479c-99bd-b57d01a98670','ad5cec7a-e866-493a-a39c-a0bff8d46eef'),('96ab08e8-30b2-4252-afac-8192840aa7fa','Zedruü au Grandcœur','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26','b2f7fcf3-ce9f-4898-8d6b-d667de484db2'),('b008d2cb-fd63-4530-bab9-e4944bfae79f','Valgavoth, Harrower','18f2bada-2f3c-419e-921c-0fac96324e41','3de61941-7ac0-4230-aa3b-a8f079e64472'),('b1258ee1-fd42-4100-8dbe-911669dee69b','Soul of Lord Windgrace','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26','8a0eed82-6019-46e7-9683-21b622c859b4'),('b3d362cf-bf31-4826-8056-adfec5fac8a4','Giada','f73a2cf1-38a2-4ae6-b4d5-ea3c68f10db5','04f42ef3-d4be-45ea-a289-031b7261ab38'),('b6b1cfef-78e4-4fff-a30a-15bad0280f2b','Isshin','18f2bada-2f3c-419e-921c-0fac96324e41','9fb8539e-2258-4239-bc87-de29d55565e0'),('b7eebdbf-6687-46b5-877e-db9365f0bd5d','Niv-Mizzet revenu à la vie','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26','ff8bc843-3aa7-4cd4-9db6-c378a69f57b7'),('ca12ce09-d714-44dd-82c1-89dc2de5e9c1','Atraxa, voix des praetors','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26','d37e8574-23c4-4dd1-a017-d0b9209bac69'),('ce3adffa-6113-48f4-baa2-ade8b4f312bf','Lotho','f73a2cf1-38a2-4ae6-b4d5-ea3c68f10db5','5d5f6800-e325-4507-a1d5-d8689cd714b9'),('d166c651-2f14-4c54-a28d-bcb6990f8772','Imodane','f73a2cf1-38a2-4ae6-b4d5-ea3c68f10db5','26842c69-c93d-4ad2-8627-cbe100b600f7'),('eba29714-2b90-46df-bedb-03208008e068','Atraxa, Voice','18f2bada-2f3c-419e-921c-0fac96324e41','d37e8574-23c4-4dd1-a017-d0b9209bac69'),('f52e8e9d-cb1e-45fe-bd4b-8f95dc217e6c','Aesi','7c847407-d519-479c-99bd-b57d01a98670','702360b8-7181-41a6-b8ac-662eeace3cf2'),('f76b4c40-3f06-4638-8053-5f1d96517fe7','Zaxara, the Exemplary','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26','b5fa6356-25a5-48d5-b2dc-c08a7df6ebe9');
/*!40000 ALTER TABLE `Decks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Games`
--

DROP TABLE IF EXISTS `Games`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Games` (
  `id` varchar(64) NOT NULL,
  `game_name` varchar(1024) DEFAULT NULL,
  `month` varchar(16) DEFAULT NULL,
  `year` int DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `game_time` varchar(64) DEFAULT NULL,
  `winning_deck_id` varchar(64) DEFAULT NULL,
  `winning_player_id` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `games_ibfk_1` (`winning_deck_id`),
  KEY `games_ibfk_2` (`winning_player_id`),
  CONSTRAINT `games_ibfk_1` FOREIGN KEY (`winning_deck_id`) REFERENCES `Decks` (`id`),
  CONSTRAINT `games_ibfk_2` FOREIGN KEY (`winning_player_id`) REFERENCES `Players` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Games`
--

LOCK TABLES `Games` WRITE;
/*!40000 ALTER TABLE `Games` DISABLE KEYS */;
INSERT INTO `Games` VALUES ('815f4404-cebc-4885-9222-6d1d4784f8c2','2025-05-30 19:35 - 20:14','May',2025,'2025-05-30 19:35:00','2025-05-30 20:14:00','0:39:00','ce3adffa-6113-48f4-baa2-ade8b4f312bf','f73a2cf1-38a2-4ae6-b4d5-ea3c68f10db5'),('991e0ee3-c5fa-4cc5-943b-4de3e6ed8505','2025-05-30 18:51 - 19:28','May',2025,'2025-05-30 18:51:00','2025-05-30 19:28:00','0:37:00','d166c651-2f14-4c54-a28d-bcb6990f8772','f73a2cf1-38a2-4ae6-b4d5-ea3c68f10db5'),('b0947f69-f401-42b0-93d6-951dab5c6e84','2025-05-30 21:13 - 22:13','May',2025,'2025-05-30 21:13:00','2025-05-30 22:13:00','1:00:00','b6b1cfef-78e4-4fff-a30a-15bad0280f2b','18f2bada-2f3c-419e-921c-0fac96324e41'),('c9924d51-69e4-4ad8-8d2c-491f5b039fbb','2025-05-30 17:36 - 18:41','May',2025,'2025-05-30 17:36:00','2025-05-30 18:41:00','1:05:00','8fa9c10a-9a9a-4c75-bdd7-cc95d9591850','7c847407-d519-479c-99bd-b57d01a98670'),('fd0a1582-ef87-4a4c-9530-7dfa8f6237f5','2025-05-30 20:20 - 21:07','May',2025,'2025-05-30 20:20:00','2025-05-30 21:07:00','0:47:00','b008d2cb-fd63-4530-bab9-e4944bfae79f','18f2bada-2f3c-419e-921c-0fac96324e41');
/*!40000 ALTER TABLE `Games` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Players`
--

DROP TABLE IF EXISTS `Players`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Players` (
  `id` varchar(64) NOT NULL,
  `player_name` varchar(128) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Players`
--

LOCK TABLES `Players` WRITE;
/*!40000 ALTER TABLE `Players` DISABLE KEYS */;
INSERT INTO `Players` VALUES ('18f2bada-2f3c-419e-921c-0fac96324e41','Jay F'),('7c847407-d519-479c-99bd-b57d01a98670','Arik H'),('bcdc66af-d20f-42e0-8bc2-21fee1c7ec26','Kieran H'),('f73a2cf1-38a2-4ae6-b4d5-ea3c68f10db5','Cyrus T');
/*!40000 ALTER TABLE `Players` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Seats`
--

DROP TABLE IF EXISTS `Seats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Seats` (
  `id` varchar(64) NOT NULL,
  `seat_no` int NOT NULL,
  `ko_turn` int DEFAULT NULL,
  `deck_id` varchar(64) NOT NULL,
  `game_id` varchar(64) NOT NULL,
  `player_id` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `deck_id` (`deck_id`),
  KEY `game_id` (`game_id`),
  KEY `player_id` (`player_id`),
  CONSTRAINT `seats_ibfk_1` FOREIGN KEY (`deck_id`) REFERENCES `Decks` (`id`),
  CONSTRAINT `seats_ibfk_2` FOREIGN KEY (`game_id`) REFERENCES `Games` (`id`),
  CONSTRAINT `seats_ibfk_3` FOREIGN KEY (`player_id`) REFERENCES `Players` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Seats`
--

LOCK TABLES `Seats` WRITE;
/*!40000 ALTER TABLE `Seats` DISABLE KEYS */;
INSERT INTO `Seats` VALUES ('0761a3ef-fba2-45e2-a0f5-67b7031849dc',4,NULL,'ce3adffa-6113-48f4-baa2-ade8b4f312bf','815f4404-cebc-4885-9222-6d1d4784f8c2','f73a2cf1-38a2-4ae6-b4d5-ea3c68f10db5'),('164e724f-6001-4c09-99b8-94bbe67e4659',4,7,'66c75202-6a2b-45cc-b4d4-08585053e0ef','fd0a1582-ef87-4a4c-9530-7dfa8f6237f5','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26'),('2ac3b644-7864-4c90-9ca7-f2f1536f63e5',1,7,'442a348e-0a25-460e-9b1f-0804fb716f93','815f4404-cebc-4885-9222-6d1d4784f8c2','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26'),('2cf0f241-462a-418e-85ac-60397a13917e',3,NULL,'b6b1cfef-78e4-4fff-a30a-15bad0280f2b','b0947f69-f401-42b0-93d6-951dab5c6e84','18f2bada-2f3c-419e-921c-0fac96324e41'),('2eb8add3-681c-458d-aa8b-9833ee22dc8f',3,7,'b1258ee1-fd42-4100-8dbe-911669dee69b','991e0ee3-c5fa-4cc5-943b-4de3e6ed8505','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26'),('2f04eecf-d75c-4f81-8442-e6e98c5db775',2,NULL,'8fa9c10a-9a9a-4c75-bdd7-cc95d9591850','c9924d51-69e4-4ad8-8d2c-491f5b039fbb','7c847407-d519-479c-99bd-b57d01a98670'),('4186f147-77cc-4218-ae51-b3abec9ec2b9',1,7,'839b690f-adcf-4901-92d1-1e87ea6393cc','991e0ee3-c5fa-4cc5-943b-4de3e6ed8505','18f2bada-2f3c-419e-921c-0fac96324e41'),('52e12f1c-670c-45ce-92ab-a0fc68a236d8',2,7,'4872bbe1-39b7-4b48-b983-bf06f56c660c','815f4404-cebc-4885-9222-6d1d4784f8c2','7c847407-d519-479c-99bd-b57d01a98670'),('67c1a4d5-fa1c-4b45-bcd2-d3c6a9ad13c7',4,10,'b3d362cf-bf31-4826-8056-adfec5fac8a4','c9924d51-69e4-4ad8-8d2c-491f5b039fbb','f73a2cf1-38a2-4ae6-b4d5-ea3c68f10db5'),('70a18ffd-9eae-43e8-8ceb-986d74bb4ae0',1,9,'69393a02-7e5c-499f-8005-108740dee92f','b0947f69-f401-42b0-93d6-951dab5c6e84','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26'),('7307f2db-6864-499b-9af4-7ac468f5b5e0',2,NULL,'b008d2cb-fd63-4530-bab9-e4944bfae79f','fd0a1582-ef87-4a4c-9530-7dfa8f6237f5','18f2bada-2f3c-419e-921c-0fac96324e41'),('826e5801-baf5-471f-a801-632977463e7c',2,7,'f52e8e9d-cb1e-45fe-bd4b-8f95dc217e6c','b0947f69-f401-42b0-93d6-951dab5c6e84','7c847407-d519-479c-99bd-b57d01a98670'),('89dc3819-bcaf-45df-bd9f-0c1d5753b728',4,9,'0bef737c-68ef-4f15-81e2-49d0477d7e13','b0947f69-f401-42b0-93d6-951dab5c6e84','f73a2cf1-38a2-4ae6-b4d5-ea3c68f10db5'),('8aa514c7-0f6e-44f4-b389-56e3f01610cc',1,7,'25fa61be-722d-4a60-b7bc-d374310469ac','fd0a1582-ef87-4a4c-9530-7dfa8f6237f5','7c847407-d519-479c-99bd-b57d01a98670'),('97c0721d-beb3-49c9-82ad-0137978068fe',2,NULL,'d166c651-2f14-4c54-a28d-bcb6990f8772','991e0ee3-c5fa-4cc5-943b-4de3e6ed8505','f73a2cf1-38a2-4ae6-b4d5-ea3c68f10db5'),('9d8a81dd-3d98-4a94-99f8-c244c412fabb',4,7,'59f538d7-3159-41bf-884a-49010663c67a','991e0ee3-c5fa-4cc5-943b-4de3e6ed8505','7c847407-d519-479c-99bd-b57d01a98670'),('9f3a20c5-b9c9-416f-8c41-1cb566190c23',3,7,'55966c99-36e5-48a1-855c-227d114223b3','fd0a1582-ef87-4a4c-9530-7dfa8f6237f5','f73a2cf1-38a2-4ae6-b4d5-ea3c68f10db5'),('c4d3fcb3-2302-4d62-9394-65385b2763b3',3,10,'49f2b076-a321-4123-92b5-ab2e81a5f451','c9924d51-69e4-4ad8-8d2c-491f5b039fbb','18f2bada-2f3c-419e-921c-0fac96324e41'),('f0c05367-4874-42b1-95e4-fec0c13ff7a6',1,10,'8ad26608-ed95-4b9e-ab80-e8b2b1a5ed11','c9924d51-69e4-4ad8-8d2c-491f5b039fbb','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26'),('f76af721-ff8f-443a-b509-f05c73291248',3,7,'eba29714-2b90-46df-bedb-03208008e068','815f4404-cebc-4885-9222-6d1d4784f8c2','18f2bada-2f3c-419e-921c-0fac96324e41');
/*!40000 ALTER TABLE `Seats` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-12  1:26:16
