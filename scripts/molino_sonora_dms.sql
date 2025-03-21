-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: molino_sonora_dms
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
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `areas`
--

LOCK TABLES `areas` WRITE;
/*!40000 ALTER TABLE `areas` DISABLE KEYS */;
INSERT INTO `areas` VALUES (1,'GERENTE GENERAL',NULL,1,'2025-03-08 10:51:50'),(2,'GERENTE OPERATIVO',NULL,1,'2025-03-08 10:51:50'),(3,'GERENTE ADMINISTRATIVA Y FINANCIERA',NULL,1,'2025-03-08 10:51:50'),(4,'CONTRALORIA','',1,'2025-03-08 10:51:50'),(5,'ASISTENTE ADMINISTRATIVO',NULL,1,'2025-03-08 10:51:50'),(6,'SUPERNUMERARIO',NULL,1,'2025-03-08 10:51:50'),(7,'SISTEMAS',NULL,1,'2025-03-08 10:51:50'),(8,'TESORERIA','',1,'2025-03-08 10:51:50'),(9,'COMPRAS PADDY',NULL,1,'2025-03-08 10:51:50'),(10,'CONTABILIDAD',NULL,1,'2025-03-08 10:51:50'),(11,'FLETES',NULL,1,'2025-03-08 10:51:50'),(12,'COSTOS',NULL,1,'2025-03-08 10:51:50'),(13,'AUDITORIA','',1,'2025-03-08 10:51:50'),(14,'CARTERA',NULL,1,'2025-03-08 10:51:50'),(15,'VENTAS',NULL,1,'2025-03-08 10:51:50'),(16,'RRHH',NULL,1,'2025-03-08 10:51:50'),(17,'FACTURACION','',1,'2025-03-08 10:51:50'),(18,'SST',NULL,1,'2025-03-08 10:51:50'),(19,'CALIDAD',NULL,1,'2025-03-08 10:51:50'),(20,'PRODUCCION','',1,'2025-03-08 10:51:50'),(21,'COMPRAS Y ALMACEN','',1,'2025-03-08 10:51:50'),(22,'ARCHIVO','',1,'2025-03-08 10:51:50'),(23,'RECEPCION','',1,'2025-03-15 16:24:02'),(27,'LOGISTICA','',1,'2025-03-17 14:19:14');
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
) ENGINE=InnoDB AUTO_INCREMENT=224 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cargos`
--

LOCK TABLES `cargos` WRITE;
/*!40000 ALTER TABLE `cargos` DISABLE KEYS */;
INSERT INTO `cargos` VALUES (169,'FACTURADOR','',1,'2025-03-15 13:56:35'),(170,'ASISTENTE DE COMPRAS MATERIA PRIMA','',1,'2025-03-15 13:56:35'),(171,'SUPERNUMERARIO SST','',1,'2025-03-15 13:56:35'),(172,'ASISTENTE DE CONTABILIDAD','',1,'2025-03-15 13:56:35'),(173,'RECEPCIONISTA','',1,'2025-03-15 13:56:35'),(174,'JEFE DE COSTOS','',1,'2025-03-15 13:56:35'),(175,'AUXILIAR SST','',1,'2025-03-15 13:56:35'),(176,'AUXILIAR DE COMPRAS MATERIA PRIMA','',1,'2025-03-15 13:56:35'),(177,'MENSAJERO','',1,'2025-03-15 13:56:35'),(178,'AUXILIAR DE CONTABILIDAD','',1,'2025-03-15 13:56:35'),(179,'GERENTE GENERAL','',1,'2025-03-15 13:56:35'),(180,'AUXILIAR CAFETERIA','',1,'2025-03-15 13:56:35'),(181,'AUXILIAR ADMINISTRATIVO','',1,'2025-03-15 13:56:35'),(182,'ANALISTA DE PROCESOS SAP','',1,'2025-03-15 13:56:35'),(183,'GERENTE OPERATIVO PLANTA LA MARIA','',1,'2025-03-15 13:56:35'),(184,'APRENDIZ SENA','',1,'2025-03-15 13:56:35'),(185,'GERENTE ADMINISTRATIVO Y FINANCIERO','',1,'2025-03-15 13:56:35'),(186,'JEFE DE AUDITORIA','',1,'2025-03-15 13:56:35'),(187,'JEFE DE SEGURIDAD Y SALUD EN EL TRABAJO','',1,'2025-03-15 13:56:35'),(188,'AUXILIAR DE TESORERIA','',1,'2025-03-15 13:56:35'),(189,'ASISTENTE ADMINISTRATIVO','',1,'2025-03-15 13:56:35'),(190,'AUXILIAR DE CARTERA','',1,'2025-03-15 13:56:35'),(191,'ANALISTA DE SISTEMAS','',1,'2025-03-15 13:56:35'),(192,'ALMACENISTA','',1,'2025-03-15 13:56:35'),(193,'ASISTENTE DE RECURSOS HUMANOS','',1,'2025-03-15 13:56:35'),(194,'COORDINADOR DE ARCHIVO','',1,'2025-03-15 13:56:35'),(195,'SUPERNUMERARIO','',1,'2025-03-15 13:56:35'),(196,'JEFE DE CARTERA','',1,'2025-03-15 13:56:35'),(197,'ASISTENTE DE TESORERIA','',1,'2025-03-15 13:56:35'),(198,'ASISTENTE DE CARTERA','',1,'2025-03-15 13:56:35'),(199,'AUXILIAR DE AUDITORIA','',1,'2025-03-15 13:56:35'),(200,'JEFE DE RECURSOS HUMANOS','',1,'2025-03-15 13:56:35'),(201,'TESORERO','',1,'2025-03-15 13:56:35'),(202,'CONDUCTOR','',1,'2025-03-15 13:56:35'),(203,'ASISTENTE DE CONTABILIDAD II','',1,'2025-03-15 13:56:35'),(204,'COMPRADOR MATERIA PRIMA TOLIMA CENTRO','',1,'2025-03-15 13:56:35'),(205,'CONTRALOR','',1,'2025-03-15 13:56:35'),(206,'ASISTENTE DE COSTOS','',1,'2025-03-15 13:56:35'),(207,'JEFE DE CONTABILIDAD','',1,'2025-03-15 13:56:35'),(208,'AUXILIAR DE ALMACEN','',1,'2025-03-15 13:56:35'),(209,'COMPRADOR MATERIA PRIMA TOLIMA SUR','',1,'2025-03-15 13:56:35'),(210,'JEFE DE COMPRAS Y ALMACEN','',1,'2025-03-15 13:56:35'),(211,'VENDEDOR','',1,'2025-03-15 13:56:35'),(212,'COORDINADOR DE VENTAS','',1,'2025-03-15 13:56:35'),(213,'AUXILIAR DE VENTAS','',1,'2025-03-15 13:56:35'),(214,'COORDINADOR DE DESPACHOS','',1,'2025-03-15 13:56:35'),(215,'SUPERVISOR DE VIGILANCIA','',1,'2025-03-15 13:56:35'),(216,'VIGILANTE','',1,'2025-03-15 13:56:35'),(218,'JEFE GESTI?N DE CALIDAD','',1,'2025-03-17 14:10:58'),(219,'COORDINADOR CONTROL DE CALIDAD','',1,'2025-03-17 14:15:38'),(220,'AUXILIAR LOGISTICO ','',1,'2025-03-17 14:17:41'),(221,'COORDINADOR LOGISTICO','',1,'2025-03-17 14:23:00'),(222,'COORDINADOR FLOTA PROPIA','',1,'2025-03-17 14:25:20'),(223,'JEFE DE PLANTA U OBRA LA MARIA','',1,'2025-03-17 14:38:57');
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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `documentos`
--

LOCK TABLES `documentos` WRITE;
/*!40000 ALTER TABLE `documentos` DISABLE KEYS */;
INSERT INTO `documentos` VALUES (1,'20250311-0001','2025-03-11 21:57:00',10,'0123456789','Lina',3,':)',':)',6,NULL,1,NULL,1,NULL,1,NULL,'2025-03-12 02:58:22',NULL),(2,'20250312-0001','2025-03-12 18:58:00',3,'159753','Albertano',9,'','',4,NULL,1,NULL,1,NULL,1,NULL,'2025-03-12 23:59:14',NULL),(4,'20250315-0001','2025-03-15 21:00:00',10,'0123456789','Lina',9,'','',7,1,1,NULL,1,NULL,1,1,'2025-03-16 02:42:05','2025-03-16 10:57:40'),(5,'20250316-0001','2025-03-16 22:53:00',3,'0123456789','Lina',5,'','',13,NULL,1,NULL,1,NULL,3,NULL,'2025-03-17 03:53:33',NULL),(6,'20250316-0002','2025-03-16 22:53:00',NULL,'0123456789','Lina',2,'','',16,NULL,1,NULL,1,NULL,3,NULL,'2025-03-17 03:53:56',NULL),(7,'20250316-0003','2025-03-16 23:01:00',3,'741258','Albertano',3,'','',6,NULL,1,NULL,1,NULL,3,NULL,'2025-03-17 04:01:38',NULL),(8,'20250316-0004','2025-03-16 23:25:00',13,'','Alexis',4,'','',20,NULL,1,NULL,1,NULL,1,NULL,'2025-03-17 04:26:20',NULL),(9,'20250316-0005','2025-03-16 23:28:00',4,'741258','Albertano',1,'','',3,NULL,1,NULL,1,NULL,3,NULL,'2025-03-17 04:28:28',NULL),(10,'20250317-0001','2025-03-17 08:14:00',4,'0123456789','TONY',4,'','',17,NULL,1,NULL,1,NULL,1,NULL,'2025-03-17 13:15:18',NULL);
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
INSERT INTO `estados_documento` VALUES (1,'Recibido','Documento recibido en recepci?n','#3498db','2025-03-08 10:51:50'),(2,'En proceso','Documento en proceso de revisi?n','#f39c12','2025-03-08 10:51:50'),(3,'Transferido','Documento transferido a otra ?rea','#9b59b6','2025-03-08 10:51:50'),(4,'Finalizado','Proceso completado','#2ecc71','2025-03-08 10:51:50'),(5,'Archivado','Documento archivado','#7f8c8d','2025-03-08 10:51:50');
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
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historial_movimientos`
--

LOCK TABLES `historial_movimientos` WRITE;
/*!40000 ALTER TABLE `historial_movimientos` DISABLE KEYS */;
INSERT INTO `historial_movimientos` VALUES (1,1,'2025-03-11 21:57:00',7,NULL,6,NULL,1,'Registro inicial del documento',1,'2025-03-11 21:58:21'),(2,1,'2025-03-12 02:58:22',7,1,6,NULL,1,':)',1,'2025-03-12 02:58:22'),(3,2,'2025-03-12 18:58:00',7,NULL,4,NULL,1,'Registro inicial del documento',1,'2025-03-12 18:59:13'),(4,2,'2025-03-12 23:59:14',7,1,4,NULL,1,'',1,'2025-03-12 23:59:14'),(5,4,'2025-03-15 21:00:00',7,NULL,15,17,1,'Registro inicial del documento',1,'2025-03-15 21:42:04'),(6,4,'2025-03-15 21:00:00',7,1,15,17,1,'',1,'2025-03-16 02:42:05'),(7,4,'2025-03-16 10:52:28',15,17,22,5,3,'Transferencia de documento. Estado: Transferido',1,'2025-03-16 10:52:28'),(8,4,'2025-03-16 10:52:29',15,17,22,5,3,'No es de mi ?rea',1,'2025-03-16 15:52:29'),(9,4,'2025-03-16 10:54:36',22,5,22,5,1,'Transferencia de documento. Estado: Recibido',2,'2025-03-16 10:54:36'),(10,4,'2025-03-16 10:54:37',22,5,22,5,1,'',2,'2025-03-16 15:54:37'),(11,4,'2025-03-16 10:56:00',22,5,7,1,3,'Transferencia de documento. Estado: Transferido',2,'2025-03-16 10:56:00'),(12,4,'2025-03-16 10:56:00',22,5,7,1,3,'',2,'2025-03-16 15:56:00'),(13,4,'2025-03-16 10:57:40',7,1,7,1,1,'Transferencia de documento. Estado: Recibido',1,'2025-03-16 10:57:40'),(14,4,'2025-03-16 10:57:40',7,1,7,1,1,'',1,'2025-03-16 15:57:40'),(15,5,'2025-03-16 22:53:00',7,NULL,13,NULL,1,'Registro inicial del documento',3,'2025-03-16 22:53:32'),(16,5,'2025-03-16 22:53:00',23,15,13,NULL,1,'',3,'2025-03-17 03:53:33'),(17,6,'2025-03-16 22:53:00',7,NULL,16,NULL,1,'Registro inicial del documento',3,'2025-03-16 22:53:55'),(18,6,'2025-03-16 22:53:00',23,15,16,NULL,1,'',3,'2025-03-17 03:53:56'),(19,7,'2025-03-16 23:01:00',7,NULL,6,NULL,1,'Registro inicial del documento',3,'2025-03-16 23:01:38'),(20,7,'2025-03-16 23:01:00',23,15,6,NULL,1,'',3,'2025-03-17 04:01:38'),(21,8,'2025-03-16 23:25:00',7,NULL,20,NULL,1,'Registro inicial del documento',1,'2025-03-16 23:26:19'),(22,8,'2025-03-16 23:25:00',7,1,20,NULL,1,'',1,'2025-03-17 04:26:20'),(23,9,'2025-03-16 23:28:00',7,NULL,3,NULL,1,'Registro inicial del documento',3,'2025-03-16 23:28:28'),(24,9,'2025-03-16 23:28:00',23,15,3,NULL,1,'',3,'2025-03-17 04:28:28'),(25,10,'2025-03-17 08:14:00',7,1,17,NULL,1,'',1,'2025-03-17 13:15:18');
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notificaciones`
--

LOCK TABLES `notificaciones` WRITE;
/*!40000 ALTER TABLE `notificaciones` DISABLE KEYS */;
INSERT INTO `notificaciones` VALUES (1,2,4,'El documento 20250315-0001 ha sido transferido a tu ?rea',0,'2025-03-16 15:52:29'),(2,2,4,'Se te ha asignado el documento 20250315-0001',0,'2025-03-16 15:54:37'),(3,1,4,'El documento 20250315-0001 ha sido transferido a tu ?rea',1,'2025-03-16 15:56:00'),(4,1,4,'Se te ha asignado el documento 20250315-0001',1,'2025-03-16 15:57:40');
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
  `cargo_id` int DEFAULT NULL,
  `activo` tinyint(1) DEFAULT '1',
  `creado_en` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `area_id` (`area_id`),
  KEY `cargo_id` (`cargo_id`),
  KEY `email` (`email`),
  CONSTRAINT `personas_ibfk_1` FOREIGN KEY (`area_id`) REFERENCES `areas` (`id`),
  CONSTRAINT `personas_ibfk_2` FOREIGN KEY (`cargo_id`) REFERENCES `cargos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `personas`
--

LOCK TABLES `personas` WRITE;
/*!40000 ALTER TABLE `personas` DISABLE KEYS */;
INSERT INTO `personas` VALUES (1,'Ricardo Alexander','Bohorquez Mendez','rbohorquez@arrozsonora.com.co','311 2815201',7,191,1,'2025-03-08 16:10:16'),(2,'Myriam','Rodriguez Arciniegas','mrodriguez@arrozsonora.com.co','318 5683317',4,205,1,'2025-03-08 16:59:35'),(3,'Jairo Antonio','Lozano Vargas','sst@arrozsonora.com.co','310 2118013',18,187,1,'2025-03-08 17:10:04'),(4,'Ana Maria','Rodriguez Mora','arodriguez@arrozsonora.com.co','',16,200,1,'2025-03-10 02:43:01'),(5,'Jaime','Vargas Ramirez','jvargas@arrozsonora.com.co','',22,194,1,'2025-03-10 02:47:03'),(7,'Olga Patricia','Ortiz Rivas','oortiz@arrozsonora.com.co','',21,210,1,'2025-03-10 02:48:43'),(8,'Luis Alberto','Barreto Guzman','lbarreto@arrozsonora.com.co','',21,192,1,'2025-03-10 02:49:26'),(11,'Luis Alejandro','Oliveros Guarnizo','','',21,208,1,'2025-03-10 02:52:45'),(13,'James Eduardo','Rueda Trujillo','jrueda@arrozsonora.com.co','',20,223,1,'2025-03-10 02:57:55'),(14,'Martha Yaneth','Diaz Trigueros','mdiaz@arrozsonora.com.co','',8,201,1,'2025-03-11 16:08:04'),(15,'Yazmina Lorena','Fayad Gutierrez','yfayad@arrozsonora.com.co','',23,173,1,'2025-03-15 15:50:28'),(16,'Yendy Fannory','Bravo Guti?rrez ','ybravo@arrozsonora.com.co','',17,169,1,'2025-03-15 21:19:37'),(17,'Luana Simona','Sendoya Echeverry','lsendoya@arrozsonora.com.co','',15,212,1,'2025-03-16 01:59:11'),(18,'Jairo','Sedan Murra','jsedan@arrozsonora.com.co','',1,179,1,'2025-03-16 16:05:12'),(19,'Julio Cesar','Cepeda Rodr?guez','jcepeda@arrozsonora.com.co','',2,183,1,'2025-03-16 16:06:14'),(20,'Yuly Slendy','Castillo Robayo','ycastillo@arrozsonora.com.co','',3,185,1,'2025-03-16 16:09:49'),(21,'Brayan Santick','Quintero Cordoba','bquintero@arrozsonora.com.co','',5,189,1,'2025-03-16 16:10:54'),(22,'Viviana ','Caycedo Bocanegra','vcaycedo@arrozsonora.com.co','',6,195,1,'2025-03-16 16:12:38'),(23,'Sandra Bibiana','Laverde Parra','slaverde@arrozsonora.com.co','',8,181,1,'2025-03-16 16:15:14'),(24,'Juan David','Lozano Guzman','jlozano@arrozsonora.com.co','',8,197,1,'2025-03-16 16:17:19'),(25,'Diana Marcela','Bocanegra Tovar','dbocanegra@arrozsonora.com.co','',8,197,1,'2025-03-16 16:19:15'),(26,'Teresa','Tovar Rivera','ttovar@arrozsonora.com.co','',9,170,1,'2025-03-16 16:20:47'),(27,'Angy Yulitza','Vargas Padilla','avargas@arrozsonora.com.co','',9,176,1,'2025-03-16 16:22:14'),(28,'Ximena Paola','Bocanegra Ortiz','xbocanegra@arrozsonora.com.co','',10,207,1,'2025-03-16 16:23:24'),(29,'Joan Jair','Rodriguez Portela','jrodriguez@arrozsonora.com.co','',10,172,1,'2025-03-16 21:51:28'),(30,'Adriana Lucia','Gonzalez Serrano','agonzalez@arrozsonora.com.co','',10,203,1,'2025-03-16 21:53:23'),(31,'Lizeth Daniela','Melo Olis','lmelo@arrozsonora.com.co','',10,178,1,'2025-03-16 21:55:46'),(32,'Maria Paula','Lozano Lozano','mlozano@arrozsonora.com.co','',10,172,1,'2025-03-16 22:06:55'),(33,'Silvia Patricia','Rivera Zabala','srivera@arrozsonora.com.co','',10,178,1,'2025-03-16 22:07:59'),(34,'Andres Felipe','Arias Vargas','aarias@arrozsonora.com.co','',10,178,1,'2025-03-16 22:13:15'),(35,'Laura Maria','Rodriguez Cuervo','lrodriguez@arrozsonora.com.co','',10,178,1,'2025-03-16 22:14:41'),(36,'Andrea Del Pilar','Morales Trujillo','amorales@arrozsonora.com.co','',10,178,1,'2025-03-16 22:16:02'),(37,'Karen Nureidys','Carcamo Londono','kcarcamo@arrozsonora.com.co','',12,174,1,'2025-03-16 22:17:02'),(38,'Julian Andres','Molina Avila','jmolina@arrozsonora.com.co','',12,206,1,'2025-03-16 22:18:40'),(39,'Nataly Tatiana','Puentes Sierra','npuentes@arrozsonora.com.co','',13,186,1,'2025-03-16 22:20:05'),(40,'Adriana del Pilar','Lopez Bustos','alopez@arrozsonora.com.co','',13,188,1,'2025-03-16 22:21:13'),(41,'Lina Fernanda','Fierro Fierro','lfierro@arrozsonora.com.co','',13,NULL,1,'2025-03-16 22:23:37'),(42,'Leidy Johana','Avila Gonzalez','lavila@arrozsonora.com.co','',14,196,1,'2025-03-16 22:25:25'),(43,'Julieth Paola','Gonzalez Onatra','jgonzalez@arrozsonora.com.co','',14,198,1,'2025-03-16 22:26:35'),(44,'Jonathan Fabian','Manrique Rodriguez','jmanrique@arrozsonora.com.co','',14,190,1,'2025-03-16 22:28:32'),(45,'Angie Katherine','Zamora Cordoba','azamora@arrozsonora.com.co','',14,190,1,'2025-03-16 22:30:18'),(46,'Angi Xiomara','Ramirez Ortiz','aramirez@arrozsonora.com.co','',15,213,1,'2025-03-16 22:32:10'),(47,'Juan Jose','Cote Hernandez','jcote@arrozsonora.com.co','',27,221,1,'2025-03-16 22:33:36'),(48,'Sandra Milena','Garcia Gonzalez','sgarcia@arrozsonora.com.co','',16,193,1,'2025-03-16 22:34:49'),(49,'Angela Maria','Zartha Leal','azartha@arrozsonora.com.co','',27,220,1,'2025-03-16 22:36:12'),(50,'Juan Pablo','Celis Castillo','jcelis@arrozsonora.com.co','',27,222,1,'2025-03-16 22:38:44'),(51,'Kelly Johanna','Gomez Lozano','kgomez@arrozsonora.com.co','',18,175,1,'2025-03-16 22:39:41'),(52,'Sandra Milena','Villa Rojas','smvilla@arrozsonora.com.co','',19,218,1,'2025-03-16 22:41:57'),(53,'Diana Alejandra','Ortiz Jara','dortiz@arrozsonora.com.co','',19,219,1,'2025-03-16 22:42:44'),(55,'Jorge Elias','Ortiz','jortiz@arrozsonora.com.co','',15,214,1,'2025-03-17 14:29:46'),(56,'Lina Julieth','Carvajal Mendoza','','',7,184,1,'2025-03-17 16:05:54');
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
INSERT INTO `roles` VALUES (1,'Superadministrador','Control total del sistema',1,'2025-03-08 10:51:50'),(2,'Usuario','Acceso limitado a visualizaci?n de documentos',0,'2025-03-08 10:51:50');
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
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipos_documento`
--

LOCK TABLES `tipos_documento` WRITE;
/*!40000 ALTER TABLE `tipos_documento` DISABLE KEYS */;
INSERT INTO `tipos_documento` VALUES (1,'Facturas',NULL,1,'2025-03-08 10:51:50'),(2,'Comprobantes',NULL,1,'2025-03-08 10:51:50'),(3,'Contratos',NULL,1,'2025-03-08 10:51:50'),(4,'Correspondencia',NULL,1,'2025-03-08 10:51:50'),(5,'Tiquetes',NULL,1,'2025-03-08 10:51:50'),(6,'Cotizaciones',NULL,1,'2025-03-08 10:51:50'),(7,'Ordenes de compra','',1,'2025-03-08 10:51:50'),(9,'Hojas de vida',NULL,1,'2025-03-08 10:51:50'),(10,'Manuales',NULL,1,'2025-03-08 10:51:50'),(11,'Informes',NULL,1,'2025-03-08 10:51:50'),(15,'Fletes','',1,'2025-03-16 00:23:04');
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
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transportadoras`
--

LOCK TABLES `transportadoras` WRITE;
/*!40000 ALTER TABLE `transportadoras` DISABLE KEYS */;
INSERT INTO `transportadoras` VALUES (1,'DEPRISA',NULL,1,'2025-03-08 10:51:50'),(2,'SERVIENTREGA',NULL,1,'2025-03-08 10:51:50'),(3,'ENVIA',NULL,1,'2025-03-08 10:51:50'),(4,'COORDINADORA',NULL,1,'2025-03-08 10:51:50'),(5,'SAFERBO',NULL,1,'2025-03-08 10:51:50'),(6,'INTERRAPIDISIMO',NULL,1,'2025-03-08 10:51:50'),(7,'AXPRESS',NULL,1,'2025-03-08 10:51:50'),(8,'REDETRANS',NULL,1,'2025-03-08 10:51:50'),(9,'TCC',NULL,1,'2025-03-08 10:51:50'),(10,'4-72','',1,'2025-03-08 10:51:50'),(11,'TRANSPRENSA',NULL,1,'2025-03-08 10:51:50'),(12,'PORTER?A',NULL,1,'2025-03-08 10:51:50'),(13,'CERTIPOSTAL',NULL,1,'2025-03-08 10:51:50'),(14,'ENCO EXPRES',NULL,1,'2025-03-08 10:51:50'),(15,'X-CARGO',NULL,1,'2025-03-08 10:51:50'),(16,'DHL EXPRESS',NULL,1,'2025-03-08 10:51:50'),(17,'OPEN MARKET',NULL,1,'2025-03-08 10:51:50'),(18,'EXPRESO BOLIVARIANO',NULL,1,'2025-03-08 10:51:50'),(19,'MERCADOLIBRE',NULL,1,'2025-03-08 10:51:50'),(20,'INTERSERVICE',NULL,1,'2025-03-08 10:51:50');
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
INSERT INTO `usuarios` VALUES (1,'rbohorquez','pbkdf2:sha256:600000$QGcwmQ2QjUQqEWLY$a8578b2aa6bcc13f1a12925801fed78a1ab40334f442282864afcb996ad6e959',1,1,'2025-03-17 13:51:46',1,'2025-03-08 16:10:16'),(2,'jvargas','pbkdf2:sha256:600000$s9ZHOW1fQKDEqzsh$3530955ea9adc8130e9b08e16cef014208bd4328405c2ba4922fe945d92b1c4e',5,2,'2025-03-17 13:32:05',1,'2025-03-12 01:15:43'),(3,'yfayad','pbkdf2:sha256:600000$QuA3nZtCAEv90k2y$8da98364c29d5140dcc10075781f3c05a59fb1b7ccd259ca93ed5d74da77266f',15,2,'2025-03-17 13:24:31',1,'2025-03-15 15:51:06');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `zonas_economicas`
--

DROP TABLE IF EXISTS `zonas_economicas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `zonas_economicas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  `activo` tinyint(1) DEFAULT '1',
  `creado_en` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zonas_economicas`
--

LOCK TABLES `zonas_economicas` WRITE;
/*!40000 ALTER TABLE `zonas_economicas` DISABLE KEYS */;
INSERT INTO `zonas_economicas` VALUES (1,'PLANTA LA MARIA','',1,'2025-03-15 15:31:13'),(2,'BODEGA BARRANQUILLA','',1,'2025-03-15 15:31:31'),(3,'PLANTA AGUAZUL','',1,'2025-03-15 15:31:59'),(4,'BODEGA BOGOTA','',1,'2025-03-15 15:32:15'),(9,'BODEGA CALI','',1,'2025-03-17 13:48:30'),(10,'BODEGA GIRON','',1,'2025-03-17 13:49:27'),(11,'BODEGA MEDELLIN','',1,'2025-03-17 13:50:12'),(12,'BODEGA PEREIRA','',1,'2025-03-17 13:50:51');
/*!40000 ALTER TABLE `zonas_economicas` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-17 11:35:06
