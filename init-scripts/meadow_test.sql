-- MySQL dump 10.13  Distrib 5.7.44, for Linux (x86_64)
--
-- Host: localhost    Database: meadow_test
-- ------------------------------------------------------
-- Server version	5.7.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `account_myuser`
--

DROP TABLE IF EXISTS `account_myuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account_myuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(20) NOT NULL,
  `first_name` varchar(10) NOT NULL,
  `last_name` varchar(10) NOT NULL,
  `email` varchar(50) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `realname` varchar(20) NOT NULL,
  `jobrole` varchar(10) NOT NULL,
  `staff_num` varchar(10) NOT NULL,
  `belong` int(11) NOT NULL,
  `mobile` varchar(11) NOT NULL,
  `qq` varchar(16) NOT NULL,
  `weChat` varchar(50) NOT NULL,
  `addr` varchar(100) NOT NULL,
  `id_card` varchar(50) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `username` (`username`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `account_myuser_groups`
--

DROP TABLE IF EXISTS `account_myuser_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account_myuser_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `myuser_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `account_myuser_groups_myuser_id_group_id_7d7152e7_uniq` (`myuser_id`,`group_id`) USING BTREE,
  KEY `account_myuser_groups_group_id_44b24908_fk_auth_group_id` (`group_id`) USING BTREE,
  CONSTRAINT `account_myuser_groups_group_id_44b24908_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `account_myuser_groups_myuser_id_5adbe57d_fk_account_myuser_id` FOREIGN KEY (`myuser_id`) REFERENCES `account_myuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `account_myuser_user_permissions`
--

DROP TABLE IF EXISTS `account_myuser_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account_myuser_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `myuser_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `account_myuser_user_perm_myuser_id_permission_id_36f9bf13_uniq` (`myuser_id`,`permission_id`) USING BTREE,
  KEY `account_myuser_user__permission_id_17807c80_fk_auth_perm` (`permission_id`) USING BTREE,
  CONSTRAINT `account_myuser_user__myuser_id_cdc8ab14_fk_account_m` FOREIGN KEY (`myuser_id`) REFERENCES `account_myuser` (`id`),
  CONSTRAINT `account_myuser_user__permission_id_17807c80_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9914 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `analysis_daily_grass_asset`
--

DROP TABLE IF EXISTS `analysis_daily_grass_asset`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `analysis_daily_grass_asset` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hu_0_0` double DEFAULT NULL COMMENT '经济型草地种植区草/草株/草地/幼草/母草/种草',
  `hu_0_1` double DEFAULT NULL COMMENT '经济型草地种植区草/草株/草地/幼草/母草/种草',
  `hu_1_0` double DEFAULT NULL COMMENT '经济型草地生产区草/草株/草地/幼草/母草/种草',
  `hu_1_1` double DEFAULT NULL COMMENT '经济型草地生产区草/草株/草地/幼草/母草/种草',
  `hu_2_0` double DEFAULT NULL COMMENT '经济型草地生长/发育1月草/草株/草地/幼草/母草/种草',
  `hu_2_1` double DEFAULT NULL COMMENT '经济型草地生长/发育1月草/草株/草地/幼草/母草/种草',
  `hu_3_0` double DEFAULT NULL COMMENT '经济型草地生长/发育2月草/草株/草地/幼草/母草/种草',
  `hu_3_1` double DEFAULT NULL COMMENT '经济型草地生长/发育2月草/草株/草地/幼草/母草/种草',
  `xw_0_0` double DEFAULT NULL COMMENT '经济型草地种植区草/草株/草地/幼草/母草/种草',
  `xw_0_1` double DEFAULT NULL COMMENT '经济型草地种植区草/草株/草地/幼草/母草/种草',
  `xw_1_0` double DEFAULT NULL COMMENT '经济型草地生产区草/草株/草地/幼草/母草/种草',
  `xw_1_1` double DEFAULT NULL COMMENT '经济型草地生产区草/草株/草地/幼草/母草/种草',
  `xw_2_0` double DEFAULT NULL COMMENT '经济型草地生长/发育1月草/草株/草地/幼草/母草/种草',
  `xw_2_1` double DEFAULT NULL COMMENT '经济型草地生长/发育1月草/草株/草地/幼草/母草/种草',
  `xw_3_0` double DEFAULT NULL COMMENT '经济型草地生长/发育2月草/草株/草地/幼草/母草/种草',
  `xw_3_1` double DEFAULT NULL COMMENT '经济型草地生长/发育2月草/草株/草地/幼草/母草/种草',
  `other` double DEFAULT NULL COMMENT '其他草/草株/草地/幼草/母草/种草',
  `belong` int(11) NOT NULL,
  `f_date` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=75 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `analysis_daily_income`
--

DROP TABLE IF EXISTS `analysis_daily_income`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `analysis_daily_income` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `number_0` double DEFAULT NULL,
  `weight_0` double DEFAULT NULL,
  `value_0` double DEFAULT NULL,
  `number_1` double DEFAULT NULL,
  `weight_1` double DEFAULT NULL,
  `value_1` double DEFAULT NULL,
  `number_2` double DEFAULT NULL,
  `weight_2` double DEFAULT NULL,
  `value_2` double DEFAULT NULL,
  `number_3` double DEFAULT NULL,
  `weight_3` double DEFAULT NULL,
  `value_3` double DEFAULT NULL,
  `number_9` double DEFAULT NULL,
  `weight_9` double DEFAULT NULL,
  `value_9` double DEFAULT NULL,
  `dung_value` double DEFAULT NULL,
  `wool_value` double DEFAULT NULL,
  `skin_value` double DEFAULT NULL,
  `manure_value` double DEFAULT NULL,
  `feed_value` double DEFAULT NULL,
  `producted_value` double DEFAULT NULL,
  `other_value` double DEFAULT NULL,
  `f_date` date DEFAULT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `analysis_daily_sheet`
--

DROP TABLE IF EXISTS `analysis_daily_sheet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `analysis_daily_sheet` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '作为主键',
  `date` date NOT NULL COMMENT '作为日期记录',
  `buygrass_fees` double(11,2) DEFAULT NULL COMMENT '购买种植区费用',
  `caoliao_fees` double(11,2) DEFAULT NULL COMMENT '饲料分类的基肥成本',
  `jingliao_fees` double(11,2) DEFAULT NULL COMMENT '饲料分类的复合肥成本',
  `yimiao_fees` double(11,2) DEFAULT NULL COMMENT '农药的费用',
  `yaopin_fees` double(11,2) DEFAULT NULL COMMENT '农药的费用',
  `food_fees` double(11,2) DEFAULT NULL COMMENT '饲料费用-弃用',
  `drug_fees` double(11,2) DEFAULT NULL COMMENT '农药植保药剂费用-弃用',
  `test_fees` double(11,2) DEFAULT NULL COMMENT '检测费用',
  `labor_fees` double(11,2) DEFAULT NULL COMMENT '人工费用',
  `waterEle_fees` double(11,2) DEFAULT NULL COMMENT '水电费用',
  `land_fees` double(11,2) DEFAULT NULL COMMENT '地租费用',
  `maintenance_fees` double(11,2) DEFAULT NULL COMMENT '设备维修费用',
  `cheep_fees` double(11,2) DEFAULT NULL COMMENT '低值易耗品费用',
  `manage_fees` double(11,2) DEFAULT NULL COMMENT '管理费用',
  `research_fees` double(11,2) DEFAULT NULL COMMENT '研发费用',
  `other_fees` double(11,2) DEFAULT NULL COMMENT '其他费用',
  `other_text` text COMMENT '其他费用说明',
  `day_compute` double(11,2) DEFAULT NULL COMMENT '日核算-弃用',
  `directtotal_fees` double(11,2) DEFAULT NULL COMMENT '直接总花费-弃用',
  `indirecttotal_fees` double(11,2) DEFAULT NULL COMMENT '间接总花费-弃用',
  `total_fees` double(11,2) DEFAULT NULL COMMENT '总花费-弃用',
  `f_date` date DEFAULT NULL COMMENT '创建日期',
  `f_staff` varchar(20) DEFAULT NULL COMMENT '创建人',
  `belong` int(11) DEFAULT NULL COMMENT 'belong',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=91 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `analysis_daily_stock_sheet`
--

DROP TABLE IF EXISTS `analysis_daily_stock_sheet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `analysis_daily_stock_sheet` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date DEFAULT NULL COMMENT '日期',
  `garlicskin_num` double(11,2) DEFAULT NULL COMMENT '蒜片数量',
  `garlicskin_val` double(11,2) DEFAULT NULL COMMENT '有机添加剂总价值',
  `peanutseedling_num` double(11,2) DEFAULT NULL COMMENT '有机肥料数量',
  `peanutseedling_val` double(11,2) DEFAULT NULL COMMENT '有机肥料价值',
  `ensilage_num` double(11,2) DEFAULT NULL COMMENT '青贮肥肥作物数量',
  `ensilage_val` double(11,2) DEFAULT NULL COMMENT '青贮肥肥作物价值',
  `otherforage_num` double(11,2) DEFAULT NULL COMMENT '其他基肥数量',
  `otherforage_val` double(11,2) DEFAULT NULL COMMENT '其他基肥价值',
  `corn_num` double(11,2) DEFAULT NULL COMMENT '氮肥/磷肥数量',
  `corn_val` double(11,2) DEFAULT NULL COMMENT '氮肥/磷肥总价值',
  `premix_num` double(11,2) DEFAULT NULL COMMENT '混合肥数量',
  `premix_val` double(11,2) DEFAULT NULL COMMENT '混合肥价值',
  `bran_num` double(11,2) DEFAULT NULL COMMENT '有机肥数量',
  `bran_val` double(11,2) DEFAULT NULL COMMENT '有机肥价值',
  `soybeanmeal_num` double(11,2) DEFAULT NULL COMMENT '有机肥数量',
  `soybeanmeal_val` double(11,2) DEFAULT NULL COMMENT '有机肥价值',
  `salt_num` double(11,2) DEFAULT NULL COMMENT '微量元素肥数量',
  `salt_val` double(11,2) DEFAULT NULL COMMENT '微量元素肥价值',
  `bakingsoda_num` double(11,2) DEFAULT NULL COMMENT '土壤调节剂数量',
  `bakingsoda_val` double(11,2) DEFAULT NULL COMMENT '土壤调节剂价值',
  `calciumlactate_num` double(11,2) DEFAULT NULL COMMENT '乳酸钙数量',
  `calciumlactate_val` double(11,2) DEFAULT NULL COMMENT '乳酸钙价值',
  `otherfinefodder_num` double(11,2) DEFAULT NULL COMMENT '其他复合肥数量',
  `otherfinefodder_val` double(11,2) DEFAULT NULL COMMENT '其他复合肥价值',
  `smallvaccine_num` double(11,2) DEFAULT NULL COMMENT '草地病毒抑制剂数量',
  `smallvaccine_val` double(11,2) DEFAULT NULL COMMENT '草地病毒抑制剂价值',
  `threePfourD_num` double(11,2) DEFAULT NULL COMMENT '草地综合防治药剂数量',
  `threePfourD_val` double(11,2) DEFAULT NULL COMMENT '草地综合防治药剂价值',
  `footAmouthdisease_num` double(11,2) DEFAULT NULL COMMENT '草地斑点病数量',
  `footAmouthdisease_val` double(11,2) DEFAULT NULL COMMENT '草地斑点病价值',
  `duolianbiying_num` double(11,2) DEFAULT NULL COMMENT '草地多效防治剂数量',
  `duolianbiying_val` double(11,2) DEFAULT NULL COMMENT '草地多效防治剂价值',
  `othervaccine_num` double(11,2) DEFAULT NULL COMMENT '其他农药数量',
  `othervaccine_val` double(11,2) DEFAULT NULL COMMENT '其他农药价值',
  `gentamicin_num` double(11,2) DEFAULT NULL COMMENT '草地白粉病专用药数量',
  `gentamicin_val` double(11,2) DEFAULT NULL COMMENT '草地白粉病专用药价值',
  `zhongling_num` double(11,2) DEFAULT NULL COMMENT '中灵数量',
  `zhongling_val` double(11,2) DEFAULT NULL COMMENT '中灵价值',
  `tilmicosin_num` double(11,2) DEFAULT NULL COMMENT '草地锈病专用药数量',
  `tilmicosin_val` double(11,2) DEFAULT NULL COMMENT '草地锈病专用药价值',
  `othermedicine_num` double(11,2) DEFAULT NULL COMMENT '其他农药数量',
  `othermedicine_val` double(11,2) DEFAULT NULL COMMENT '其他农药价值',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=167 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_auth`
--

DROP TABLE IF EXISTS `app_auth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_auth` (
  `id` int(11) DEFAULT NULL,
  `auth_group_id` int(11) DEFAULT NULL,
  `permit_func_id` int(11) DEFAULT NULL,
  `permit_func_farm` int(11) DEFAULT NULL,
  `name` varchar(254) DEFAULT NULL,
  `desc` varchar(254) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_banner_article`
--

DROP TABLE IF EXISTS `app_banner_article`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_banner_article` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(254) DEFAULT NULL,
  `author_name` varchar(254) DEFAULT NULL,
  `cover` varchar(254) DEFAULT NULL,
  `published_at` date DEFAULT NULL,
  `content` longtext,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_config`
--

DROP TABLE IF EXISTS `app_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_config` (
  `config_name` varchar(100) NOT NULL,
  `config_value` varchar(254) DEFAULT NULL,
  `desc` varchar(254) DEFAULT NULL,
  PRIMARY KEY (`config_name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=COMPACT;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_list_article`
--

DROP TABLE IF EXISTS `app_list_article`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_list_article` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(254) DEFAULT NULL,
  `author_name` varchar(254) DEFAULT NULL,
  `cover` varchar(254) DEFAULT NULL,
  `published_at` date DEFAULT NULL,
  `content` varchar(254) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_logs`
--

DROP TABLE IF EXISTS `app_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `operate_time` date DEFAULT NULL,
  `username` varchar(100) NOT NULL,
  `operate_type` varchar(254) DEFAULT NULL,
  `operate_details` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`,`username`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=5601 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=COMPACT;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_transfer_record`
--

DROP TABLE IF EXISTS `app_transfer_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_transfer_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ele_num` varchar(254) DEFAULT NULL,
  `old_houseid` int(11) DEFAULT NULL,
  `old_house` varchar(254) DEFAULT NULL,
  `old_hurdleid` int(11) DEFAULT NULL,
  `old_hurdle` varchar(254) DEFAULT NULL,
  `new_houseid` int(11) DEFAULT NULL,
  `new_house` varchar(254) DEFAULT NULL,
  `new_hurdleid` int(11) DEFAULT NULL,
  `new_hurdle` varchar(254) DEFAULT NULL,
  `transfer_time` date DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=COMPACT;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `app_users`
--

DROP TABLE IF EXISTS `app_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password` varchar(254) DEFAULT NULL,
  `auth_group_id` int(11) DEFAULT NULL,
  `desc` varchar(254) DEFAULT NULL,
  PRIMARY KEY (`id`,`username`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=COMPACT;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `name` (`name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`) USING BTREE,
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`) USING BTREE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`) USING BTREE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=277 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `basic_basicinfo`
--

DROP TABLE IF EXISTS `basic_basicinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `basic_basicinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ele_num` varchar(20) NOT NULL COMMENT '都改成20位',
  `pre_num` varchar(20) NOT NULL,
  `purpose` int(11) DEFAULT NULL,
  `variety` int(11) DEFAULT NULL,
  `sex` int(11) DEFAULT NULL,
  `manu_info_id` int(11) DEFAULT NULL,
  `manu_info_name` varchar(50) DEFAULT NULL,
  `state` int(11) DEFAULT NULL,
  `weight` double DEFAULT NULL COMMENT '当下株高/长势',
  `birth` date NOT NULL,
  `bir_weight` double DEFAULT NULL,
  `wea_date` date DEFAULT NULL COMMENT '移栽/分株日期',
  `wea_weight` double DEFAULT NULL,
  `note` date DEFAULT NULL,
  `house_id` int(11) DEFAULT NULL,
  `hurdle_id` int(11) DEFAULT NULL,
  `house_name` varchar(30) DEFAULT NULL,
  `hurdle_name` varchar(30) NOT NULL,
  `mon_age` double DEFAULT NULL,
  `father_id` int(11) DEFAULT NULL,
  `mother_id` int(11) DEFAULT NULL,
  `f_ele_num` varchar(20) DEFAULT NULL,
  `f_pre_num` varchar(16) DEFAULT NULL,
  `m_ele_num` varchar(20) DEFAULT NULL,
  `m_pre_num` varchar(16) DEFAULT NULL,
  `f_staff` varchar(20) DEFAULT NULL,
  `f_date` date DEFAULT NULL,
  `img_positive` varchar(100) DEFAULT NULL,
  `img_left` varchar(100) DEFAULT NULL,
  `img_right` varchar(100) DEFAULT NULL,
  `note1` longtext,
  `belong` int(6) NOT NULL,
  `color` int(11) DEFAULT NULL,
  `rank` int(11) DEFAULT NULL,
  `cunzai` int(11) DEFAULT NULL,
  `gene_a` int(11) DEFAULT NULL,
  `gene_b` int(11) DEFAULT NULL,
  `gene_c` int(11) DEFAULT NULL,
  `score` int(11) DEFAULT NULL,
  `score_2` int(11) DEFAULT NULL,
  `score_6` int(11) DEFAULT NULL,
  `score_12` int(11) DEFAULT NULL,
  `score_24` int(11) DEFAULT NULL,
  `maternal_grandfather_id` int(11) DEFAULT NULL,
  `maternal_grandfather_ele_num` varchar(20) DEFAULT NULL,
  `maternal_grandfather_pre_num` varchar(16) DEFAULT NULL,
  `maternal_grandmother_id` int(11) DEFAULT NULL,
  `maternal_grandmother_ele_num` varchar(20) DEFAULT NULL,
  `maternal_grandmother_pre_num` varchar(16) DEFAULT NULL,
  `paternal_grandfather_id` int(11) DEFAULT NULL,
  `paternal_grandfather_ele_num` varchar(20) DEFAULT NULL,
  `paternal_grandfather_pre_num` varchar(16) DEFAULT NULL,
  `paternal_grandmother_id` int(11) DEFAULT NULL,
  `paternal_grandmother_ele_num` varchar(20) DEFAULT NULL,
  `paternal_grandmother_pre_num` varchar(16) DEFAULT NULL,
  `localization_num` varchar(11) DEFAULT NULL COMMENT '定位草标',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `ele_num` (`ele_num`) USING BTREE,
  UNIQUE KEY `pre_num` (`pre_num`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=21144 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `basic_canopyperformance`
--

DROP TABLE IF EXISTS `basic_canopyperformance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `basic_canopyperformance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `basic_id` int(11) NOT NULL,
  `skin_area` double DEFAULT NULL,
  `skin_thick` double DEFAULT NULL,
  `date` date NOT NULL,
  `f_staff` varchar(20) DEFAULT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `basic_fertilizerinfo`
--

DROP TABLE IF EXISTS `basic_fertilizerinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `basic_fertilizerinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `house_id` int(11) NOT NULL,
  `num` int(11) NOT NULL,
  `weight` double DEFAULT NULL,
  `notes` longtext NOT NULL,
  `f_staff` varchar(8) NOT NULL,
  `f_date` date NOT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `basic_fieldconditioninfo`
--

DROP TABLE IF EXISTS `basic_fieldconditioninfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `basic_fieldconditioninfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `basic_id` int(11) NOT NULL,
  `age` int(11) NOT NULL,
  `high` double NOT NULL,
  `weight` double NOT NULL,
  `Llong` double NOT NULL,
  `bust` double DEFAULT NULL,
  `root_shape` varchar(20) DEFAULT NULL,
  `t_staff` varchar(8) DEFAULT NULL,
  `AE` longtext,
  `performance_traits` varchar(40) DEFAULT NULL,
  `with_plantings` int(11) DEFAULT NULL,
  `wea_weight` double DEFAULT NULL,
  `June_heavy` double DEFAULT NULL,
  `health` varchar(40) DEFAULT NULL,
  `f_date` date NOT NULL,
  `f_staff` varchar(20) DEFAULT NULL,
  `notes` longtext,
  `belong` int(11) NOT NULL,
  `color` int(11) DEFAULT NULL,
  `mon_age` int(11) DEFAULT NULL,
  `rank` int(11) DEFAULT NULL,
  `back_fat` double DEFAULT NULL,
  `eye` double DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=129760 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `basic_groupmalecapacity`
--

DROP TABLE IF EXISTS `basic_groupmalecapacity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `basic_groupmalecapacity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `one_year_ram` double DEFAULT NULL,
  `two_year_ram` double DEFAULT NULL,
  `three_year_ram` double DEFAULT NULL,
  `four_year_ram` double DEFAULT NULL,
  `five_year_ram` double DEFAULT NULL,
  `six_year_ram` double DEFAULT NULL,
  `belong` int(11) NOT NULL,
  `capa_ram` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=188 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=COMPACT;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `basic_harvestinfo`
--

DROP TABLE IF EXISTS `basic_harvestinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `basic_harvestinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `house_id` int(11) NOT NULL,
  `ele_quantity` int(11) DEFAULT NULL,
  `variety` int(11) DEFAULT NULL,
  `harvest_time` date DEFAULT NULL,
  `rank` int(11) DEFAULT NULL,
  `color` int(11) DEFAULT NULL,
  `weight` double DEFAULT NULL,
  `staff` varchar(8) NOT NULL,
  `notes` longtext NOT NULL,
  `belong` int(11) NOT NULL,
  `f_date` date NOT NULL,
  `harvest_num` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `basic_makescore`
--

DROP TABLE IF EXISTS `basic_makescore`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `basic_makescore` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `variety` int(11) DEFAULT NULL,
  `sex` int(11) DEFAULT NULL,
  `gene_a` int(11) DEFAULT NULL,
  `fetus_num` double DEFAULT NULL,
  `birth_weight_1` double DEFAULT NULL,
  `birth_weight_2` double DEFAULT NULL,
  `birth_weight_3` double DEFAULT NULL,
  `weaning_weight_1` double DEFAULT NULL,
  `weaning_weight_2` double DEFAULT NULL,
  `weaning_weight_3` double DEFAULT NULL,
  `weight_six` double DEFAULT NULL,
  `weight_twelve` double DEFAULT NULL,
  `weight_twenty_four` double DEFAULT NULL,
  `height_2` double DEFAULT NULL,
  `height_6` double DEFAULT NULL,
  `height_12` double DEFAULT NULL,
  `height_24` double DEFAULT NULL,
  `length_2` double DEFAULT NULL,
  `length_6` double DEFAULT NULL,
  `length_12` double DEFAULT NULL,
  `length_24` double DEFAULT NULL,
  `bust_2` double DEFAULT NULL,
  `bust_6` double DEFAULT NULL,
  `bust_12` double DEFAULT NULL,
  `bust_24` double DEFAULT NULL,
  `back_fat_2` double DEFAULT NULL,
  `back_fat_6` double DEFAULT NULL,
  `back_fat_12` double DEFAULT NULL,
  `back_fat_24` double DEFAULT NULL,
  `eye_muscle_2` double DEFAULT NULL,
  `eye_muscle_6` double DEFAULT NULL,
  `eye_muscle_12` double DEFAULT NULL,
  `eye_muscle_24` double DEFAULT NULL,
  `daily_weight_gain` double DEFAULT NULL,
  `born_per_year_1` double DEFAULT NULL,
  `born_per_year_2` double DEFAULT NULL,
  `m_birth_num_1` double DEFAULT NULL,
  `m_birth_num_2` double DEFAULT NULL,
  `f_birth_num` double DEFAULT NULL,
  `n_birth_num` double DEFAULT NULL,
  `survival_rate` double DEFAULT NULL,
  `lambs_per_year` double DEFAULT NULL,
  `m_lambs_year` double DEFAULT NULL,
  `f_lambs_year` double DEFAULT NULL,
  `n_lambs_year` double DEFAULT NULL,
  `small_rum` int(11) DEFAULT NULL,
  `fmd` int(11) DEFAULT NULL,
  `grass_pox` int(11) DEFAULT NULL,
  `tnq` int(11) DEFAULT NULL,
  `brucella` int(11) DEFAULT NULL,
  `belong` int(11) NOT NULL,
  `note` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=COMPACT;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `basic_manuinfo`
--

DROP TABLE IF EXISTS `basic_manuinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `basic_manuinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `manu_name` varchar(40) NOT NULL,
  `scale` int(11) NOT NULL,
  `type` int(11) DEFAULT NULL,
  `BP_license_num` varchar(30) DEFAULT NULL,
  `AP_certificate_num` varchar(30) DEFAULT NULL,
  `BL_num` varchar(30) DEFAULT NULL,
  `legal` varchar(10) DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  `contact` varchar(15) DEFAULT NULL,
  `province` varchar(8) DEFAULT NULL,
  `city` varchar(8) DEFAULT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `manu_name` (`manu_name`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `basic_obsoletegrassinfo`
--

DROP TABLE IF EXISTS `basic_obsoletegrassinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `basic_obsoletegrassinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `basic_id` int(11) NOT NULL,
  `obsolete_type` int(11) DEFAULT NULL,
  `obsolete_date` date DEFAULT NULL,
  `ele_num` varchar(20) NOT NULL,
  `pre_num` varchar(20) NOT NULL,
  `dead_date` date DEFAULT NULL,
  `sales_date` date DEFAULT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `basic_obsoleteinfo`
--

DROP TABLE IF EXISTS `basic_obsoleteinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `basic_obsoleteinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `basic_id` int(11) NOT NULL,
  `obsolete_type` int(11) DEFAULT NULL,
  `obsolete_date` date DEFAULT NULL,
  `ele_num` varchar(20) NOT NULL,
  `pre_num` varchar(20) NOT NULL,
  `dead_date` date DEFAULT NULL,
  `sales_date` date DEFAULT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `basic_pollen_capacity`
--

DROP TABLE IF EXISTS `basic_pollen_capacity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `basic_pollen_capacity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ele_num` varchar(50) DEFAULT NULL,
  `long` double DEFAULT NULL,
  `weight` double DEFAULT NULL,
  `sperm_motility` double DEFAULT NULL,
  `ewe_lambing_rate` double DEFAULT NULL,
  `off_weaning_weight` double DEFAULT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=COMPACT;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `basic_productivityinfo`
--

DROP TABLE IF EXISTS `basic_productivityinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `basic_productivityinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `basic_id` int(11) NOT NULL,
  `weight` double DEFAULT NULL,
  `high` double DEFAULT NULL,
  `Llong` double DEFAULT NULL,
  `bust` double DEFAULT NULL,
  `month_age` double DEFAULT NULL,
  `fecundity` int(11) DEFAULT NULL,
  `per_meat` int(11) DEFAULT NULL,
  `per_milk` int(11) DEFAULT NULL,
  `per_hair` int(11) DEFAULT NULL,
  `per_skin` int(11) DEFAULT NULL,
  `growth_rate` varchar(10) NOT NULL,
  `FCR` double DEFAULT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `basic_sportsinfo`
--

DROP TABLE IF EXISTS `basic_sportsinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `basic_sportsinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `basic_id` int(11) NOT NULL,
  `exercise_time` varchar(10) NOT NULL,
  `exercise` double DEFAULT NULL,
  `belong` int(11) NOT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `basic_yield_capacity`
--

DROP TABLE IF EXISTS `basic_yield_capacity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `basic_yield_capacity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `capa_id` varchar(100) DEFAULT NULL,
  `mating_rate` double DEFAULT NULL,
  `total_conception_rate` double DEFAULT NULL,
  `lamb_num` int(11) DEFAULT NULL,
  `live_lamb_num` int(11) DEFAULT NULL,
  `wean_lamb_num` int(11) DEFAULT NULL,
  `deliver_rate` double DEFAULT NULL,
  `lambing_rate` double DEFAULT NULL,
  `wean_live_rate` double DEFAULT NULL,
  `reproductive_rate` double DEFAULT NULL,
  `reproductive_live_rate` double DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `belong` int(11) NOT NULL,
  `breed` int(11) DEFAULT NULL,
  `conception_num` int(11) DEFAULT NULL,
  `deliver_num` int(11) DEFAULT NULL,
  `fit_reproduction` int(11) DEFAULT NULL,
  `pregnancy_num` int(11) DEFAULT NULL,
  `ewes_daily_gain` double DEFAULT NULL,
  `wean_lamb_daily_gain` double DEFAULT NULL,
  `five_year_ram` double DEFAULT NULL,
  `four_year_ram` double DEFAULT NULL,
  `one_year_ram` double DEFAULT NULL,
  `six_year_ram` double DEFAULT NULL,
  `three_year_ram` double DEFAULT NULL,
  `two_year_ram` double DEFAULT NULL,
  `mate_success_rate` double DEFAULT NULL,
  `time_frame` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=492 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=COMPACT;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `basic_yieldperformance`
--

DROP TABLE IF EXISTS `basic_yieldperformance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `basic_yieldperformance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `basic_id` int(11) NOT NULL,
  `milk_volume` varchar(40) NOT NULL,
  `lamb_num` int(11) DEFAULT NULL,
  `date` date NOT NULL,
  `f_staff` varchar(20) DEFAULT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `d_plantcare_damageinfo`
--

DROP TABLE IF EXISTS `d_plantcare_damageinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `d_plantcare_damageinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `basic_id` int(11) NOT NULL,
  `notes` varchar(40) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `method` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `staff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `date` date DEFAULT NULL,
  `f_staff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `f_date` date NOT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `d_plantcare_diseaseinfo`
--

DROP TABLE IF EXISTS `d_plantcare_diseaseinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `d_plantcare_diseaseinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `basic_id` int(11) NOT NULL,
  `disease_time` date DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `disease` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `treatment_time` date DEFAULT NULL,
  `m_staff` varchar(8) COLLATE utf8mb4_unicode_ci NOT NULL,
  `drug_id` int(11) DEFAULT NULL,
  `drug_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `WDT` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cur_effect` int(11) DEFAULT NULL,
  `cur_time` date DEFAULT NULL,
  `out_time` date DEFAULT NULL,
  `out_no` int(11) DEFAULT NULL,
  `f_staff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `d_plantcare_immunization_b_s`
--

DROP TABLE IF EXISTS `d_plantcare_immunization_b_s`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `d_plantcare_immunization_b_s` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `basic_id` int(11) NOT NULL,
  `ele_num` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL,
  `pre_num` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL,
  `imm_age` double DEFAULT NULL,
  `imm_date` date DEFAULT NULL,
  `vaccine_id` int(11) DEFAULT NULL,
  `cname` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `maker_id` int(11) DEFAULT NULL,
  `supplier_name` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `dose` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `anti_level` varchar(40) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `post_stage` varchar(40) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `out_time` date NOT NULL,
  `f_date` date NOT NULL,
  `operators` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `belong` int(11) NOT NULL,
  `f_staff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ele_num` (`ele_num`),
  UNIQUE KEY `pre_num` (`pre_num`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `d_plantcare_immunizationinfo`
--

DROP TABLE IF EXISTS `d_plantcare_immunizationinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `d_plantcare_immunizationinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `basic_id` int(11) NOT NULL,
  `imm_age` double DEFAULT NULL,
  `imm_date` date DEFAULT NULL,
  `vaccine_id` int(11) DEFAULT NULL,
  `maker_id` int(11) DEFAULT NULL,
  `dose` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `anti_level` varchar(40) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `post_stage` varchar(40) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `out_time` date NOT NULL,
  `f_date` date NOT NULL,
  `operators` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `belong` int(11) NOT NULL,
  `f_staff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `d_plantcare_nursinginfo`
--

DROP TABLE IF EXISTS `d_plantcare_nursinginfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `d_plantcare_nursinginfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `basic_id` int(11) NOT NULL,
  `age` int(11) DEFAULT NULL,
  `nurse` varchar(8) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nur_time` date DEFAULT NULL,
  `root_shape` int(11) DEFAULT NULL,
  `prenatal_paralysi` int(11) DEFAULT NULL,
  `uterus_fall` int(11) DEFAULT NULL,
  `swelling` int(11) DEFAULT NULL,
  `Ab_color` int(11) DEFAULT NULL,
  `Ab_smell` int(11) DEFAULT NULL,
  `information` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `f_date` date NOT NULL,
  `belong` int(11) NOT NULL,
  `f_staff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `d_plantcare_protectioninfo`
--

DROP TABLE IF EXISTS `d_plantcare_protectioninfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `d_plantcare_protectioninfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `basic_id` int(11) NOT NULL,
  `protection_age` double DEFAULT NULL,
  `take_time` date DEFAULT NULL,
  `drug_id` int(11) DEFAULT NULL,
  `vac_maker` int(11) DEFAULT NULL,
  `effect` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `timing` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `IR_bath` varchar(40) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `out_time` date NOT NULL,
  `f_date` date NOT NULL,
  `operators` varchar(8) COLLATE utf8mb4_unicode_ci NOT NULL,
  `belong` int(11) NOT NULL,
  `f_staff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `d_plantcare_quarantineinfo`
--

DROP TABLE IF EXISTS `d_plantcare_quarantineinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `d_plantcare_quarantineinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `basic_id` int(11) NOT NULL,
  `date` date DEFAULT NULL,
  `detection_mode` int(11) DEFAULT NULL,
  `item` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `num` int(11) DEFAULT NULL,
  `antibody` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `institutions` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `third_name` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `inspector` varchar(8) COLLATE utf8mb4_unicode_ci NOT NULL,
  `result1` int(11) DEFAULT NULL,
  `result2` int(11) DEFAULT NULL,
  `result3` int(11) DEFAULT NULL,
  `situation` int(11) DEFAULT NULL,
  `attachment` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `notes` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `belong` int(11) NOT NULL,
  `f_staff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `d_plantcare_witherinfo`
--

DROP TABLE IF EXISTS `d_plantcare_witherinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `d_plantcare_witherinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `basic_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `age` int(11) DEFAULT NULL,
  `cause` int(11) NOT NULL,
  `harmless_treatment` int(11) NOT NULL,
  `t_time` date NOT NULL,
  `t_staff` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `f_staff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `f_date` date NOT NULL,
  `notes` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `deathview`
--

DROP TABLE IF EXISTS `deathview`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `deathview` (
  `id` int(11) DEFAULT NULL,
  `ele_num` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `pre_num` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `purpose` int(11) DEFAULT NULL,
  `variety` int(11) DEFAULT NULL,
  `sex` int(11) DEFAULT NULL,
  `manu_info_id` int(11) DEFAULT NULL,
  `manu_info_name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `state` int(11) DEFAULT NULL,
  `birth` date DEFAULT NULL,
  `bir_weight` double DEFAULT NULL,
  `wea_weight` double DEFAULT NULL,
  `house_id` int(11) DEFAULT NULL,
  `hurdle_id` int(11) DEFAULT NULL,
  `house_name` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `hurdle_name` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `mon_age` double DEFAULT NULL,
  `father_id` int(11) DEFAULT NULL,
  `mother_id` int(11) DEFAULT NULL,
  `f_ele_num` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `f_pre_num` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `m_ele_num` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `m_pre_num` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `f_staff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `f_date` date DEFAULT NULL,
  `img_positive` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `img_left` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `img_right` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `note` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `belong` int(11) DEFAULT NULL,
  `color` int(11) DEFAULT NULL,
  `rank` int(11) DEFAULT NULL,
  `cunzai` int(11) DEFAULT NULL,
  `gene_a` int(11) DEFAULT NULL,
  `gene_b` int(11) DEFAULT NULL,
  `gene_c` int(11) DEFAULT NULL,
  `score` int(11) DEFAULT NULL,
  `score_2` int(11) DEFAULT NULL,
  `score_6` int(11) DEFAULT NULL,
  `score_12` int(11) DEFAULT NULL,
  `score_24` int(11) DEFAULT NULL,
  `deathdate` date DEFAULT NULL,
  `deathage` int(11) DEFAULT NULL,
  `deathtstaff` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `deathfstaff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `deathfdate` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint(6) NOT NULL,
  `change_message` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_django_admin_log_content_type_id` (`content_type_id`),
  KEY `ix_django_admin_log_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_ibfk_1` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `account_myuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_migrations_a`
--

DROP TABLE IF EXISTS `django_migrations_a`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations_a` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `ix_django_session_expire_date` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `e_cultivation_cultivationinfo`
--

DROP TABLE IF EXISTS `e_cultivation_cultivationinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `e_cultivation_cultivationinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cultivation_date` date NOT NULL,
  `pre_harvest_date` date NOT NULL,
  `cultivation_way` int(11) NOT NULL,
  `mother_id` int(11) DEFAULT NULL,
  `mother_variety` int(11) NOT NULL,
  `father_id` int(11) DEFAULT NULL,
  `father_variety` int(11) NOT NULL,
  `cultivation_state` int(11) NOT NULL,
  `staff` varchar(8) COLLATE utf8mb4_unicode_ci NOT NULL,
  `f_staff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `f_date` date NOT NULL,
  `belong` int(11) NOT NULL,
  `growth_period` int(11) DEFAULT NULL,
  `single_success` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `e_cultivation_floweringinfo`
--

DROP TABLE IF EXISTS `e_cultivation_floweringinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `e_cultivation_floweringinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `check_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cultivation_id` int(11) NOT NULL,
  `flowering_status` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `f_staff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `f_date` date NOT NULL,
  `notes` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `e_cultivation_germinationinfo`
--

DROP TABLE IF EXISTS `e_cultivation_germinationinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `e_cultivation_germinationinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sprout_id` int(11) NOT NULL,
  `Delivery_date` date NOT NULL,
  `cultivation_way` int(11) NOT NULL,
  `Seedling_weight` double DEFAULT NULL,
  `wea_weight` double DEFAULT NULL,
  `belong` int(11) NOT NULL,
  `f_staff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `rank` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `e_cultivation_irrigationinfo`
--

DROP TABLE IF EXISTS `e_cultivation_irrigationinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `e_cultivation_irrigationinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sprout_id` int(11) NOT NULL,
  `delivery_date` date NOT NULL,
  `BW` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `reason` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `feeding_material` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `mcal` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `health` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `help` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `dose` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `feeding_staff` varchar(8) COLLATE utf8mb4_unicode_ci NOT NULL,
  `belong` int(11) NOT NULL,
  `f_staff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `e_cultivation_maturationinfo`
--

DROP TABLE IF EXISTS `e_cultivation_maturationinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `e_cultivation_maturationinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cultivation_id` int(11) DEFAULT NULL,
  `cultivation_date` date DEFAULT NULL,
  `delivery_date` date DEFAULT NULL,
  `father_id` int(11) DEFAULT NULL,
  `mother_id` int(11) DEFAULT NULL,
  `Booroola` double DEFAULT NULL,
  `mother_health` int(11) NOT NULL,
  `mother_condition` int(11) NOT NULL,
  `sprout_ele_num` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sprout_state` int(11) DEFAULT NULL,
  `sprout_weight` double DEFAULT NULL,
  `live_seedling_num` int(11) DEFAULT NULL,
  `planting_attendants` varchar(8) COLLATE utf8mb4_unicode_ci NOT NULL,
  `f_staff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `f_date` date DEFAULT NULL,
  `notes` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `e_cultivation_polleninfo`
--

DROP TABLE IF EXISTS `e_cultivation_polleninfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `e_cultivation_polleninfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `basic_id` int(11) NOT NULL,
  `E_date` date NOT NULL,
  `dilution_ratio` double DEFAULT NULL,
  `diluent_type` int(11) DEFAULT NULL,
  `disused` int(11) NOT NULL,
  `f_staff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `f_date` date NOT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `e_cultivation_seedinginfo`
--

DROP TABLE IF EXISTS `e_cultivation_seedinginfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `e_cultivation_seedinginfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `basic_id` int(11) NOT NULL,
  `age` int(11) DEFAULT NULL,
  `seeding_status` int(11) NOT NULL,
  `f_staff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `f_date` date NOT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `e_cultivation_sproutinfo`
--

DROP TABLE IF EXISTS `e_cultivation_sproutinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `e_cultivation_sproutinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cultivation_id` int(11) NOT NULL,
  `basic_id` int(11) DEFAULT NULL,
  `tobasic` int(11) NOT NULL,
  `logo` varchar(35) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ele_num` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `pre_num` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `purpose` int(11) DEFAULT NULL,
  `variety` int(11) DEFAULT NULL,
  `sex` int(11) DEFAULT NULL,
  `belong` int(11) NOT NULL,
  `manu_info_id` int(11) DEFAULT NULL,
  `manu_info_name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `state` int(11) DEFAULT NULL,
  `sprout_date` date DEFAULT NULL,
  `sprout_weight` double DEFAULT NULL,
  `wea_date` date DEFAULT NULL,
  `wea_weight` double DEFAULT NULL,
  `house_id` int(11) DEFAULT NULL,
  `hurdle_id` int(11) DEFAULT NULL,
  `house_name` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `hurdle_name` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `mon_age` double DEFAULT NULL,
  `father_id` int(11) DEFAULT NULL,
  `mother_id` int(11) DEFAULT NULL,
  `f_ele_num` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `f_pre_num` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `m_ele_num` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `m_pre_num` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `f_staff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `f_date` date DEFAULT NULL,
  `img_positive` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `img_left` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `img_right` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `note` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `color` int(11) DEFAULT NULL,
  `rank` int(11) DEFAULT NULL,
  `gene_a` int(11) DEFAULT NULL,
  `score` int(11) DEFAULT NULL,
  `score_2` int(11) DEFAULT NULL,
  `score_6` int(11) DEFAULT NULL,
  `score_12` int(11) DEFAULT NULL,
  `score_24` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `logo` (`logo`),
  UNIQUE KEY `ele_num` (`ele_num`),
  UNIQUE KEY `pre_num` (`pre_num`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `field_disinfectioninfo`
--

DROP TABLE IF EXISTS `field_disinfectioninfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `field_disinfectioninfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `house_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `staff` varchar(8) NOT NULL,
  `drug` varchar(50) NOT NULL,
  `dose` double DEFAULT NULL,
  `method` int(11) NOT NULL,
  `notes` longtext NOT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=181899 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `field_houseinfo`
--

DROP TABLE IF EXISTS `field_houseinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `field_houseinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pid` int(11) NOT NULL,
  `name` varchar(40) NOT NULL,
  `build_time` date NOT NULL,
  `function` int(11) NOT NULL,
  `area` double DEFAULT NULL,
  `h_type` int(6) NOT NULL,
  `h_lwh` varchar(40) NOT NULL,
  `sports_lwh` varchar(40) NOT NULL,
  `grass_type` int(11) DEFAULT NULL,
  `area_pro` varchar(100) NOT NULL,
  `staff` varchar(8) NOT NULL,
  `grass_quantity` int(11) DEFAULT NULL,
  `difinfect_time` date DEFAULT NULL,
  `belong` int(11) NOT NULL,
  `f_staff` varchar(20) DEFAULT NULL,
  `add_area` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=634 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `field_maintenanceinfo`
--

DROP TABLE IF EXISTS `field_maintenanceinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `field_maintenanceinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `house_id` int(11) NOT NULL,
  `M_condition` longtext NOT NULL,
  `M_details` longtext NOT NULL,
  `M_time` date NOT NULL,
  `M_cost` double NOT NULL,
  `f_date` date NOT NULL,
  `f_staff` varchar(20) DEFAULT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `field_transferinfo`
--

DROP TABLE IF EXISTS `field_transferinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `field_transferinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `basic_id` int(11) NOT NULL,
  `new_house_id` int(11) DEFAULT NULL,
  `old_house_id` int(11) DEFAULT NULL,
  `reason` int(11) DEFAULT NULL,
  `trans_time` date NOT NULL,
  `grass_type` varchar(20) NOT NULL,
  `f_date` date NOT NULL,
  `f_staff` varchar(20) DEFAULT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `g_harvest_binformationinfo`
--

DROP TABLE IF EXISTS `g_harvest_binformationinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `g_harvest_binformationinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `belong` int(11) NOT NULL,
  `date` date NOT NULL,
  `month` double DEFAULT NULL,
  `basic_id` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL,
  `variety` int(11) NOT NULL,
  `source` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `back_fat_thickness` double DEFAULT NULL,
  `net_meat_ratio` double DEFAULT NULL,
  `CWT` double DEFAULT NULL,
  `emuscle_area` double DEFAULT NULL,
  `back_thickness` double DEFAULT NULL,
  `level` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `recorder` varchar(5) COLLATE utf8mb4_unicode_ci NOT NULL,
  `notes` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `f_staff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `g_harvest_economicinfo`
--

DROP TABLE IF EXISTS `g_harvest_economicinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `g_harvest_economicinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `belong` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `basic_id` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL,
  `age` double DEFAULT NULL,
  `house_id` int(11) NOT NULL,
  `in_weight` double DEFAULT NULL,
  `in_1_5` double DEFAULT NULL,
  `in_3` double DEFAULT NULL,
  `in_4_5` double DEFAULT NULL,
  `out_weight` double DEFAULT NULL,
  `put_volume` double DEFAULT NULL,
  `intake` double DEFAULT NULL,
  `menu` double DEFAULT NULL,
  `cost` double DEFAULT NULL,
  `FCR` double DEFAULT NULL,
  `ADG` double DEFAULT NULL,
  `f_staff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `g_harvest_g_salesinfo`
--

DROP TABLE IF EXISTS `g_harvest_g_salesinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `g_harvest_g_salesinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `belong` int(11) NOT NULL,
  `sales_date` date NOT NULL,
  `sales_order` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `type` int(11) NOT NULL,
  `billing_unit` varchar(5) COLLATE utf8mb4_unicode_ci NOT NULL,
  `unit_price` double DEFAULT NULL,
  `weight` double DEFAULT NULL,
  `total_price` double DEFAULT NULL,
  `transportation` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `img_trans` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sales_site` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `buyer` varchar(5) COLLATE utf8mb4_unicode_ci NOT NULL,
  `buyer_phone` varchar(11) COLLATE utf8mb4_unicode_ci NOT NULL,
  `selling_type` int(11) NOT NULL,
  `notes` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `f_staff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `g_harvest_s_salesinfo`
--

DROP TABLE IF EXISTS `g_harvest_s_salesinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `g_harvest_s_salesinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `belong` int(11) NOT NULL,
  `sales_date` date NOT NULL,
  `sales_order` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `type` int(11) NOT NULL,
  `quarantine_coding` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ele_num` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL,
  `age` double DEFAULT NULL,
  `medical_leave` int(11) NOT NULL,
  `billing_unit` varchar(5) COLLATE utf8mb4_unicode_ci NOT NULL,
  `unit_price` double DEFAULT NULL,
  `weight` double DEFAULT NULL,
  `total_price` double DEFAULT NULL,
  `transportation` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `img_trans` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sales_site` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `buyer` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `buyer_phone` varchar(11) COLLATE utf8mb4_unicode_ci NOT NULL,
  `selling_type` int(11) NOT NULL,
  `basic_id` int(11) NOT NULL,
  `notes` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `f_staff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ele_num` (`ele_num`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `g_harvest_segmentinfo`
--

DROP TABLE IF EXISTS `g_harvest_segmentinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `g_harvest_segmentinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `belong` int(11) NOT NULL,
  `basic_id` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL,
  `age` double DEFAULT NULL,
  `source` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `in_weight` double DEFAULT NULL,
  `CWT` double DEFAULT NULL,
  `net_meat_weight` double DEFAULT NULL,
  `spine` double DEFAULT NULL,
  `chops_weight` double DEFAULT NULL,
  `stick_bone_weight` double DEFAULT NULL,
  `others_weight` double DEFAULT NULL,
  `head_weight` double DEFAULT NULL,
  `blood_weight` double DEFAULT NULL,
  `skin_weight` double DEFAULT NULL,
  `heart_weight` double DEFAULT NULL,
  `liver_weight` double DEFAULT NULL,
  `lungs_weight` double DEFAULT NULL,
  `tripe_weight` double DEFAULT NULL,
  `hoof_weight` double DEFAULT NULL,
  `L_intestine_weight` double DEFAULT NULL,
  `S_intestine_weight` double DEFAULT NULL,
  `kidney_weight` double DEFAULT NULL,
  `white_weight` double DEFAULT NULL,
  `date` date NOT NULL,
  `f_staff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `grass_asset_standardinfo`
--

DROP TABLE IF EXISTS `grass_asset_standardinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `grass_asset_standardinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `variety` int(11) DEFAULT NULL,
  `sex` int(11) DEFAULT NULL,
  `purpose` int(11) DEFAULT NULL,
  `unit_price` double DEFAULT NULL,
  `rank_0` double DEFAULT NULL,
  `rank_1` double DEFAULT NULL,
  `rank_2` double DEFAULT NULL,
  `rank_3` double DEFAULT NULL,
  `rank_9` double DEFAULT NULL,
  `f_staff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `f_date` date DEFAULT NULL,
  `notes` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `grass_assetinfo`
--

DROP TABLE IF EXISTS `grass_assetinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `grass_assetinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `variety` int(11) DEFAULT NULL,
  `sex` int(11) DEFAULT NULL,
  `purpose` int(11) DEFAULT NULL,
  `number` int(11) DEFAULT NULL,
  `sum_value` double DEFAULT NULL,
  `sum_weight` double DEFAULT NULL,
  `f_date` date DEFAULT NULL,
  `notes` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `h_store_feeding_out`
--

DROP TABLE IF EXISTS `h_store_feeding_out`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `h_store_feeding_out` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `outbound_no` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `type` int(11) NOT NULL,
  `f_name` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ingredientsType` int(11) NOT NULL,
  `warehouse_num` int(11) DEFAULT NULL,
  `delivery_time` date NOT NULL,
  `out_purposes` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `num` int(11) DEFAULT NULL,
  `out_price` double DEFAULT NULL,
  `out_staff` varchar(12) COLLATE utf8mb4_unicode_ci NOT NULL,
  `maker_id` int(11) DEFAULT NULL,
  `contact_phone` varchar(11) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `notes` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `belong` int(11) NOT NULL,
  `f_staff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `outbound_no` (`outbound_no`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `h_store_feedingin`
--

DROP TABLE IF EXISTS `h_store_feedingin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `h_store_feedingin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` int(11) NOT NULL,
  `f_name` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ingredientsType` int(11) NOT NULL,
  `warehouse_num` int(11) DEFAULT NULL,
  `nutrients` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `buy_time` date NOT NULL,
  `billing_unit` varchar(3) COLLATE utf8mb4_unicode_ci NOT NULL,
  `quantity` double NOT NULL,
  `unit_price` double NOT NULL,
  `total_price` double DEFAULT NULL,
  `specifications` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `purpose` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `water_content` varchar(5) COLLATE utf8mb4_unicode_ci NOT NULL,
  `mildew` varchar(5) COLLATE utf8mb4_unicode_ci NOT NULL,
  `impurity_content` varchar(5) COLLATE utf8mb4_unicode_ci NOT NULL,
  `maker_id` int(11) DEFAULT NULL,
  `notes` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `f_date` date NOT NULL,
  `operation` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `keep_amount` double DEFAULT NULL,
  `belong` int(11) NOT NULL,
  `f_staff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fare` double DEFAULT NULL,
  `avg_price` double DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `h_store_inventory`
--

DROP TABLE IF EXISTS `h_store_inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `h_store_inventory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` int(11) DEFAULT NULL,
  `goods` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `maker_id` int(11) DEFAULT NULL,
  `ingredientsType` int(11) NOT NULL,
  `quantity` double DEFAULT NULL,
  `stockPrice` double DEFAULT NULL,
  `totalCost` double DEFAULT NULL,
  `alert` double DEFAULT NULL,
  `f_date` date DEFAULT NULL,
  `operation` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `belong` int(11) NOT NULL,
  `out_time` date DEFAULT NULL,
  `f_staff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `h_store_protection_in`
--

DROP TABLE IF EXISTS `h_store_protection_in`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `h_store_protection_in` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `v_name` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `type` int(11) NOT NULL,
  `ingredientsType` int(11) NOT NULL,
  `maker_id` int(11) DEFAULT NULL,
  `purpose` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `produce_date` date NOT NULL,
  `expiration_date` date NOT NULL,
  `produce_num` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `billing_unit` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `in_amount` int(11) NOT NULL,
  `unit_price` double NOT NULL,
  `total_price` double DEFAULT NULL,
  `in_time` date NOT NULL,
  `keep_amount` double DEFAULT NULL,
  `f_date` date NOT NULL,
  `operation` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `belong` int(11) NOT NULL,
  `f_staff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fare` double DEFAULT NULL,
  `avg_price` double DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `h_store_protection_out`
--

DROP TABLE IF EXISTS `h_store_protection_out`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `h_store_protection_out` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `outbound_no` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `v_name` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `type` int(11) NOT NULL,
  `ingredientsType` int(11) NOT NULL,
  `delivery_time` date NOT NULL,
  `out_purposes` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `num` int(11) DEFAULT NULL,
  `out_price` double DEFAULT NULL,
  `maker_id` int(11) DEFAULT NULL,
  `out_staff` varchar(12) COLLATE utf8mb4_unicode_ci NOT NULL,
  `contact_phone` varchar(11) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `notes` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `belong` int(11) NOT NULL,
  `f_staff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `outbound_no` (`outbound_no`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `home_dailysheet`
--

DROP TABLE IF EXISTS `home_dailysheet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `home_dailysheet` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `labor` double NOT NULL,
  `power` double NOT NULL,
  `land` double NOT NULL,
  `work` double NOT NULL,
  `other` double NOT NULL,
  `f_date` date NOT NULL,
  `f_staff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `supply_commodityinfo`
--

DROP TABLE IF EXISTS `supply_commodityinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `supply_commodityinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` int(11) NOT NULL,
  `cname` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `explain` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `belong` int(11) NOT NULL,
  `f_staff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `supply_f_suppliersinfo`
--

DROP TABLE IF EXISTS `supply_f_suppliersinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `supply_f_suppliersinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `belong` int(11) NOT NULL,
  `supplier_name` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sale_type` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sup_linkman` varchar(5) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sup_contact` varchar(11) COLLATE utf8mb4_unicode_ci NOT NULL,
  `contact` varchar(11) COLLATE utf8mb4_unicode_ci NOT NULL,
  `mail` varchar(25) COLLATE utf8mb4_unicode_ci NOT NULL,
  `address` varchar(40) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `f_date` date NOT NULL,
  `operation` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `f_staff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `supplier_name` (`supplier_name`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `supply_insuranceinfo`
--

DROP TABLE IF EXISTS `supply_insuranceinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `supply_insuranceinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `belong` int(11) NOT NULL,
  `in_name` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `contact` varchar(11) COLLATE utf8mb4_unicode_ci NOT NULL,
  `mail` varchar(25) COLLATE utf8mb4_unicode_ci NOT NULL,
  `handler` varchar(5) COLLATE utf8mb4_unicode_ci NOT NULL,
  `link` varchar(11) COLLATE utf8mb4_unicode_ci NOT NULL,
  `f_date` date NOT NULL,
  `f_staff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `in_name` (`in_name`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `supply_v_suppliersinfo`
--

DROP TABLE IF EXISTS `supply_v_suppliersinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `supply_v_suppliersinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `belong` int(11) NOT NULL,
  `supplier_name` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sale_type` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sup_linkman` varchar(5) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sup_contact` varchar(11) COLLATE utf8mb4_unicode_ci NOT NULL,
  `contact` varchar(11) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `mail` varchar(25) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `address` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `f_date` date NOT NULL,
  `operation` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `f_staff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_grade`
--

DROP TABLE IF EXISTS `tb_grade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_grade` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_student`
--

DROP TABLE IF EXISTS `tb_student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_student` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `gradeid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_tb_student_gradeid` (`gradeid`),
  CONSTRAINT `tb_student_ibfk_1` FOREIGN KEY (`gradeid`) REFERENCES `tb_grade` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_user`
--

DROP TABLE IF EXISTS `tb_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `testuser`
--

DROP TABLE IF EXISTS `testuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `testuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `threshold_setting`
--

DROP TABLE IF EXISTS `threshold_setting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `threshold_setting` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `vaccine_id` int(11) NOT NULL,
  `threshold` int(11) DEFAULT NULL,
  `threshold_mon` int(11) DEFAULT NULL,
  `threshold_year` int(11) DEFAULT NULL,
  `ifyear` int(11) DEFAULT NULL,
  `ifchange` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `w_information_immunizationMessageinfo`
--

DROP TABLE IF EXISTS `w_information_immunizationMessageinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `w_information_immunizationMessageinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `basic_id` int(11) NOT NULL,
  `ele_num` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `pre_num` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sex` int(11) DEFAULT NULL,
  `variety` int(11) DEFAULT NULL,
  `mon_age` double DEFAULT NULL,
  `house` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `hurdle_name` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `vaccine_id` int(11) DEFAULT NULL,
  `birth` date DEFAULT NULL,
  `imm_date` date DEFAULT NULL,
  `distance_date` int(11) DEFAULT NULL,
  `dead_date` date DEFAULT NULL,
  `state` int(11) DEFAULT NULL,
  `f_staff` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `f_date` datetime DEFAULT NULL,
  `note` longtext COLLATE utf8mb4_unicode_ci,
  `belong` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=74498 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-28  5:37:34
