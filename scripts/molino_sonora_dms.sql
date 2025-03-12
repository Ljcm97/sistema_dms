<<<<<<< HEAD
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
INSERT INTO `alembic_version` VALUES ('bd3425f707ea');
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
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `areas`
--

LOCK TABLES `areas` WRITE;
/*!40000 ALTER TABLE `areas` DISABLE KEYS */;
INSERT INTO `areas` VALUES (1,'GERENTE GENERAL',NULL,1,'2025-03-08 10:51:50'),(2,'GERENTE OPERATIVO',NULL,1,'2025-03-08 10:51:50'),(3,'GERENTE ADMINISTRATIVA Y FINANCIERA',NULL,1,'2025-03-08 10:51:50'),(4,'CONTRALORÍA',NULL,1,'2025-03-08 10:51:50'),(5,'ASISTENTE ADMINISTRATIVO',NULL,1,'2025-03-08 10:51:50'),(6,'SUPERNUMERARIO',NULL,1,'2025-03-08 10:51:50'),(7,'SISTEMAS',NULL,1,'2025-03-08 10:51:50'),(8,'TESORERÍA',NULL,1,'2025-03-08 10:51:50'),(9,'COMPRAS PADDY',NULL,1,'2025-03-08 10:51:50'),(10,'CONTABILIDAD',NULL,1,'2025-03-08 10:51:50'),(11,'FLETES',NULL,1,'2025-03-08 10:51:50'),(12,'COSTOS',NULL,1,'2025-03-08 10:51:50'),(13,'AUDITORÍA',NULL,1,'2025-03-08 10:51:50'),(14,'CARTERA',NULL,1,'2025-03-08 10:51:50'),(15,'VENTAS',NULL,1,'2025-03-08 10:51:50'),(16,'RRHH',NULL,1,'2025-03-08 10:51:50'),(17,'FACTURACIÓN',NULL,1,'2025-03-08 10:51:50'),(18,'SST',NULL,1,'2025-03-08 10:51:50'),(19,'CALIDAD',NULL,1,'2025-03-08 10:51:50'),(20,'PRODUCCIÓN',NULL,1,'2025-03-08 10:51:50'),(21,'COMPRAS Y ALMACÉN',NULL,1,'2025-03-08 10:51:50'),(22,'ARCHIVO',NULL,1,'2025-03-08 10:51:50');
/*!40000 ALTER TABLE `areas` ENABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `documentos`
--

LOCK TABLES `documentos` WRITE;
/*!40000 ALTER TABLE `documentos` DISABLE KEYS */;
/*!40000 ALTER TABLE `documentos` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `after_documento_insert` AFTER INSERT ON `documentos` FOR EACH ROW BEGIN
    
    INSERT INTO historial_movimientos (
        documento_id, fecha_movimiento, area_origen_id, 
        persona_origen_id, area_destino_id, persona_destino_id,
        estado_id, observaciones, usuario_id
    ) VALUES (
        NEW.id, NEW.fecha_recepcion, 
        (SELECT id FROM areas WHERE nombre = 'SISTEMAS'), 
        NULL, 
        NEW.area_actual_id, 
        NEW.persona_actual_id, 
        NEW.estado_id, 
        'Registro inicial del documento', 
        NEW.usuario_creacion_id 
    );
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `after_documento_update` AFTER UPDATE ON `documentos` FOR EACH ROW BEGIN
    
    IF NEW.area_actual_id != OLD.area_actual_id OR 
       NEW.persona_actual_id != OLD.persona_actual_id OR
       NEW.estado_id != OLD.estado_id THEN
        
        INSERT INTO historial_movimientos (
            documento_id, fecha_movimiento, area_origen_id, 
            persona_origen_id, area_destino_id, persona_destino_id,
            estado_id, observaciones, usuario_id
        ) VALUES (
            NEW.id, NOW(), 
            OLD.area_actual_id, 
            OLD.persona_actual_id, 
            NEW.area_actual_id, 
            NEW.persona_actual_id, 
            NEW.estado_id, 
            CONCAT('Transferencia de documento. Estado: ', 
                  (SELECT nombre FROM estados_documento WHERE id = NEW.estado_id)), 
            NEW.usuario_actualizacion_id 
        );
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historial_movimientos`
--

LOCK TABLES `historial_movimientos` WRITE;
/*!40000 ALTER TABLE `historial_movimientos` DISABLE KEYS */;
/*!40000 ALTER TABLE `historial_movimientos` ENABLE KEYS */;
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
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `area_id` (`area_id`),
  CONSTRAINT `personas_ibfk_1` FOREIGN KEY (`area_id`) REFERENCES `areas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `personas`
--

LOCK TABLES `personas` WRITE;
/*!40000 ALTER TABLE `personas` DISABLE KEYS */;
INSERT INTO `personas` VALUES (1,'Ricardo Alexander','Bohórquez Méndez','rbohorquez@arrozsonora.com.co','311 2815201',7,1,'2025-03-08 16:10:16'),(2,'Myriam','Rodríguez Arciniegas','mrodriguez@arrozsonora.com.co','318 5683317',4,1,'2025-03-08 16:59:35'),(3,'Jairo Antonio','Lozano Vargas','sst@arrozsonora.com.co','310 2118013',18,1,'2025-03-08 17:10:04'),(4,'Ana María','Rodríguez Mora','arodriguez@arrozsonora.com.co','',16,0,'2025-03-10 02:43:01'),(5,'Jaime','Vargas Ramírez','jvargas@arrozsonora.com','',22,1,'2025-03-10 02:47:03'),(7,'Olga Patricia','Ortiz Rivas','oortiz@arrozsonora.com.co','',21,1,'2025-03-10 02:48:43'),(8,'Luis Alberto','Barreto Guzmán','lbarreto@arrozsonora.com.co','',21,1,'2025-03-10 02:49:26'),(11,'Luis Alejandro','Oliveros','','',21,1,'2025-03-10 02:52:45'),(13,'James Eduardo','Rueda Trujillo','jrueda@arrozsonora.com','',20,1,'2025-03-10 02:57:55'),(14,'Martha Yaneth','Díaz Trigueros','mdiaz@arrozsonora.com.co','',8,1,'2025-03-11 16:08:04');
/*!40000 ALTER TABLE `personas` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipos_documento`
--

LOCK TABLES `tipos_documento` WRITE;
/*!40000 ALTER TABLE `tipos_documento` DISABLE KEYS */;
INSERT INTO `tipos_documento` VALUES (1,'Facturas',NULL,1,'2025-03-08 10:51:50'),(2,'Comprobantes',NULL,1,'2025-03-08 10:51:50'),(3,'Contratos',NULL,1,'2025-03-08 10:51:50'),(4,'Correspondencia',NULL,1,'2025-03-08 10:51:50'),(5,'Tiquetes',NULL,1,'2025-03-08 10:51:50'),(6,'Cotizaciones',NULL,1,'2025-03-08 10:51:50'),(7,'Órdenes de compra',NULL,1,'2025-03-08 10:51:50'),(8,'Remisiones',NULL,1,'2025-03-08 10:51:50'),(9,'Hojas de vida',NULL,1,'2025-03-08 10:51:50'),(10,'Manuales',NULL,1,'2025-03-08 10:51:50'),(11,'Informes',NULL,1,'2025-03-08 10:51:50');
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
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transportadoras`
--

LOCK TABLES `transportadoras` WRITE;
/*!40000 ALTER TABLE `transportadoras` DISABLE KEYS */;
INSERT INTO `transportadoras` VALUES (1,'DEPRISA',NULL,1,'2025-03-08 10:51:50'),(2,'SERVIENTREGA',NULL,1,'2025-03-08 10:51:50'),(3,'ENVIA',NULL,1,'2025-03-08 10:51:50'),(4,'COORDINADORA',NULL,1,'2025-03-08 10:51:50'),(5,'SAFERBO',NULL,1,'2025-03-08 10:51:50'),(6,'INTERRAPIDISIMO',NULL,1,'2025-03-08 10:51:50'),(7,'AXPRESS',NULL,1,'2025-03-08 10:51:50'),(8,'REDETRANS',NULL,1,'2025-03-08 10:51:50'),(9,'TCC',NULL,1,'2025-03-08 10:51:50'),(10,'4-72',NULL,1,'2025-03-08 10:51:50'),(11,'TRANSPRENSA',NULL,1,'2025-03-08 10:51:50'),(12,'PORTERÍA',NULL,1,'2025-03-08 10:51:50'),(13,'CERTIPOSTAL',NULL,1,'2025-03-08 10:51:50'),(14,'ENCO EXPRES',NULL,1,'2025-03-08 10:51:50'),(15,'X-CARGO',NULL,1,'2025-03-08 10:51:50'),(16,'DHL EXPRESS',NULL,1,'2025-03-08 10:51:50'),(17,'OPEN MARKET',NULL,1,'2025-03-08 10:51:50'),(18,'EXPRESO BOLIVARIANO',NULL,1,'2025-03-08 10:51:50'),(19,'MERCADOLIBRE',NULL,1,'2025-03-08 10:51:50'),(20,'INTERSERVICE',NULL,1,'2025-03-08 10:51:50');
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'admin','pbkdf2:sha256:600000$OoechBv80gxzDVK6$b81f7d12ffed38b20fff85429c33c62cf1fe0ccedb7a6f413143f67388a15c8e',1,1,'2025-03-11 20:48:53',1,'2025-03-08 16:10:16');
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
-- Dumping events for database 'molino_sonora_dms'
--

--
-- Dumping routines for database 'molino_sonora_dms'
--
/*!50003 DROP PROCEDURE IF EXISTS `GenerarRadicado` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GenerarRadicado`(OUT radicado VARCHAR(20))
BEGIN
    DECLARE year VARCHAR(4);
    DECLARE month VARCHAR(2);
    DECLARE day VARCHAR(2);
    DECLARE counter INT;
    
    SET year = DATE_FORMAT(NOW(), '%Y');
    SET month = DATE_FORMAT(NOW(), '%m');
    SET day = DATE_FORMAT(NOW(), '%d');
    
    
    SELECT IFNULL(MAX(CAST(SUBSTRING_INDEX(radicado, '-', -1) AS UNSIGNED)), 0) + 1
    INTO counter
    FROM documentos
    WHERE radicado LIKE CONCAT(year, month, day, '-%');
    
    
    SET radicado = CONCAT(year, month, day, '-', LPAD(counter, 4, '0'));
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

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

-- Dump completed on 2025-03-11 17:10:31
=======
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
INSERT INTO `alembic_version` VALUES ('bd3425f707ea');
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
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `areas`
--

LOCK TABLES `areas` WRITE;
/*!40000 ALTER TABLE `areas` DISABLE KEYS */;
INSERT INTO `areas` VALUES (1,'GERENTE GENERAL',NULL,1,'2025-03-08 10:51:50'),(2,'GERENTE OPERATIVO',NULL,1,'2025-03-08 10:51:50'),(3,'GERENTE ADMINISTRATIVA Y FINANCIERA',NULL,1,'2025-03-08 10:51:50'),(4,'CONTRALORÍA',NULL,1,'2025-03-08 10:51:50'),(5,'ASISTENTE ADMINISTRATIVO',NULL,1,'2025-03-08 10:51:50'),(6,'SUPERNUMERARIO',NULL,1,'2025-03-08 10:51:50'),(7,'SISTEMAS',NULL,1,'2025-03-08 10:51:50'),(8,'TESORERÍA',NULL,1,'2025-03-08 10:51:50'),(9,'COMPRAS PADDY',NULL,1,'2025-03-08 10:51:50'),(10,'CONTABILIDAD',NULL,1,'2025-03-08 10:51:50'),(11,'FLETES',NULL,1,'2025-03-08 10:51:50'),(12,'COSTOS',NULL,1,'2025-03-08 10:51:50'),(13,'AUDITORÍA',NULL,1,'2025-03-08 10:51:50'),(14,'CARTERA',NULL,1,'2025-03-08 10:51:50'),(15,'VENTAS',NULL,1,'2025-03-08 10:51:50'),(16,'RRHH',NULL,1,'2025-03-08 10:51:50'),(17,'FACTURACIÓN',NULL,1,'2025-03-08 10:51:50'),(18,'SST',NULL,1,'2025-03-08 10:51:50'),(19,'CALIDAD',NULL,1,'2025-03-08 10:51:50'),(20,'PRODUCCIÓN',NULL,1,'2025-03-08 10:51:50'),(21,'COMPRAS Y ALMACÉN',NULL,1,'2025-03-08 10:51:50'),(22,'ARCHIVO',NULL,1,'2025-03-08 10:51:50');
/*!40000 ALTER TABLE `areas` ENABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `documentos`
--

LOCK TABLES `documentos` WRITE;
/*!40000 ALTER TABLE `documentos` DISABLE KEYS */;
/*!40000 ALTER TABLE `documentos` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `after_documento_insert` AFTER INSERT ON `documentos` FOR EACH ROW BEGIN
    
    INSERT INTO historial_movimientos (
        documento_id, fecha_movimiento, area_origen_id, 
        persona_origen_id, area_destino_id, persona_destino_id,
        estado_id, observaciones, usuario_id
    ) VALUES (
        NEW.id, NEW.fecha_recepcion, 
        (SELECT id FROM areas WHERE nombre = 'SISTEMAS'), 
        NULL, 
        NEW.area_actual_id, 
        NEW.persona_actual_id, 
        NEW.estado_id, 
        'Registro inicial del documento', 
        NEW.usuario_creacion_id 
    );
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `after_documento_update` AFTER UPDATE ON `documentos` FOR EACH ROW BEGIN
    
    IF NEW.area_actual_id != OLD.area_actual_id OR 
       NEW.persona_actual_id != OLD.persona_actual_id OR
       NEW.estado_id != OLD.estado_id THEN
        
        INSERT INTO historial_movimientos (
            documento_id, fecha_movimiento, area_origen_id, 
            persona_origen_id, area_destino_id, persona_destino_id,
            estado_id, observaciones, usuario_id
        ) VALUES (
            NEW.id, NOW(), 
            OLD.area_actual_id, 
            OLD.persona_actual_id, 
            NEW.area_actual_id, 
            NEW.persona_actual_id, 
            NEW.estado_id, 
            CONCAT('Transferencia de documento. Estado: ', 
                  (SELECT nombre FROM estados_documento WHERE id = NEW.estado_id)), 
            NEW.usuario_actualizacion_id 
        );
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historial_movimientos`
--

LOCK TABLES `historial_movimientos` WRITE;
/*!40000 ALTER TABLE `historial_movimientos` DISABLE KEYS */;
/*!40000 ALTER TABLE `historial_movimientos` ENABLE KEYS */;
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
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `area_id` (`area_id`),
  CONSTRAINT `personas_ibfk_1` FOREIGN KEY (`area_id`) REFERENCES `areas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `personas`
--

LOCK TABLES `personas` WRITE;
/*!40000 ALTER TABLE `personas` DISABLE KEYS */;
INSERT INTO `personas` VALUES (1,'Ricardo Alexander','Bohórquez Méndez','rbohorquez@arrozsonora.com.co','311 2815201',7,1,'2025-03-08 16:10:16'),(2,'Myriam','Rodríguez Arciniegas','mrodriguez@arrozsonora.com.co','318 5683317',4,1,'2025-03-08 16:59:35'),(3,'Jairo Antonio','Lozano Vargas','sst@arrozsonora.com.co','310 2118013',18,1,'2025-03-08 17:10:04'),(4,'Ana María','Rodríguez Mora','arodriguez@arrozsonora.com.co','',16,0,'2025-03-10 02:43:01'),(5,'Jaime','Vargas Ramírez','jvargas@arrozsonora.com','',22,1,'2025-03-10 02:47:03'),(7,'Olga Patricia','Ortiz Rivas','oortiz@arrozsonora.com.co','',21,1,'2025-03-10 02:48:43'),(8,'Luis Alberto','Barreto Guzmán','lbarreto@arrozsonora.com.co','',21,1,'2025-03-10 02:49:26'),(11,'Luis Alejandro','Oliveros','','',21,1,'2025-03-10 02:52:45'),(13,'James Eduardo','Rueda Trujillo','jrueda@arrozsonora.com','',20,1,'2025-03-10 02:57:55'),(14,'Martha Yaneth','Díaz Trigueros','mdiaz@arrozsonora.com.co','',8,1,'2025-03-11 16:08:04');
/*!40000 ALTER TABLE `personas` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipos_documento`
--

LOCK TABLES `tipos_documento` WRITE;
/*!40000 ALTER TABLE `tipos_documento` DISABLE KEYS */;
INSERT INTO `tipos_documento` VALUES (1,'Facturas',NULL,1,'2025-03-08 10:51:50'),(2,'Comprobantes',NULL,1,'2025-03-08 10:51:50'),(3,'Contratos',NULL,1,'2025-03-08 10:51:50'),(4,'Correspondencia',NULL,1,'2025-03-08 10:51:50'),(5,'Tiquetes',NULL,1,'2025-03-08 10:51:50'),(6,'Cotizaciones',NULL,1,'2025-03-08 10:51:50'),(7,'Órdenes de compra',NULL,1,'2025-03-08 10:51:50'),(8,'Remisiones',NULL,1,'2025-03-08 10:51:50'),(9,'Hojas de vida',NULL,1,'2025-03-08 10:51:50'),(10,'Manuales',NULL,1,'2025-03-08 10:51:50'),(11,'Informes',NULL,1,'2025-03-08 10:51:50');
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
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transportadoras`
--

LOCK TABLES `transportadoras` WRITE;
/*!40000 ALTER TABLE `transportadoras` DISABLE KEYS */;
INSERT INTO `transportadoras` VALUES (1,'DEPRISA',NULL,1,'2025-03-08 10:51:50'),(2,'SERVIENTREGA',NULL,1,'2025-03-08 10:51:50'),(3,'ENVIA',NULL,1,'2025-03-08 10:51:50'),(4,'COORDINADORA',NULL,1,'2025-03-08 10:51:50'),(5,'SAFERBO',NULL,1,'2025-03-08 10:51:50'),(6,'INTERRAPIDISIMO',NULL,1,'2025-03-08 10:51:50'),(7,'AXPRESS',NULL,1,'2025-03-08 10:51:50'),(8,'REDETRANS',NULL,1,'2025-03-08 10:51:50'),(9,'TCC',NULL,1,'2025-03-08 10:51:50'),(10,'4-72',NULL,1,'2025-03-08 10:51:50'),(11,'TRANSPRENSA',NULL,1,'2025-03-08 10:51:50'),(12,'PORTERÍA',NULL,1,'2025-03-08 10:51:50'),(13,'CERTIPOSTAL',NULL,1,'2025-03-08 10:51:50'),(14,'ENCO EXPRES',NULL,1,'2025-03-08 10:51:50'),(15,'X-CARGO',NULL,1,'2025-03-08 10:51:50'),(16,'DHL EXPRESS',NULL,1,'2025-03-08 10:51:50'),(17,'OPEN MARKET',NULL,1,'2025-03-08 10:51:50'),(18,'EXPRESO BOLIVARIANO',NULL,1,'2025-03-08 10:51:50'),(19,'MERCADOLIBRE',NULL,1,'2025-03-08 10:51:50'),(20,'INTERSERVICE',NULL,1,'2025-03-08 10:51:50');
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'admin','pbkdf2:sha256:600000$OoechBv80gxzDVK6$b81f7d12ffed38b20fff85429c33c62cf1fe0ccedb7a6f413143f67388a15c8e',1,1,'2025-03-11 20:48:53',1,'2025-03-08 16:10:16');
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
-- Dumping events for database 'molino_sonora_dms'
--

--
-- Dumping routines for database 'molino_sonora_dms'
--
/*!50003 DROP PROCEDURE IF EXISTS `GenerarRadicado` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `GenerarRadicado`(OUT radicado VARCHAR(20))
BEGIN
    DECLARE year VARCHAR(4);
    DECLARE month VARCHAR(2);
    DECLARE day VARCHAR(2);
    DECLARE counter INT;
    
    SET year = DATE_FORMAT(NOW(), '%Y');
    SET month = DATE_FORMAT(NOW(), '%m');
    SET day = DATE_FORMAT(NOW(), '%d');
    
    
    SELECT IFNULL(MAX(CAST(SUBSTRING_INDEX(radicado, '-', -1) AS UNSIGNED)), 0) + 1
    INTO counter
    FROM documentos
    WHERE radicado LIKE CONCAT(year, month, day, '-%');
    
    
    SET radicado = CONCAT(year, month, day, '-', LPAD(counter, 4, '0'));
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

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

-- Dump completed on 2025-03-11 17:10:31
>>>>>>> 8829def (Corregido error en app/__init__.py y añadido modelo de notificaciones)
