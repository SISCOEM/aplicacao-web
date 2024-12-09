CREATE DATABASE  IF NOT EXISTS `sicomb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `sicomb`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: sicomb
-- ------------------------------------------------------
-- Server version	8.0.34

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
-- Table structure for table `assistant_load_aux`
--

DROP TABLE IF EXISTS `assistant_load_aux`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assistant_load_aux` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `police_id` bigint NOT NULL,
  `police_adjunct_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `assistant_load_aux_police_id_a004fafe_fk_police_police_id` (`police_id`),
  KEY `assistant_load_aux_police_adjunct_id_e914cef7_fk_police_po` (`police_adjunct_id`),
  CONSTRAINT `assistant_load_aux_police_adjunct_id_e914cef7_fk_police_po` FOREIGN KEY (`police_adjunct_id`) REFERENCES `police_police` (`id`),
  CONSTRAINT `assistant_load_aux_police_id_a004fafe_fk_police_police_id` FOREIGN KEY (`police_id`) REFERENCES `police_police` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assistant_load_aux`
--

LOCK TABLES `assistant_load_aux` WRITE;
/*!40000 ALTER TABLE `assistant_load_aux` DISABLE KEYS */;
/*!40000 ALTER TABLE `assistant_load_aux` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assistant_matricula_aux`
--

DROP TABLE IF EXISTS `assistant_matricula_aux`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assistant_matricula_aux` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `session_key` varchar(100) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `police_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `assistant_matricula_aux_police_id_c3ac0060_fk_police_police_id` (`police_id`),
  CONSTRAINT `assistant_matricula_aux_police_id_c3ac0060_fk_police_police_id` FOREIGN KEY (`police_id`) REFERENCES `police_police` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assistant_matricula_aux`
--

LOCK TABLES `assistant_matricula_aux` WRITE;
/*!40000 ALTER TABLE `assistant_matricula_aux` DISABLE KEYS */;
/*!40000 ALTER TABLE `assistant_matricula_aux` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assistant_uuids_aux`
--

DROP TABLE IF EXISTS `assistant_uuids_aux`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assistant_uuids_aux` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `uuid` varchar(200) NOT NULL,
  `quantity` int NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `load_aux_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `assistant_uuids_aux_load_aux_id_e7560900_fk_assistant` (`load_aux_id`),
  CONSTRAINT `assistant_uuids_aux_load_aux_id_e7560900_fk_assistant` FOREIGN KEY (`load_aux_id`) REFERENCES `assistant_load_aux` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assistant_uuids_aux`
--

LOCK TABLES `assistant_uuids_aux` WRITE;
/*!40000 ALTER TABLE `assistant_uuids_aux` DISABLE KEYS */;
/*!40000 ALTER TABLE `assistant_uuids_aux` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (3,'adjunct'),(4,'police');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=317 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (215,'Can add log entry',15,'add_logentry'),(216,'Can change log entry',15,'change_logentry'),(217,'Can delete log entry',15,'delete_logentry'),(218,'Can view log entry',15,'view_logentry'),(219,'Can add permission',17,'add_permission'),(220,'Can change permission',17,'change_permission'),(221,'Can delete permission',17,'delete_permission'),(222,'Can view permission',17,'view_permission'),(223,'Can add group',16,'add_group'),(224,'Can change group',16,'change_group'),(225,'Can delete group',16,'delete_group'),(226,'Can view group',16,'view_group'),(227,'Can add content type',18,'add_contenttype'),(228,'Can change content type',18,'change_contenttype'),(229,'Can delete content type',18,'delete_contenttype'),(230,'Can view content type',18,'view_contenttype'),(231,'Can add session',28,'add_session'),(232,'Can change session',28,'change_session'),(233,'Can delete session',28,'delete_session'),(234,'Can view session',28,'view_session'),(235,'Can add Policial',27,'add_police'),(236,'Can change Policial',27,'change_police'),(237,'Can delete Policial',27,'delete_police'),(238,'Can view Policial',27,'view_police'),(239,'Can add bullet',19,'add_bullet'),(240,'Can change bullet',19,'change_bullet'),(241,'Can delete bullet',19,'delete_bullet'),(242,'Can view bullet',19,'view_bullet'),(243,'Can add model_accessory',21,'add_model_accessory'),(244,'Can change model_accessory',21,'change_model_accessory'),(245,'Can delete model_accessory',21,'delete_model_accessory'),(246,'Can view model_accessory',21,'view_model_accessory'),(247,'Can add model_armament',22,'add_model_armament'),(248,'Can change model_armament',22,'change_model_armament'),(249,'Can delete model_armament',22,'delete_model_armament'),(250,'Can view model_armament',22,'view_model_armament'),(251,'Can add model_grenada',23,'add_model_grenada'),(252,'Can change model_grenada',23,'change_model_grenada'),(253,'Can delete model_grenada',23,'delete_model_grenada'),(254,'Can view model_grenada',23,'view_model_grenada'),(255,'Can add model_wearable',24,'add_model_wearable'),(256,'Can change model_wearable',24,'change_model_wearable'),(257,'Can delete model_wearable',24,'delete_model_wearable'),(258,'Can view model_wearable',24,'view_model_wearable'),(259,'Can add Equipamento',20,'add_equipment'),(260,'Can change Equipamento',20,'change_equipment'),(261,'Can delete Equipamento',20,'delete_equipment'),(262,'Can view Equipamento',20,'view_equipment'),(263,'Can add load',26,'add_load'),(264,'Can change load',26,'change_load'),(265,'Can delete load',26,'delete_load'),(266,'Can view load',26,'view_load'),(267,'Can add equipment_load',25,'add_equipment_load'),(268,'Can change equipment_load',25,'change_equipment_load'),(269,'Can delete equipment_load',25,'delete_equipment_load'),(270,'Can view equipment_load',25,'view_equipment_load'),(281,'Can add report',57,'add_report'),(282,'Can change report',57,'change_report'),(283,'Can delete report',57,'delete_report'),(284,'Can view report',57,'view_report'),(285,'Can add report_field',58,'add_report_field'),(286,'Can change report_field',58,'change_report_field'),(287,'Can delete report_field',58,'delete_report_field'),(288,'Can view report_field',58,'view_report_field'),(289,'Can add user',59,'add_user'),(290,'Can change user',59,'change_user'),(291,'Can delete user',59,'delete_user'),(292,'Can view user',59,'view_user'),(293,'Can add Token',60,'add_token'),(294,'Can change Token',60,'change_token'),(295,'Can delete Token',60,'delete_token'),(296,'Can view Token',60,'view_token'),(297,'Can add Token',61,'add_tokenproxy'),(298,'Can change Token',61,'change_tokenproxy'),(299,'Can delete Token',61,'delete_tokenproxy'),(300,'Can view Token',61,'view_tokenproxy'),(301,'Can add notification',62,'add_notification'),(302,'Can change notification',62,'change_notification'),(303,'Can delete notification',62,'delete_notification'),(304,'Can view notification',62,'view_notification'),(305,'Can add load_aux',63,'add_load_aux'),(306,'Can change load_aux',63,'change_load_aux'),(307,'Can delete load_aux',63,'delete_load_aux'),(308,'Can view load_aux',63,'view_load_aux'),(309,'Can add matricula_aux',64,'add_matricula_aux'),(310,'Can change matricula_aux',64,'change_matricula_aux'),(311,'Can delete matricula_aux',64,'delete_matricula_aux'),(312,'Can view matricula_aux',64,'view_matricula_aux'),(313,'Can add uuids_aux',65,'add_uuids_aux'),(314,'Can change uuids_aux',65,'change_uuids_aux'),(315,'Can delete uuids_aux',65,'delete_uuids_aux'),(316,'Can view uuids_aux',65,'view_uuids_aux');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authtoken_token`
--

DROP TABLE IF EXISTS `authtoken_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_police_police_id` FOREIGN KEY (`user_id`) REFERENCES `police_police` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authtoken_token`
--

LOCK TABLES `authtoken_token` WRITE;
/*!40000 ALTER TABLE `authtoken_token` DISABLE KEYS */;
INSERT INTO `authtoken_token` VALUES ('13dc5a2a0c3caf20f558c6a9891fc83d69e24dca','2024-07-13 05:38:46.007766',9),('16be6fc92d9379426d8360e5e2bd0e581e16fcb1','2024-06-17 22:06:27.112144',8),('ca9b90054f878828606639ab3fd053f2358ba3fc','2024-07-09 11:03:57.284849',3),('ebdd78401fdb9d5e85dae624209db487065f129f','2024-07-09 11:02:45.674210',4);
/*!40000 ALTER TABLE `authtoken_token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_police_police_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_police_police_id` FOREIGN KEY (`user_id`) REFERENCES `police_police` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2024-05-20 03:20:40.086875','4','police',2,'[]',16,7);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (15,'admin','logentry'),(63,'assistant','load_aux'),(64,'assistant','matricula_aux'),(65,'assistant','uuids_aux'),(16,'auth','group'),(17,'auth','permission'),(59,'auth','user'),(60,'authtoken','token'),(61,'authtoken','tokenproxy'),(18,'contenttypes','contenttype'),(19,'equipment','bullet'),(20,'equipment','equipment'),(21,'equipment','model_accessory'),(22,'equipment','model_armament'),(23,'equipment','model_grenada'),(24,'equipment','model_wearable'),(25,'load','equipment_load'),(26,'load','load'),(62,'notifications_app_mobile','notification'),(27,'police','police'),(57,'report','report'),(58,'report','report_field'),(28,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=125 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (25,'contenttypes','0001_initial','2023-10-06 22:29:22.030792'),(26,'contenttypes','0002_remove_content_type_name','2023-10-06 22:29:22.187666'),(27,'auth','0001_initial','2023-10-06 22:29:22.687740'),(28,'auth','0002_alter_permission_name_max_length','2023-10-06 22:29:22.747905'),(29,'auth','0003_alter_user_email_max_length','2023-10-06 22:29:22.762415'),(30,'auth','0004_alter_user_username_opts','2023-10-06 22:29:22.770509'),(31,'auth','0005_alter_user_last_login_null','2023-10-06 22:29:22.797828'),(32,'auth','0006_require_contenttypes_0002','2023-10-06 22:29:22.813849'),(33,'auth','0007_alter_validators_add_error_messages','2023-10-06 22:29:22.831580'),(34,'auth','0008_alter_user_username_max_length','2023-10-06 22:29:22.847630'),(35,'auth','0009_alter_user_last_name_max_length','2023-10-06 22:29:22.867754'),(36,'auth','0010_alter_group_name_max_length','2023-10-06 22:29:22.948078'),(37,'auth','0011_update_proxy_permissions','2023-10-06 22:29:22.960470'),(38,'auth','0012_alter_user_first_name_max_length','2023-10-06 22:29:22.979427'),(39,'police','0001_initial','2023-10-06 22:29:23.585516'),(40,'admin','0001_initial','2023-10-06 22:29:23.786142'),(41,'admin','0002_logentry_remove_auto_add','2023-10-06 22:29:23.797870'),(42,'admin','0003_logentry_add_action_flag_choices','2023-10-06 22:29:23.810799'),(43,'equipment','0001_initial','2023-10-06 22:29:24.074223'),(44,'load','0001_initial','2023-10-06 22:29:24.692951'),(45,'sessions','0001_initial','2023-10-06 22:29:24.757666'),(46,'police','0002_police_name','2023-10-07 00:24:35.112762'),(47,'load','0002_load_load_unload','2023-10-12 14:45:40.522911'),(48,'police','0003_alter_police_name','2023-10-12 14:45:40.533003'),(49,'contenttypes','0001_initial','2023-10-06 22:29:22.030792'),(50,'contenttypes','0002_remove_content_type_name','2023-10-06 22:29:22.187666'),(51,'auth','0001_initial','2023-10-06 22:29:22.687740'),(52,'auth','0002_alter_permission_name_max_length','2023-10-06 22:29:22.747905'),(53,'auth','0003_alter_user_email_max_length','2023-10-06 22:29:22.762415'),(54,'auth','0004_alter_user_username_opts','2023-10-06 22:29:22.770509'),(55,'auth','0005_alter_user_last_login_null','2023-10-06 22:29:22.797828'),(56,'auth','0006_require_contenttypes_0002','2023-10-06 22:29:22.813849'),(57,'auth','0007_alter_validators_add_error_messages','2023-10-06 22:29:22.831580'),(58,'auth','0008_alter_user_username_max_length','2023-10-06 22:29:22.847630'),(59,'auth','0009_alter_user_last_name_max_length','2023-10-06 22:29:22.867754'),(60,'auth','0010_alter_group_name_max_length','2023-10-06 22:29:22.948078'),(61,'auth','0011_update_proxy_permissions','2023-10-06 22:29:22.960470'),(62,'auth','0012_alter_user_first_name_max_length','2023-10-06 22:29:22.979427'),(63,'police','0001_initial','2023-10-06 22:29:23.585516'),(64,'admin','0001_initial','2023-10-06 22:29:23.786142'),(65,'admin','0002_logentry_remove_auto_add','2023-10-06 22:29:23.797870'),(66,'admin','0003_logentry_add_action_flag_choices','2023-10-06 22:29:23.810799'),(67,'equipment','0001_initial','2023-10-06 22:29:24.074223'),(68,'load','0001_initial','2023-10-06 22:29:24.692951'),(69,'sessions','0001_initial','2023-10-06 22:29:24.757666'),(70,'police','0002_police_name','2023-10-07 00:24:35.112762'),(71,'load','0002_load_load_unload','2023-10-12 14:45:40.522911'),(72,'police','0003_alter_police_name','2023-10-12 14:45:40.533003'),(73,'equipment','0002_bullet_activator_equipment_activator_and_more','2024-01-16 23:43:26.657630'),(74,'equipment','0003_alter_equipment_uid','2024-01-16 23:43:26.922524'),(75,'equipment','0004_alter_equipment_serial_number','2024-01-16 23:43:26.963572'),(76,'equipment','0005_alter_bullet_activated_alter_bullet_caliber_and_more','2024-01-17 00:03:14.360079'),(77,'load','0003_alter_equipment_load_status_alter_load_status','2024-01-17 00:03:14.390647'),(78,'police','0004_police_activator','2024-01-17 00:03:14.645605'),(79,'police','0005_alter_police_tipo','2024-01-17 00:03:14.662655'),(80,'police','0006_police_fingerprint','2024-01-17 00:03:14.774113'),(81,'police','0007_alter_police_posto','2024-01-17 00:03:14.846820'),(82,'police','0008_alter_police_activated_alter_police_posto_and_more','2024-01-17 00:03:15.109770'),(83,'report','0001_initial','2024-01-17 00:03:15.324867'),(84,'report','0002_report_date_creation','2024-01-17 00:03:15.442521'),(85,'report','0003_alter_report_date_creation_alter_report_title','2024-01-17 00:03:15.476677'),(86,'report','0004_alter_report_date_creation','2024-01-17 00:03:15.485448'),(87,'police','0009_alter_police_posto','2024-01-17 00:04:11.190319'),(88,'report','0005_alter_report_date_creation','2024-01-17 00:04:11.230545'),(89,'report','0006_alter_report_date_creation','2024-01-17 00:04:40.138632'),(90,'report','0007_alter_report_date_creation','2024-01-17 00:05:24.817331'),(91,'report','0008_alter_report_date_creation','2024-01-17 00:05:24.837774'),(92,'report','0009_alter_report_date_creation','2024-01-17 00:05:24.847412'),(93,'report','0010_alter_report_date_creation','2024-01-17 00:05:24.857716'),(94,'report','0011_alter_report_date_creation','2024-01-17 00:05:24.869155'),(95,'report','0012_alter_report_date_creation','2024-01-17 00:05:24.879260'),(96,'report','0013_alter_report_date_creation','2024-01-17 00:05:24.893135'),(97,'equipment','0006_alter_bullet_caliber_alter_model_armament_caliber','2024-01-30 19:15:05.151158'),(98,'police','0010_alter_police_posto','2024-01-30 19:15:05.177266'),(99,'authtoken','0001_initial','2024-06-17 22:06:15.500032'),(100,'authtoken','0002_auto_20160226_1747','2024-06-17 22:06:15.566056'),(101,'authtoken','0003_tokenproxy','2024-06-17 22:06:15.570049'),(102,'authtoken','0004_alter_tokenproxy_options','2024-06-17 22:06:15.577129'),(103,'equipment','0007_alter_model_accessory_model_and_more','2024-08-11 23:41:33.882694'),(104,'police','0011_police_pushtoken','2024-08-11 23:41:34.126934'),(105,'notifications_app_mobile','0001_initial','2024-08-13 20:01:26.642011'),(106,'report','0014_alter_report_date_creation','2024-09-06 04:23:52.580535'),(107,'report','0015_alter_report_date_creation','2024-09-06 04:23:52.592837'),(108,'notifications_app_mobile','0002_remove_notification_message','2024-09-13 14:49:00.314227'),(109,'report','0016_alter_report_date_creation','2024-09-13 14:49:00.396396'),(110,'load','0004_alter_load_date_load','2024-09-13 14:49:19.334009'),(111,'report','0017_alter_report_date_creation','2024-09-13 14:49:19.342101'),(112,'load','0005_alter_load_date_load','2024-09-18 17:23:53.878573'),(113,'load','0006_alter_load_date_load','2024-09-18 17:23:53.906130'),(114,'report','0017_report_type_alter_report_date_creation','2024-09-18 17:23:53.973788'),(115,'report','0018_report_police_alter_report_date_creation','2024-09-18 17:23:54.105516'),(116,'report','0019_remove_report_police_alter_report_date_creation','2024-09-18 17:23:54.270934'),(117,'report','0020_merge_20240918_1423','2024-09-18 17:23:54.270934'),(118,'assistant','0001_initial','2024-09-18 18:33:07.054213'),(119,'load','0007_alter_load_date_load','2024-09-18 18:33:07.073641'),(120,'report','0021_remove_report_type_alter_report_date_creation','2024-09-18 18:33:07.097081'),(121,'report','0018_alter_report_date_creation','2024-09-25 21:20:44.330636'),(122,'report','0019_alter_report_date_creation','2024-09-25 21:21:07.788415'),(123,'load','0008_alter_load_date_load','2024-09-25 21:21:21.884747'),(124,'report','0020_alter_report_date_creation','2024-09-25 21:21:21.892863');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('1amtefe62e9w55wzytgciaiig1hj5uqi','.eJxVjEEOwiAQRe_C2hCgFhiX7nsGMgyDVA0kpV0Z765NutDtf-_9lwi4rSVsnZcwJ3ERIE6_W0R6cN1BumO9NUmtrssc5a7Ig3Y5tcTP6-H-HRTs5VsTOqNZ-WxHMhGUyZYh2rNC1jxaInJ-iImMRm18ZufAj8CDBUhZ2yzeH_K6OCI:1sdqBg:15C3m4Eh4-N7w9kHaZ6SPl0uPYLPLxB5ZyBhqVCYd_U','2024-08-27 11:59:40.905477'),('1of03qx0d0783hana2fv1m6dxpway8y6','.eJxVjDsOwjAQBe_iGln-sWtT0ucM1vqHA8iW4qRC3B0ipYD2zcx7MU_bWv028uLnxC5Ms9PvFig-cttBulO7dR57W5c58F3hBx186ik_r4f7d1Bp1G8dDFiKJC0WIVNRqpCFYKSzIFM2mPSZhARnjXWkBGAGFAYViEIaKbP3B9URNxs:1sdqXt:qO66bWk1so81xTw4Sk2k_dhdUj-A8Sst_tNKU1GGQHY','2024-08-27 12:22:37.368046'),('2czypks6iq23sgmnp6koeeiv3b6rn7dh','.eJxVjDsOwjAQBe_iGln-JWtT0nMGa71e4wBypDipEHeHSCmgfTPzXiLitta4dV7ilMVZeHH63RLSg9sO8h3bbZY0t3WZktwVedAur3Pm5-Vw_w4q9vqtiYPW5CFYhuCdG5UdLHgFSM4FKBqLMiORxoRZq-LTELBwMdmDscmI9wfMizex:1sOHAk:0QXQLvNMpaIyi2rbkq-HHebXQCkNdCsd8eMu1_moB1A','2024-07-15 13:34:22.520033'),('2ho4gdk82h1tvqzifh9tcyexfla8lj7c','.eJxVjEEOgjAQRe_StWloK7Xj0j1nIDOdGYsaSCisjHcXEha6_e-9_zY9rkvp1ypzP7C5GmdOvxthfsq4A37geJ9snsZlHsjuij1otd3E8rod7t9BwVq22oOjNigBRPY5tBqYhGOjySmCRAU9x4RBE6k2bjO9RGrAZ0G-AJrPF_7KOQc:1r699v:Qpf7WS9EPG30J5qM-34T38kqrYSC6dyKgwlJgvBLa_s','2023-12-07 12:50:19.723220'),('4nquebw2kn0vwgiqeym0p31u6sf4jl7p','.eJxVjMsOwiAUBf-FtSFAK1dcuvcbyH2AVA0kpV0Z_12bdKHbMzPnpSKuS4lrT3OcRJ3VoA6_GyE_Ut2A3LHemuZWl3kivSl6p11fm6TnZXf_Dgr28q0dZCs8nEgsukzkIJCId5YojewNmwzEIAjmaGSwAJB9IAs-hRFQ1PsDCOY4jQ:1rQr15:ddDWxt-bMsgePR4fF4HIAkjMBrfrVoVx6Yz6PcEfRFY','2024-02-02 15:42:47.061503'),('4o8vfc12hjlylm48mxwefhjq4yhv6xa1','.eJxVjDsOwjAQBe_iGln-sWtT0ucM1vqHA8iW4qRC3B0ipYD2zcx7MU_bWv028uLnxC5Ms9PvFig-cttBulO7dR57W5c58F3hBx186ik_r4f7d1Bp1G8dDFiKJC0WIVNRqpCFYKSzIFM2mPSZhARnjXWkBGAGFAYViEIaKbP3B9URNxs:1rhTwq:k8zmuWaOJhqm8V_mvDwNF-idrceZy9ewtXCPT98TOEQ','2024-03-19 12:31:08.068769'),('65iujuxd54d10q5assfikxzhr6d94tdp','.eJxVjMsOwiAUBf-FtSFAK1dcuvcbyH2AVA0kpV0Z_12bdKHbMzPnpSKuS4lrT3OcRJ3VoA6_GyE_Ut2A3LHemuZWl3kivSl6p11fm6TnZXf_Dgr28q0dZCs8nEgsukzkIJCId5YojewNmwzEIAjmaGSwAJB9IAs-hRFQ1PsDCOY4jQ:1rQaj5:Zdd55TaNXpdMcOyFQJz0vMqvdodeeghUhxwbHKkNFpQ','2024-02-01 22:19:07.450056'),('6c8ith8b1l6157ugqug4h3ek8ryxsj7t','.eJxVjEEOwiAQRe_C2hCgFhiX7nsGMgyDVA0kpV0Z765NutDtf-_9lwi4rSVsnZcwJ3ERIE6_W0R6cN1BumO9NUmtrssc5a7Ig3Y5tcTP6-H-HRTs5VsTOqNZ-WxHMhGUyZYh2rNC1jxaInJ-iImMRm18ZufAj8CDBUhZ2yzeH_K6OCI:1slByh:4gmLamEK-d8AYdSJDg_ieY76xI8xxktjfTDiuHhKjVo','2024-09-16 18:40:39.062326'),('7ufaeug0qycsq5gdmyttf13bbhnz33ut','.eJxVjEsOAiEQBe_C2hBskI9L956BNDQtowaSYWZlvLtOMgvdvqp6LxFxXWpcR5njROIsgjj8bgnzo7QN0B3brcvc2zJPSW6K3OmQ107ledndv4OKo35r7TxoCmAguQKsFbjsDah0tIYJGBhNAmu90pxP2ZJBAA4WMyt0yov3B8XcN24:1tKPqM:xdqGsxDcoZ0OOzWXVPbwLO4HGJ5WQngQV-7qXRAKOtU','2024-12-22 22:33:38.081073'),('84nm2j1cu3z3sosdy0ogr1u9btrf1brq','e30:1sgcVc:mRBpiOAtUK9EaLEmu_2w-b2mWGZeu_h9fv3utJAKP7Y','2024-09-04 03:59:44.981482'),('9qv7teyt0xs8z1y0f1bm3n48cjvc00of','.eJxVjEEOwiAQRe_C2hCgFhiX7nsGMgyDVA0kpV0Z765NutDtf-_9lwi4rSVsnZcwJ3ERIE6_W0R6cN1BumO9NUmtrssc5a7Ig3Y5tcTP6-H-HRTs5VsTOqNZ-WxHMhGUyZYh2rNC1jxaInJ-iImMRm18ZufAj8CDBUhZ2yzeH_K6OCI:1smZ0H:r4BvYXgJRdWN11_6U0K24RXHylLBvGFM_lxCuX9DpIQ','2024-09-20 13:27:57.150318'),('ad9ptjcfhp61kakii88e4wvnlhk16gt0','.eJxVjMsOwiAUBf-FtSFAK1dcuvcbyH2AVA0kpV0Z_12bdKHbMzPnpSKuS4lrT3OcRJ3VoA6_GyE_Ut2A3LHemuZWl3kivSl6p11fm6TnZXf_Dgr28q0dZCs8nEgsukzkIJCId5YojewNmwzEIAjmaGSwAJB9IAs-hRFQ1PsDCOY4jQ:1rQqMQ:MRvXzAN6k7_Sv42cp9zWffPeesmIVAHhM_lDE1qxVCI','2024-02-02 15:00:46.409165'),('alrxwponlrkeictv4f0u717lp4hcqrle','e30:1sgcWT:NY-zVd1P6P4_584i7R_-6Nh01lq_YRwHOjXxiYYqz3k','2024-09-04 04:00:37.557153'),('c43s5gnetqus2wkl3jjpk6vzrm56x88p','.eJxVjEEOwiAQRe_C2pBhgGJduu8ZyMCAVA0kpV0Z765NutDtf-_9l_C0rcVvPS1-ZnERTpx-t0DxkeoO-E711mRsdV3mIHdFHrTLqXF6Xg_376BQL986GRydBpuyCyaSyQw8BCZWrBE1ks3OKrBw5giE0Y7KgMUBEJXTwYn3B-bfNyE:1s9Omd:fa99F86qaUkhOa9Oes5yIl7B4l29HTDpCA3xnZMMeVA','2024-06-04 12:39:59.308991'),('c7026dwg92dl0g10qs02969ib8lwodwu','.eJxVjEEOwiAQRe_C2hCgFhiX7nsGMgyDVA0kpV0Z765NutDtf-_9lwi4rSVsnZcwJ3ERIE6_W0R6cN1BumO9NUmtrssc5a7Ig3Y5tcTP6-H-HRTs5VsTOqNZ-WxHMhGUyZYh2rNC1jxaInJ-iImMRm18ZufAj8CDBUhZ2yzeH_K6OCI:1tKI1O:YYeP3i4Nh32N6QcoX2_tlm2C2N1uB3ksUdpleiWN6uc','2024-12-22 14:12:30.939548'),('cfupuiphsx4jp74yt89r9kviqwb9yc6o','.eJxVjEEOwiAQRe_C2hCgFhiX7nsGMgyDVA0kpV0Z765NutDtf-_9lwi4rSVsnZcwJ3ERIE6_W0R6cN1BumO9NUmtrssc5a7Ig3Y5tcTP6-H-HRTs5VsTOqNZ-WxHMhGUyZYh2rNC1jxaInJ-iImMRm18ZufAj8CDBUhZ2yzeH_K6OCI:1stYab:7p4lC47GIKBcGKi44bo_kzagkz6fQT0MJifTW8Nx4FM','2024-10-09 20:26:21.053652'),('dcnz362ysy8726h6efkiqwkwa60toqy4','e30:1sgcYV:6sGLDMyLRc2clvYe5xS64LIXjb_T6UGpVW3LOLYbaaY','2024-09-04 04:02:43.393474'),('dw4se5e7un1n1nj32f4rsyivc95uihpk','.eJxVjEEOgjAQRe_StWloK7Xj0j1nIDOdGYsaSCisjHcXEha6_e-9_zY9rkvp1ypzP7C5GmdOvxthfsq4A37geJ9snsZlHsjuij1otd3E8rod7t9BwVq22oOjNigBRPY5tBqYhGOjySmCRAU9x4RBE6k2bjO9RGrAZ0G-AJrPF_7KOQc:1qvGsl:-4NKqafmHZvybe4vTTE4ptgxEJMjJdWiUelOi3zSoMM','2023-11-07 12:51:39.984836'),('eeygqk7pxw0c9a7oefqdcelgnctiweue','.eJxVjEEOwiAQRe_C2hCgFhiX7nsGMgyDVA0kpV0Z765NutDtf-_9lwi4rSVsnZcwJ3ERIE6_W0R6cN1BumO9NUmtrssc5a7Ig3Y5tcTP6-H-HRTs5VsTOqNZ-WxHMhGUyZYh2rNC1jxaInJ-iImMRm18ZufAj8CDBUhZ2yzeH_K6OCI:1sgN93:d1aoib8gQVM5A953rRobV5S4tz1tfAWm3wGHmIhlNp8','2024-09-03 11:35:25.897793'),('etra4dou1r3646anvwj15jgqyl5ajivy','.eJxVjDsOwjAQBe_iGln-JP5Q0nMGa3ftxQHkSHFSIe4OkVJA-2bmvUSCba1p62VJUxZnYcXpd0OgR2k7yHdot1nS3NZlQrkr8qBdXudcnpfD_Tuo0Ou3xoEcDt64oAB8ZGOd1xZIabYR_GBYYWCTIxNQVozjaNEHpqi0dkaL9wfgRjfH:1rXWYn:PEhFC4o3KiZ9GOqdCti1EUAoyFcYOB27rD9rs_iKwQg','2024-02-21 01:17:09.078055'),('fez0wds7y9tvf1j8z4e553lq2cxwre60','.eJxVjDsOwjAQBe_iGln-sWtT0ucM1vqHA8iW4qRC3B0ipYD2zcx7MU_bWv028uLnxC5Ms9PvFig-cttBulO7dR57W5c58F3hBx186ik_r4f7d1Bp1G8dDFiKJC0WIVNRqpCFYKSzIFM2mPSZhARnjXWkBGAGFAYViEIaKbP3B9URNxs:1sdqTs:dpEX_ApcFUgNc2oDxx1_93zaxaLTAGVWRs7LwAjPvW0','2024-08-27 12:18:28.375489'),('fww5q66g9jse7jfc2ufe5n6bw8ay6jip','.eJxVjDsOwjAQBe_iGln-sWtT0ucM1vqHA8iW4qRC3B0ipYD2zcx7MU_bWv028uLnxC5Ms9PvFig-cttBulO7dR57W5c58F3hBx186ik_r4f7d1Bp1G8dDFiKJC0WIVNRqpCFYKSzIFM2mPSZhARnjXWkBGAGFAYViEIaKbP3B9URNxs:1raqMz:WlFs9mSLdovBjT2Jvp62Y-D-EzoL96u2zHB9vHNu67I','2024-03-01 05:02:41.466194'),('fyxdmboq4le2ei1iq0qi4j04ddckrjld','.eJxVjDsOwjAQBe_iGln-sWtT0ucM1vqHA8iW4qRC3B0ipYD2zcx7MU_bWv028uLnxC5Ms9PvFig-cttBulO7dR57W5c58F3hBx186ik_r4f7d1Bp1G8dDFiKJC0WIVNRqpCFYKSzIFM2mPSZhARnjXWkBGAGFAYViEIaKbP3B9URNxs:1rhTvR:4v1FaiTTaZghWxTwVnqMe3YiP6Znntdkl_zpDEgNn9g','2024-03-19 12:29:41.069451'),('hanubdqgsoe8kk35qkaay98o8uqbtxwi','.eJxVjEEOwiAQRe_C2hCgFhiX7nsGMgyDVA0kpV0Z765NutDtf-_9lwi4rSVsnZcwJ3ERIE6_W0R6cN1BumO9NUmtrssc5a7Ig3Y5tcTP6-H-HRTs5VsTOqNZ-WxHMhGUyZYh2rNC1jxaInJ-iImMRm18ZufAj8CDBUhZ2yzeH_K6OCI:1sdqO0:rfbM0JNyAdfLQjgiiZEA5EkyYurx2UfYZrjBt4wopSs','2024-08-27 12:12:24.154371'),('hjt7rp5mwjtbs6hvr7wu99dau9dd3jny','.eJxVjDsOwjAQBe_iGln-JWtT0nMGa71e4wBypDipEHeHSCmgfTPzXiLitta4dV7ilMVZeHH63RLSg9sO8h3bbZY0t3WZktwVedAur3Pm5-Vw_w4q9vqtiYPW5CFYhuCdG5UdLHgFSM4FKBqLMiORxoRZq-LTELBwMdmDscmI9wfMizex:1sPFRL:W2e-Tu7knWlNzP1rvzKVTGt_0bsBAASQ55Bm6ADmsZ4','2024-07-18 05:55:31.677681'),('i6ejgf2o545mkt0uk7srkdlh063nwemn','.eJxVjEEOwiAQRe_C2hCgFhiX7nsGMgyDVA0kpV0Z765NutDtf-_9lwi4rSVsnZcwJ3ERIE6_W0R6cN1BumO9NUmtrssc5a7Ig3Y5tcTP6-H-HRTs5VsTOqNZ-WxHMhGUyZYh2rNC1jxaInJ-iImMRm18ZufAj8CDBUhZ2yzeH_K6OCI:1sr013:n_o6VSwXzUDPMry9TD8h4Bt-GF26x4166NGuNaU4T4I','2024-10-02 19:07:05.087200'),('i71evm0p48h0by9kdc6wt31c4e0t80z8','.eJxVjEEOwiAQRe_C2hCgFhiX7nsGMgyDVA0kpV0Z765NutDtf-_9lwi4rSVsnZcwJ3ERIE6_W0R6cN1BumO9NUmtrssc5a7Ig3Y5tcTP6-H-HRTs5VsTOqNZ-WxHMhGUyZYh2rNC1jxaInJ-iImMRm18ZufAj8CDBUhZ2yzeH_K6OCI:1tKPZx:mWYuyFJVPZGzntV-CopukJtGHRzeeKVy5U9tgNWo6vo','2024-12-22 22:16:41.068740'),('iw43d2n7l6r9l30j0olwxl26nx1l4v7r','.eJxVi70OwiAQgN-F2TR3wJHi6O4zkAPOQGzUlDIZ3100HXT9fp4qcN9K6E3WULM6KlKHXxY5XeX2EY_7UpNMX7XTNp15W2vqC5_27m8u3Mo4jSZtDUY_o9ZWDFJEBMxECExA3gm7weZEnC828agFfDTAzgGKer0Bwss1Tw:1rQqsv:jRber90uSm60ZPptkH1oYnyDT-P6zeYPEtiaKtunjOY','2024-02-02 15:34:21.010233'),('jb17e0c1uoorolyr3icsch1qv0jov4p3','.eJxVjEEOwiAQRe_C2pBhgGJduu8ZyMCAVA0kpV0Z765NutDtf-_9l_C0rcVvPS1-ZnERTpx-t0DxkeoO-E711mRsdV3mIHdFHrTLqXF6Xg_376BQL986GRydBpuyCyaSyQw8BCZWrBE1ks3OKrBw5giE0Y7KgMUBEJXTwYn3B-bfNyE:1s9Ooy:WcfaH4_WLy-k2CuSBNTSdayrOrz9VWyQj02nH9TRbgs','2024-06-04 12:42:24.293580'),('k24glkboswvw8z6bzpt78rspsdqp8j3t','e30:1sgcXg:bLvgfEHNhf5tWZ721S5yM6K6wqM_QFF3v2010KZdT6M','2024-09-04 04:01:52.662945'),('k9xkqn6l84oapy20nlqind4dlnrthhc1','.eJxVjEEOwiAURO_C2pDCLx9w6b5nIMAHqRqalHZlvLs06UKXM_PmvZnz-1bc3tLqZmJXZtnltws-PlM9Bnr4el94XOq2zoEfCD_XxqeF0ut2sn-C4lvpbwQcJI1aI8asUSdlg8yyZ5BGRxiyMMIkY2EESNYqKRC7npQSZIRnny-r_TZ7:1t3HmK:B-ThDJpbdlFmM83yx2FG1fAfqgtzqAsfy-aJ3vnq0tM','2024-11-05 16:30:40.989911'),('m5ze6lz1doehwi4fnp88mulxnhqjyjlo','.eJxVjEEOwiAQRe_C2hCgFhiX7nsGMgyDVA0kpV0Z765NutDtf-_9lwi4rSVsnZcwJ3ERIE6_W0R6cN1BumO9NUmtrssc5a7Ig3Y5tcTP6-H-HRTs5VsTOqNZ-WxHMhGUyZYh2rNC1jxaInJ-iImMRm18ZufAj8CDBUhZ2yzeH_K6OCI:1sgyhX:4QYU1_kFoMCQKYcmOiOaC8f-oiw96dL0N-WHwxL6HAo','2024-09-05 03:41:31.505355'),('mh994qdu78phkvm8u0if6sglgfwlse6l','.eJxVi0kOwiAUhu_C2jTAY2hduvcM5AE_gdioacvKeHeHdKHbb3iIwH2roa9YQsviKIw4_LLI6YLrR9xvc0sYvmqn63DmbWmpz3zau7-58lrfJ0mbJwmjwTFaJGJih2ypjPC6sEYcDakE5zVbzyAvizLeTZKhYMXzBSPXNyQ:1sRbao:Tff5_dukjMLFKJMa5Jza-F8WT9whr0FqE_Xx-xwchk4','2024-07-24 17:59:02.534646'),('nyssx4fm350r2qqy136be49t2hzslgyj','.eJxVjEEOwiAQRe_C2hCgFhiX7nsGMgyDVA0kpV0Z765NutDtf-_9lwi4rSVsnZcwJ3ERIE6_W0R6cN1BumO9NUmtrssc5a7Ig3Y5tcTP6-H-HRTs5VsTOqNZ-WxHMhGUyZYh2rNC1jxaInJ-iImMRm18ZufAj8CDBUhZ2yzeH_K6OCI:1sSNj1:swj7Xy571XneJpUp8eOKWYNf9MR-_n70Fknq1p1ujO0','2024-07-26 21:22:43.362604'),('pajez12bttgv0c3hsknn0oizgaa0l65b','.eJxVjEEOgjAQRe_StWloK7Xj0j1nIDOdGYsaSCisjHcXEha6_e-9_zY9rkvp1ypzP7C5GmdOvxthfsq4A37geJ9snsZlHsjuij1otd3E8rod7t9BwVq22oOjNigBRPY5tBqYhGOjySmCRAU9x4RBE6k2bjO9RGrAZ0G-AJrPF_7KOQc:1qvIzk:eYBLmUTFkSACDzMNQB_9lGQvjhiPjrgLncZNY4zRMOE','2023-11-07 15:07:00.510097'),('ptxkq5cs09bzxe9fccf51kkhg6cp2b66','.eJxVjEEOgjAQRe_StWloK7Xj0j1nIDOdGYsaSCisjHcXEha6_e-9_zY9rkvp1ypzP7C5GmdOvxthfsq4A37geJ9snsZlHsjuij1otd3E8rod7t9BwVq22oOjNigBRPY5tBqYhGOjySmCRAU9x4RBE6k2bjO9RGrAZ0G-AJrPF_7KOQc:1qotKl:BJ5TiKMUhiNDDNgXZbWvNevdTRiC0i1Es2SLySIaTD4','2023-10-20 22:30:11.047838'),('q9cgl984vggz7i1c5oiq602sr596a41q','.eJxVjDsOwjAQBe_iGln-JP5Q0nMGa3ftxQHkSHFSIe4OkVJA-2bmvUSCba1p62VJUxZnYcXpd0OgR2k7yHdot1nS3NZlQrkr8qBdXudcnpfD_Tuo0Ou3xoEcDt64oAB8ZGOd1xZIabYR_GBYYWCTIxNQVozjaNEHpqi0dkaL9wfgRjfH:1rXWzn:BreL0Op88MudZ4ClQ5lcI8eNF6gLndP25LWACFn1k7g','2024-02-21 01:45:03.227368'),('r9d4jlybdgp4rz5m23w9gkcbbd51kjmf','.eJxVjEEOwiAQRe_C2hCgFhiX7nsGMgyDVA0kpV0Z765NutDtf-_9lwi4rSVsnZcwJ3ERIE6_W0R6cN1BumO9NUmtrssc5a7Ig3Y5tcTP6-H-HRTs5VsTOqNZ-WxHMhGUyZYh2rNC1jxaInJ-iImMRm18ZufAj8CDBUhZ2yzeH_K6OCI:1sgNMq:ExnOW4_la7Eme7UL6K5_3-PXFMsIHeUfSp1VSeQGpPQ','2024-09-03 11:49:40.752063'),('rda8hw8knjdhhxl2n3jxuh3bkua950kw','.eJxVjEEOwiAQRe_C2hCgFhiX7nsGMgyDVA0kpV0Z765NutDtf-_9lwi4rSVsnZcwJ3ERIE6_W0R6cN1BumO9NUmtrssc5a7Ig3Y5tcTP6-H-HRTs5VsTOqNZ-WxHMhGUyZYh2rNC1jxaInJ-iImMRm18ZufAj8CDBUhZ2yzeH_K6OCI:1sNINW:QEBHz_UnoMfCu4Q82Bc9LzW4J_r7WhERT9wO0Z_IEdY','2024-07-12 20:39:30.141908'),('rvquulsvtvnwz8ogaoo27gkc9uba0uj0','.eJxVjDsOwjAQBe_iGln-JP5Q0nMGa3ftxQHkSHFSIe4OkVJA-2bmvUSCba1p62VJUxZnYcXpd0OgR2k7yHdot1nS3NZlQrkr8qBdXudcnpfD_Tuo0Ou3xoEcDt64oAB8ZGOd1xZIabYR_GBYYWCTIxNQVozjaNEHpqi0dkaL9wfgRjfH:1rXWDu:atcOjqr9jJ0izs2cYGjIXSphjjrWeDZjxrXa3Fp8Vh0','2024-02-21 00:55:34.076764'),('rykckipt5scb479t94al1ozeb38c48dj','.eJxVjEEOwiAQRe_C2pBhgGJduu8ZyMCAVA0kpV0Z765NutDtf-_9l_C0rcVvPS1-ZnERTpx-t0DxkeoO-E711mRsdV3mIHdFHrTLqXF6Xg_376BQL986GRydBpuyCyaSyQw8BCZWrBE1ks3OKrBw5giE0Y7KgMUBEJXTwYn3B-bfNyE:1sCYC4:PjI_8p3kZH1cit7LuHJc_kSOsFX0N8Wn1wBXugbCeCI','2024-06-13 05:19:16.497003'),('rzr3kostyx4sezzpbcmqhu2b3iz05wsj','.eJxVjDsOwjAQBe_iGln-4Q8lfc5g7dprHEC2FCcV4u4QKQW0b2bei0XY1hq3QUucM7swzU6_G0J6UNtBvkO7dZ56W5cZ-a7wgw4-9UzP6-H-HVQY9Vsnr1RAfU7okdAU6Ui5nHyQAqT1xgQXSIecjLdQikbS5LIR2pJCAZa9P-rmOBI:1r948W:KWerrynwoLzBF4mgRmgAax0oAH5JFFmdg8npgTSdRN0','2023-12-15 14:04:56.514073'),('s6fb1zvtmlwkcu80yybfo5k6wprm160z','.eJxVjMsOwiAUBf-FtSFAK1dcuvcbyH2AVA0kpV0Z_12bdKHbMzPnpSKuS4lrT3OcRJ3VoA6_GyE_Ut2A3LHemuZWl3kivSl6p11fm6TnZXf_Dgr28q0dZCs8nEgsukzkIJCId5YojewNmwzEIAjmaGSwAJB9IAs-hRFQ1PsDCOY4jQ:1rPtSO:0m0jFl9Z-uwQzkt0IYoXQISFHLE4pfeljYt1zWlPNnw','2024-01-31 00:07:00.825900'),('samjude6zo19hvhlk3j00bj9tcdvdjol','.eJxVjDsOwjAQBe_iGln-sWtT0ucM1vqHA8iW4qRC3B0ipYD2zcx7MU_bWv028uLnxC5Ms9PvFig-cttBulO7dR57W5c58F3hBx186ik_r4f7d1Bp1G8dDFiKJC0WIVNRqpCFYKSzIFM2mPSZhARnjXWkBGAGFAYViEIaKbP3B9URNxs:1slCXp:qwr-4Ymefdn5tt2P1eJlPaqahvYIFu01MEVSQIivXeo','2024-09-16 19:16:57.230877'),('sb8d9kbse3om8idewluux5e22tqnxc3s','.eJxVi70OwiAQgN-F2TR3wJHi6O4zkAPOQGzUlDIZ3100HXT9fp4qcN9K6E3WULM6KlKHXxY5XeX2EY_7UpNMX7XTNp15W2vqC5_27m8u3Mo4jSZtDUY_o9ZWDFJEBMxECExA3gm7weZEnC828agFfDTAzgGKer0Bwss1Tw:1rQrMG:fHZ14CvbDHCpTW1uRd23zZhnXGE1zF60GqisJMZpe3s','2024-02-02 16:04:40.540500'),('sdt4yqy4200c2iqkvdlqtcgwhpu5yysg','.eJxVjDsOwjAQBe_iGln-JWtT0nMGa71e4wBypDipEHeHSCmgfTPzXiLitta4dV7ilMVZeHH63RLSg9sO8h3bbZY0t3WZktwVedAur3Pm5-Vw_w4q9vqtiYPW5CFYhuCdG5UdLHgFSM4FKBqLMiORxoRZq-LTELBwMdmDscmI9wfMizex:1sNIGo:4WQ_bSCT_BXvwMUNZACvbBCNUQ9MQI-Ru2_Watl7TFI','2024-07-12 20:32:34.292617'),('t2mzc5h671xgtffbl9yqu6j99038gu1o','.eJxVjEEOgjAQRe_StWloK7Xj0j1nIDOdGYsaSCisjHcXEha6_e-9_zY9rkvp1ypzP7C5GmdOvxthfsq4A37geJ9snsZlHsjuij1otd3E8rod7t9BwVq22oOjNigBRPY5tBqYhGOjySmCRAU9x4RBE6k2bjO9RGrAZ0G-AJrPF_7KOQc:1qotKk:MBT624Zu9fh9LcGTovilp7t-oRxxX5hS4-lqPgMbXjE','2023-10-20 22:30:10.217902'),('tjzn302xih6e5npv5z3sj194vbm3j6jg','.eJxVjEEOgjAQRe_StWloK7Xj0j1nIDOdGYsaSCisjHcXEha6_e-9_zY9rkvp1ypzP7C5GmdOvxthfsq4A37geJ9snsZlHsjuij1otd3E8rod7t9BwVq22oOjNigBRPY5tBqYhGOjySmCRAU9x4RBE6k2bjO9RGrAZ0G-AJrPF_7KOQc:1r68yv:7EXghYUCB3eV4BoJ6WMkeoUfOeUWRf4GpDJKjZeNydg','2023-12-07 12:38:57.779138'),('u063convos50cttt5d13jsxxaowizoxi','.eJxVjEEOwiAURO_C2pDCLx9w6b5nIMAHqRqalHZlvLs06UKXM_PmvZnz-1bc3tLqZmJXZtnltws-PlM9Bnr4el94XOq2zoEfCD_XxqeF0ut2sn-C4lvpbwQcJI1aI8asUSdlg8yyZ5BGRxiyMMIkY2EESNYqKRC7npQSZIRnny-r_TZ7:1t3GYQ:xR3_TyeMEE1QE6OnyJHHwcFK51rmRZwA_rHCbCGHth4','2024-11-05 15:12:14.749225'),('u9wp65pyfowg5x4flur447bqo3sx2i7q','.eJxVjDsOwjAQBe_iGln-JWtT0nMGa71e4wBypDipEHeHSCmgfTPzXiLitta4dV7ilMVZeHH63RLSg9sO8h3bbZY0t3WZktwVedAur3Pm5-Vw_w4q9vqtiYPW5CFYhuCdG5UdLHgFSM4FKBqLMiORxoRZq-LTELBwMdmDscmI9wfMizex:1sJIER:YqWKaeufU-TqtH6m2ZQ1nBjORt4egC09LdVWSloJtno','2024-07-01 19:41:35.551554'),('w6islbdmeo2j22euex2vepk5nto6exs0','.eJxVi0kOwiAUhu_C2jTAY2hduvcM5AE_gdioacvKeHeHdKHbb3iIwH2roa9YQsviKIw4_LLI6YLrR9xvc0sYvmqn63DmbWmpz3zau7-58lrfJ0mbJwmjwTFaJGJih2ypjPC6sEYcDakE5zVbzyAvizLeTZKhYMXzBSPXNyQ:1sRNg7:imvYGg6JmcJukVmkpAJdRDGnfqBPf9442GXrtyRwFPU','2024-07-24 03:07:35.622447'),('xf1rbncgmfc0rybi3bn9pfju8vh6t3s5','.eJxVjDsOwjAQBe_iGln-sWtT0ucM1vqHA8iW4qRC3B0ipYD2zcx7MU_bWv028uLnxC5Ms9PvFig-cttBulO7dR57W5c58F3hBx186ik_r4f7d1Bp1G8dDFiKJC0WIVNRqpCFYKSzIFM2mPSZhARnjXWkBGAGFAYViEIaKbP3B9URNxs:1raqME:3YZCpPxsjLbqhHvC_mgqiNe-nXTempL3ftRWM_A4Zs0','2024-03-01 05:01:54.293449'),('xh862ugeohf7ytozuf76q33wk487og0y','.eJxVjEEOgjAQRe_StWloK7Xj0j1nIDOdGYsaSCisjHcXEha6_e-9_zY9rkvp1ypzP7C5GmdOvxthfsq4A37geJ9snsZlHsjuij1otd3E8rod7t9BwVq22oOjNigBRPY5tBqYhGOjySmCRAU9x4RBE6k2bjO9RGrAZ0G-AJrPF_7KOQc:1qqkER:OFX3kn3mw42evVPyDtsu3KRuzlr-1IcZFwTPT5hI8cU','2023-10-26 01:11:19.681578'),('yhtbae3d0odzcrloq940pirtckgg0eom','.eJxVjEEOwiAQRe_C2hCgFhiX7nsGMgyDVA0kpV0Z765NutDtf-_9lwi4rSVsnZcwJ3ERIE6_W0R6cN1BumO9NUmtrssc5a7Ig3Y5tcTP6-H-HRTs5VsTOqNZ-WxHMhGUyZYh2rNC1jxaInJ-iImMRm18ZufAj8CDBUhZ2yzeH_K6OCI:1sy80H:TvHLDP8A1-ZpknuOxxwt8xveJVNV5kFAO4bcjUUXXPo','2024-10-22 11:03:45.194472'),('yl45w93a9egp83ahmumdvlp5pcwy8gyv','.eJxVjEEOwiAQRe_C2hCgFhiX7nsGMgyDVA0kpV0Z765NutDtf-_9lwi4rSVsnZcwJ3ERIE6_W0R6cN1BumO9NUmtrssc5a7Ig3Y5tcTP6-H-HRTs5VsTOqNZ-WxHMhGUyZYh2rNC1jxaInJ-iImMRm18ZufAj8CDBUhZ2yzeH_K6OCI:1sgNSJ:FiEw7RxVd7cC5xv5m8l_Fe-G_pM6jqUTOitKxFh8QnI','2024-09-03 11:55:19.594502'),('yx0a6kihwvu42bss0edp8erd5wvh57me','.eJxVjEEOwiAQRe_C2hCgFhiX7nsGMgyDVA0kpV0Z765NutDtf-_9lwi4rSVsnZcwJ3ERIE6_W0R6cN1BumO9NUmtrssc5a7Ig3Y5tcTP6-H-HRTs5VsTOqNZ-WxHMhGUyZYh2rNC1jxaInJ-iImMRm18ZufAj8CDBUhZ2yzeH_K6OCI:1sONZW:LmcHEBwrJ5N3v486BSj0KeOpE8MyW7TIB91rZJAqdII','2024-07-15 20:24:22.419615'),('yzmiww2e9z9918ydzlmeki9boqmg3vsm','.eJxVjEEOgjAQRe_StWloK7Xj0j1nIDOdGYsaSCisjHcXEha6_e-9_zY9rkvp1ypzP7C5GmdOvxthfsq4A37geJ9snsZlHsjuij1otd3E8rod7t9BwVq22oOjNigBRPY5tBqYhGOjySmCRAU9x4RBE6k2bjO9RGrAZ0G-AJrPF_7KOQc:1qwNqJ:EWTvoWHy7xGzwOE92xnrvbI5FS2JnY7n-bzr711kE6g','2023-11-10 14:29:43.638501'),('zt8bj0k43eo8duqy0v5qircgt52zomfu','.eJxVjEEOwiAQRe_C2hCgFhiX7nsGMgyDVA0kpV0Z765NutDtf-_9lwi4rSVsnZcwJ3ERIE6_W0R6cN1BumO9NUmtrssc5a7Ig3Y5tcTP6-H-HRTs5VsTOqNZ-WxHMhGUyZYh2rNC1jxaInJ-iImMRm18ZufAj8CDBUhZ2yzeH_K6OCI:1soY8N:P1GSnRXh6EMX28d2zKewNHODQImweKufzERI3u-oz6E','2024-09-26 00:56:31.265686');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `equipment_bullet`
--

DROP TABLE IF EXISTS `equipment_bullet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipment_bullet` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `activated` int NOT NULL,
  `amount` int NOT NULL,
  `image_path` varchar(100) NOT NULL,
  `caliber` varchar(30) NOT NULL,
  `description` longtext NOT NULL,
  `activator_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `equipment_bullet_caliber_83e71a78_uniq` (`caliber`),
  KEY `equipment_bullet_activator_id_0ccab690_fk_police_police_id` (`activator_id`),
  CONSTRAINT `equipment_bullet_activator_id_0ccab690_fk_police_police_id` FOREIGN KEY (`activator_id`) REFERENCES `police_police` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipment_bullet`
--

LOCK TABLES `equipment_bullet` WRITE;
/*!40000 ALTER TABLE `equipment_bullet` DISABLE KEYS */;
INSERT INTO `equipment_bullet` VALUES (5,1,1089,'Modelos/municoes/45acp.png','.45 ACP','Munição ACP',3),(6,1,50,'Modelos/municoes/municao-9mm.jpg','9mm','Munição 9mm',3);
/*!40000 ALTER TABLE `equipment_bullet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `equipment_equipment`
--

DROP TABLE IF EXISTS `equipment_equipment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipment_equipment` (
  `date_register` datetime(6) NOT NULL,
  `activated` int NOT NULL,
  `serial_number` varchar(200) DEFAULT NULL,
  `uid` varchar(200) NOT NULL,
  `status` varchar(20) NOT NULL,
  `model_id` int unsigned NOT NULL,
  `model_type_id` int NOT NULL,
  `activator_id` bigint DEFAULT NULL,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `serial_number` (`serial_number`),
  KEY `equipment_equipment_model_type_id_5e24e40c_fk_django_co` (`model_type_id`),
  KEY `equipment_equipment_activator_id_6db463cb_fk_police_police_id` (`activator_id`),
  CONSTRAINT `equipment_equipment_activator_id_6db463cb_fk_police_police_id` FOREIGN KEY (`activator_id`) REFERENCES `police_police` (`id`),
  CONSTRAINT `equipment_equipment_model_type_id_5e24e40c_fk_django_co` FOREIGN KEY (`model_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `equipment_equipment_chk_1` CHECK ((`model_id` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipment_equipment`
--

LOCK TABLES `equipment_equipment` WRITE;
/*!40000 ALTER TABLE `equipment_equipment` DISABLE KEYS */;
INSERT INTO `equipment_equipment` VALUES ('2024-01-19 14:38:44.380773',1,'SVH58737','3000E280699500004003762771ACC343','12H',6,22,3),('2024-01-17 20:17:38.256289',1,'98450605054150','3400E20047066C706821','12H',3,24,3),('2024-02-01 23:42:35.923804',1,'4534','414C5355504552416C7465633132000000008B76','12H',3,22,3),('2024-02-01 23:47:01.617886',1,'6894956163451','454C5355504552416C7465633132000000007BD1','Disponível',4,22,3),('2024-01-17 03:58:05.764644',1,'45656485','456','Disponível',3,21,3);
/*!40000 ALTER TABLE `equipment_equipment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `equipment_model_accessory`
--

DROP TABLE IF EXISTS `equipment_model_accessory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipment_model_accessory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `activated` int NOT NULL,
  `model` longtext NOT NULL,
  `description` longtext NOT NULL,
  `image_path` varchar(100) NOT NULL,
  `activator_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `equipment_model_acce_activator_id_4ec27a1d_fk_police_po` (`activator_id`),
  CONSTRAINT `equipment_model_acce_activator_id_4ec27a1d_fk_police_po` FOREIGN KEY (`activator_id`) REFERENCES `police_police` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipment_model_accessory`
--

LOCK TABLES `equipment_model_accessory` WRITE;
/*!40000 ALTER TABLE `equipment_model_accessory` DISABLE KEYS */;
INSERT INTO `equipment_model_accessory` VALUES (3,1,'Bastão','Bastão','Modelos/acessorios/bastao.jpg',3),(4,1,'Cone','Cone','Modelos/acessorios/cone.jpg',3),(5,1,'Bastão','Bastão','Modelos/acessorios/bastao.jpg',3),(6,1,'Cone','Cone','Modelos/acessorios/cone.jpg',3);
/*!40000 ALTER TABLE `equipment_model_accessory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `equipment_model_armament`
--

DROP TABLE IF EXISTS `equipment_model_armament`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipment_model_armament` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `activated` int NOT NULL,
  `model` longtext NOT NULL,
  `caliber` varchar(30) NOT NULL,
  `description` longtext NOT NULL,
  `image_path` varchar(100) NOT NULL,
  `activator_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `equipment_model_arma_activator_id_929159ee_fk_police_po` (`activator_id`),
  CONSTRAINT `equipment_model_arma_activator_id_929159ee_fk_police_po` FOREIGN KEY (`activator_id`) REFERENCES `police_police` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipment_model_armament`
--

LOCK TABLES `equipment_model_armament` WRITE;
/*!40000 ALTER TABLE `equipment_model_armament` DISABLE KEYS */;
INSERT INTO `equipment_model_armament` VALUES (3,1,'Glok G22','.22 LR','Glok G22, munição .22 LR','Modelos/armamentos/Glock_g22_GNtS5RI.jpg',3),(4,1,'Glok 9mm','9mm','Pistola Glok 9mm','Modelos/armamentos/1016504_pistola-taurus-th380-oxidada-cal-380-cth380-ox_s1_636711376069468013.jpg',3),(5,1,'GLOCK G22 CAL 9MM','9mm','ANO 2013','Modelos/armamentos/pistol-glock.jpg',3),(6,1,'TAURUS PT100','.40 S&W','Pistola - TAURUS PT100','Modelos/armamentos/TaurusPT100.png',3);
/*!40000 ALTER TABLE `equipment_model_armament` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `equipment_model_grenada`
--

DROP TABLE IF EXISTS `equipment_model_grenada`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipment_model_grenada` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `activated` int NOT NULL,
  `model` longtext NOT NULL,
  `image_path` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `activator_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `equipment_model_gren_activator_id_117d0e77_fk_police_po` (`activator_id`),
  CONSTRAINT `equipment_model_gren_activator_id_117d0e77_fk_police_po` FOREIGN KEY (`activator_id`) REFERENCES `police_police` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipment_model_grenada`
--

LOCK TABLES `equipment_model_grenada` WRITE;
/*!40000 ALTER TABLE `equipment_model_grenada` DISABLE KEYS */;
INSERT INTO `equipment_model_grenada` VALUES (3,1,'Granada de Fumaça','Modelos/granadas/Granada_de_Fumaça.jpg','Granada de Fumaça',3),(4,1,'Granada de Fogo','Modelos/granadas/granada-fogo.jpg','Granada de Fogo',3);
/*!40000 ALTER TABLE `equipment_model_grenada` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `equipment_model_wearable`
--

DROP TABLE IF EXISTS `equipment_model_wearable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipment_model_wearable` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `activated` int NOT NULL,
  `model` longtext NOT NULL,
  `size` varchar(10) NOT NULL,
  `description` longtext NOT NULL,
  `image_path` varchar(100) NOT NULL,
  `activator_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `equipment_model_wear_activator_id_008b8112_fk_police_po` (`activator_id`),
  CONSTRAINT `equipment_model_wear_activator_id_008b8112_fk_police_po` FOREIGN KEY (`activator_id`) REFERENCES `police_police` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipment_model_wearable`
--

LOCK TABLES `equipment_model_wearable` WRITE;
/*!40000 ALTER TABLE `equipment_model_wearable` DISABLE KEYS */;
INSERT INTO `equipment_model_wearable` VALUES (3,1,'Capacete','M','Capacete','Modelos/vestiveis/capacete.jpg',3),(4,1,'Colete','M','Colete','Modelos/vestiveis/colete.jpg',3);
/*!40000 ALTER TABLE `equipment_model_wearable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `load_equipment_load`
--

DROP TABLE IF EXISTS `load_equipment_load`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `load_equipment_load` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `amount` int DEFAULT NULL,
  `observation` longtext,
  `status` varchar(20) NOT NULL,
  `bullet_id` bigint DEFAULT NULL,
  `equipment_id` varchar(200) DEFAULT NULL,
  `load_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `load_equipment_load_bullet_id_9e652871_fk_equipment_bullet_id` (`bullet_id`),
  KEY `load_equipment_load_equipment_id_41d867d3_fk_equipment` (`equipment_id`),
  KEY `load_equipment_load_load_id_f3cd723b_fk_load_load_id` (`load_id`),
  CONSTRAINT `load_equipment_load_bullet_id_9e652871_fk_equipment_bullet_id` FOREIGN KEY (`bullet_id`) REFERENCES `equipment_bullet` (`id`),
  CONSTRAINT `load_equipment_load_equipment_id_41d867d3_fk` FOREIGN KEY (`equipment_id`) REFERENCES `equipment_equipment` (`uid`),
  CONSTRAINT `load_equipment_load_load_id_f3cd723b_fk_load_load_id` FOREIGN KEY (`load_id`) REFERENCES `load_load` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=330 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `load_equipment_load`
--

LOCK TABLES `load_equipment_load` WRITE;
/*!40000 ALTER TABLE `load_equipment_load` DISABLE KEYS */;
INSERT INTO `load_equipment_load` VALUES (237,50,'obs','Justificado',6,NULL,88),(238,50,'-','Devolvido',6,NULL,88),(239,50,'-','Devolvido',6,NULL,89),(240,70,'tdyhjsrehjery','Devolvido',6,NULL,90),(241,1,'4356356346','Devolvido',NULL,'456',90),(242,10,'-','Devolvido',6,NULL,90),(243,10,'-','Devolvido',6,NULL,91),(244,10,NULL,'Devolvido',6,NULL,90),(245,10,'-','Justificado',6,NULL,92),(246,10,NULL,'Devolvido',6,NULL,90),(247,10,'werhert','Devolvido',6,NULL,93),(248,70,'-','Devolvido',6,NULL,94),(249,80,'adsasd','Justificado',6,NULL,95),(250,1,'-','Devolvido',NULL,'456',96),(251,10,NULL,'Devolvido',6,NULL,95),(252,10,'ertyjrwrtyjwr','Justificado',6,NULL,97),(253,10,'adsasd','Devolvido',6,NULL,98),(254,1,'-','Devolvido',NULL,'456',99),(255,90,'usado em campo','Justificado',6,NULL,99),(256,10,NULL,'Devolvido',6,NULL,99),(257,10,'usado em campo','Devolvido',6,NULL,100),(258,1,'-','Devolvido',NULL,'456',101),(259,100,'-','Pendente',6,NULL,102),(260,1,'-','Pendente',NULL,'456',102),(261,1,'-','Pendente',NULL,'3400E20047066C706821',102),(262,90,'-','Devolvido',6,NULL,103),(263,10,NULL,'Devolvido',6,NULL,103),(264,10,'-','Devolvido',6,NULL,104),(265,90,'-','Devolvido',6,NULL,105),(266,1,'-','Devolvido',NULL,'3000E280699500004003762771ACC343',106),(267,3,'disparos ocorridos no dia tal ...','Justificado',6,NULL,106),(268,1,'-','Devolvido',NULL,'456',106),(269,1,'-','Devolvido',NULL,'456',107),(270,21,NULL,'Devolvido',6,NULL,106),(271,21,'disparos ocorridos no dia tal ...','Devolvido',6,NULL,107),(272,1,'-','Devolvido',NULL,'3000E280699500004003762771ACC343',108),(273,1,'-','Devolvido',NULL,'414C5355504552416C7465633132000000008B76',109),(274,1,'-','Devolvido',NULL,'454C5355504552416C7465633132000000007BD1',109),(275,10,'disparo durante a operação','Justificado',6,NULL,109),(276,1,'-','Devolvido',NULL,'3000E280699500004003762771ACC343',109),(277,1,'-','Devolvido',NULL,'454C5355504552416C7465633132000000007BD1',110),(278,1,'-','Devolvido',NULL,'414C5355504552416C7465633132000000008B76',110),(279,90,NULL,'Devolvido',6,NULL,109),(280,90,'disparo durante a operação','Devolvido',6,NULL,110),(281,1,'-','Devolvido',NULL,'3000E280699500004003762771ACC343',111),(282,1,'-','Pendente',NULL,'3000E280699500004003762771ACC343',112),(283,776,'-','Pendente',6,NULL,112),(284,1,'-','Pendente',NULL,'3400E20047066C706821',112),(285,0,'-','Pendente',6,NULL,113),(286,0,'-','Pendente',6,NULL,114),(287,0,'-','Pendente',6,NULL,115),(288,0,'-','Pendente',6,NULL,116),(289,0,'-','Pendente',6,NULL,117),(290,0,'-','Pendente',6,NULL,118),(291,1,'-','Pendente',5,NULL,119),(292,0,'-','Devolvido',6,NULL,120),(293,0,'-','Devolvido',6,NULL,121),(294,50,'-','Devolvido',5,NULL,122),(295,1,'-','Devolvido',6,NULL,122),(296,1,'-','Devolvido',6,NULL,123),(297,50,'-','Devolvido',5,NULL,123),(298,1,'-','Pendente',6,NULL,124),(299,1,'-','Devolvido',NULL,'414C5355504552416C7465633132000000008B76',125),(300,0,'-','Devolvido',6,NULL,125),(301,1,'-','Devolvido',NULL,'414C5355504552416C7465633132000000008B76',126),(302,0,'-','Devolvido',6,NULL,126),(303,1,'-','Devolvido',NULL,'414C5355504552416C7465633132000000008B76',127),(304,1,'-','Devolvido',NULL,'414C5355504552416C7465633132000000008B76',128),(305,1,'-','Pendente',NULL,'3000E280699500004003762771ACC343',129),(306,1,'-','Devolvido',NULL,'414C5355504552416C7465633132000000008B76',130),(307,1,'-','Devolvido',NULL,'3000E280699500004003762771ACC343',130),(308,1,'-','Devolvido',6,NULL,130),(309,1,'-','Devolvido',NULL,'414C5355504552416C7465633132000000008B76',131),(310,1,'-','Devolvido',NULL,'3000E280699500004003762771ACC343',131),(311,1,'-','Devolvido',6,NULL,131),(312,1,'-','Devolvido',NULL,'3000E280699500004003762771ACC343',132),(313,50,'-','Devolvido',6,NULL,132),(314,1,'-','Devolvido',NULL,'3000E280699500004003762771ACC343',133),(315,1,'-','Devolvido',NULL,'3000E280699500004003762771ACC343',134),(316,1,'-','Devolvido',NULL,'3000E280699500004003762771ACC343',135),(317,50,'-','Devolvido',6,NULL,135),(318,1,'-','Pendente',NULL,'3000E280699500004003762771ACC343',136),(319,60,'-','Pendente',5,NULL,136),(320,1,'-','Pendente',NULL,'414C5355504552416C7465633132000000008B76',137),(321,1,'-','Pendente',NULL,'3000E280699500004003762771ACC343',138),(322,1,'-','Pendente',6,NULL,138),(323,1,'-','Devolvido',NULL,'414C5355504552416C7465633132000000008B76',139),(324,49,'-','Devolvido',6,NULL,139),(325,0,'-','Devolvido',6,NULL,140),(326,0,'-','Devolvido',6,NULL,141),(327,1,'-','Devolvido',NULL,'414C5355504552416C7465633132000000008B76',142),(328,49,'-','Devolvido',6,NULL,142),(329,1,'-','Pendente',NULL,'414C5355504552416C7465633132000000008B76',143);
/*!40000 ALTER TABLE `load_equipment_load` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `load_load`
--

DROP TABLE IF EXISTS `load_load`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `load_load` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date_load` datetime(6) NOT NULL,
  `expected_load_return_date` datetime(6) DEFAULT NULL,
  `returned_load_date` datetime(6) DEFAULT NULL,
  `turn_type` varchar(20) NOT NULL,
  `status` varchar(50) NOT NULL,
  `adjunct_id` bigint NOT NULL,
  `police_id` bigint NOT NULL,
  `load_unload_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `load_load_adjunct_id_896d6c02_fk_police_police_id` (`adjunct_id`),
  KEY `load_load_police_id_99893b6d_fk_police_police_id` (`police_id`),
  KEY `load_load_load_unload_id_4661658e_fk_load_load_id` (`load_unload_id`),
  CONSTRAINT `load_load_adjunct_id_896d6c02_fk_police_police_id` FOREIGN KEY (`adjunct_id`) REFERENCES `police_police` (`id`),
  CONSTRAINT `load_load_load_unload_id_4661658e_fk_load_load_id` FOREIGN KEY (`load_unload_id`) REFERENCES `load_load` (`id`),
  CONSTRAINT `load_load_police_id_99893b6d_fk_police_police_id` FOREIGN KEY (`police_id`) REFERENCES `police_police` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=144 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `load_load`
--

LOCK TABLES `load_load` WRITE;
/*!40000 ALTER TABLE `load_load` DISABLE KEYS */;
INSERT INTO `load_load` VALUES (88,'2024-01-17 00:30:45.666293','2024-01-17 06:30:45.665293','2024-01-17 00:36:03.517288','6H','DESCARREGADA',3,4,NULL),(89,'2024-01-17 00:36:03.412119',NULL,'2024-01-17 00:36:03.425363','descarga','descarga',3,4,88),(90,'2024-01-17 04:00:16.554989','2024-01-17 10:00:16.554989','2024-01-17 05:19:17.034247','6H','DESCARREGADA',3,4,NULL),(91,'2024-01-17 04:01:27.639633',NULL,'2024-01-17 04:01:27.657640','descarga','descarga',3,4,90),(92,'2024-01-17 05:04:52.904723',NULL,'2024-01-17 05:04:52.912938','descarga','descarga',3,4,90),(93,'2024-01-17 05:14:21.301488',NULL,'2024-01-17 05:14:21.314643','descarga','descarga',3,4,90),(94,'2024-01-17 05:18:16.355771',NULL,'2024-01-17 05:18:16.367080','descarga','descarga',3,4,90),(95,'2024-01-17 05:18:56.715610','2024-01-17 11:18:56.714613','2024-01-17 05:31:48.847778','6H','DESCARREGADA',3,4,NULL),(96,'2024-01-17 05:19:16.951971',NULL,'2024-01-17 05:19:16.980509','descarga','descarga',3,4,90),(97,'2024-01-17 05:19:49.850470',NULL,'2024-01-17 05:19:49.866041','descarga','descarga',3,4,95),(98,'2024-01-17 05:31:48.776250',NULL,'2024-01-17 05:31:48.791801','descarga','descarga',3,4,95),(99,'2024-01-18 22:45:12.085907','2024-01-19 04:45:12.084994','2024-01-18 23:16:19.546669','6H','DESCARREGADA',3,4,NULL),(100,'2024-01-18 22:46:12.830756',NULL,'2024-01-18 22:46:12.837847','descarga','descarga',3,4,99),(101,'2024-01-18 22:48:44.257338',NULL,'2024-01-18 22:48:44.266710','descarga','descarga',3,4,99),(102,'2024-01-19 00:15:55.571690','2024-01-19 06:15:55.568690',NULL,'6H','ATRASADA',3,4,NULL),(103,'2024-01-19 01:10:58.740671',NULL,'2024-01-19 01:35:23.765071','CONSERTO','DESCARREGADA',3,4,NULL),(104,'2024-01-19 01:14:47.324366',NULL,'2024-01-19 01:14:47.332396','descarga','descarga',3,4,103),(105,'2024-01-19 01:17:59.540752',NULL,'2024-01-19 01:17:59.553460','descarga','descarga',3,4,103),(106,'2024-01-19 15:30:23.132095','2024-01-20 15:30:23.131078','2024-01-19 15:55:08.785858','24H','DESCARREGADA',3,5,NULL),(107,'2024-01-19 15:51:21.648629',NULL,'2024-01-19 15:51:21.665931','descarga','descarga',3,5,106),(108,'2024-01-19 15:55:08.671349',NULL,'2024-01-19 15:55:08.710936','descarga','descarga',3,5,106),(109,'2024-02-06 15:43:45.422230','2024-02-06 21:43:45.420177','2024-02-06 15:57:34.402697','6H','DESCARREGADA',3,4,NULL),(110,'2024-02-06 15:54:36.965386',NULL,'2024-02-06 15:54:36.983010','descarga','descarga',3,4,109),(111,'2024-02-06 15:57:34.313050',NULL,'2024-02-06 15:57:34.335198','descarga','descarga',3,4,109),(112,'2024-02-06 19:13:30.778035','2024-02-07 07:13:30.776035',NULL,'12H','ATRASADA',3,4,NULL),(113,'2024-08-13 19:47:01.670704','2024-08-14 07:47:01.668704',NULL,'12H','ATRASADA',9,8,NULL),(114,'2024-08-13 20:06:46.643666','2024-08-14 02:06:46.642669',NULL,'6H','ATRASADA',9,8,NULL),(115,'2024-08-13 20:08:42.018651','2024-08-14 02:08:42.017653',NULL,'6H','ATRASADA',9,8,NULL),(116,'2024-08-13 20:18:13.511636','2024-08-14 20:18:13.509635',NULL,'24H','ATRASADA',9,8,NULL),(117,'2024-08-13 20:22:42.981410','2024-08-14 08:22:42.979389',NULL,'12H','ATRASADA',9,8,NULL),(118,'2024-08-13 20:27:28.851751','2024-08-14 20:27:28.849750',NULL,'24H','ATRASADA',9,8,NULL),(119,'2024-08-13 20:28:21.628216','2024-08-14 20:28:21.627215',NULL,'24H','ATRASADA',9,8,NULL),(120,'2024-08-13 20:49:24.609521','2024-08-14 20:49:24.607522','2024-08-13 20:55:11.930553','24H','DESCARREGADA',9,8,NULL),(121,'2024-08-13 20:55:10.942057',NULL,'2024-08-13 20:55:10.952479','descarga','descarga',9,8,120),(122,'2024-08-15 13:18:31.941460','2024-08-16 13:18:31.939456','2024-08-15 13:36:54.107298','24H','DESCARREGADA',9,8,NULL),(123,'2024-08-15 13:36:53.135731',NULL,'2024-08-15 13:36:53.144001','descarga','descarga',9,8,122),(124,'2024-08-16 12:47:24.095184','2024-08-17 12:47:24.093185',NULL,'24H','ATRASADA',9,8,NULL),(125,'2024-08-22 05:10:51.288220','2024-08-22 17:10:51.285207','2024-08-22 05:11:53.615416','12H','DESCARREGADA',9,8,NULL),(126,'2024-08-22 05:11:52.652936',NULL,'2024-08-22 05:11:52.661142','descarga','descarga',9,8,125),(127,'2024-08-23 19:43:36.119162','2024-08-24 07:43:36.117163','2024-08-23 19:44:24.830095','12H','DESCARREGADA',9,8,NULL),(128,'2024-08-23 19:44:23.866887',NULL,'2024-08-23 19:44:23.874444','descarga','descarga',9,8,127),(129,'2024-09-02 19:08:04.956374','2024-09-03 07:08:04.948584',NULL,'12H','ATRASADA',9,8,NULL),(130,'2024-09-02 19:11:25.849591','2024-09-03 07:11:25.849591','2024-09-02 19:14:19.733745','12H','DESCARREGADA',9,8,NULL),(131,'2024-09-02 19:14:16.989089',NULL,'2024-09-02 19:14:17.057420','descarga','descarga',9,8,130),(132,'2024-09-11 23:58:08.842463','2024-09-12 23:58:08.840463','2024-09-12 00:59:40.493303','24H','DESCARREGADA',9,8,NULL),(133,'2024-09-12 00:58:27.751553','2024-09-13 00:58:27.748555','2024-09-12 00:58:59.016549','24H','DESCARREGADA',9,8,NULL),(134,'2024-09-12 00:58:58.181184',NULL,'2024-09-12 00:58:58.183371','descarga','descarga',9,8,133),(135,'2024-09-12 00:59:39.465981',NULL,'2024-09-12 00:59:39.478133','descarga','descarga',9,8,132),(136,'2024-09-13 14:49:24.022860','2024-09-14 02:50:13.359610',NULL,'12H','ATRASADA',9,8,NULL),(137,'2024-09-13 14:58:30.413680','2024-09-14 02:59:56.257186',NULL,'12H','ATRASADA',9,8,NULL),(138,'2024-09-25 20:40:57.599111','2024-09-26 08:42:16.932311',NULL,'12H','ATRASADA',9,8,NULL),(139,'2024-09-25 21:21:38.279176','2024-09-26 09:22:31.400446','2024-10-08 11:07:12.659713','12H','DESCARREGADA COM ATRASO',9,8,NULL),(140,'2024-09-25 22:48:52.464773','2024-09-26 10:50:11.750005','2024-09-25 22:56:03.730411','12H','DESCARREGADA',9,8,NULL),(141,'2024-09-25 22:54:56.857419',NULL,'2024-09-25 22:56:02.791526','descarga','descarga',9,8,140),(142,'2024-10-08 11:03:28.058894',NULL,'2024-10-08 11:07:10.466742','descarga','descarga',9,8,139),(143,'2024-12-08 14:12:16.341576','2024-12-09 02:42:23.616778',NULL,'12H','DENTRO DO PRAZO',9,8,NULL);
/*!40000 ALTER TABLE `load_load` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications_app_mobile_notification`
--

DROP TABLE IF EXISTS `notifications_app_mobile_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications_app_mobile_notification` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `body` varchar(100) NOT NULL,
  `data` varchar(100) NOT NULL,
  `to` varchar(100) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications_app_mobile_notification`
--

LOCK TABLES `notifications_app_mobile_notification` WRITE;
/*!40000 ALTER TABLE `notifications_app_mobile_notification` DISABLE KEYS */;
INSERT INTO `notifications_app_mobile_notification` VALUES (1,'CARGA REALIZADA','Olá policial, nova carga realizada por Anthonius Miguel!','{\'load_id\': 118}','ExponentPushToken[M9ekQvEsJM6d9ZmWgLYG28]','2024-08-13 20:27:29.732948'),(2,'CARGA REALIZADA','Olá policial, nova carga realizada por Anthonius Miguel!','{\'load_id\': 120}','ExponentPushToken[M9ekQvEsJM6d9ZmWgLYG28]','2024-08-13 20:49:25.537632'),(3,'CARGA DEVOLVIDA COM SUCESSO','Olá policial, a sua descarga de equipamentos se encontra ok!','{\'load_id\': 121}','ExponentPushToken[M9ekQvEsJM6d9ZmWgLYG28]','2024-08-13 20:55:11.919097'),(4,'CARGA REALIZADA','Olá policial, nova carga realizada por Anthonius Miguel!','{\'load_id\': 122}','ExponentPushToken[M9ekQvEsJM6d9ZmWgLYG28]','2024-08-15 13:18:33.598438'),(5,'CARGA DEVOLVIDA COM SUCESSO','Olá policial, a sua descarga de equipamentos se encontra ok!','{\'load_id\': 123}','ExponentPushToken[M9ekQvEsJM6d9ZmWgLYG28]','2024-08-15 13:36:54.099865'),(6,'CARGA REALIZADA','Olá policial, nova carga realizada por Anthonius Miguel!','{\'load_id\': 124}','ExponentPushToken[M9ekQvEsJM6d9ZmWgLYG28]','2024-08-16 12:47:25.256854'),(7,'CARGA REALIZADA','Olá policial, nova carga realizada por Anthonius Miguel!','{\'load_id\': 125}','ExponentPushToken[M9ekQvEsJM6d9ZmWgLYG28]','2024-08-22 05:10:52.400039'),(8,'CARGA DEVOLVIDA COM SUCESSO','Olá policial, a sua descarga de equipamentos se encontra ok!','{\'load_id\': 126}','ExponentPushToken[M9ekQvEsJM6d9ZmWgLYG28]','2024-08-22 05:11:53.607905'),(9,'CARGA REALIZADA','Olá policial, nova carga realizada por Anthonius Miguel!','{\'load_id\': 127}','ExponentPushToken[M9ekQvEsJM6d9ZmWgLYG28]','2024-08-23 19:43:37.099970'),(10,'CARGA DEVOLVIDA COM SUCESSO','Olá policial, a sua descarga de equipamentos se encontra ok!','{\'load_id\': 128}','ExponentPushToken[M9ekQvEsJM6d9ZmWgLYG28]','2024-08-23 19:44:24.818099'),(11,'CARGA REALIZADA','Olá policial, nova carga realizada por Anthonius Miguel!','{\'load_id\': 129}','ExponentPushToken[M9ekQvEsJM6d9ZmWgLYG28]','2024-09-02 19:08:07.669401'),(12,'CARGA REALIZADA','Olá policial, nova carga realizada por Anthonius Miguel!','{\'load_id\': 130}','ExponentPushToken[M9ekQvEsJM6d9ZmWgLYG28]','2024-09-02 19:11:28.580647'),(13,'CARGA DEVOLVIDA COM SUCESSO','Olá policial, a sua descarga de equipamentos se encontra ok!','{\'load_id\': 131}','ExponentPushToken[M9ekQvEsJM6d9ZmWgLYG28]','2024-09-02 19:14:19.689639'),(14,'CARGA REALIZADA','Olá policial, nova carga realizada por Anthonius Miguel!','{\'load_id\': 132}','ExponentPushToken[M9ekQvEsJM6d9ZmWgLYG28]','2024-09-11 23:58:09.726087'),(15,'CARGA REALIZADA','Olá policial, nova carga realizada por Anthonius Miguel!','{\'load_id\': 133}','ExponentPushToken[M9ekQvEsJM6d9ZmWgLYG28]','2024-09-12 00:58:28.657727'),(16,'CARGA DEVOLVIDA COM SUCESSO','Olá policial, a sua descarga de equipamentos se encontra ok!','{\'load_id\': 134}','ExponentPushToken[M9ekQvEsJM6d9ZmWgLYG28]','2024-09-12 00:58:59.005961'),(17,'CARGA DEVOLVIDA COM SUCESSO','Olá policial, a sua descarga de equipamentos se encontra ok!','{\'load_id\': 135}','ExponentPushToken[M9ekQvEsJM6d9ZmWgLYG28]','2024-09-12 00:59:40.482747'),(18,'CARGA REALIZADA','Olá policial, nova carga realizada por Anthonius Miguel!','{\'load_id\': 136}','ExponentPushToken[M9ekQvEsJM6d9ZmWgLYG28]','2024-09-13 14:50:14.351365'),(19,'CARGA REALIZADA','Olá policial, nova carga realizada por Anthonius Miguel!','{\'load_id\': 137}','ExponentPushToken[M9ekQvEsJM6d9ZmWgLYG28]','2024-09-13 14:59:57.264207'),(20,'CARGA REALIZADA','Olá policial, nova carga realizada por Anthonius Miguel!','{\'load_id\': 138}','ExponentPushToken[M9ekQvEsJM6d9ZmWgLYG28]','2024-09-25 20:42:17.983684'),(21,'CARGA REALIZADA','Olá policial, nova carga realizada por Anthonius Miguel!','{\'load_id\': 139}','ExponentPushToken[M9ekQvEsJM6d9ZmWgLYG28]','2024-09-25 21:22:32.268915'),(22,'CARGA REALIZADA','Olá policial, nova carga realizada por Anthonius Miguel!','{\'load_id\': 140}','ExponentPushToken[M9ekQvEsJM6d9ZmWgLYG28]','2024-09-25 22:50:12.704488'),(23,'CARGA DEVOLVIDA COM SUCESSO','Olá policial, a sua descarga de equipamentos se encontra ok!','{\'load_id\': 141}','ExponentPushToken[M9ekQvEsJM6d9ZmWgLYG28]','2024-09-25 22:56:03.719389'),(24,'CARGA DEVOLVIDA COM SUCESSO','Olá policial, a sua descarga de equipamentos se encontra ok!','{\'load_id\': 142}','ExponentPushToken[M9ekQvEsJM6d9ZmWgLYG28]','2024-10-08 11:07:12.614420'),(25,'CARGA REALIZADA','Olá policial, nova carga realizada por Anthonius Miguel!','{\'load_id\': 143}','ExponentPushToken[M9ekQvEsJM6d9ZmWgLYG28]','2024-12-08 14:42:27.512796');
/*!40000 ALTER TABLE `notifications_app_mobile_notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `police_police`
--

DROP TABLE IF EXISTS `police_police`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `police_police` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `activated` int NOT NULL,
  `matricula` varchar(20) NOT NULL,
  `telefone` varchar(20) NOT NULL,
  `lotacao` varchar(50) NOT NULL,
  `posto` varchar(50) NOT NULL,
  `image_path` varchar(100) NOT NULL,
  `tipo` varchar(20) NOT NULL,
  `name` varchar(200) NOT NULL,
  `activator_id` bigint DEFAULT NULL,
  `fingerprint` varchar(250) DEFAULT NULL,
  `pushToken` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `telefone` (`telefone`),
  UNIQUE KEY `name` (`name`),
  KEY `police_police_activator_id_cc99b9cc_fk_police_police_id` (`activator_id`),
  CONSTRAINT `police_police_activator_id_cc99b9cc_fk_police_police_id` FOREIGN KEY (`activator_id`) REFERENCES `police_police` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `police_police`
--

LOCK TABLES `police_police` WRITE;
/*!40000 ALTER TABLE `police_police` DISABLE KEYS */;
INSERT INTO `police_police` VALUES (3,'pbkdf2_sha256$720000$kex2hz8CGHzdTqokHZZFRq$jY2Qq/SAgQoNLYXWSYxia3CTc280DvZG7aJGAVanQmc=','2024-09-02 19:16:57.217383',1,'admin','','','',1,1,'2023-10-06 22:29:56.561030',1,'','123','','','','Police','Ediel',3,NULL,NULL),(4,'pbkdf2_sha256$720000$JXgc22LnonW2oqSRyIMuxN$w0Euk6tc0RK9wo4OlbOhDgQ193UsxgCIpPeeufh73KY=','2024-12-08 22:29:36.726169',0,'Ediel','','','edielromily7@gmail.com',0,1,'2023-10-07 00:27:39.840923',1,'123','+5577991083244','GBI','Soldado','policiais/2023-10-06/ediel_dStLppJ.jpg','Police','ediel romily',3,NULL,'ExponentPushToken[M9ekQvEsJM6d9ZmWgLYG28]'),(5,'pbkdf2_sha256$720000$NkYy8CiNjMX5RaNCnndxU7$6v7xEFkpwIlbG9TJDF6V3qgxdeFsWj3nl7AZw9R9BJA=','2024-01-19 16:04:40.529206',0,'Jessica','','','jessicaar1@hotmail.com',0,1,'2024-01-19 14:46:10.642470',1,'306475963','77 99954 4220','38º CIPM','Soldado','policiais/2024-01-19/imagem_2024-01-19_114600272.png','Adjunto','Jéssica Alves Reis',3,'1',NULL),(7,'pbkdf2_sha256$720000$lAZ1imeKdhT6ry489IlX8e$lqfJSRTVXKOJKykqg8QvhDiVzmoDaBIbZ36FW08ZLW0=','2024-12-08 22:33:15.872724',1,'Anthonius','','','anthoniusmiguel@gmail.com',1,1,'2024-05-20 03:18:37.998390',1,'','','','','','Policial','',7,NULL,NULL),(8,'pbkdf2_sha256$720000$ExNPTcSVr5LlwbfO4hWl0S$4mtZlTrJgvdNEmFm6XytIMv335h8+J5uLVGaiQqw4aE=','2024-09-12 00:09:26.289529',0,'anthonius_policial','','','anthoniusmiguel@gmail.com',0,1,'2024-06-06 14:14:28.002203',1,'202110024','77999255474','4º CIPM','Major','policiais/2024-06-06/fot_anthonius.png','Policial','Anthonius Souza',7,NULL,'ExponentPushToken[M9ekQvEsJM6d9ZmWgLYG28]'),(9,'pbkdf2_sha256$720000$dn8DDCizCzsZeLsXsEaXMX$lF7AWbJkEbKbRbzvOtpa6z1t8Mtmp/SCNGs92d8VFMI=','2024-12-08 22:33:38.081073',0,'anthonius_adjunto','','','anthoniusmessi@gmail.com',0,1,'2024-06-28 20:36:49.850523',1,'20211','77999255473','38º CIPM','Aspirante','policiais/2024-06-28/fot_anthonius.png','Adjunto','Anthonius Miguel',7,NULL,NULL);
/*!40000 ALTER TABLE `police_police` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `police_police_groups`
--

DROP TABLE IF EXISTS `police_police_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `police_police_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `police_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `police_police_groups_police_id_group_id_64b060f7_uniq` (`police_id`,`group_id`),
  KEY `police_police_groups_group_id_aff6a325_fk_auth_group_id` (`group_id`),
  CONSTRAINT `police_police_groups_group_id_aff6a325_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `police_police_groups_police_id_e73596cf_fk_police_police_id` FOREIGN KEY (`police_id`) REFERENCES `police_police` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `police_police_groups`
--

LOCK TABLES `police_police_groups` WRITE;
/*!40000 ALTER TABLE `police_police_groups` DISABLE KEYS */;
INSERT INTO `police_police_groups` VALUES (13,3,3),(12,4,4),(11,5,3),(14,7,4),(15,8,4),(17,9,3);
/*!40000 ALTER TABLE `police_police_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `police_police_user_permissions`
--

DROP TABLE IF EXISTS `police_police_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `police_police_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `police_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `police_police_user_permi_police_id_permission_id_2238c6b7_uniq` (`police_id`,`permission_id`),
  KEY `police_police_user_p_permission_id_fb01c691_fk_auth_perm` (`permission_id`),
  CONSTRAINT `police_police_user_p_permission_id_fb01c691_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `police_police_user_p_police_id_744319bf_fk_police_po` FOREIGN KEY (`police_id`) REFERENCES `police_police` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `police_police_user_permissions`
--

LOCK TABLES `police_police_user_permissions` WRITE;
/*!40000 ALTER TABLE `police_police_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `police_police_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `report_report`
--

DROP TABLE IF EXISTS `report_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `report_report` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(256) NOT NULL,
  `date_creation` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `report_report`
--

LOCK TABLES `report_report` WRITE;
/*!40000 ALTER TABLE `report_report` DISABLE KEYS */;
INSERT INTO `report_report` VALUES (1,'Relatório de carga','2024-01-17 00:10:19.654705'),(2,'Relatório de carga','2024-01-17 00:34:05.019995'),(3,'Relatório de carga','2024-01-17 03:55:14.386099'),(4,'Relatório de carga','2024-01-17 03:55:14.386099'),(5,'Relatório de carga','2024-01-17 05:13:45.189676'),(6,'Relatório de carga','2024-01-17 05:17:29.528467'),(7,'Relatório de carga','2024-01-17 05:17:29.528467'),(8,'Relatório de carga','2024-01-17 05:17:29.528467'),(9,'Relatório de carga','2024-01-17 05:17:29.528467'),(10,'Relatório de carga','2024-01-17 05:30:54.803307'),(11,'Relatório de carga','2024-01-18 22:41:49.322409'),(12,'Relatório de carga','2024-01-18 22:41:49.322409'),(13,'Relatório de carga','2024-01-18 22:41:49.322409'),(14,'Relatório de carga','2024-01-19 00:13:57.474987'),(15,'Relatório de carga','2024-01-19 01:09:41.169767'),(16,'Relatório de carga','2024-01-19 01:09:41.169767'),(17,'Relatório de carga','2024-01-19 01:09:41.169767'),(18,'Relatório de carga','2024-01-19 15:21:17.883954'),(19,'Relatório de carga','2024-01-19 15:41:55.468865'),(20,'Relatório de carga','2024-01-19 15:41:55.468865'),(21,'Relatório de carga','2024-02-06 15:39:39.844915'),(22,'Relatório de carga','2024-02-06 15:39:39.844915'),(23,'Relatório de carga','2024-02-06 15:39:39.844915'),(24,'Relatório de carga','2024-02-06 19:01:26.519356'),(25,'Relatório de carga','2024-09-13 14:58:30.412173'),(26,'Relatório de carga','2024-09-25 20:40:57.598102'),(27,'Relatório de carga','2024-09-25 21:21:38.278356'),(28,'Relatório de carga','2024-09-25 22:48:52.462782'),(29,'Relatório de carga','2024-12-08 14:12:16.340561');
/*!40000 ALTER TABLE `report_report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `report_report_field`
--

DROP TABLE IF EXISTS `report_report_field`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `report_report_field` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `field` longtext,
  `content` longtext,
  `report_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `report_report_field_report_id_c2172ca6_fk_report_report_id` (`report_id`),
  CONSTRAINT `report_report_field_report_id_c2172ca6_fk_report_report_id` FOREIGN KEY (`report_id`) REFERENCES `report_report` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=413 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `report_report_field`
--

LOCK TABLES `report_report_field` WRITE;
/*!40000 ALTER TABLE `report_report_field` DISABLE KEYS */;
INSERT INTO `report_report_field` VALUES (1,'Data de Carga:','17/01/2024 00:30',1),(2,'Data Prevista de Devolução:','17/01/2024 03:30',1),(3,'Data de Descarregamento:','N/A',1),(4,'Tipo de Turno:','6H',1),(5,'Status:','-',1),(6,'Policial:','ediel romily',1),(7,'Adjunto:','Ediel',1),(8,'Informações dos equipamentos',NULL,1),(9,'Equipamento','9mm',1),(10,'Quantidade','100',1),(11,'Observação','-',1),(12,'Status','Pendente',1),(13,'Data de Carga:','17/01/2024 00:36',2),(14,'Data Prevista de Devolução:','N/A',2),(15,'Data de Descarregamento:','16/01/2024 21:36',2),(16,'Tipo de Turno:','descarga',2),(17,'Status:','descarga',2),(18,'Policial:','ediel romily',2),(19,'Adjunto:','Ediel',2),(20,'Informações dos equipamentos',NULL,2),(21,'Equipamento','9mm',2),(22,'Quantidade','50',2),(23,'Observação','-',2),(24,'Status','Retorno',2),(25,'Data de Carga:','17/01/2024 04:00',3),(26,'Data Prevista de Devolução:','17/01/2024 07:00',3),(27,'Data de Descarregamento:','N/A',3),(28,'Tipo de Turno:','6H',3),(29,'Status:','-',3),(30,'Policial:','ediel romily',3),(31,'Adjunto:','Ediel',3),(32,'Informações dos equipamentos',NULL,3),(33,'Equipamento','9mm',3),(34,'Quantidade','100',3),(35,'Observação','-',3),(36,'Status','Pendente',3),(37,'Equipamento','Bastão',3),(38,'Quantidade','1',3),(39,'Observação','-',3),(40,'Status','Pendente',3),(41,'Data de Carga:','17/01/2024 04:01',4),(42,'Data Prevista de Devolução:','N/A',4),(43,'Data de Descarregamento:','17/01/2024 01:01',4),(44,'Tipo de Turno:','descarga',4),(45,'Status:','descarga',4),(46,'Policial:','ediel romily',4),(47,'Adjunto:','Ediel',4),(48,'Informações dos equipamentos',NULL,4),(49,'Equipamento','9mm',4),(50,'Quantidade','10',4),(51,'Observação','-',4),(52,'Status','Retorno',4),(53,'Data de Carga:','17/01/2024 05:14',5),(54,'Data Prevista de Devolução:','N/A',5),(55,'Data de Descarregamento:','17/01/2024 02:14',5),(56,'Tipo de Turno:','descarga',5),(57,'Status:','descarga',5),(58,'Policial:','ediel romily',5),(59,'Adjunto:','Ediel',5),(60,'Informações dos equipamentos',NULL,5),(61,'Equipamento','9mm',5),(62,'Quantidade','10',5),(63,'Observação','werhert',5),(64,'Status','Retorno',5),(65,'Data de Carga:','17/01/2024 05:18',6),(66,'Data Prevista de Devolução:','N/A',6),(67,'Data de Descarregamento:','17/01/2024 02:18',6),(68,'Tipo de Turno:','descarga',6),(69,'Status:','descarga',6),(70,'Policial:','ediel romily',6),(71,'Adjunto:','Ediel',6),(72,'Informações dos equipamentos',NULL,6),(73,'Equipamento','9mm',6),(74,'Quantidade','70',6),(75,'Observação','-',6),(76,'Status','Retorno',6),(77,'Data de Carga:','17/01/2024 05:18',7),(78,'Data Prevista de Devolução:','17/01/2024 08:18',7),(79,'Data de Descarregamento:','N/A',7),(80,'Tipo de Turno:','6H',7),(81,'Status:','-',7),(82,'Policial:','ediel romily',7),(83,'Adjunto:','Ediel',7),(84,'Informações dos equipamentos',NULL,7),(85,'Equipamento','9mm',7),(86,'Quantidade','100',7),(87,'Observação','-',7),(88,'Status','Pendente',7),(89,'Data de Carga:','17/01/2024 05:19',8),(90,'Data Prevista de Devolução:','N/A',8),(91,'Data de Descarregamento:','17/01/2024 02:19',8),(92,'Tipo de Turno:','descarga',8),(93,'Status:','descarga',8),(94,'Policial:','ediel romily',8),(95,'Adjunto:','Ediel',8),(96,'Informações dos equipamentos',NULL,8),(97,'Equipamento','Bastão',8),(98,'Quantidade','1',8),(99,'Observação','-',8),(100,'Status','Retorno',8),(101,'Data de Carga:','17/01/2024 05:19',9),(102,'Data Prevista de Devolução:','N/A',9),(103,'Data de Descarregamento:','17/01/2024 02:19',9),(104,'Tipo de Turno:','descarga',9),(105,'Status:','descarga',9),(106,'Policial:','ediel romily',9),(107,'Adjunto:','Ediel',9),(108,'Informações dos equipamentos',NULL,9),(109,'Equipamento','9mm',9),(110,'Quantidade','10',9),(111,'Observação','ertyjrwrtyjwr',9),(112,'Status','Justificado',9),(113,'Data de Carga:','17/01/2024 05:31',10),(114,'Data Prevista de Devolução:','N/A',10),(115,'Data de Descarregamento:','17/01/2024 02:31',10),(116,'Tipo de Turno:','descarga',10),(117,'Status:','descarga',10),(118,'Policial:','ediel romily',10),(119,'Adjunto:','Ediel',10),(120,'Informações dos equipamentos',NULL,10),(121,'Equipamento','9mm',10),(122,'Quantidade','10',10),(123,'Observação','adsasd',10),(124,'Status','Retorno',10),(125,'Data de Carga:','18/01/2024 22:45',11),(126,'Data Prevista de Devolução:','19/01/2024 01:45',11),(127,'Data de Descarregamento:','N/A',11),(128,'Tipo de Turno:','6H',11),(129,'Status:','-',11),(130,'Policial:','ediel romily',11),(131,'Adjunto:','Ediel',11),(132,'Informações dos equipamentos',NULL,11),(133,'Equipamento','Bastão',11),(134,'Quantidade','1',11),(135,'Observação','-',11),(136,'Status','Pendente',11),(137,'Equipamento','9mm',11),(138,'Quantidade','100',11),(139,'Observação','-',11),(140,'Status','Pendente',11),(141,'Data de Carga:','18/01/2024 22:46',12),(142,'Data Prevista de Devolução:','N/A',12),(143,'Data de Descarregamento:','18/01/2024 19:46',12),(144,'Tipo de Turno:','descarga',12),(145,'Status:','descarga',12),(146,'Policial:','ediel romily',12),(147,'Adjunto:','Ediel',12),(148,'Informações dos equipamentos',NULL,12),(149,'Equipamento','9mm',12),(150,'Quantidade','10',12),(151,'Observação','usado em campo',12),(152,'Status','Retorno',12),(153,'Data de Carga:','18/01/2024 22:48',13),(154,'Data Prevista de Devolução:','N/A',13),(155,'Data de Descarregamento:','18/01/2024 19:48',13),(156,'Tipo de Turno:','descarga',13),(157,'Status:','descarga',13),(158,'Policial:','ediel romily',13),(159,'Adjunto:','Ediel',13),(160,'Informações dos equipamentos',NULL,13),(161,'Equipamento','Bastão',13),(162,'Quantidade','1',13),(163,'Observação','-',13),(164,'Status','Retorno',13),(165,'Data de Carga:','19/01/2024 00:15',14),(166,'Data Prevista de Devolução:','19/01/2024 03:15',14),(167,'Data de Descarregamento:','N/A',14),(168,'Tipo de Turno:','6H',14),(169,'Status:','-',14),(170,'Policial:','ediel romily',14),(171,'Adjunto:','Ediel',14),(172,'Informações dos equipamentos',NULL,14),(173,'Equipamento','9mm',14),(174,'Quantidade','100',14),(175,'Observação','-',14),(176,'Status','Pendente',14),(177,'Equipamento','Bastão',14),(178,'Quantidade','1',14),(179,'Observação','-',14),(180,'Status','Pendente',14),(181,'Equipamento','Capacete',14),(182,'Quantidade','1',14),(183,'Observação','-',14),(184,'Status','Pendente',14),(185,'Data de Carga:','19/01/2024 01:10',15),(186,'Data Prevista de Devolução:','N/A',15),(187,'Data de Descarregamento:','N/A',15),(188,'Tipo de Turno:','CONSERTO',15),(189,'Status:','-',15),(190,'Policial:','ediel romily',15),(191,'Adjunto:','Ediel',15),(192,'Informações dos equipamentos',NULL,15),(193,'Equipamento','9mm',15),(194,'Quantidade','100',15),(195,'Observação','-',15),(196,'Status','Pendente',15),(197,'Data de Carga:','19/01/2024 01:14',16),(198,'Data Prevista de Devolução:','N/A',16),(199,'Data de Descarregamento:','18/01/2024 22:14',16),(200,'Tipo de Turno:','descarga',16),(201,'Status:','descarga',16),(202,'Policial:','ediel romily',16),(203,'Adjunto:','Ediel',16),(204,'Informações dos equipamentos',NULL,16),(205,'Equipamento','9mm',16),(206,'Quantidade','10',16),(207,'Observação','-',16),(208,'Status','Devolvido',16),(209,'Data de Carga:','19/01/2024 01:17',17),(210,'Data Prevista de Devolução:','N/A',17),(211,'Data de Descarregamento:','18/01/2024 22:17',17),(212,'Tipo de Turno:','descarga',17),(213,'Status:','descarga',17),(214,'Policial:','ediel romily',17),(215,'Adjunto:','Ediel',17),(216,'Informações dos equipamentos',NULL,17),(217,'Equipamento','9mm',17),(218,'Quantidade','90',17),(219,'Observação','-',17),(220,'Status','Devolvido',17),(221,'Data de Carga:','19/01/2024 15:30',18),(222,'Data Prevista de Devolução:','20/01/2024 12:30',18),(223,'Data de Descarregamento:','N/A',18),(224,'Tipo de Turno:','24H',18),(225,'Status:','-',18),(226,'Policial:','Jéssica Alves Reis',18),(227,'Adjunto:','Ediel',18),(228,'Informações dos equipamentos',NULL,18),(229,'Equipamento','TAURUS PT100',18),(230,'Quantidade','1',18),(231,'Observação','-',18),(232,'Status','Pendente',18),(233,'Equipamento','9mm',18),(234,'Quantidade','24',18),(235,'Observação','-',18),(236,'Status','Pendente',18),(237,'Equipamento','Bastão',18),(238,'Quantidade','1',18),(239,'Observação','-',18),(240,'Status','Pendente',18),(241,'Data de Carga:','19/01/2024 15:51',19),(242,'Data Prevista de Devolução:','N/A',19),(243,'Data de Descarregamento:','19/01/2024 12:51',19),(244,'Tipo de Turno:','descarga',19),(245,'Status:','descarga',19),(246,'Policial:','Jéssica Alves Reis',19),(247,'Adjunto:','Ediel',19),(248,'Informações dos equipamentos',NULL,19),(249,'Equipamento','Bastão',19),(250,'Quantidade','1',19),(251,'Observação','-',19),(252,'Status','Devolvido',19),(253,'Equipamento','9mm',19),(254,'Quantidade','21',19),(255,'Observação','disparos ocorridos no dia tal ...',19),(256,'Status','Devolvido',19),(257,'Data de Carga:','19/01/2024 15:55',20),(258,'Data Prevista de Devolução:','N/A',20),(259,'Data de Descarregamento:','19/01/2024 12:55',20),(260,'Tipo de Turno:','descarga',20),(261,'Status:','descarga',20),(262,'Policial:','Jéssica Alves Reis',20),(263,'Adjunto:','Ediel',20),(264,'Informações dos equipamentos',NULL,20),(265,'Equipamento','TAURUS PT100',20),(266,'Quantidade','1',20),(267,'Observação','-',20),(268,'Status','Devolvido',20),(269,'Data de Carga:','06/02/2024 15:43',21),(270,'Data Prevista de Devolução:','06/02/2024 18:43',21),(271,'Data de Descarregamento:','N/A',21),(272,'Tipo de Turno:','6H',21),(273,'Status:','-',21),(274,'Policial:','ediel romily',21),(275,'Adjunto:','Ediel',21),(276,'Informações dos equipamentos',NULL,21),(277,'Equipamento','Glok G22',21),(278,'Quantidade','1',21),(279,'Observação','-',21),(280,'Status','Pendente',21),(281,'Equipamento','Glok 9mm',21),(282,'Quantidade','1',21),(283,'Observação','-',21),(284,'Status','Pendente',21),(285,'Equipamento','9mm',21),(286,'Quantidade','100',21),(287,'Observação','-',21),(288,'Status','Pendente',21),(289,'Equipamento','TAURUS PT100',21),(290,'Quantidade','1',21),(291,'Observação','-',21),(292,'Status','Pendente',21),(293,'Data de Carga:','06/02/2024 15:54',22),(294,'Data Prevista de Devolução:','N/A',22),(295,'Data de Descarregamento:','06/02/2024 12:54',22),(296,'Tipo de Turno:','descarga',22),(297,'Status:','descarga',22),(298,'Policial:','ediel romily',22),(299,'Adjunto:','Ediel',22),(300,'Informações dos equipamentos',NULL,22),(301,'Equipamento','Glok 9mm',22),(302,'Quantidade','1',22),(303,'Observação','-',22),(304,'Status','Devolvido',22),(305,'Equipamento','Glok G22',22),(306,'Quantidade','1',22),(307,'Observação','-',22),(308,'Status','Devolvido',22),(309,'Equipamento','9mm',22),(310,'Quantidade','90',22),(311,'Observação','disparo durante a operação',22),(312,'Status','Devolvido',22),(313,'Data de Carga:','06/02/2024 15:57',23),(314,'Data Prevista de Devolução:','N/A',23),(315,'Data de Descarregamento:','06/02/2024 12:57',23),(316,'Tipo de Turno:','descarga',23),(317,'Status:','descarga',23),(318,'Policial:','ediel romily',23),(319,'Adjunto:','Ediel',23),(320,'Informações dos equipamentos',NULL,23),(321,'Equipamento','TAURUS PT100',23),(322,'Quantidade','1',23),(323,'Observação','-',23),(324,'Status','Devolvido',23),(325,'Data de Carga:','06/02/2024 19:13',24),(326,'Data Prevista de Devolução:','07/02/2024 04:13',24),(327,'Data de Descarregamento:','N/A',24),(328,'Tipo de Turno:','12H',24),(329,'Status:','-',24),(330,'Policial:','ediel romily',24),(331,'Adjunto:','Ediel',24),(332,'Informações dos equipamentos',NULL,24),(333,'Equipamento','TAURUS PT100',24),(334,'Quantidade','1',24),(335,'Observação','-',24),(336,'Status','Pendente',24),(337,'Equipamento','9mm',24),(338,'Quantidade','776',24),(339,'Observação','-',24),(340,'Status','Pendente',24),(341,'Equipamento','Capacete',24),(342,'Quantidade','1',24),(343,'Observação','-',24),(344,'Status','Pendente',24),(345,'Data de Carga:','13/09/2024 11:58',25),(346,'Data Prevista de Devolução:','13/09/2024 23:59',25),(347,'Data de Descarregamento:','N/A',25),(348,'Tipo de Turno:','12H',25),(349,'Status:','-',25),(350,'Policial:','Anthonius Miguel Vaz Figueiredo Souza',25),(351,'Adjunto:','Anthonius Miguel',25),(352,'Informações dos equipamentos',NULL,25),(353,'Equipamento','Glok G22',25),(354,'Quantidade','1',25),(355,'Observação','-',25),(356,'Status','Pendente',25),(357,'Data de Carga:','25/09/2024 17:40',26),(358,'Data Prevista de Devolução:','26/09/2024 05:42',26),(359,'Data de Descarregamento:','N/A',26),(360,'Tipo de Turno:','12H',26),(361,'Status:','-',26),(362,'Policial:','Anthonius Miguel Vaz Figueiredo Souza',26),(363,'Adjunto:','Anthonius Miguel',26),(364,'Informações dos equipamentos',NULL,26),(365,'Equipamento','TAURUS PT100',26),(366,'Quantidade','1',26),(367,'Observação','-',26),(368,'Status','Pendente',26),(369,'Equipamento','9mm',26),(370,'Quantidade','1',26),(371,'Observação','-',26),(372,'Status','Pendente',26),(373,'Data de Carga:','25/09/2024 18:21',27),(374,'Data Prevista de Devolução:','26/09/2024 06:22',27),(375,'Data de Descarregamento:','N/A',27),(376,'Tipo de Turno:','12H',27),(377,'Status:','-',27),(378,'Policial:','Anthonius Miguel Vaz Figueiredo Souza',27),(379,'Adjunto:','Anthonius Miguel',27),(380,'Informações dos equipamentos',NULL,27),(381,'Equipamento','Glok G22',27),(382,'Quantidade','1',27),(383,'Observação','-',27),(384,'Status','Pendente',27),(385,'Equipamento','9mm',27),(386,'Quantidade','49',27),(387,'Observação','-',27),(388,'Status','Pendente',27),(389,'Data de Carga:','25/09/2024 19:48',28),(390,'Data Prevista de Devolução:','26/09/2024 07:50',28),(391,'Data de Descarregamento:','N/A',28),(392,'Tipo de Turno:','12H',28),(393,'Status:','-',28),(394,'Policial:','Anthonius Miguel Vaz Figueiredo Souza',28),(395,'Adjunto:','Anthonius Miguel',28),(396,'Informações dos equipamentos',NULL,28),(397,'Equipamento','9mm',28),(398,'Quantidade','0',28),(399,'Observação','-',28),(400,'Status','Pendente',28),(401,'Data de Carga:','08/12/2024 11:12',29),(402,'Data Prevista de Devolução:','08/12/2024 23:42',29),(403,'Data de Descarregamento:','N/A',29),(404,'Tipo de Turno:','12H',29),(405,'Status:','-',29),(406,'Policial:','Anthonius Miguel Vaz Figueiredo Souza',29),(407,'Adjunto:','Anthonius Miguel',29),(408,'Informações dos equipamentos',NULL,29),(409,'Equipamento','Glok G22',29),(410,'Quantidade','1',29),(411,'Observação','-',29),(412,'Status','Pendente',29);
/*!40000 ALTER TABLE `report_report_field` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'sicomb'
--

--
-- Dumping routines for database 'sicomb'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-09  1:14:53
