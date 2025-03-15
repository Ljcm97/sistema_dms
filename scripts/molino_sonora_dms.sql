-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: molino_sonora_dms
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('c3f8fb049f40');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `areas`
--

DROP TABLE IF EXISTS `areas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `areas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  `activo` tinyint(1) DEFAULT '1',
  `creado_en` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `areas`
--

LOCK TABLES `areas` WRITE;
/*!40000 ALTER TABLE `areas` DISABLE KEYS */;
INSERT INTO `areas` VALUES (1,'GERENTE GENERAL',NULL,1,'2025-03-08 10:51:50'),(2,'GERENTE OPERATIVO',NULL,1,'2025-03-08 10:51:50'),(3,'GERENTE ADMINISTRATIVA Y FINANCIERA',NULL,1,'2025-03-08 10:51:50'),(4,'CONTRALORÍA',NULL,1,'2025-03-08 10:51:50'),(5,'ASISTENTE ADMINISTRATIVO',NULL,1,'2025-03-08 10:51:50'),(6,'SUPERNUMERARIO',NULL,1,'2025-03-08 10:51:50'),(7,'SISTEMAS',NULL,1,'2025-03-08 10:51:50'),(8,'TESORERÍA',NULL,1,'2025-03-08 10:51:50'),(9,'COMPRAS PADDY',NULL,1,'2025-03-08 10:51:50'),(10,'CONTABILIDAD',NULL,1,'2025-03-08 10:51:50'),(11,'FLETES',NULL,1,'2025-03-08 10:51:50'),(12,'COSTOS',NULL,1,'2025-03-08 10:51:50'),(13,'AUDITORÍA',NULL,1,'2025-03-08 10:51:50'),(14,'CARTERA',NULL,1,'2025-03-08 10:51:50'),(15,'VENTAS',NULL,1,'2025-03-08 10:51:50'),(16,'RRHH',NULL,1,'2025-03-08 10:51:50'),(17,'FACTURACIÓN',NULL,1,'2025-03-08 10:51:50'),(18,'SST',NULL,1,'2025-03-08 10:51:50'),(19,'CALIDAD',NULL,1,'2025-03-08 10:51:50'),(20,'PRODUCCIÓN',NULL,1,'2025-03-08 10:51:50'),(21,'COMPRAS Y ALMACÉN',NULL,1,'2025-03-08 10:51:50'),(22,'ARCHIVO','',1,'2025-03-08 10:51:50'),(23,'RECEPCIÓN','',1,'2025-03-15 16:24:02');
/*!40000 ALTER TABLE `areas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cargos`
--

DROP TABLE IF EXISTS `cargos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cargos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  `activo` tinyint(1) DEFAULT NULL,
  `creado_en` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=217 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cargos`
--

LOCK TABLES `cargos` WRITE;
/*!40000 ALTER TABLE `cargos` DISABLE KEYS */;
INSERT INTO `cargos` VALUES (169,'FACTURADOR','',1,'2025-03-15 13:56:35'),(170,'ASISTENTE DE COMPRAS MATERIA PRIMA','',1,'2025-03-15 13:56:35'),(171,'SUPERNUMERARIO SST','',1,'2025-03-15 13:56:35'),(172,'ASISTENTE DE CONTABILIDAD','',1,'2025-03-15 13:56:35'),(173,'RECEPCIONISTA','',1,'2025-03-15 13:56:35'),(174,'JEFE DE COSTOS','',1,'2025-03-15 13:56:35'),(175,'AUXILIAR SST.','',1,'2025-03-15 13:56:35'),(176,'AUXILIAR DE COMPRAS MATERIA PRIMA','',1,'2025-03-15 13:56:35'),(177,'MENSAJERO','',1,'2025-03-15 13:56:35'),(178,'AUXILIAR DE CONTABILIDAD','',1,'2025-03-15 13:56:35'),(179,'GERENTE GENERAL','',1,'2025-03-15 13:56:35'),(180,'AUXILIAR CAFETERIA','',1,'2025-03-15 13:56:35'),(181,'AUXILIAR ADMINISTRATIVO','',1,'2025-03-15 13:56:35'),(182,'ANALISTA DE PROCESOS SAP','',1,'2025-03-15 13:56:35'),(183,'GERENTE OPERATIVO PLANTA LA MARIA','',1,'2025-03-15 13:56:35'),(184,'APRENDIZ SENA','',1,'2025-03-15 13:56:35'),(185,'GERENTE ADMINISTRATIVO Y FINANCIERO','',1,'2025-03-15 13:56:35'),(186,'JEFE DE AUDITORIA','',1,'2025-03-15 13:56:35'),(187,'JEFE DE SEGURIDAD Y SALUD EN EL TRABAJO','',1,'2025-03-15 13:56:35'),(188,'AUXILIAR DE TESORERIA','',1,'2025-03-15 13:56:35'),(189,'ASISTENTE ADMINISTRATIVO','',1,'2025-03-15 13:56:35'),(190,'AUXILIAR DE CARTERA','',1,'2025-03-15 13:56:35'),(191,'ANALISTA DE SISTEMAS','',1,'2025-03-15 13:56:35'),(192,'ALMACENISTA','',1,'2025-03-15 13:56:35'),(193,'ASISTENTE DE RECURSOS HUMANOS','',1,'2025-03-15 13:56:35'),(194,'COORDINADOR DE ARCHIVO','',1,'2025-03-15 13:56:35'),(195,'SUPERNUMERARIO','',1,'2025-03-15 13:56:35'),(196,'JEFE DE CARTERA','',1,'2025-03-15 13:56:35'),(197,'ASISTENTE DE TESORERIA','',1,'2025-03-15 13:56:35'),(198,'ASISTENTE DE CARTERA','',1,'2025-03-15 13:56:35'),(199,'AUXILIAR DE AUDITORIA','',1,'2025-03-15 13:56:35'),(200,'JEFE DE RECURSOS HUMANOS','',1,'2025-03-15 13:56:35'),(201,'TESORERO','',1,'2025-03-15 13:56:35'),(202,'CONDUCTOR','',1,'2025-03-15 13:56:35'),(203,'ASISTENTE DE CONTABILIDAD II','',1,'2025-03-15 13:56:35'),(204,'COMPRADOR MATERIA PRIMA TOLIMA CENTRO','',1,'2025-03-15 13:56:35'),(205,'CONTRALOR','',1,'2025-03-15 13:56:35'),(206,'ASISTENTE DE COSTOS','',1,'2025-03-15 13:56:35'),(207,'JEFE DE CONTABILIDAD','',1,'2025-03-15 13:56:35'),(208,'AUXILIAR DE ALMACEN','',1,'2025-03-15 13:56:35'),(209,'COMPRADOR MATERIA PRIMA TOLIMA SUR','',1,'2025-03-15 13:56:35'),(210,'JEFE DE COMPRAS Y ALMACEN','',1,'2025-03-15 13:56:35'),(211,'VENDEDOR','',1,'2025-03-15 13:56:35'),(212,'COORDINADOR DE VENTAS','',1,'2025-03-15 13:56:35'),(213,'AUXILIAR DE VENTAS','',1,'2025-03-15 13:56:35'),(214,'COORDINADOR DE DESPACHOS','',1,'2025-03-15 13:56:35'),(215,'SUPERVISOR DE VIGILANCIA','',1,'2025-03-15 13:56:35'),(216,'VIGILANTE','',1,'2025-03-15 13:56:35');
/*!40000 ALTER TABLE `cargos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `documentos`
--

DROP TABLE IF EXISTS `documentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `documentos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `radicado` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `fecha_recepcion` datetime NOT NULL,
  `transportadora_id` int DEFAULT NULL,
  `numero_guia` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `remitente` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tipo_documento_id` int NOT NULL,
  `contenido` text COLLATE utf8mb4_unicode_ci,
  `observaciones` text COLLATE utf8mb4_unicode_ci,
  `area_actual_id` int NOT NULL,
  `persona_actual_id` int DEFAULT NULL,
  `estado_id` int NOT NULL,
  `ruta_adjunto` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `es_entrada` tinyint(1) DEFAULT '1',
  `fecha_finalizacion` datetime DEFAULT NULL,
  `usuario_creacion_id` int NOT NULL,
  `usuario_actualizacion_id` int DEFAULT NULL,
  `creado_en` datetime DEFAULT CURRENT_TIMESTAMP,
  `actualizado_en` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `radicado` (`radicado`),
  KEY `area_actual_id` (`area_actual_id`),
  KEY `tipo_documento_id` (`tipo_documento_id`),
  KEY `persona_actual_id` (`persona_actual_id`),
  KEY `usuario_actualizacion_id` (`usuario_actualizacion_id`),
  KEY `transportadora_id` (`transportadora_id`),
  KEY `estado_id` (`estado_id`),
  KEY `usuario_creacion_id` (`usuario_creacion_id`),
  CONSTRAINT `documentos_ibfk_1` FOREIGN KEY (`area_actual_id`) REFERENCES `areas` (`id`),
  CONSTRAINT `documentos_ibfk_2` FOREIGN KEY (`tipo_documento_id`) REFERENCES `tipos_documento` (`id`),
  CONSTRAINT `documentos_ibfk_3` FOREIGN KEY (`persona_actual_id`) REFERENCES `personas` (`id`),
  CONSTRAINT `documentos_ibfk_4` FOREIGN KEY (`usuario_actualizacion_id`) REFERENCES `usuarios` (`id`),
  CONSTRAINT `documentos_ibfk_5` FOREIGN KEY (`transportadora_id`) REFERENCES `transportadoras` (`id`),
  CONSTRAINT `documentos_ibfk_6` FOREIGN KEY (`estado_id`) REFERENCES `estados_documento` (`id`),
  CONSTRAINT `documentos_ibfk_7` FOREIGN KEY (`usuario_creacion_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `documentos`
--

LOCK TABLES `documentos` WRITE;
/*!40000 ALTER TABLE `documentos` DISABLE KEYS */;
INSERT INTO `documentos` VALUES (1,'20250311-0001','2025-03-11 21:57:00',10,'0123456789','Lina',3,':)',':)',6,NULL,1,NULL,1,NULL,1,NULL,'2025-03-12 02:58:22',NULL),(2,'20250312-0001','2025-03-12 18:58:00',3,'159753','Albertano',9,'','',4,NULL,1,NULL,1,NULL,1,NULL,'2025-03-12 23:59:14',NULL);
/*!40000 ALTER TABLE `documentos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estados_documento`
--

DROP TABLE IF EXISTS `estados_documento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estados_documento` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  `color` varchar(7) COLLATE utf8mb4_unicode_ci DEFAULT '#000000',
  `creado_en` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estados_documento`
--

LOCK TABLES `estados_documento` WRITE;
/*!40000 ALTER TABLE `estados_documento` DISABLE KEYS */;
INSERT INTO `estados_documento` VALUES (1,'Recibido','Documento recibido en recepción','#3498db','2025-03-08 10:51:50'),(2,'En proceso','Documento en proceso de revisión','#f39c12','2025-03-08 10:51:50'),(3,'Transferido','Documento transferido a otra área','#9b59b6','2025-03-08 10:51:50'),(4,'Finalizado','Proceso completado','#2ecc71','2025-03-08 10:51:50'),(5,'Archivado','Documento archivado','#7f8c8d','2025-03-08 10:51:50');
/*!40000 ALTER TABLE `estados_documento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `historial_movimientos`
--

DROP TABLE IF EXISTS `historial_movimientos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historial_movimientos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `documento_id` int NOT NULL,
  `fecha_movimiento` datetime NOT NULL,
  `area_origen_id` int NOT NULL,
  `persona_origen_id` int DEFAULT NULL,
  `area_destino_id` int NOT NULL,
  `persona_destino_id` int DEFAULT NULL,
  `estado_id` int NOT NULL,
  `observaciones` text COLLATE utf8mb4_unicode_ci,
  `usuario_id` int NOT NULL,
  `creado_en` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `area_origen_id` (`area_origen_id`),
  KEY `documento_id` (`documento_id`),
  KEY `area_destino_id` (`area_destino_id`),
  KEY `persona_destino_id` (`persona_destino_id`),
  KEY `persona_origen_id` (`persona_origen_id`),
  KEY `estado_id` (`estado_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `historial_movimientos_ibfk_1` FOREIGN KEY (`area_origen_id`) REFERENCES `areas` (`id`),
  CONSTRAINT `historial_movimientos_ibfk_2` FOREIGN KEY (`documento_id`) REFERENCES `documentos` (`id`),
  CONSTRAINT `historial_movimientos_ibfk_3` FOREIGN KEY (`area_destino_id`) REFERENCES `areas` (`id`),
  CONSTRAINT `historial_movimientos_ibfk_4` FOREIGN KEY (`persona_destino_id`) REFERENCES `personas` (`id`),
  CONSTRAINT `historial_movimientos_ibfk_5` FOREIGN KEY (`persona_origen_id`) REFERENCES `personas` (`id`),
  CONSTRAINT `historial_movimientos_ibfk_6` FOREIGN KEY (`estado_id`) REFERENCES `estados_documento` (`id`),
  CONSTRAINT `historial_movimientos_ibfk_7` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historial_movimientos`
--

LOCK TABLES `historial_movimientos` WRITE;
/*!40000 ALTER TABLE `historial_movimientos` DISABLE KEYS */;
INSERT INTO `historial_movimientos` VALUES (1,1,'2025-03-11 21:57:00',7,NULL,6,NULL,1,'Registro inicial del documento',1,'2025-03-11 21:58:21'),(2,1,'2025-03-12 02:58:22',7,1,6,NULL,1,':)',1,'2025-03-12 02:58:22'),(3,2,'2025-03-12 18:58:00',7,NULL,4,NULL,1,'Registro inicial del documento',1,'2025-03-12 18:59:13'),(4,2,'2025-03-12 23:59:14',7,1,4,NULL,1,'',1,'2025-03-12 23:59:14');
/*!40000 ALTER TABLE `historial_movimientos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notificaciones`
--

DROP TABLE IF EXISTS `notificaciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notificaciones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int NOT NULL,
  `documento_id` int DEFAULT NULL,
  `mensaje` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `leida` tinyint(1) DEFAULT NULL,
  `creado_en` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `documento_id` (`documento_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `notificaciones_ibfk_1` FOREIGN KEY (`documento_id`) REFERENCES `documentos` (`id`),
  CONSTRAINT `notificaciones_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notificaciones`
--

LOCK TABLES `notificaciones` WRITE;
/*!40000 ALTER TABLE `notificaciones` DISABLE KEYS */;
/*!40000 ALTER TABLE `notificaciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `personas`
--

DROP TABLE IF EXISTS `personas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `personas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `apellido` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `telefono` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `area_id` int NOT NULL,
  `activo` tinyint(1) DEFAULT '1',
  `creado_en` datetime DEFAULT CURRENT_TIMESTAMP,
  `cargo_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `area_id` (`area_id`),
  KEY `cargo_id` (`cargo_id`),
  CONSTRAINT `personas_ibfk_1` FOREIGN KEY (`area_id`) REFERENCES `areas` (`id`),
  CONSTRAINT `personas_ibfk_2` FOREIGN KEY (`cargo_id`) REFERENCES `cargos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `personas`
--

LOCK TABLES `personas` WRITE;
/*!40000 ALTER TABLE `personas` DISABLE KEYS */;
INSERT INTO `personas` VALUES (1,'Ricardo Alexander','Bohórquez Méndez','rbohorquez@arrozsonora.com.co','311 2815201',7,1,'2025-03-08 16:10:16',170),(2,'Myriam','Rodríguez Arciniegas','mrodriguez@arrozsonora.com.co','318 5683317',4,1,'2025-03-08 16:59:35',NULL),(3,'Jairo Antonio','Lozano Vargas','sst@arrozsonora.com.co','310 2118013',18,1,'2025-03-08 17:10:04',NULL),(4,'Ana María','Rodríguez Mora','arodriguez@arrozsonora.com.co','',16,1,'2025-03-10 02:43:01',NULL),(5,'Jaime','Vargas Ramírez','jvargas@arrozsonora.com','',22,1,'2025-03-10 02:47:03',NULL),(7,'Olga Patricia','Ortiz Rivas','oortiz@arrozsonora.com.co','',21,1,'2025-03-10 02:48:43',NULL),(8,'Luis Alberto','Barreto Guzmán','lbarreto@arrozsonora.com.co','',21,1,'2025-03-10 02:49:26',NULL),(11,'Luis Alejandro','Oliveros Guarnizo','','',21,1,'2025-03-10 02:52:45',NULL),(13,'James Eduardo','Rueda Trujillo','jrueda@arrozsonora.com','',20,1,'2025-03-10 02:57:55',NULL),(14,'Martha Yaneth','Díaz Trigueros','mdiaz@arrozsonora.com.co','',8,1,'2025-03-11 16:08:04',NULL),(15,'Yazmina Lorena','Fayad Gutiérrez','yfayad@arrozsonora.com.co','',23,1,'2025-03-15 15:50:28',NULL),(16,'Yendy Fannory','Bravo Gutiérrez ','Aniiljulieth@hotmail.com','',17,1,'2025-03-15 21:19:37',NULL);
/*!40000 ALTER TABLE `personas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `privilegios`
--

DROP TABLE IF EXISTS `privilegios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `privilegios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int NOT NULL,
  `puede_registrar_documentos` tinyint(1) DEFAULT '0',
  `puede_ver_documentos_area` tinyint(1) DEFAULT '0',
  `creado_por` int NOT NULL,
  `creado_en` datetime DEFAULT CURRENT_TIMESTAMP,
  `actualizado_en` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  KEY `creado_por` (`creado_por`),
  CONSTRAINT `privilegios_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  CONSTRAINT `privilegios_ibfk_2` FOREIGN KEY (`creado_por`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `privilegios`
--

LOCK TABLES `privilegios` WRITE;
/*!40000 ALTER TABLE `privilegios` DISABLE KEYS */;
INSERT INTO `privilegios` VALUES (1,3,1,1,1,'2025-03-15 15:51:12','2025-03-15 16:46:07');
/*!40000 ALTER TABLE `privilegios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  `es_superadmin` tinyint(1) DEFAULT '0',
  `creado_en` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'Superadministrador','Control total del sistema',1,'2025-03-08 10:51:50'),(2,'Usuario','Acceso limitado a visualización de documentos',0,'2025-03-08 10:51:50');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipos_documento`
--

DROP TABLE IF EXISTS `tipos_documento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipos_documento` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  `activo` tinyint(1) DEFAULT '1',
  `creado_en` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipos_documento`
--

LOCK TABLES `tipos_documento` WRITE;
/*!40000 ALTER TABLE `tipos_documento` DISABLE KEYS */;
INSERT INTO `tipos_documento` VALUES (1,'Facturas',NULL,1,'2025-03-08 10:51:50'),(2,'Comprobantes',NULL,1,'2025-03-08 10:51:50'),(3,'Contratos',NULL,1,'2025-03-08 10:51:50'),(4,'Correspondencia',NULL,1,'2025-03-08 10:51:50'),(5,'Tiquetes',NULL,1,'2025-03-08 10:51:50'),(6,'Cotizaciones',NULL,1,'2025-03-08 10:51:50'),(7,'Órdenes de compra',NULL,1,'2025-03-08 10:51:50'),(9,'Hojas de vida',NULL,1,'2025-03-08 10:51:50'),(10,'Manuales',NULL,1,'2025-03-08 10:51:50'),(11,'Informes',NULL,1,'2025-03-08 10:51:50');
/*!40000 ALTER TABLE `tipos_documento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transportadoras`
--

DROP TABLE IF EXISTS `transportadoras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transportadoras` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  `activo` tinyint(1) DEFAULT '1',
  `creado_en` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transportadoras`
--

LOCK TABLES `transportadoras` WRITE;
/*!40000 ALTER TABLE `transportadoras` DISABLE KEYS */;
INSERT INTO `transportadoras` VALUES (1,'DEPRISA',NULL,1,'2025-03-08 10:51:50'),(2,'SERVIENTREGA',NULL,1,'2025-03-08 10:51:50'),(3,'ENVIA',NULL,1,'2025-03-08 10:51:50'),(4,'COORDINADORA',NULL,1,'2025-03-08 10:51:50'),(5,'SAFERBO',NULL,1,'2025-03-08 10:51:50'),(6,'INTERRAPIDISIMO',NULL,1,'2025-03-08 10:51:50'),(7,'AXPRESS',NULL,1,'2025-03-08 10:51:50'),(8,'REDETRANS',NULL,1,'2025-03-08 10:51:50'),(9,'TCC',NULL,1,'2025-03-08 10:51:50'),(10,'4-72','',1,'2025-03-08 10:51:50'),(11,'TRANSPRENSA',NULL,1,'2025-03-08 10:51:50'),(12,'PORTERÍA',NULL,1,'2025-03-08 10:51:50'),(13,'CERTIPOSTAL',NULL,1,'2025-03-08 10:51:50'),(14,'ENCO EXPRES',NULL,1,'2025-03-08 10:51:50'),(15,'X-CARGO',NULL,1,'2025-03-08 10:51:50'),(16,'DHL EXPRESS',NULL,1,'2025-03-08 10:51:50'),(17,'OPEN MARKET',NULL,1,'2025-03-08 10:51:50'),(18,'EXPRESO BOLIVARIANO',NULL,1,'2025-03-08 10:51:50'),(19,'MERCADOLIBRE',NULL,1,'2025-03-08 10:51:50'),(20,'INTERSERVICE',NULL,1,'2025-03-08 10:51:50');
/*!40000 ALTER TABLE `transportadoras` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `persona_id` int NOT NULL,
  `rol_id` int NOT NULL,
  `ultimo_acceso` datetime DEFAULT NULL,
  `activo` tinyint(1) DEFAULT '1',
  `creado_en` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `persona_id` (`persona_id`),
  KEY `rol_id` (`rol_id`),
  CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`persona_id`) REFERENCES `personas` (`id`),
  CONSTRAINT `usuarios_ibfk_2` FOREIGN KEY (`rol_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'admin','pbkdf2:sha256:600000$QGcwmQ2QjUQqEWLY$a8578b2aa6bcc13f1a12925801fed78a1ab40334f442282864afcb996ad6e959',1,1,'2025-03-15 21:16:57',1,'2025-03-08 16:10:16'),(2,'archivo','pbkdf2:sha256:600000$s9ZHOW1fQKDEqzsh$3530955ea9adc8130e9b08e16cef014208bd4328405c2ba4922fe945d92b1c4e',5,2,'2025-03-15 16:46:38',1,'2025-03-12 01:15:43'),(3,'Recepcion','pbkdf2:sha256:600000$QuA3nZtCAEv90k2y$8da98364c29d5140dcc10075781f3c05a59fb1b7ccd259ca93ed5d74da77266f',15,2,'2025-03-15 16:46:21',1,'2025-03-15 15:51:06');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `vista_documentos`
--

DROP TABLE IF EXISTS `vista_documentos`;
/*!50001 DROP VIEW IF EXISTS `vista_documentos`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vista_documentos` AS SELECT 
 1 AS `id`,
 1 AS `radicado`,
 1 AS `fecha_recepcion`,
 1 AS `transportadora`,
 1 AS `numero_guia`,
 1 AS `remitente`,
 1 AS `tipo_documento`,
 1 AS `contenido`,
 1 AS `observaciones`,
 1 AS `area_actual`,
 1 AS `persona_actual`,
 1 AS `estado`,
 1 AS `estado_color`,
 1 AS `ruta_adjunto`,
 1 AS `tipo_movimiento`,
 1 AS `fecha_finalizacion`,
 1 AS `creado_en`,
 1 AS `actualizado_en`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vista_historial`
--

DROP TABLE IF EXISTS `vista_historial`;
/*!50001 DROP VIEW IF EXISTS `vista_historial`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vista_historial` AS SELECT 
 1 AS `id`,
 1 AS `documento_id`,
 1 AS `radicado`,
 1 AS `fecha_movimiento`,
 1 AS `area_origen`,
 1 AS `persona_origen_nombre`,
 1 AS `persona_origen_apellido`,
 1 AS `area_destino`,
 1 AS `persona_destino_nombre`,
 1 AS `persona_destino_apellido`,
 1 AS `estado`,
 1 AS `estado_color`,
 1 AS `observaciones`,
 1 AS `usuario`,
 1 AS `creado_en`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `zonas_economicas`
--

DROP TABLE IF EXISTS `zonas_economicas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `zonas_economicas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `activo` tinyint(1) DEFAULT '1',
  `creado_en` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zonas_economicas`
--

LOCK TABLES `zonas_economicas` WRITE;
/*!40000 ALTER TABLE `zonas_economicas` DISABLE KEYS */;
INSERT INTO `zonas_economicas` VALUES (1,'Planta La María','',1,'2025-03-15 15:31:13'),(2,'Bodega Barranquilla','',1,'2025-03-15 15:31:31'),(3,'Planta Aguazul','',1,'2025-03-15 15:31:59'),(4,'Bodega Bogotá','',1,'2025-03-15 15:32:15');
/*!40000 ALTER TABLE `zonas_economicas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `vista_documentos`
--

/*!50001 DROP VIEW IF EXISTS `vista_documentos`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = cp850 */;
/*!50001 SET character_set_results     = cp850 */;
/*!50001 SET collation_connection      = cp850_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_documentos` AS select `d`.`id` AS `id`,`d`.`radicado` AS `radicado`,`d`.`fecha_recepcion` AS `fecha_recepcion`,`t`.`nombre` AS `transportadora`,`d`.`numero_guia` AS `numero_guia`,`d`.`remitente` AS `remitente`,`td`.`nombre` AS `tipo_documento`,`d`.`contenido` AS `contenido`,`d`.`observaciones` AS `observaciones`,`a`.`nombre` AS `area_actual`,concat(`p`.`nombre`,' ',`p`.`apellido`) AS `persona_actual`,`e`.`nombre` AS `estado`,`e`.`color` AS `estado_color`,`d`.`ruta_adjunto` AS `ruta_adjunto`,(case when `d`.`es_entrada` then 'Entrada' else 'Salida' end) AS `tipo_movimiento`,`d`.`fecha_finalizacion` AS `fecha_finalizacion`,`d`.`creado_en` AS `creado_en`,`d`.`actualizado_en` AS `actualizado_en` from (((((`documentos` `d` left join `transportadoras` `t` on((`d`.`transportadora_id` = `t`.`id`))) left join `tipos_documento` `td` on((`d`.`tipo_documento_id` = `td`.`id`))) left join `areas` `a` on((`d`.`area_actual_id` = `a`.`id`))) left join `personas` `p` on((`d`.`persona_actual_id` = `p`.`id`))) left join `estados_documento` `e` on((`d`.`estado_id` = `e`.`id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vista_historial`
--

/*!50001 DROP VIEW IF EXISTS `vista_historial`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = cp850 */;
/*!50001 SET character_set_results     = cp850 */;
/*!50001 SET collation_connection      = cp850_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_historial` AS select `h`.`id` AS `id`,`h`.`documento_id` AS `documento_id`,`d`.`radicado` AS `radicado`,`h`.`fecha_movimiento` AS `fecha_movimiento`,`a_orig`.`nombre` AS `area_origen`,`p_orig`.`nombre` AS `persona_origen_nombre`,`p_orig`.`apellido` AS `persona_origen_apellido`,`a_dest`.`nombre` AS `area_destino`,`p_dest`.`nombre` AS `persona_destino_nombre`,`p_dest`.`apellido` AS `persona_destino_apellido`,`e`.`nombre` AS `estado`,`e`.`color` AS `estado_color`,`h`.`observaciones` AS `observaciones`,concat(`u`.`username`,' (',`pu`.`nombre`,' ',`pu`.`apellido`,')') AS `usuario`,`h`.`creado_en` AS `creado_en` from ((((((((`historial_movimientos` `h` join `documentos` `d` on((`h`.`documento_id` = `d`.`id`))) join `areas` `a_orig` on((`h`.`area_origen_id` = `a_orig`.`id`))) left join `personas` `p_orig` on((`h`.`persona_origen_id` = `p_orig`.`id`))) join `areas` `a_dest` on((`h`.`area_destino_id` = `a_dest`.`id`))) left join `personas` `p_dest` on((`h`.`persona_destino_id` = `p_dest`.`id`))) join `estados_documento` `e` on((`h`.`estado_id` = `e`.`id`))) join `usuarios` `u` on((`h`.`usuario_id` = `u`.`id`))) join `personas` `pu` on((`u`.`persona_id` = `pu`.`id`))) order by `h`.`documento_id`,`h`.`fecha_movimiento` */;
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

-- Dump completed on 2025-03-15 16:40:56
