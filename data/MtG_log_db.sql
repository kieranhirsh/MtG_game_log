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
-- Table structure for table `colour_identities`
--

DROP TABLE IF EXISTS `colour_identities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `colour_identities` (
  `id` varchar(64) NOT NULL,
  `ci_name` varchar(128) NOT NULL,
  `colours` varchar(128) NOT NULL,
  `num_colours` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `colour_identities`
--

LOCK TABLES `colour_identities` WRITE;
/*!40000 ALTER TABLE `colour_identities` DISABLE KEYS */;
INSERT INTO `colour_identities` VALUES ('018240aa-1533-4c89-9a7e-8f7d57d849a4','Colourless','c',0),('04f42ef3-d4be-45ea-a289-031b7261ab38','Mono-white','w',1),('1447712e-0fb2-4a08-a23e-9345923f3be1','Mono-blue','u',1),('218a0838-cbe1-4308-aabb-8de17cc5873b','Mono-black','b',1),('26842c69-c93d-4ad2-8627-cbe100b600f7','Mono-red','r',1),('302f8628-53b7-44e1-8d77-2aaf65538ba8','Mono-green','g',1),('3256d58c-f465-46ff-94f7-435625da0a3a','Azorius','wu',2),('3b391a97-4c58-4132-8200-68bc2898aef9','Dimir','ub',2),('3de61941-7ac0-4230-aa3b-a8f079e64472','Rakdos','br',2),('532de6fb-59c1-487b-8931-47e70d5cefb2','Gruul','rg',2),('59cb4e07-0520-4b9e-b59c-96088df32978','Selesnya','gw',2),('5d5f6800-e325-4507-a1d5-d8689cd714b9','Orzhov','wb',2),('62eb1f23-0289-46f6-8d3e-ed016a341945','Golgari','bg',2),('702360b8-7181-41a6-b8ac-662eeace3cf2','Simic','gu',2),('71f2e91c-12aa-4358-ae0b-affd4f823cb2','Izzet','ur',2),('7aa24b49-5e15-4fef-8e2a-8f8ee2984cc9','Boros','rw',2),('7c705ad4-f0c3-467e-b480-63a9a809871c','Bant','gwu',3),('7eda5111-5c65-493c-bc32-92a6261ce547','Esper','wub',3),('880393b9-3191-4a6b-a4c5-42f97a659e2c','Grixis','ubr',3),('8a0eed82-6019-46e7-9683-21b622c859b4','Jund','brg',3),('9aa54b57-e5f0-44b6-9c26-09b357a4d54f','Naya','rgw',3),('9fb8539e-2258-4239-bc87-de29d55565e0','Mardu','rwb',3),('a3dec342-cc95-49ec-8dae-4f966da95624','Temur','gur',3),('ad5cec7a-e866-493a-a39c-a0bff8d46eef','Abzan','wbg',3),('b2f7fcf3-ce9f-4898-8d6b-d667de484db2','Jeskai','urw',3),('b5fa6356-25a5-48d5-b2dc-c08a7df6ebe9','Sultai','bgu',3),('b6092dea-04b5-4c40-a089-6d297fb86cfb','Glint-Eye','ubrg',4),('c3daee5a-4ce2-4ccd-bec1-43953ee105c5','Dune-Brood','brgw',4),('cf77b2f2-70ea-432b-8af0-46bfae139e50','Ink-Treader','rgwu',4),('d37e8574-23c4-4dd1-a017-d0b9209bac69','Witch-Maw','gwub',4),('ee1465f8-e828-4a00-baf7-adf39653c678','Yore-Tiller','wubr',4),('ff8bc843-3aa7-4cd4-9db6-c378a69f57b7','Rainbow','wubrg',5);
/*!40000 ALTER TABLE `colour_identities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `decks`
--

DROP TABLE IF EXISTS `decks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `decks` (
  `id` varchar(64) NOT NULL,
  `deck_name` varchar(128) NOT NULL,
  `player_id` varchar(64) NOT NULL,
  `colour_identity_id` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `player_id` (`player_id`),
  KEY `colour_identity_id` (`colour_identity_id`),
  CONSTRAINT `decks_ibfk_1` FOREIGN KEY (`player_id`) REFERENCES `Players` (`id`),
  CONSTRAINT `decks_ibfk_2` FOREIGN KEY (`colour_identity_id`) REFERENCES `colour_identities` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `decks`
--

LOCK TABLES `decks` WRITE;
/*!40000 ALTER TABLE `decks` DISABLE KEYS */;
INSERT INTO `decks` VALUES ('07e23f42-63ec-4c82-9ecf-4cf07ce8c901','Slimefoot & Squee','31c2bb6a-1161-4981-98ef-ca9d4cc302c6','8a0eed82-6019-46e7-9683-21b622c859b4'),('0bef737c-68ef-4f15-81e2-49d0477d7e13','Gut / Agent of the Iron Throne','f73a2cf1-38a2-4ae6-b4d5-ea3c68f10db5','3de61941-7ac0-4230-aa3b-a8f079e64472'),('0d79e631-f0fa-4f96-9b4b-0c6567c41403','Lonis, Cryptozoologist','31c2bb6a-1161-4981-98ef-ca9d4cc302c6','702360b8-7181-41a6-b8ac-662eeace3cf2'),('15dec003-5456-43ea-a6da-cf981333f6a5','Xyris, Hedron Grinder','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26','a3dec342-cc95-49ec-8dae-4f966da95624'),('1d60ad87-e35e-43b7-8885-21797d13f593','Imskir Iron-Eater','9f16663c-f653-471a-8bb3-b4eb26524b67','3de61941-7ac0-4230-aa3b-a8f079e64472'),('220d4a83-9cc0-418a-9b38-5f81de40edfb','Omnath, Locus of the Roil','494925c2-0147-4381-9b5d-eb1b15622f73','a3dec342-cc95-49ec-8dae-4f966da95624'),('238370d5-306e-4cde-a891-849b365ee683','Obeka, Brute Chronologist','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26','880393b9-3191-4a6b-a4c5-42f97a659e2c'),('258758eb-a829-4b20-8939-3f6bf8593326','Satya, Aetherflux Genius','494925c2-0147-4381-9b5d-eb1b15622f73','b2f7fcf3-ce9f-4898-8d6b-d667de484db2'),('25fa61be-722d-4a60-b7bc-d374310469ac','Bruse, Kamahl Herder','7c847407-d519-479c-99bd-b57d01a98670','9aa54b57-e5f0-44b6-9c26-09b357a4d54f'),('38265ce2-f73d-4d47-bac2-59dd855e3c06','Atraxa, Praetors\' Voice','be1d79dd-b907-4fcc-8ead-1bd50eb01571','d37e8574-23c4-4dd1-a017-d0b9209bac69'),('442a348e-0a25-460e-9b1f-0804fb716f93','Extus, suzerain de l\'Oriq','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26','5d5f6800-e325-4507-a1d5-d8689cd714b9'),('4872bbe1-39b7-4b48-b983-bf06f56c660c','Bhaal','7c847407-d519-479c-99bd-b57d01a98670','8a0eed82-6019-46e7-9683-21b622c859b4'),('48991208-3f7e-4821-b37b-ed13839ce3a6','Esika, Tree','bcd17dd0-e430-40b5-954f-9a7289a8bac7','ff8bc843-3aa7-4cd4-9db6-c378a69f57b7'),('49f2b076-a321-4123-92b5-ab2e81a5f451','Atraxa, Unifier','18f2bada-2f3c-419e-921c-0fac96324e41','d37e8574-23c4-4dd1-a017-d0b9209bac69'),('55966c99-36e5-48a1-855c-227d114223b3','Raffine','f73a2cf1-38a2-4ae6-b4d5-ea3c68f10db5','7eda5111-5c65-493c-bc32-92a6261ce547'),('59f538d7-3159-41bf-884a-49010663c67a','Rashmi & Ragavan','7c847407-d519-479c-99bd-b57d01a98670','a3dec342-cc95-49ec-8dae-4f966da95624'),('6408be34-d9f2-45ff-81cf-9c9f97ff16b1','Big Booty Beaches','7d5d6490-bb57-4a6d-a268-92c6d0fc6d43','3256d58c-f465-46ff-94f7-435625da0a3a'),('64643a32-3b11-4d3c-9746-1f9d6edab87e','Eligeth / Esior','f73a2cf1-38a2-4ae6-b4d5-ea3c68f10db5','1447712e-0fb2-4a08-a23e-9345923f3be1'),('66c75202-6a2b-45cc-b4d4-08585053e0ef','Réveiller l\'Avatar de sang','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26','3de61941-7ac0-4230-aa3b-a8f079e64472'),('69393a02-7e5c-499f-8005-108740dee92f','General Ferrous Rokiric','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26','7aa24b49-5e15-4fef-8e2a-8f8ee2984cc9'),('6c30333c-1ef4-4a96-9af2-537edfda94b1','Kodama of the West Tree','be1d79dd-b907-4fcc-8ead-1bd50eb01571','302f8628-53b7-44e1-8d77-2aaf65538ba8'),('70e716a9-a879-4372-8543-a119900ec96c','Zimone, Mystery Unraveler','9f16663c-f653-471a-8bb3-b4eb26524b67','702360b8-7181-41a6-b8ac-662eeace3cf2'),('77fc2f5f-4551-484c-9551-e493f4828747','Nethroi, Apex of Death','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26','ad5cec7a-e866-493a-a39c-a0bff8d46eef'),('786adef8-fff7-441c-a4de-6eab07fdacd7','Belbe, Corrupted Observer','bcd17dd0-e430-40b5-954f-9a7289a8bac7','62eb1f23-0289-46f6-8d3e-ed016a341945'),('839b690f-adcf-4901-92d1-1e87ea6393cc','Myrel','18f2bada-2f3c-419e-921c-0fac96324e41','04f42ef3-d4be-45ea-a289-031b7261ab38'),('8ad26608-ed95-4b9e-ab80-e8b2b1a5ed11','Ratadrabik of Urborg','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26','5d5f6800-e325-4507-a1d5-d8689cd714b9'),('8eb54151-0939-43e5-a433-defea8048355','Zur, Eternal Schemer','494925c2-0147-4381-9b5d-eb1b15622f73','7eda5111-5c65-493c-bc32-92a6261ce547'),('8fa9c10a-9a9a-4c75-bdd7-cc95d9591850','Michael, Bone Manager','7c847407-d519-479c-99bd-b57d01a98670','ad5cec7a-e866-493a-a39c-a0bff8d46eef'),('906b4c5d-123c-428b-a7e2-91c75f731d75','Ojer Kaslem, Deepest Growth','f73a2cf1-38a2-4ae6-b4d5-ea3c68f10db5','302f8628-53b7-44e1-8d77-2aaf65538ba8'),('913ce649-0495-4197-9aa4-aeb49bfa25d4','Kozilek, Butcher of Truth','be1d79dd-b907-4fcc-8ead-1bd50eb01571','018240aa-1533-4c89-9a7e-8f7d57d849a4'),('96ab08e8-30b2-4252-afac-8192840aa7fa','Zedruü au Grandcœur','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26','b2f7fcf3-ce9f-4898-8d6b-d667de484db2'),('b008d2cb-fd63-4530-bab9-e4944bfae79f','Valgavoth, Harrower','18f2bada-2f3c-419e-921c-0fac96324e41','3de61941-7ac0-4230-aa3b-a8f079e64472'),('b1258ee1-fd42-4100-8dbe-911669dee69b','Soul of Lord Windgrace','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26','8a0eed82-6019-46e7-9683-21b622c859b4'),('b3d362cf-bf31-4826-8056-adfec5fac8a4','Giada','f73a2cf1-38a2-4ae6-b4d5-ea3c68f10db5','04f42ef3-d4be-45ea-a289-031b7261ab38'),('b6b1cfef-78e4-4fff-a30a-15bad0280f2b','Isshin','18f2bada-2f3c-419e-921c-0fac96324e41','9fb8539e-2258-4239-bc87-de29d55565e0'),('b7eebdbf-6687-46b5-877e-db9365f0bd5d','Niv-Mizzet revenu à la vie','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26','ff8bc843-3aa7-4cd4-9db6-c378a69f57b7'),('c1c7dc9b-4223-4172-a82f-1fe434305cf8','Lord of the Nazgûl','f73a2cf1-38a2-4ae6-b4d5-ea3c68f10db5','3b391a97-4c58-4132-8200-68bc2898aef9'),('ca12ce09-d714-44dd-82c1-89dc2de5e9c1','Atraxa, voix des praetors','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26','d37e8574-23c4-4dd1-a017-d0b9209bac69'),('ce3adffa-6113-48f4-baa2-ade8b4f312bf','Lotho','f73a2cf1-38a2-4ae6-b4d5-ea3c68f10db5','5d5f6800-e325-4507-a1d5-d8689cd714b9'),('d166c651-2f14-4c54-a28d-bcb6990f8772','Imodane','f73a2cf1-38a2-4ae6-b4d5-ea3c68f10db5','26842c69-c93d-4ad2-8627-cbe100b600f7'),('d9e2a41f-6f60-4ec0-a45a-9595cc725536','Yawgmoth, Thran Physician','7d5d6490-bb57-4a6d-a268-92c6d0fc6d43','218a0838-cbe1-4308-aabb-8de17cc5873b'),('e527deb5-3666-4385-a3ef-f3ae959e20ea','Nekusar, the Mindrazer','494925c2-0147-4381-9b5d-eb1b15622f73','880393b9-3191-4a6b-a4c5-42f97a659e2c'),('eba29714-2b90-46df-bedb-03208008e068','Atraxa, Voice','18f2bada-2f3c-419e-921c-0fac96324e41','d37e8574-23c4-4dd1-a017-d0b9209bac69'),('f52e8e9d-cb1e-45fe-bd4b-8f95dc217e6c','Aesi','7c847407-d519-479c-99bd-b57d01a98670','702360b8-7181-41a6-b8ac-662eeace3cf2'),('f76b4c40-3f06-4638-8053-5f1d96517fe7','Zaxara, the Exemplary','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26','b5fa6356-25a5-48d5-b2dc-c08a7df6ebe9');
/*!40000 ALTER TABLE `decks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `games`
--

DROP TABLE IF EXISTS `games`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `games` (
  `id` varchar(64) NOT NULL,
  `game_name` varchar(1024) DEFAULT NULL,
  `month` varchar(16) DEFAULT NULL,
  `year` int DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `game_time` varchar(64) DEFAULT NULL,
  `game_turns` int DEFAULT NULL,
  `winning_deck_id` varchar(64) DEFAULT NULL,
  `winning_player_id` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `games_ibfk_1` (`winning_deck_id`),
  KEY `games_ibfk_2` (`winning_player_id`),
  CONSTRAINT `games_ibfk_1` FOREIGN KEY (`winning_deck_id`) REFERENCES `decks` (`id`),
  CONSTRAINT `games_ibfk_2` FOREIGN KEY (`winning_player_id`) REFERENCES `Players` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `games`
--

LOCK TABLES `games` WRITE;
/*!40000 ALTER TABLE `games` DISABLE KEYS */;
INSERT INTO `games` VALUES ('11e45865-09b3-4c32-aafe-18caaaed35cb','2025-06-02 17:29 - 19:29','June',2025,'2025-06-02 17:29:00','2025-06-02 19:29:00','2:00:00',12,'e527deb5-3666-4385-a3ef-f3ae959e20ea','494925c2-0147-4381-9b5d-eb1b15622f73'),('3287a41e-23ee-46ae-822d-eb4cc35f8753','2025-02-17 17:33 - 19:30','February',2025,'2025-02-17 17:33:00','2025-02-17 19:30:00','1:57:00',14,'b3d362cf-bf31-4826-8056-adfec5fac8a4','f73a2cf1-38a2-4ae6-b4d5-ea3c68f10db5'),('4093f31c-6122-4f82-bd5d-40140ffc585b','2025-03-17 19:35 - 20:48','March',2025,'2025-03-17 19:35:00','2025-03-17 20:48:00','1:13:00',8,'d9e2a41f-6f60-4ec0-a45a-9595cc725536','7d5d6490-bb57-4a6d-a268-92c6d0fc6d43'),('5e4ac305-c8f7-4b83-bc4e-4b9efea1deb3','2025-03-17 17:12 - 18:20','March',2025,'2025-03-17 17:12:00','2025-03-17 18:20:00','1:08:00',7,'6c30333c-1ef4-4a96-9af2-537edfda94b1','be1d79dd-b907-4fcc-8ead-1bd50eb01571'),('815f4404-cebc-4885-9222-6d1d4784f8c2','2025-05-30 19:35 - 20:14','May',2025,'2025-05-30 19:35:00','2025-05-30 20:14:00','0:39:00',7,'ce3adffa-6113-48f4-baa2-ade8b4f312bf','f73a2cf1-38a2-4ae6-b4d5-ea3c68f10db5'),('8f4cf8e7-0b0f-42a7-8f06-1eac617c423f','2025-02-17 19:37 - 20:45','February',2025,'2025-02-17 19:37:00','2025-02-17 20:45:00','1:08:00',13,'8eb54151-0939-43e5-a433-defea8048355','494925c2-0147-4381-9b5d-eb1b15622f73'),('991e0ee3-c5fa-4cc5-943b-4de3e6ed8505','2025-05-30 18:51 - 19:28','May',2025,'2025-05-30 18:51:00','2025-05-30 19:28:00','0:37:00',7,'d166c651-2f14-4c54-a28d-bcb6990f8772','f73a2cf1-38a2-4ae6-b4d5-ea3c68f10db5'),('b0947f69-f401-42b0-93d6-951dab5c6e84','2025-05-30 21:13 - 22:13','May',2025,'2025-05-30 21:13:00','2025-05-30 22:13:00','1:00:00',9,'b6b1cfef-78e4-4fff-a30a-15bad0280f2b','18f2bada-2f3c-419e-921c-0fac96324e41'),('c9924d51-69e4-4ad8-8d2c-491f5b039fbb','2025-05-30 17:36 - 18:41','May',2025,'2025-05-30 17:36:00','2025-05-30 18:41:00','1:05:00',10,'8fa9c10a-9a9a-4c75-bdd7-cc95d9591850','7c847407-d519-479c-99bd-b57d01a98670'),('cb62d32a-cbc8-41b2-8fa7-269198bd1e5a','2025-06-02 19:37 - 20:22','June',2025,'2025-06-02 19:37:00','2025-06-02 20:22:00','0:45:00',6,'07e23f42-63ec-4c82-9ecf-4cf07ce8c901','31c2bb6a-1161-4981-98ef-ca9d4cc302c6'),('d0eb425a-682f-4bd4-807e-82d064ad9364','2025-03-17 18:26 - 19:31','March',2025,'2025-03-17 18:26:00','2025-03-17 19:31:00','1:05:00',9,'913ce649-0495-4197-9aa4-aeb49bfa25d4','be1d79dd-b907-4fcc-8ead-1bd50eb01571'),('fd0a1582-ef87-4a4c-9530-7dfa8f6237f5','2025-05-30 20:20 - 21:07','May',2025,'2025-05-30 20:20:00','2025-05-30 21:07:00','0:47:00',7,'b008d2cb-fd63-4530-bab9-e4944bfae79f','18f2bada-2f3c-419e-921c-0fac96324e41');
/*!40000 ALTER TABLE `games` ENABLE KEYS */;
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
INSERT INTO `Players` VALUES ('18f2bada-2f3c-419e-921c-0fac96324e41','Jay F'),('31c2bb6a-1161-4981-98ef-ca9d4cc302c6','Bailey M'),('494925c2-0147-4381-9b5d-eb1b15622f73','Liam R'),('7c847407-d519-479c-99bd-b57d01a98670','Arik H'),('7d5d6490-bb57-4a6d-a268-92c6d0fc6d43','Zoltán M'),('9f16663c-f653-471a-8bb3-b4eb26524b67','Dean P'),('bcd17dd0-e430-40b5-954f-9a7289a8bac7','Dan F'),('bcdc66af-d20f-42e0-8bc2-21fee1c7ec26','Kieran H'),('be1d79dd-b907-4fcc-8ead-1bd50eb01571','Brayden M'),('f73a2cf1-38a2-4ae6-b4d5-ea3c68f10db5','Cyrus T');
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
  CONSTRAINT `seats_ibfk_1` FOREIGN KEY (`deck_id`) REFERENCES `decks` (`id`),
  CONSTRAINT `seats_ibfk_2` FOREIGN KEY (`game_id`) REFERENCES `games` (`id`),
  CONSTRAINT `seats_ibfk_3` FOREIGN KEY (`player_id`) REFERENCES `Players` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Seats`
--

LOCK TABLES `Seats` WRITE;
/*!40000 ALTER TABLE `Seats` DISABLE KEYS */;
INSERT INTO `Seats` VALUES ('0761a3ef-fba2-45e2-a0f5-67b7031849dc',4,NULL,'ce3adffa-6113-48f4-baa2-ade8b4f312bf','815f4404-cebc-4885-9222-6d1d4784f8c2','f73a2cf1-38a2-4ae6-b4d5-ea3c68f10db5'),('14276c1d-44e2-4266-bc40-cccee6ba3434',4,11,'258758eb-a829-4b20-8939-3f6bf8593326','3287a41e-23ee-46ae-822d-eb4cc35f8753','494925c2-0147-4381-9b5d-eb1b15622f73'),('14b63224-f8fe-4d0c-a857-f5be540e5f3c',4,NULL,'d9e2a41f-6f60-4ec0-a45a-9595cc725536','4093f31c-6122-4f82-bd5d-40140ffc585b','7d5d6490-bb57-4a6d-a268-92c6d0fc6d43'),('164e724f-6001-4c09-99b8-94bbe67e4659',4,7,'66c75202-6a2b-45cc-b4d4-08585053e0ef','fd0a1582-ef87-4a4c-9530-7dfa8f6237f5','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26'),('19569c9c-5798-434c-b38f-94e550003c67',4,NULL,'6c30333c-1ef4-4a96-9af2-537edfda94b1','5e4ac305-c8f7-4b83-bc4e-4b9efea1deb3','be1d79dd-b907-4fcc-8ead-1bd50eb01571'),('1ed6c126-8239-4b25-9aa2-82f1000c9295',2,NULL,'913ce649-0495-4197-9aa4-aeb49bfa25d4','d0eb425a-682f-4bd4-807e-82d064ad9364','be1d79dd-b907-4fcc-8ead-1bd50eb01571'),('2976336f-ea3d-4036-8768-57dd23f3e0b3',3,12,'70e716a9-a879-4372-8543-a119900ec96c','3287a41e-23ee-46ae-822d-eb4cc35f8753','9f16663c-f653-471a-8bb3-b4eb26524b67'),('2ac3b644-7864-4c90-9ca7-f2f1536f63e5',1,7,'442a348e-0a25-460e-9b1f-0804fb716f93','815f4404-cebc-4885-9222-6d1d4784f8c2','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26'),('2cf0f241-462a-418e-85ac-60397a13917e',3,NULL,'b6b1cfef-78e4-4fff-a30a-15bad0280f2b','b0947f69-f401-42b0-93d6-951dab5c6e84','18f2bada-2f3c-419e-921c-0fac96324e41'),('2eb8add3-681c-458d-aa8b-9833ee22dc8f',3,7,'b1258ee1-fd42-4100-8dbe-911669dee69b','991e0ee3-c5fa-4cc5-943b-4de3e6ed8505','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26'),('2f04eecf-d75c-4f81-8442-e6e98c5db775',2,NULL,'8fa9c10a-9a9a-4c75-bdd7-cc95d9591850','c9924d51-69e4-4ad8-8d2c-491f5b039fbb','7c847407-d519-479c-99bd-b57d01a98670'),('40d66199-c4b0-4801-b781-2fb14522c371',3,12,'0d79e631-f0fa-4f96-9b4b-0c6567c41403','11e45865-09b3-4c32-aafe-18caaaed35cb','31c2bb6a-1161-4981-98ef-ca9d4cc302c6'),('4186f147-77cc-4218-ae51-b3abec9ec2b9',1,7,'839b690f-adcf-4901-92d1-1e87ea6393cc','991e0ee3-c5fa-4cc5-943b-4de3e6ed8505','18f2bada-2f3c-419e-921c-0fac96324e41'),('4820542b-6dd0-4593-9817-77ef1aa057dd',1,7,'6408be34-d9f2-45ff-81cf-9c9f97ff16b1','d0eb425a-682f-4bd4-807e-82d064ad9364','7d5d6490-bb57-4a6d-a268-92c6d0fc6d43'),('4821a916-050c-4067-84bd-04eacbb868f3',2,NULL,'e527deb5-3666-4385-a3ef-f3ae959e20ea','11e45865-09b3-4c32-aafe-18caaaed35cb','494925c2-0147-4381-9b5d-eb1b15622f73'),('4a6aa2e0-0d93-450b-b943-092fd05d5647',1,7,'c1c7dc9b-4223-4172-a82f-1fe434305cf8','5e4ac305-c8f7-4b83-bc4e-4b9efea1deb3','f73a2cf1-38a2-4ae6-b4d5-ea3c68f10db5'),('52e12f1c-670c-45ce-92ab-a0fc68a236d8',2,7,'4872bbe1-39b7-4b48-b983-bf06f56c660c','815f4404-cebc-4885-9222-6d1d4784f8c2','7c847407-d519-479c-99bd-b57d01a98670'),('5450c3c3-ee63-4cbd-8c4e-fec3a48849d9',2,NULL,'b3d362cf-bf31-4826-8056-adfec5fac8a4','3287a41e-23ee-46ae-822d-eb4cc35f8753','f73a2cf1-38a2-4ae6-b4d5-ea3c68f10db5'),('5c2fe873-f597-4605-96c9-2c7a74aba89d',1,14,'15dec003-5456-43ea-a6da-cf981333f6a5','3287a41e-23ee-46ae-822d-eb4cc35f8753','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26'),('5ddbea21-3ce7-4279-8b57-0472bae770d8',3,7,'6408be34-d9f2-45ff-81cf-9c9f97ff16b1','5e4ac305-c8f7-4b83-bc4e-4b9efea1deb3','7d5d6490-bb57-4a6d-a268-92c6d0fc6d43'),('67c1a4d5-fa1c-4b45-bcd2-d3c6a9ad13c7',4,10,'b3d362cf-bf31-4826-8056-adfec5fac8a4','c9924d51-69e4-4ad8-8d2c-491f5b039fbb','f73a2cf1-38a2-4ae6-b4d5-ea3c68f10db5'),('68e39b8d-637e-4939-b5bc-e06e6d519d87',1,8,'38265ce2-f73d-4d47-bac2-59dd855e3c06','4093f31c-6122-4f82-bd5d-40140ffc585b','be1d79dd-b907-4fcc-8ead-1bd50eb01571'),('69ce6d56-a3bd-4b7f-b804-73ba2f625ea8',4,12,'48991208-3f7e-4821-b37b-ed13839ce3a6','11e45865-09b3-4c32-aafe-18caaaed35cb','bcd17dd0-e430-40b5-954f-9a7289a8bac7'),('6aeee813-b175-4998-8065-08ffca9d4870',4,9,'906b4c5d-123c-428b-a7e2-91c75f731d75','8f4cf8e7-0b0f-42a7-8f06-1eac617c423f','f73a2cf1-38a2-4ae6-b4d5-ea3c68f10db5'),('6e3f956f-4e82-4e3b-ac28-64b2dbdfc603',4,9,'8ad26608-ed95-4b9e-ab80-e8b2b1a5ed11','d0eb425a-682f-4bd4-807e-82d064ad9364','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26'),('6f83d587-7e92-4acb-bcb6-616ced0907e8',2,NULL,'8eb54151-0939-43e5-a433-defea8048355','8f4cf8e7-0b0f-42a7-8f06-1eac617c423f','494925c2-0147-4381-9b5d-eb1b15622f73'),('704e81d7-1aa6-44d0-956f-4daafeef33e2',2,8,'ce3adffa-6113-48f4-baa2-ade8b4f312bf','4093f31c-6122-4f82-bd5d-40140ffc585b','f73a2cf1-38a2-4ae6-b4d5-ea3c68f10db5'),('70a18ffd-9eae-43e8-8ceb-986d74bb4ae0',1,9,'69393a02-7e5c-499f-8005-108740dee92f','b0947f69-f401-42b0-93d6-951dab5c6e84','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26'),('7307f2db-6864-499b-9af4-7ac468f5b5e0',2,NULL,'b008d2cb-fd63-4530-bab9-e4944bfae79f','fd0a1582-ef87-4a4c-9530-7dfa8f6237f5','18f2bada-2f3c-419e-921c-0fac96324e41'),('7dedb9c9-cd06-4d73-9935-86a017ef3e14',1,6,'238370d5-306e-4cde-a891-849b365ee683','cb62d32a-cbc8-41b2-8fa7-269198bd1e5a','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26'),('826e5801-baf5-471f-a801-632977463e7c',2,7,'f52e8e9d-cb1e-45fe-bd4b-8f95dc217e6c','b0947f69-f401-42b0-93d6-951dab5c6e84','7c847407-d519-479c-99bd-b57d01a98670'),('850bb3c7-0f02-4d8b-86ba-118b4683ba46',1,10,'8ad26608-ed95-4b9e-ab80-e8b2b1a5ed11','11e45865-09b3-4c32-aafe-18caaaed35cb','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26'),('8652f649-7824-4892-a057-6f6be96c98f5',1,8,'1d60ad87-e35e-43b7-8885-21797d13f593','8f4cf8e7-0b0f-42a7-8f06-1eac617c423f','9f16663c-f653-471a-8bb3-b4eb26524b67'),('89dc3819-bcaf-45df-bd9f-0c1d5753b728',4,9,'0bef737c-68ef-4f15-81e2-49d0477d7e13','b0947f69-f401-42b0-93d6-951dab5c6e84','f73a2cf1-38a2-4ae6-b4d5-ea3c68f10db5'),('8aa514c7-0f6e-44f4-b389-56e3f01610cc',1,7,'25fa61be-722d-4a60-b7bc-d374310469ac','fd0a1582-ef87-4a4c-9530-7dfa8f6237f5','7c847407-d519-479c-99bd-b57d01a98670'),('97948a6f-9a94-47d2-acf4-ef58dd57a740',3,13,'8ad26608-ed95-4b9e-ab80-e8b2b1a5ed11','8f4cf8e7-0b0f-42a7-8f06-1eac617c423f','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26'),('97c0721d-beb3-49c9-82ad-0137978068fe',2,NULL,'d166c651-2f14-4c54-a28d-bcb6990f8772','991e0ee3-c5fa-4cc5-943b-4de3e6ed8505','f73a2cf1-38a2-4ae6-b4d5-ea3c68f10db5'),('9d8a81dd-3d98-4a94-99f8-c244c412fabb',4,7,'59f538d7-3159-41bf-884a-49010663c67a','991e0ee3-c5fa-4cc5-943b-4de3e6ed8505','7c847407-d519-479c-99bd-b57d01a98670'),('9e38a4d6-18dd-4c1e-99e5-bffdf3f18a4f',2,6,'220d4a83-9cc0-418a-9b38-5f81de40edfb','cb62d32a-cbc8-41b2-8fa7-269198bd1e5a','494925c2-0147-4381-9b5d-eb1b15622f73'),('9f3a20c5-b9c9-416f-8c41-1cb566190c23',3,7,'55966c99-36e5-48a1-855c-227d114223b3','fd0a1582-ef87-4a4c-9530-7dfa8f6237f5','f73a2cf1-38a2-4ae6-b4d5-ea3c68f10db5'),('a0437659-f31c-43ce-8a3c-411f67df5f70',2,6,'f76b4c40-3f06-4638-8053-5f1d96517fe7','5e4ac305-c8f7-4b83-bc4e-4b9efea1deb3','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26'),('b0b40338-0d19-4e84-adc7-be71844c83a7',3,6,'64643a32-3b11-4d3c-9746-1f9d6edab87e','d0eb425a-682f-4bd4-807e-82d064ad9364','f73a2cf1-38a2-4ae6-b4d5-ea3c68f10db5'),('be9fa25c-72f5-4169-bafd-87802b6a98ef',3,8,'69393a02-7e5c-499f-8005-108740dee92f','4093f31c-6122-4f82-bd5d-40140ffc585b','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26'),('c26f3ee8-ea62-4e73-879b-e8e6ce38040b',4,6,'786adef8-fff7-441c-a4de-6eab07fdacd7','cb62d32a-cbc8-41b2-8fa7-269198bd1e5a','bcd17dd0-e430-40b5-954f-9a7289a8bac7'),('c4d3fcb3-2302-4d62-9394-65385b2763b3',3,10,'49f2b076-a321-4123-92b5-ab2e81a5f451','c9924d51-69e4-4ad8-8d2c-491f5b039fbb','18f2bada-2f3c-419e-921c-0fac96324e41'),('df90999a-3e2f-4ff2-8caf-5fa59f61bda4',3,NULL,'07e23f42-63ec-4c82-9ecf-4cf07ce8c901','cb62d32a-cbc8-41b2-8fa7-269198bd1e5a','31c2bb6a-1161-4981-98ef-ca9d4cc302c6'),('f0c05367-4874-42b1-95e4-fec0c13ff7a6',1,10,'8ad26608-ed95-4b9e-ab80-e8b2b1a5ed11','c9924d51-69e4-4ad8-8d2c-491f5b039fbb','bcdc66af-d20f-42e0-8bc2-21fee1c7ec26'),('f76af721-ff8f-443a-b509-f05c73291248',3,7,'eba29714-2b90-46df-bedb-03208008e068','815f4404-cebc-4885-9222-6d1d4784f8c2','18f2bada-2f3c-419e-921c-0fac96324e41');
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

-- Dump completed on 2025-06-15 23:13:58
