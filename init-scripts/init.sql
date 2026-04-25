-- AgroGuard Database Init Script - sheep database schema only

-- MySQL dump 10.13  Distrib 5.7.44, for Win64 (x86_64)
--
-- Host: 182.92.207.3    Database: 
-- ------------------------------------------------------
-- Server version	5.7.40

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

-- Current Database: `sheep`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `sheep` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `sheep`;

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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `analysis_daily_sheep_asset`
--

DROP TABLE IF EXISTS `analysis_daily_sheep_asset`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `analysis_daily_sheep_asset` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hu_0_0` double DEFAULT NULL COMMENT '禾本科草种植区草/草株/草地/幼草/母草/种草',
  `hu_0_1` double DEFAULT NULL COMMENT '禾本科草种植区草/草株/草地/幼草/母草/种草',
  `hu_1_0` double DEFAULT NULL COMMENT '禾本科草生产区草/草株/草地/幼草/母草/种草',
  `hu_1_1` double DEFAULT NULL COMMENT '禾本科草生产区草/草株/草地/幼草/母草/种草',
  `hu_2_0` double DEFAULT NULL COMMENT '禾本科草生长/发育1月草/草株/草地/幼草/母草/种草',
  `hu_2_1` double DEFAULT NULL COMMENT '禾本科草生长/发育1月草/草株/草地/幼草/母草/种草',
  `hu_3_0` double DEFAULT NULL COMMENT '禾本科草生长/发育2月草/草株/草地/幼草/母草/种草',
  `hu_3_1` double DEFAULT NULL COMMENT '禾本科草生长/发育2月草/草株/草地/幼草/母草/种草',
  `xw_0_0` double DEFAULT NULL COMMENT '豆科草种植区草/草株/草地/幼草/母草/种草',
  `xw_0_1` double DEFAULT NULL COMMENT '豆科草种植区草/草株/草地/幼草/母草/种草',
  `xw_1_0` double DEFAULT NULL COMMENT '豆科草生产区草/草株/草地/幼草/母草/种草',
  `xw_1_1` double DEFAULT NULL COMMENT '豆科草生产区草/草株/草地/幼草/母草/种草',
  `xw_2_0` double DEFAULT NULL COMMENT '豆科草生长/发育1月草/草株/草地/幼草/母草/种草',
  `xw_2_1` double DEFAULT NULL COMMENT '豆科草生长/发育1月草/草株/草地/幼草/母草/种草',
  `xw_3_0` double DEFAULT NULL COMMENT '豆科草生长/发育2月草/草株/草地/幼草/母草/种草',
  `xw_3_1` double DEFAULT NULL COMMENT '豆科草生长/发育2月草/草株/草地/幼草/母草/种草',
  `other` double DEFAULT NULL COMMENT '其他草/草株/草地/幼草/母草/种草',
  `belong` int(11) NOT NULL,
  `f_date` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
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
  `buysheep_fees` double(11,2) DEFAULT NULL COMMENT '购买种植区费用',
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=COMPACT;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=COMPACT;
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=COMPACT;
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
  `ewe_grandfather_id` int(11) DEFAULT NULL,
  `ewe_grandfather_ele_num` varchar(20) DEFAULT NULL,
  `ewe_grandfather_pre_num` varchar(16) DEFAULT NULL,
  `ewe_grandmother_id` int(11) DEFAULT NULL,
  `ewe_grandmother_ele_num` varchar(20) DEFAULT NULL,
  `ewe_grandmother_pre_num` varchar(16) DEFAULT NULL,
  `ram_grandfather_id` int(11) DEFAULT NULL,
  `ram_grandfather_ele_num` varchar(20) DEFAULT NULL,
  `ram_grandfather_pre_num` varchar(16) DEFAULT NULL,
  `ram_grandmother_id` int(11) DEFAULT NULL,
  `ram_grandmother_ele_num` varchar(20) DEFAULT NULL,
  `ram_grandmother_pre_num` varchar(16) DEFAULT NULL,
  `localization_num` varchar(11) DEFAULT NULL COMMENT '定位草标',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `ele_num` (`ele_num`) USING BTREE,
  UNIQUE KEY `pre_num` (`pre_num`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `basic_basicinfo_`
--

DROP TABLE IF EXISTS `basic_basicinfo_`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `basic_basicinfo_` (
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
  `ewe_grandfather_id` int(11) DEFAULT NULL,
  `ewe_grandfather_ele_num` varchar(20) DEFAULT NULL,
  `ewe_grandfather_pre_num` varchar(16) DEFAULT NULL,
  `ewe_grandmother_id` int(11) DEFAULT NULL,
  `ewe_grandmother_ele_num` varchar(20) DEFAULT NULL,
  `ewe_grandmother_pre_num` varchar(16) DEFAULT NULL,
  `ram_grandfather_id` int(11) DEFAULT NULL,
  `ram_grandfather_ele_num` varchar(20) DEFAULT NULL,
  `ram_grandfather_pre_num` varchar(16) DEFAULT NULL,
  `ram_grandmother_id` int(11) DEFAULT NULL,
  `ram_grandmother_ele_num` varchar(20) DEFAULT NULL,
  `ram_grandmother_pre_num` varchar(16) DEFAULT NULL,
  `localization_num` varchar(11) DEFAULT NULL COMMENT '定位草标',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `ele_num` (`ele_num`) USING BTREE,
  UNIQUE KEY `pre_num` (`pre_num`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `basic_breederconditioninfo`
--

DROP TABLE IF EXISTS `basic_breederconditioninfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `basic_breederconditioninfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `basic_id` int(11) NOT NULL,
  `age` int(11) NOT NULL,
  `high` double NOT NULL,
  `weight` double NOT NULL,
  `Llong` double NOT NULL,
  `bust` double DEFAULT NULL,
  `testis_shape` varchar(20) DEFAULT NULL,
  `t_staff` varchar(8) DEFAULT NULL,
  `AE` longtext,
  `performance_traits` varchar(40) DEFAULT NULL,
  `with_births` int(11) DEFAULT NULL,
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `basic_capacity`
--

DROP TABLE IF EXISTS `basic_capacity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `basic_capacity` (
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `basic_capacityrams`
--

DROP TABLE IF EXISTS `basic_capacityrams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `basic_capacityrams` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ele_num` varchar(50) DEFAULT NULL,
  `long` double DEFAULT NULL,
  `weight` double DEFAULT NULL,
  `sperm_motility` double DEFAULT NULL,
  `ewe_lambing_rate` double DEFAULT NULL,
  `off_weaning_weight` double DEFAULT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `basic_comprehensive_eva`
--

DROP TABLE IF EXISTS `basic_comprehensive_eva`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `basic_comprehensive_eva` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ele_num` varchar(255) DEFAULT NULL,
  `gene_fecb` varchar(255) DEFAULT NULL,
  `f_date` date DEFAULT NULL,
  `basic_score` double DEFAULT NULL,
  `births_num` double DEFAULT NULL,
  `birth_weight` double DEFAULT NULL,
  `wean_weight` double DEFAULT NULL,
  `body_score` double DEFAULT NULL,
  `weight` double DEFAULT NULL,
  `high` double DEFAULT NULL,
  `Llong` double DEFAULT NULL,
  `bust` double DEFAULT NULL,
  `thick_fat` double DEFAULT NULL,
  `eye_area` double DEFAULT NULL,
  `daily_gain` double DEFAULT NULL,
  `descendant_score` double DEFAULT NULL,
  `ave_year_product` double DEFAULT NULL,
  `reproductive_rate` double DEFAULT NULL,
  `annual_lambs` double DEFAULT NULL,
  `epidemic_pre_score` double DEFAULT NULL,
  `small_rumination` double DEFAULT NULL,
  `foot_mouth_disease` double DEFAULT NULL,
  `sheep_pox` double DEFAULT NULL,
  `three_four` double DEFAULT NULL,
  `is_vaccinate` double DEFAULT NULL,
  `total_score` double DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `basic_cutinfo`
--

DROP TABLE IF EXISTS `basic_cutinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `basic_cutinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `house_id` int(11) NOT NULL,
  `ele_quantity` int(11) DEFAULT NULL,
  `variety` int(11) DEFAULT NULL,
  `cut_time` int(11) DEFAULT NULL,
  `rank` int(11) DEFAULT NULL,
  `color` int(11) DEFAULT NULL,
  `weight` double DEFAULT NULL,
  `staff` varchar(8) NOT NULL,
  `notes` longtext NOT NULL,
  `belong` int(11) NOT NULL,
  `f_date` date NOT NULL,
  `cut_num` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `basic_dailycost`
--

DROP TABLE IF EXISTS `basic_dailycost`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `basic_dailycost` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date DEFAULT NULL,
  `feed_expenditure` double DEFAULT NULL,
  `vacdrug_expenditures` double DEFAULT NULL,
  `sales_revenue` double DEFAULT NULL,
  `electric_charge` double DEFAULT NULL,
  `water_rate` double DEFAULT NULL,
  `office_expenses` double DEFAULT NULL,
  `difference` double DEFAULT NULL,
  `belong` int(11) NOT NULL,
  `note` varchar(50) DEFAULT NULL,
  `feed_buy` double DEFAULT NULL,
  `vacdrug_buy` double DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `basic_elechangeinfo`
--

DROP TABLE IF EXISTS `basic_elechangeinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `basic_elechangeinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `basic_id` int(11) NOT NULL,
  `new_num` varchar(16) NOT NULL,
  `old_num` varchar(16) NOT NULL,
  `retime` date NOT NULL,
  `reason` longtext NOT NULL,
  `sheep_type` varchar(10) NOT NULL,
  `house_num` int(11) DEFAULT NULL,
  `staff` varchar(8) NOT NULL,
  `f_date` date NOT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `new_num` (`new_num`) USING BTREE,
  UNIQUE KEY `old_num` (`old_num`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `basic_groupramcapacity`
--

DROP TABLE IF EXISTS `basic_groupramcapacity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `basic_groupramcapacity` (
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
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
  `sheep_pox` int(11) DEFAULT NULL,
  `tnq` int(11) DEFAULT NULL,
  `brucella` int(11) DEFAULT NULL,
  `belong` int(11) NOT NULL,
  `note` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
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
  `BP_license_num` varchar(30) NOT NULL,
  `AP_certificate_num` varchar(30) NOT NULL,
  `BL_num` varchar(30) NOT NULL,
  `legal` varchar(10) NOT NULL,
  `address` varchar(50) NOT NULL,
  `contact` varchar(15) NOT NULL,
  `province` varchar(8) NOT NULL,
  `city` varchar(8) NOT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `manu_name` (`manu_name`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `basic_manureinfo`
--

DROP TABLE IF EXISTS `basic_manureinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `basic_manureinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `house_id` int(11) NOT NULL,
  `num` int(11) NOT NULL,
  `weight` double DEFAULT NULL,
  `notes` longtext NOT NULL,
  `f_staff` varchar(8) NOT NULL,
  `f_date` date NOT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `basic_milkperformance`
--

DROP TABLE IF EXISTS `basic_milkperformance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `basic_milkperformance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `basic_id` int(11) NOT NULL,
  `milk_volume` varchar(40) NOT NULL,
  `lamb_num` int(11) DEFAULT NULL,
  `date` date NOT NULL,
  `f_staff` varchar(20) DEFAULT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `basic_obsoletesheepinfo`
--

DROP TABLE IF EXISTS `basic_obsoletesheepinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `basic_obsoletesheepinfo` (
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `basic_skinperformance`
--

DROP TABLE IF EXISTS `basic_skinperformance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `basic_skinperformance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `basic_id` int(11) NOT NULL,
  `skin_area` double DEFAULT NULL,
  `skin_thick` double DEFAULT NULL,
  `date` date NOT NULL,
  `f_staff` varchar(20) DEFAULT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `colony_disinfectioninfo`
--

DROP TABLE IF EXISTS `colony_disinfectioninfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `colony_disinfectioninfo` (
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
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `colony_houseinfo`
--

DROP TABLE IF EXISTS `colony_houseinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `colony_houseinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pid` int(11) NOT NULL,
  `name` varchar(40) NOT NULL,
  `build_time` date NOT NULL,
  `function` int(11) NOT NULL,
  `area` double DEFAULT NULL,
  `h_type` int(6) NOT NULL,
  `h_lwh` varchar(40) NOT NULL,
  `sports_lwh` varchar(40) NOT NULL,
  `sheep_type` int(11) DEFAULT NULL,
  `area_pro` varchar(100) NOT NULL,
  `staff` varchar(8) NOT NULL,
  `sheep_quantity` int(11) DEFAULT NULL,
  `difinfect_time` date DEFAULT NULL,
  `belong` int(11) NOT NULL,
  `f_staff` varchar(20) DEFAULT NULL,
  `add_area` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `colony_maintenanceinfo`
--

DROP TABLE IF EXISTS `colony_maintenanceinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `colony_maintenanceinfo` (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `colony_transferinfo`
--

DROP TABLE IF EXISTS `colony_transferinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `colony_transferinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `basic_id` int(11) NOT NULL,
  `new_house_id` int(11) DEFAULT NULL,
  `old_house_id` int(11) DEFAULT NULL,
  `reason` int(11) DEFAULT NULL,
  `trans_time` date NOT NULL,
  `sheep_type` varchar(20) NOT NULL,
  `f_date` date NOT NULL,
  `f_staff` varchar(20) DEFAULT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `d_health_abortioninfo`
--

DROP TABLE IF EXISTS `d_health_abortioninfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `d_health_abortioninfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `basic_id` int(11) NOT NULL,
  `notes` varchar(40) DEFAULT NULL,
  `method` longtext,
  `staff` varchar(20) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `f_staff` varchar(20) DEFAULT NULL,
  `f_date` date NOT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `d_health_deathinfo`
--

DROP TABLE IF EXISTS `d_health_deathinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `d_health_deathinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `basic_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `age` int(11) DEFAULT NULL,
  `cause` int(11) NOT NULL,
  `harmless_treatment` int(11) NOT NULL,
  `t_time` date NOT NULL,
  `t_staff` varchar(30) NOT NULL,
  `f_staff` varchar(20) DEFAULT NULL,
  `f_date` date NOT NULL,
  `notes` longtext NOT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `d_health_diseaseinfo`
--

DROP TABLE IF EXISTS `d_health_diseaseinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `d_health_diseaseinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `basic_id` int(11) NOT NULL,
  `disease_time` date DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `disease` varchar(30) NOT NULL,
  `treatment_time` date DEFAULT NULL,
  `m_staff` varchar(8) NOT NULL,
  `drug_id` int(11) DEFAULT NULL,
  `drug_type` varchar(20) NOT NULL,
  `WDT` varchar(20) NOT NULL,
  `cur_effect` int(11) DEFAULT NULL,
  `cur_time` date DEFAULT NULL,
  `out_time` date DEFAULT NULL,
  `out_no` int(11) DEFAULT NULL,
  `f_staff` varchar(20) DEFAULT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `d_health_drugbathinfo`
--

DROP TABLE IF EXISTS `d_health_drugbathinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `d_health_drugbathinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `basic_id` int(11) NOT NULL,
  `drug_age` double DEFAULT NULL,
  `take_time` date DEFAULT NULL,
  `drug_id` int(11) DEFAULT NULL,
  `vac_maker` int(11) DEFAULT NULL,
  `effect` longtext,
  `timing` varchar(20) DEFAULT NULL,
  `IR_bath` varchar(40) DEFAULT NULL,
  `out_time` date NOT NULL,
  `f_date` date NOT NULL,
  `operators` varchar(8) NOT NULL,
  `belong` int(11) NOT NULL,
  `f_staff` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Temporary table structure for view `d_health_immunization_b_s`
--

DROP TABLE IF EXISTS `d_health_immunization_b_s`;
/*!50001 DROP VIEW IF EXISTS `d_health_immunization_b_s`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `d_health_immunization_b_s` AS SELECT 
 1 AS `ele_num`,
 1 AS `pre_num`,
 1 AS `b_basic_id`,
 1 AS `id`,
 1 AS `basic_id`,
 1 AS `imm_age`,
 1 AS `imm_date`,
 1 AS `vaccine_id`,
 1 AS `maker_id`,
 1 AS `dose`,
 1 AS `anti_level`,
 1 AS `post_stage`,
 1 AS `out_time`,
 1 AS `f_date`,
 1 AS `operators`,
 1 AS `belong`,
 1 AS `f_staff`,
 1 AS `sv_maker_id`,
 1 AS `supplier_name`,
 1 AS `cname`,
 1 AS `sc_vaccine_id`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `d_health_immunizationinfo`
--

DROP TABLE IF EXISTS `d_health_immunizationinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `d_health_immunizationinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `basic_id` int(11) NOT NULL,
  `imm_age` double DEFAULT NULL,
  `imm_date` date DEFAULT NULL,
  `vaccine_id` int(11) DEFAULT NULL,
  `maker_id` int(11) DEFAULT NULL,
  `dose` varchar(20) DEFAULT NULL,
  `anti_level` varchar(40) DEFAULT NULL,
  `post_stage` varchar(40) DEFAULT NULL,
  `out_time` date NOT NULL,
  `f_date` date NOT NULL,
  `operators` longtext,
  `belong` int(11) NOT NULL,
  `f_staff` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `d_health_nursinginfo`
--

DROP TABLE IF EXISTS `d_health_nursinginfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `d_health_nursinginfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `basic_id` int(11) NOT NULL,
  `age` int(11) DEFAULT NULL,
  `nurse` varchar(8) NOT NULL,
  `nur_time` date DEFAULT NULL,
  `testis_shape` tinyint(1) DEFAULT NULL,
  `prenatal_paralysi` tinyint(1) DEFAULT NULL,
  `uterus_fall` tinyint(1) DEFAULT NULL,
  `swelling` tinyint(1) DEFAULT NULL,
  `Ab_color` int(11) DEFAULT NULL,
  `Ab_smell` int(11) DEFAULT NULL,
  `information` longtext NOT NULL,
  `f_date` date NOT NULL,
  `belong` int(11) NOT NULL,
  `f_staff` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `d_health_quarantineinfo`
--

DROP TABLE IF EXISTS `d_health_quarantineinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `d_health_quarantineinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `basic_id` int(11) NOT NULL,
  `date` date DEFAULT NULL,
  `detection_mode` int(11) DEFAULT NULL,
  `item` varchar(20) NOT NULL,
  `num` int(11) DEFAULT NULL,
  `antibody` varchar(40) NOT NULL,
  `institutions` varchar(20) NOT NULL,
  `third_name` varchar(30) DEFAULT NULL,
  `inspector` varchar(8) NOT NULL,
  `result1` int(11) DEFAULT NULL,
  `result2` int(11) DEFAULT NULL,
  `result3` int(11) DEFAULT NULL,
  `situation` int(11) DEFAULT NULL,
  `attachment` varchar(100) NOT NULL,
  `notes` longtext,
  `belong` int(11) NOT NULL,
  `f_staff` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `e_breed_artificialfeedinginfo`
--

DROP TABLE IF EXISTS `e_breed_artificialfeedinginfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `e_breed_artificialfeedinginfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lamb_id` int(11) NOT NULL,
  `delivery_date` date NOT NULL,
  `BW` varchar(10) NOT NULL,
  `reason` varchar(40) NOT NULL,
  `feeding_material` varchar(20) NOT NULL,
  `mcal` varchar(20) NOT NULL,
  `health` varchar(10) NOT NULL,
  `help` longtext NOT NULL,
  `dose` varchar(20) NOT NULL,
  `feeding_staff` varchar(8) NOT NULL,
  `belong` int(11) NOT NULL,
  `f_staff` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `e_breed_breedinginfo`
--

DROP TABLE IF EXISTS `e_breed_breedinginfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `e_breed_breedinginfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `breeding_date` date NOT NULL,
  `pre_production_date` date NOT NULL,
  `breeding_way` int(11) NOT NULL,
  `ewe_id` int(11) DEFAULT NULL,
  `ewe_variety` int(11) NOT NULL,
  `ram_id` int(11) DEFAULT NULL,
  `ram_variety` int(11) NOT NULL,
  `breeding_state` int(11) NOT NULL,
  `staff` varchar(20) DEFAULT NULL COMMENT '改成非必填，因为有在产后自动填的',
  `f_staff` varchar(20) DEFAULT NULL,
  `f_date` date NOT NULL,
  `belong` int(11) NOT NULL,
  `mat_period` int(11) DEFAULT NULL,
  `single_ok` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `e_breed_breedinginfo_copy1`
--

DROP TABLE IF EXISTS `e_breed_breedinginfo_copy1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `e_breed_breedinginfo_copy1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `breeding_date` date NOT NULL,
  `pre_production_date` date NOT NULL,
  `breeding_way` int(11) NOT NULL,
  `ewe_id` int(11) DEFAULT NULL,
  `ewe_variety` int(11) NOT NULL,
  `ram_id` int(11) DEFAULT NULL,
  `ram_variety` int(11) NOT NULL,
  `breeding_state` int(11) NOT NULL,
  `staff` varchar(8) DEFAULT NULL COMMENT '改成非必填，因为有在产后自动填的',
  `f_staff` varchar(20) DEFAULT NULL,
  `f_date` date NOT NULL,
  `belong` int(11) NOT NULL,
  `mat_period` int(11) DEFAULT NULL,
  `single_ok` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `e_breed_export_breed`
--

DROP TABLE IF EXISTS `e_breed_export_breed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `e_breed_export_breed` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `breeding_id` int(11) DEFAULT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `e_breed_lambinfo`
--

DROP TABLE IF EXISTS `e_breed_lambinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `e_breed_lambinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `breeding_id` int(11) NOT NULL,
  `basic_id` int(11) DEFAULT NULL,
  `tobasic` tinyint(1) NOT NULL,
  `logo` varchar(35) DEFAULT NULL,
  `ele_num` varchar(20) DEFAULT NULL COMMENT '改成20',
  `pre_num` varchar(16) DEFAULT NULL,
  `purpose` int(11) DEFAULT NULL,
  `variety` int(11) DEFAULT NULL,
  `sex` int(11) DEFAULT NULL,
  `belong` int(11) NOT NULL,
  `manu_info_id` int(11) DEFAULT NULL,
  `manu_info_name` varchar(50) DEFAULT NULL,
  `state` int(11) DEFAULT NULL,
  `birth` date DEFAULT NULL,
  `bir_weight` double DEFAULT NULL,
  `wea_date` date DEFAULT NULL COMMENT '移栽/分株日期',
  `wea_weight` double DEFAULT NULL,
  `house_id` int(11) DEFAULT NULL,
  `hurdle_id` int(11) DEFAULT NULL,
  `house_name` varchar(30) DEFAULT NULL,
  `hurdle_name` varchar(30) DEFAULT NULL,
  `mon_age` double DEFAULT NULL,
  `father_id` int(11) DEFAULT NULL,
  `mother_id` int(11) DEFAULT NULL,
  `f_ele_num` varchar(16) DEFAULT NULL,
  `f_pre_num` varchar(16) DEFAULT NULL,
  `m_ele_num` varchar(16) DEFAULT NULL,
  `m_pre_num` varchar(16) DEFAULT NULL,
  `f_staff` varchar(20) DEFAULT NULL,
  `f_date` date DEFAULT NULL,
  `img_positive` varchar(100) DEFAULT NULL,
  `img_left` varchar(100) DEFAULT NULL,
  `img_right` varchar(100) DEFAULT NULL,
  `note` longtext,
  `color` int(11) DEFAULT NULL,
  `rank` int(11) DEFAULT NULL,
  `gene_a` int(11) DEFAULT NULL,
  `score` int(11) unsigned zerofill DEFAULT NULL,
  `score_2` int(11) DEFAULT NULL,
  `score_6` int(11) DEFAULT NULL,
  `score_12` int(11) DEFAULT NULL,
  `score_24` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `logo` (`logo`) USING BTREE,
  UNIQUE KEY `ele_num` (`ele_num`) USING BTREE,
  UNIQUE KEY `pre_num` (`pre_num`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `e_breed_lambinfo_copy1`
--

DROP TABLE IF EXISTS `e_breed_lambinfo_copy1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `e_breed_lambinfo_copy1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `breeding_id` int(11) NOT NULL,
  `basic_id` int(11) DEFAULT NULL,
  `tobasic` tinyint(1) NOT NULL,
  `logo` varchar(35) DEFAULT NULL,
  `ele_num` varchar(20) DEFAULT NULL COMMENT '改成20',
  `pre_num` varchar(16) DEFAULT NULL,
  `purpose` int(11) DEFAULT NULL,
  `variety` int(11) DEFAULT NULL,
  `sex` int(11) DEFAULT NULL,
  `belong` int(11) NOT NULL,
  `manu_info_id` int(11) DEFAULT NULL,
  `manu_info_name` varchar(50) DEFAULT NULL,
  `state` int(11) DEFAULT NULL,
  `birth` date DEFAULT NULL,
  `bir_weight` double DEFAULT NULL,
  `wea_date` date DEFAULT NULL COMMENT '移栽/分株日期',
  `wea_weight` double DEFAULT NULL,
  `house_id` int(11) DEFAULT NULL,
  `hurdle_id` int(11) DEFAULT NULL,
  `house_name` varchar(30) DEFAULT NULL,
  `hurdle_name` varchar(30) DEFAULT NULL,
  `mon_age` double DEFAULT NULL,
  `father_id` int(11) DEFAULT NULL,
  `mother_id` int(11) DEFAULT NULL,
  `f_ele_num` varchar(16) DEFAULT NULL,
  `f_pre_num` varchar(16) DEFAULT NULL,
  `m_ele_num` varchar(16) DEFAULT NULL,
  `m_pre_num` varchar(16) DEFAULT NULL,
  `f_staff` varchar(20) DEFAULT NULL,
  `f_date` date DEFAULT NULL,
  `img_positive` varchar(100) DEFAULT NULL,
  `img_left` varchar(100) DEFAULT NULL,
  `img_right` varchar(100) DEFAULT NULL,
  `note` longtext,
  `color` int(11) DEFAULT NULL,
  `rank` int(11) DEFAULT NULL,
  `gene_a` int(11) DEFAULT NULL,
  `score` int(11) unsigned zerofill DEFAULT NULL,
  `score_2` int(11) DEFAULT NULL,
  `score_6` int(11) DEFAULT NULL,
  `score_12` int(11) DEFAULT NULL,
  `score_24` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `logo` (`logo`) USING BTREE,
  UNIQUE KEY `ele_num` (`ele_num`) USING BTREE,
  UNIQUE KEY `pre_num` (`pre_num`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `e_breed_postnatalinfo`
--

DROP TABLE IF EXISTS `e_breed_postnatalinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `e_breed_postnatalinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `breeding_id` int(11) DEFAULT NULL,
  `breeding_date` date DEFAULT NULL,
  `delivery_date` date DEFAULT NULL,
  `ram_id` int(11) DEFAULT NULL,
  `ewe_id` int(11) DEFAULT NULL,
  `Booroola` double DEFAULT NULL,
  `ewe_health` tinyint(1) NOT NULL,
  `ewe_condition` int(11) NOT NULL,
  `lamb_ele_num` varchar(20) DEFAULT NULL COMMENT '改成非必填，20，这个就是个无用字段',
  `lamb_state` int(11) DEFAULT NULL,
  `bir_weight` double DEFAULT NULL,
  `live_num` int(11) DEFAULT NULL,
  `birth_attendants` varchar(8) NOT NULL COMMENT '这个得改前端成必填',
  `f_staff` varchar(20) DEFAULT NULL,
  `f_date` date DEFAULT NULL,
  `notes` longtext COMMENT '改成非必填',
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `e_breed_pregnantinfo`
--

DROP TABLE IF EXISTS `e_breed_pregnantinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `e_breed_pregnantinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `check_type` varchar(20) NOT NULL,
  `breeding_id` int(11) NOT NULL,
  `In_pregnancy` varchar(40) NOT NULL,
  `f_staff` varchar(20) DEFAULT NULL,
  `f_date` date NOT NULL,
  `notes` longtext NOT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `e_breed_pregnantinfo_copy1`
--

DROP TABLE IF EXISTS `e_breed_pregnantinfo_copy1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `e_breed_pregnantinfo_copy1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `check_type` varchar(20) NOT NULL,
  `breeding_id` int(11) NOT NULL,
  `In_pregnancy` varchar(40) NOT NULL,
  `f_staff` varchar(20) DEFAULT NULL,
  `f_date` date NOT NULL,
  `notes` longtext NOT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `e_breed_rutinfo`
--

DROP TABLE IF EXISTS `e_breed_rutinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `e_breed_rutinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `basic_id` int(11) NOT NULL,
  `age` int(11) DEFAULT NULL,
  `breeding` tinyint(1) NOT NULL,
  `f_staff` varchar(20) DEFAULT NULL,
  `f_date` date NOT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `e_breed_semencollectinfo`
--

DROP TABLE IF EXISTS `e_breed_semencollectinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `e_breed_semencollectinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `basic_id` int(11) NOT NULL,
  `E_date` date NOT NULL,
  `dilution_ratio` double DEFAULT NULL,
  `diluent_type` int(11) DEFAULT NULL,
  `disused` tinyint(1) NOT NULL,
  `f_staff` varchar(20) DEFAULT NULL,
  `f_date` date NOT NULL,
  `belong` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `e_breed_weaninginfo`
--

DROP TABLE IF EXISTS `e_breed_weaninginfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `e_breed_weaninginfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lamb_id` int(11) NOT NULL,
  `Delivery_date` date NOT NULL,
  `feeding_way` int(11) NOT NULL,
  `Bir_weight` double DEFAULT NULL,
  `wea_weight` double DEFAULT NULL,
  `belong` int(11) NOT NULL,
  `f_staff` varchar(20) DEFAULT NULL,
  `rank` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `g_slaughter_g_salesinfo`
--

DROP TABLE IF EXISTS `g_slaughter_g_salesinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `g_slaughter_g_salesinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `belong` int(11) NOT NULL,
  `sales_date` date NOT NULL,
  `sales_order` varchar(20) NOT NULL,
  `type` int(11) NOT NULL,
  `billing_unit` varchar(5) NOT NULL,
  `unit_price` double DEFAULT NULL,
  `weight` double DEFAULT NULL COMMENT '重量',
  `total_price` double DEFAULT NULL,
  `transportation` varchar(15) NOT NULL,
  `img_trans` varchar(100) DEFAULT NULL COMMENT '非必填',
  `sales_site` longtext NOT NULL,
  `name` varchar(10) NOT NULL,
  `buyer` varchar(5) NOT NULL,
  `buyer_phone` varchar(11) NOT NULL,
  `selling_type` int(11) NOT NULL,
  `notes` varchar(30) DEFAULT NULL COMMENT '非必填',
  `f_staff` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `g_slaughter_s_salesinfo`
--

DROP TABLE IF EXISTS `g_slaughter_s_salesinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `g_slaughter_s_salesinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `belong` int(11) NOT NULL,
  `sales_date` date NOT NULL,
  `sales_order` varchar(20) NOT NULL,
  `type` int(11) NOT NULL,
  `quarantine_coding` varchar(20) DEFAULT NULL,
  `ele_num` varchar(20) NOT NULL,
  `age` double DEFAULT NULL,
  `medical_leave` tinyint(1) NOT NULL,
  `billing_unit` varchar(5) NOT NULL,
  `unit_price` double DEFAULT NULL,
  `weight` double DEFAULT NULL COMMENT '株高/长势，只数',
  `total_price` double DEFAULT NULL,
  `transportation` varchar(15) NOT NULL,
  `img_trans` varchar(100) DEFAULT NULL,
  `sales_site` longtext NOT NULL,
  `name` varchar(20) NOT NULL,
  `buyer` varchar(50) NOT NULL,
  `buyer_phone` varchar(11) NOT NULL,
  `selling_type` int(11) NOT NULL,
  `basic_id` int(11) NOT NULL,
  `notes` longtext,
  `f_staff` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `ele_num` (`ele_num`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `h_store_feeding_out`
--

DROP TABLE IF EXISTS `h_store_feeding_out`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `h_store_feeding_out` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `outbound_no` varchar(20) NOT NULL,
  `type` int(11) NOT NULL,
  `f_name` varchar(15) NOT NULL,
  `ingredientsType` int(11) NOT NULL COMMENT '成分类型',
  `warehouse_num` int(11) DEFAULT NULL,
  `delivery_time` date NOT NULL,
  `out_purposes` longtext,
  `num` int(11) DEFAULT NULL,
  `out_price` double DEFAULT NULL COMMENT '出库价格，后端自动填充',
  `out_staff` varchar(12) NOT NULL,
  `maker_id` int(11) DEFAULT NULL,
  `contact_phone` varchar(11) DEFAULT NULL,
  `notes` longtext,
  `belong` int(11) NOT NULL,
  `f_staff` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `outbound_no` (`outbound_no`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;
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
  `f_name` varchar(15) NOT NULL,
  `ingredientsType` int(11) NOT NULL COMMENT '成分类型',
  `warehouse_num` int(11) DEFAULT NULL,
  `nutrients` longtext,
  `buy_time` date NOT NULL,
  `billing_unit` varchar(3) NOT NULL,
  `quantity` double NOT NULL,
  `unit_price` double NOT NULL,
  `total_price` double DEFAULT NULL,
  `specifications` varchar(15) DEFAULT NULL,
  `purpose` longtext,
  `water_content` varchar(5) DEFAULT NULL,
  `mildew` varchar(5) DEFAULT NULL,
  `impurity_content` varchar(5) DEFAULT NULL,
  `maker_id` int(11) DEFAULT NULL,
  `notes` longtext,
  `f_date` date NOT NULL,
  `operation` longtext,
  `keep_amount` double DEFAULT NULL,
  `belong` int(11) NOT NULL,
  `f_staff` varchar(20) DEFAULT NULL,
  `fare` double DEFAULT NULL,
  `avg_price` double DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;
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
  `goods` varchar(10) DEFAULT NULL,
  `maker_id` int(11) DEFAULT NULL,
  `ingredientsType` int(11) NOT NULL COMMENT '成分类型：中药，西药，生物制剂，其他',
  `quantity` double DEFAULT NULL,
  `stockPrice` double(11,2) DEFAULT NULL COMMENT '库存价格',
  `totalCost` double DEFAULT NULL COMMENT '总花费',
  `alert` double DEFAULT NULL,
  `f_date` date DEFAULT NULL,
  `operation` longtext,
  `belong` int(11) NOT NULL,
  `out_time` date DEFAULT NULL,
  `f_staff` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `h_store_vaccine_in`
--

DROP TABLE IF EXISTS `h_store_vaccine_in`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `h_store_vaccine_in` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `v_name` varchar(30) NOT NULL,
  `type` int(11) NOT NULL,
  `maker_id` int(11) DEFAULT NULL,
  `ingredientsType` int(11) NOT NULL COMMENT '类型成分',
  `purpose` varchar(30) DEFAULT NULL,
  `produce_date` date NOT NULL,
  `expiration_date` date NOT NULL,
  `produce_num` varchar(15) NOT NULL,
  `billing_unit` varchar(5) DEFAULT NULL,
  `in_amount` int(11) NOT NULL,
  `unit_price` double NOT NULL,
  `total_price` double DEFAULT NULL,
  `in_time` date NOT NULL,
  `keep_amount` double DEFAULT NULL,
  `f_date` date NOT NULL,
  `operation` longtext,
  `belong` int(11) NOT NULL,
  `f_staff` varchar(20) DEFAULT NULL,
  `fare` double DEFAULT NULL,
  `avg_price` double DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `h_store_vaccine_out`
--

DROP TABLE IF EXISTS `h_store_vaccine_out`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `h_store_vaccine_out` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `outbound_no` varchar(20) NOT NULL,
  `v_name` varchar(20) NOT NULL,
  `type` int(11) NOT NULL,
  `ingredientsType` int(11) NOT NULL COMMENT '类型成分',
  `delivery_time` date NOT NULL,
  `out_purposes` longtext,
  `num` int(11) DEFAULT NULL,
  `out_price` double DEFAULT NULL COMMENT '出库时候的价格，后端自动填充的',
  `maker_id` int(11) DEFAULT NULL,
  `out_staff` varchar(12) NOT NULL,
  `contact_phone` varchar(11) DEFAULT NULL,
  `notes` longtext,
  `belong` int(11) NOT NULL,
  `f_staff` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `outbound_no` (`outbound_no`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `sheep_asset_standardinfo`
--

DROP TABLE IF EXISTS `sheep_asset_standardinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sheep_asset_standardinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `variety` int(11) DEFAULT NULL,
  `sex` int(11) DEFAULT NULL,
  `purpose` int(11) DEFAULT NULL,
  `unit_price` double(10,2) DEFAULT NULL,
  `rank_0` double(10,2) DEFAULT NULL,
  `rank_1` double(10,2) DEFAULT NULL,
  `rank_2` double(10,2) DEFAULT NULL,
  `rank_3` double(10,2) DEFAULT NULL,
  `rank_9` double(10,2) DEFAULT NULL,
  `f_date` date DEFAULT NULL,
  `f_staff` varchar(20) DEFAULT NULL,
  `notes` longtext,
  `belong` int(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `sheep_assetinfo`
--

DROP TABLE IF EXISTS `sheep_assetinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sheep_assetinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `variety` int(11) DEFAULT NULL,
  `sex` int(11) DEFAULT NULL,
  `purpose` int(11) DEFAULT NULL,
  `number` int(11) DEFAULT NULL,
  `sum_weight` double DEFAULT NULL,
  `sum_value` double DEFAULT NULL,
  `f_date` date DEFAULT NULL,
  `notes` longtext,
  `belong` int(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
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
  `cname` varchar(20) NOT NULL,
  `explain` longtext,
  `belong` int(11) NOT NULL,
  `f_staff` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;
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
  `supplier_name` varchar(20) NOT NULL,
  `sale_type` longtext NOT NULL,
  `sup_linkman` varchar(5) NOT NULL,
  `sup_contact` varchar(11) NOT NULL,
  `contact` varchar(11) NOT NULL,
  `mail` varchar(25) DEFAULT NULL,
  `address` varchar(40) DEFAULT NULL,
  `f_date` date NOT NULL,
  `operation` longtext,
  `f_staff` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `supplier_name` (`supplier_name`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
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
  `in_name` varchar(20) NOT NULL,
  `contact` varchar(11) NOT NULL,
  `mail` varchar(25) DEFAULT NULL,
  `handler` varchar(5) NOT NULL,
  `link` varchar(11) NOT NULL,
  `f_date` date NOT NULL,
  `f_staff` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `in_name` (`in_name`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;
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
  `supplier_name` varchar(20) NOT NULL,
  `sale_type` longtext NOT NULL,
  `sup_linkman` varchar(5) NOT NULL,
  `sup_contact` varchar(11) NOT NULL,
  `contact` varchar(11) DEFAULT NULL,
  `mail` varchar(25) DEFAULT NULL,
  `address` varchar(40) NOT NULL,
  `f_date` date NOT NULL,
  `operation` longtext,
  `f_staff` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `testuser`
--

DROP TABLE IF EXISTS `testuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `testuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` char(50) NOT NULL,
  `password` char(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `threshold_setting`
--

DROP TABLE IF EXISTS `threshold_setting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `threshold_setting` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `vaccine_id` int(11) DEFAULT NULL,
  `threshold` int(11) DEFAULT NULL,
  `threshold_mon` int(11) DEFAULT NULL,
  `threshold_year` int(11) DEFAULT NULL,
  `ifyear` int(3) DEFAULT NULL,
  `ifchange` int(3) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `w_information_immunizationMessageinfo`
--

DROP TABLE IF EXISTS `w_information_immunizationMessageinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `w_information_immunizationMessageinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `basic_id` int(20) DEFAULT NULL,
  `ele_num` varchar(20) DEFAULT NULL,
  `pre_num` varchar(16) DEFAULT NULL,
  `sex` int(11) DEFAULT NULL,
  `variety` int(11) DEFAULT NULL,
  `mon_age` double DEFAULT NULL,
  `house` varchar(30) DEFAULT NULL,
  `hurdle_name` varchar(30) DEFAULT NULL,
  `vaccine_id` int(11) DEFAULT NULL,
  `birth` date DEFAULT NULL,
  `imm_date` date DEFAULT NULL,
  `distance_date` int(11) DEFAULT NULL,
  `dead_date` date DEFAULT NULL,
  `state` int(11) DEFAULT NULL,
  `f_staff` varchar(20) DEFAULT NULL,
  `f_date` datetime DEFAULT NULL,
  `note` longtext,
  `belong` int(6) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;


--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
