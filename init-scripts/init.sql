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

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `sheep_test` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `sheep_test`;

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

-- =============================================
-- Seed Data: Essential initial data for application to function
-- =============================================

-- testuser: Web login accounts (passwords are MD5 hashed)
INSERT INTO `testuser` VALUES
(1,'2213145737','b8f994d0c9e22cb4c365915254cb0d2c','2024-10-13 15:48:49'),
(2,'mmy','e10adc3949ba59abbe56e057f20f883e','2024-08-03 17:15:34'),
(3,'zzj','36e98a88e8d4b30ba495552364e1ae68','2025-03-09 00:16:05'),
(4,'qsh','a0aa2b7e42652b6435b7916d29c799e4','2025-03-21 17:59:39'),
(5,'tianyu','c039caca607ac85ccbb5beb6ec94f2c0','2025-03-21 10:16:32'),
(6,'zhihao','2db911806d1ec2263991a4615cbcbaf1','2025-03-02 11:17:09'),
(7,'admin','e10adc3949ba59abbe56e057f20f883e','2025-03-06 15:20:06'),
(8,'ggz','ff44112fd8c44ba87ee7b392a24d99b6','2025-03-20 09:14:18'),
(9,'wxf','35dfea21bda42a3f582921cbe25e4a37','2025-03-10 10:23:39'),
(10,'xyh','cb0495e9a9b008c797261e9ba4b5228f','2025-03-17 08:39:46'),
(11,'xxwfsh','0d70877519dd55ea7804de20ed511c56','2025-03-17 08:58:23');

-- app_users: App-side user accounts
INSERT INTO `app_users` VALUES
(1,'18812341234','18812341234',1,NULL),
(2,'111','111',2,NULL),
(3,'222','222',3,NULL),
(4,'zzj','zzj123456',1,NULL),
(5,'wangxinfeng','wang073425',1,NULL),
(6,'xieyunheng','xie12345678',1,NULL),
(7,'zhihao','zhihao19840610',1,NULL);

-- app_auth: Permission configuration
INSERT INTO `app_auth` VALUES
(1,0,0,NULL,'高级用户','角色'),
(2,0,0,NULL,'普通用户','角色'),
(3,0,0,NULL,'演示用户','角色'),
(4,1,0,19,'种植区_种植监测_第1个',''),
(5,1,1,19,'种植区_种植监测_第2个',NULL),
(6,1,2,19,'种植区_种植监测_第3个',NULL),
(7,1,3,19,'种植区_种植监测_第4个',NULL),
(8,1,4,19,'种植区_种植监测_第5个',NULL),
(9,1,5,19,'种植区_种植监测_第6个',NULL),
(10,2,0,0,NULL,NULL),
(11,2,1,0,NULL,NULL),
(12,1,6,19,'种植区_种植监测_第7个',NULL),
(13,1,7,19,'种植区_种植监测_第8个',NULL),
(14,1,8,19,'种植区_种植监测_第9个',NULL),
(15,1,9,19,'种植区_种植监测_第10个',NULL),
(16,1,10,19,'种植区_种植监测_第11个',NULL),
(17,1,0,0,'种植区基地',NULL),
(18,1,1,0,'扩繁基地',NULL),
(19,1,0,17,'种植区_种植监测管理',NULL),
(20,1,1,17,'种植区_防治管理',NULL),
(21,1,2,17,'种植区_营养管理',NULL),
(22,1,3,17,'种植区_效益管理',NULL),
(0,1,NULL,NULL,'全场',NULL),
(23,1,0,18,'扩繁_种植监测管理',NULL),
(24,1,1,18,'扩繁_防治管理',NULL),
(25,1,2,18,'扩繁_营养管理',NULL),
(26,1,3,18,'扩繁_效益管理',NULL),
(27,1,11,19,'种植区_种植监测_第12个',NULL),
(28,1,0,23,'扩繁_种植监测_第1个',NULL),
(29,1,1,23,'扩繁_种植监测_第2个',NULL),
(30,1,2,23,'扩繁_种植监测_第3个',NULL),
(31,1,3,23,'扩繁_种植监测_第4个',NULL),
(32,1,4,23,'扩繁_种植监测_第5个',NULL),
(33,1,5,23,'扩繁_种植监测_第6个',NULL),
(34,1,6,23,'扩繁_种植监测_第7个',NULL),
(35,1,7,23,'扩繁_种植监测_第8个',NULL),
(36,1,8,23,'扩繁_种植监测_第9个',NULL),
(37,1,9,23,'扩繁_种植监测_第10个',NULL),
(38,1,0,5,'种植区_种植监测_扩繁/育种_第1个',NULL),
(39,1,1,5,'种植区_种植监测_扩繁/育种_第2个',NULL),
(40,1,2,5,'种植区_种植监测_扩繁/育种_第3个',NULL),
(41,1,3,5,'种植区_种植监测_扩繁/育种_第4个',NULL),
(42,1,0,29,'扩繁_种植监测_扩繁/育种_第1个',NULL),
(43,1,1,29,'扩繁_种植监测_扩繁/育种_第2个',NULL),
(44,1,2,29,'扩繁_种植监测_扩繁/育种_第3个',NULL),
(45,1,3,29,'扩繁_种植监测_扩繁/育种_第4个',NULL),
(46,1,0,6,'种植区_种植监测_卫生_第1个',NULL),
(47,1,1,6,'种植区_种植监测_卫生_第2个',NULL),
(48,1,0,30,'扩繁_种植监测_卫生_第1个',NULL),
(49,1,1,30,'扩繁_种植监测_卫生_第2个',NULL),
(50,1,2,6,'种植区_种植监测_卫生_第3个',NULL),
(51,1,2,30,'扩繁_种植监测_卫生_第3个',NULL),
(52,1,0,14,'种植区_种植监测_库存_第1个',NULL),
(53,1,1,14,'种植区_种植监测_库存_第2个',NULL),
(54,1,2,14,'种植区_种植监测_库存_第3个',NULL),
(55,1,3,14,'种植区_种植监测_库存_第4个',NULL),
(56,1,4,14,'种植区_种植监测_库存_第5个',NULL),
(57,1,0,36,'种植区_种植监测_扩繁/育种_第1个',NULL),
(58,1,1,36,'种植区_种植监测_扩繁/育种_第2个',NULL),
(59,1,2,36,'种植区_种植监测_扩繁/育种_第3个',NULL),
(60,1,3,36,'种植区_种植监测_扩繁/育种_第4个',NULL),
(61,1,4,36,'种植区_种植监测_扩繁/育种_第5个',NULL);

-- app_config: Application configuration
INSERT INTO `app_config` VALUES ('secret_key','E8iT8LG6XrIjCVKJ0Kfp','app密钥');

-- basic_manuinfo: Source/farm information
INSERT INTO `basic_manuinfo` VALUES
(-1,'锡林格勒梦',0,0,'','','','','','','','',1),
(2,'呼和浩特草地/草田/草区',0,0,'','','','','','','','',2),
(3,'草原草地/草田/草区',0,0,'','','','','','','','',3),
(4,'测试草地/草田/草区4',0,0,'','','','','','','','',4),
(7,'777',0,0,'','','','','','','','',7),
(8,'888',0,0,'','','','','','','','',8),
(9,'9',0,0,'','','','','','','','',9),
(10,'10',0,0,'','','','','','','','',10),
(11,'本场扩繁',0,0,'','','','','','','','',0),
(12,'外购',1,0,'','','','','','','','',0),
(13,'韩跃朋',3,0,'','','','韩跃朋','','','','',0);

-- threshold_setting: Immunization alert thresholds
INSERT INTO `threshold_setting` VALUES
(1,12,121,0,0,0,0),
(2,9,209,NULL,NULL,0,0),
(3,25,306,0,0,0,0),
(4,11,90,0,0,0,0);

-- basic_makescore: Scoring criteria
INSERT INTO `basic_makescore` VALUES
(1,0,1,0,2,3,2.7,2.4,17,15,13.5,46.5,64.5,100,0,57.2,72.5,82,0,73,81,81,0,85,85,85,0,0.5,0.5,0.5,0,10,10,10,180,1,1.5,2,1,1,0,0.75,2.4,1.7,1,0,1,1,1,1,1,0,NULL),
(2,0,1,1,2,3,2.7,2.4,17,15,13.5,46.5,64.5,100,0,57.2,72.5,82,0,73,81,81,0,85,85,85,0,0.5,0.5,0.5,0,10,10,10,180,1,1.5,2,1,1,0,0.75,2.4,1.7,1,0,1,1,1,1,1,0,''),
(3,0,1,2,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,NULL,NULL,NULL,NULL,NULL,0,NULL),
(4,1,1,0,2,3,2.7,2.4,17,15,13.5,29,45,52,0,64,68,74,0,64,70,76,0,77,81,88,0,0.76,0.76,0.76,0,11,11,11,185,1,1.5,2,1,1,0,0.75,2.4,1.7,1,0,1,1,1,1,1,0,NULL),
(5,1,1,1,2,3,2.7,2.4,17,15,13.5,29,45,52,0,64,68,74,0,64,70,76,0,77,81,88,0,0.76,0.76,0.76,0,11,11,11,185,1,1.5,2,1,1,0,0.75,2.4,1.7,1,0,1,1,1,1,1,0,NULL),
(6,1,1,2,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,NULL,NULL,NULL,NULL,NULL,0,NULL),
(7,0,0,0,2,3.5,3,2.7,18.7,17.5,16,46.5,64.5,100,57.2,72.5,86.5,88.2,61.5,85,92.5,94.5,70,88,101,105,0,0,0,0,0,14.6,17.4,17.4,240,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,1,1,1,1,0,NULL),
(8,0,0,1,2,3.5,3,2.7,18.7,17.5,16,46.5,64.5,100,57.2,72.5,86.5,88.2,61.5,85,92.5,94.5,70,88,101,105,0,0,0,0,0,14.6,17.4,17.4,240,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,1,1,1,1,0,NULL),
(9,0,0,2,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,NULL,NULL,NULL,NULL,NULL,0,NULL),
(10,1,0,0,2,4,3.5,3,18.7,17.5,16,60,80,100,0,80,91,95,0,82,92,96,0,90,95,101,0,0.88,0.88,0.88,0,14.6,20,20,300,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,1,1,1,1,0,NULL),
(11,1,0,1,2,4,3.5,3,18.7,17.5,16,60,80,100,0,80,91,95,0,82,92,96,0,90,95,101,0,0.88,0.88,0.88,0,14.6,20,20,300,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,1,1,1,1,0,NULL),
(12,1,0,2,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,NULL,NULL,NULL,NULL,NULL,0,NULL);


-- colony_houseinfo: Ranch/house/pen hierarchy
INSERT INTO `colony_houseinfo` VALUES (2,0,'暂存区','2020-08-10',2,100,0,'6','7',1,'16.666666666666668','tom',-838,NULL,0,NULL,NULL),(5,2,'小号草棚','2020-08-02',5,234,1,'sf','df',2,'0','哈哈',-2,'2024-01-03',0,NULL,NULL),(7,0,'塘夏1草棚','2020-08-01',1,600,1,'1','500*500*500',1,'0','张国威',0,NULL,1,NULL,NULL),(12,2,'大号鹏','2020-08-05',7,45,1,'34*34*89','45*45*80',2,'0','李想',0,'2024-01-03',0,NULL,NULL),(27,0,'北场区/南场区1单元','2013-01-01',4,580.8599999999999,2,'4.2*11.5*3','0.0',0,'3.4574999999999996','admin',86,NULL,0,NULL,NULL),(28,0,'北场区/南场区2单元','2013-01-01',4,691.5,2,'5*11.5*3','0.0',0,'4.295031055900621','admin',38,NULL,0,NULL,NULL),(29,0,'北场区/南场区3单元','2013-01-01',4,691.5,2,'5*11.5*3','0.0',0,'6.01304347826087','admin',220,NULL,0,NULL,NULL),(30,0,'北场区/南场区4单元','2013-01-01',4,691.5,2,'5*11.5*3','0.0',0,'1.6865853658536585','admin',57,NULL,0,NULL,NULL),(31,0,'北场区/南场区5单元','2013-01-01',4,691.5,2,'5*11.5*3','0.0',0,'2.443462897526502','admin',-165,NULL,0,NULL,NULL),(32,0,'北场区/南场区6单元','2013-01-01',4,580.8599999999999,2,'4.2*11.5*3','0.0',0,'2.5588546255506603','admin',-119,NULL,0,NULL,NULL),(33,27,'1区','2013-01-01',4,48.3,2,'4.2*11.5*3','0.0',0,'3.4499999999999997','admin',6,'2024-01-03',0,NULL,NULL),(34,27,'2区','2013-01-01',4,50.4,2,'4.2*12*3','0.0',0,'0','admin',0,'2024-01-03',0,NULL,NULL),(35,27,'3区','2013-01-01',4,50.4,2,'4.2*12*3','0.0',0,'16.8','admin',3,'2024-01-03',0,NULL,NULL),(36,27,'4区','2013-01-01',4,50.4,2,'4.2*12*3','0.0',0,'0','admin',0,'2024-01-03',0,NULL,NULL),(37,27,'5区','2013-01-01',4,50.4,2,'4.2*12*3','0.0',0,'0','admin',25,'2024-01-03',0,NULL,NULL),(38,27,'6区','2013-01-01',4,42,2,'4.2*10*3','0.0',0,'0','admin',11,'2024-01-03',0,NULL,NULL),(39,27,'7区','2013-01-01',4,37.8,2,'4.2*9*3','0.0',0,'0','admin',5,'2024-01-03',0,NULL,NULL),(40,27,'8区','2013-01-01',4,50.4,2,'4.2*12*3','0.0',0,'2.290909090909091','admin',6,'2024-01-03',0,NULL,NULL),(41,27,'9区','2013-01-01',4,50.4,2,'4.2*12*3','0.0',0,'1.3263157894736841','admin',10,'2024-01-03',0,NULL,NULL),(42,27,'10区','2013-01-01',4,50.4,2,'4.2*12*3','0.0',0,'1.68','admin',8,'2024-01-03',0,NULL,NULL),(43,27,'11区','2013-01-01',4,50.4,2,'4.2*12*3','0.0',0,'2.016','admin',-2,'2024-01-03',0,NULL,NULL),(44,27,'12区','2013-01-01',4,49.56,2,'4.2*11.8*3','0.0',0,'1.3766666666666667','admin',14,'2024-01-03',0,NULL,NULL),(45,28,'1区','2013-01-01',4,57.5,2,'5*11.5*3','0.0',0,'0','admin',0,'2024-01-03',0,NULL,NULL),(46,28,'2区','2013-01-01',4,60,2,'5*12*3','0.0',0,'0','admin',0,'2024-01-03',0,NULL,NULL),(47,28,'3区','2013-01-01',4,60,2,'5*12*3','0.0',0,'0','admin',0,'2024-01-03',0,NULL,NULL),(48,28,'4区','2013-01-01',4,60,2,'5*12*3','0.0',0,'0','admin',0,'2024-01-03',0,NULL,NULL),(49,28,'5区','2013-01-01',4,60,2,'5*12*3','0.0',0,'0','admin',0,'2024-01-03',0,NULL,NULL),(50,28,'6区','2013-01-01',4,50,2,'5*10*3','0.0',0,'0','admin',0,'2024-01-03',0,NULL,NULL),(51,28,'7区','2013-01-01',4,45,2,'5*9*3','0.0',0,'1.25','admin',2,'2024-01-03',0,NULL,NULL),(52,28,'8区','2013-01-01',4,60,2,'5*12*3','0.0',0,'3.5294117647058822','admin',0,'2024-01-03',0,NULL,NULL),(53,28,'9区','2013-01-01',4,60,2,'5*12*3','0.0',0,'8.571428571428571','admin',0,'2024-01-03',0,NULL,NULL),(54,28,'10区','2013-01-01',4,60,2,'5*12*3','0.0',0,'1.3043478260869565','admin',19,'2024-01-03',0,NULL,NULL),(55,28,'11区','2013-01-01',4,60,2,'5*12*3','0.0',0,'1.4285714285714286','admin',18,'2024-01-03',0,NULL,NULL),(56,28,'12区','2013-01-01',4,59,2,'5*11.8*3','0.0',0,'59.0','admin',-2,'2024-01-03',0,NULL,NULL),(57,29,'1区','2013-01-01',4,57.5,2,'5*11.5*3','0.0',0,'0','admin',197,'2024-01-03',0,NULL,NULL),(58,29,'2区','2013-01-01',4,60,2,'5*12*3','0.0',0,'0','admin',0,'2024-01-03',0,NULL,NULL),(59,29,'3区','2013-01-01',4,60,2,'5*12*3','0.0',0,'0','admin',0,'2024-01-03',0,NULL,NULL),(60,29,'4区','2013-01-01',4,60,2,'5*12*3','0.0',0,'0','admin',0,'2024-01-03',0,NULL,NULL),(61,29,'5区','2013-01-01',4,60,2,'5*12*3','0.0',0,'0','admin',0,'2024-01-03',0,NULL,NULL),(62,29,'6区','2013-01-01',4,50,2,'5*10*3','0.0',0,'0','admin',0,'2024-01-03',0,NULL,NULL),(63,29,'7区','2013-01-01',4,45,2,'5*9*3','0.0',0,'0','admin',-1,'2024-01-03',0,NULL,NULL),(64,29,'8区','2013-01-01',4,60,2,'5*12*3','0.0',0,'0','admin',0,'2024-01-03',0,NULL,NULL),(65,29,'9区','2013-01-01',4,60,2,'5*12*3','0.0',0,'1.0344827586206897','admin',23,'2024-01-03',0,NULL,NULL),(66,29,'10区','2013-01-01',4,60,2,'5*12*3','0.0',0,'4.0','admin',0,'2024-01-03',0,NULL,NULL),(67,29,'11区','2013-01-01',4,60,2,'5*12*3','0.0',0,'2.857142857142857','admin',0,'2024-01-03',0,NULL,NULL),(68,29,'12区','2013-01-01',4,59,2,'5*11.8*3','0.0',0,'29.5','admin',1,'2024-01-03',0,NULL,NULL),(69,30,'1区','2013-01-01',4,57.5,2,'5*11.5*3','0.0',0,'1.7424242424242424','admin',0,'2024-01-03',0,NULL,NULL),(70,30,'2区','2013-01-01',4,60,2,'5*12*3','0.0',0,'1.8181818181818181','admin',-3,'2024-01-03',0,NULL,NULL),(71,30,'3区','2013-01-01',4,60,2,'5*12*3','0.0',0,'2.0','admin',-2,'2024-01-03',0,NULL,NULL),(72,30,'4区','2013-01-01',4,60,2,'5*12*3','0.0',0,'1.6216216216216217','admin',0,'2024-01-03',0,NULL,NULL),(73,30,'5区','2013-01-01',4,60,2,'5*12*3','0.0',0,'1.5789473684210527','admin',-2,'2024-01-03',0,NULL,NULL),(74,30,'6区','2013-01-01',4,50,2,'5*10*3','0.0',0,'1.9230769230769231','admin',18,'2024-01-03',0,NULL,NULL),(75,30,'7区','2013-01-01',4,45,2,'5*9*3','0.0',0,'15.0','admin',3,'2024-01-03',0,NULL,NULL),(76,30,'8区','2013-01-01',4,60,2,'5*12*3','0.0',0,'2.608695652173913','admin',8,'2024-01-03',0,NULL,NULL),(77,30,'9区','2013-01-01',4,60,2,'5*12*3','0.0',0,'0.9836065573770492','admin',10,'2024-01-03',0,NULL,NULL),(78,30,'10区','2013-01-01',4,60,2,'5*12*3','0.0',0,'0','admin',2,'2024-01-03',0,NULL,NULL),(79,30,'11区','2013-01-01',4,60,2,'5*12*3','0.0',0,'0','admin',0,'2024-01-03',0,NULL,NULL),(80,30,'12区','2013-01-01',4,59,2,'5*11.8*3','0.0',0,'0.47580645161290325','admin',33,'2024-01-03',0,NULL,NULL),(81,31,'1区','2013-01-01',4,57.5,2,'5*11.5*3','0.0',0,'0','admin',-43,'2024-01-03',0,NULL,NULL),(82,31,'2区','2013-01-01',4,60,2,'5*12*3','0.0',0,'1.7647058823529411','admin',-123,'2024-01-03',0,NULL,NULL),(83,31,'3区','2013-01-01',4,60,2,'5*12*3','0.0',0,'2.0689655172413794','admin',-21,'2024-01-03',0,NULL,NULL),(84,31,'4区','2013-01-01',4,60,2,'5*12*3','0.0',0,'1.875','admin',-38,'2024-01-03',0,NULL,NULL),(85,31,'5区','2013-01-01',4,60,2,'5*12*3','0.0',0,'0','admin',9,'2024-01-03',0,NULL,NULL),(86,31,'6区','2013-01-01',4,50,2,'5*10*3','0.0',0,'2.7777777777777777','admin',-12,'2024-01-03',0,NULL,NULL),(87,31,'7区','2013-01-01',4,45,2,'5*9*3','0.0',0,'1.2162162162162162','admin',3,'2024-01-03',0,NULL,NULL),(88,31,'8区','2013-01-01',4,60,2,'5*12*3','0.0',0,'5.454545454545454','admin',16,'2024-01-03',0,NULL,NULL),(89,31,'9区','2013-01-01',4,60,2,'5*12*3','0.0',0,'1.7647058823529411','admin',18,'2024-01-03',0,NULL,NULL),(90,31,'10区','2013-01-01',4,60,2,'5*12*3','0.0',0,'3.1578947368421053','admin',22,'2024-01-03',0,NULL,NULL),(91,31,'11区','2013-01-01',4,60,2,'5*12*3','0.0',0,'2.4','admin',1,'2024-01-03',0,NULL,NULL),(92,31,'12区','2013-01-01',4,59,2,'5*11.8*3','0.0',0,'2.6818181818181817','admin',2,'2024-01-03',0,NULL,NULL),(93,32,'1区','2013-01-01',4,48.3,2,'4.2*11.5*3','0.0',0,'48.3','admin',-32,'2024-01-03',0,NULL,NULL),(94,32,'2区','2013-01-01',4,50.4,2,'4.2*12*3','0.0',0,'0','admin',-19,'2024-01-03',0,NULL,NULL),(95,32,'3区','2013-01-01',4,50.4,2,'4.2*12*3','0.0',0,'1.9384615384615385','admin',-12,'2024-01-03',0,NULL,NULL),(96,32,'4区','2013-01-01',4,50.4,2,'4.2*12*3','0.0',0,'1.8666666666666667','admin',-13,'2024-01-03',0,NULL,NULL),(97,32,'5区','2013-01-01',4,50.4,2,'4.2*12*3','0.0',0,'1.7379310344827585','admin',-22,'2024-01-03',0,NULL,NULL),(98,32,'6区','2013-01-01',4,42,2,'4.2*10*3','0.0',0,'0','admin',0,'2024-01-03',0,NULL,NULL),(99,32,'7区','2013-01-01',4,37.8,2,'4.2*9*3','0.0',0,'18.9','admin',4,'2024-01-03',0,NULL,NULL),(100,32,'8区','2013-01-01',4,50.4,2,'4.2*12*3','0.0',0,'2.1913043478260867','admin',2,'2024-01-03',0,NULL,NULL),(101,32,'9区','2013-01-01',4,50.4,2,'4.2*12*3','0.0',0,'5.6','admin',-6,'2024-01-03',0,NULL,NULL),(102,32,'10区','2013-01-01',4,50.4,2,'4.2*12*3','0.0',0,'0.9692307692307692','admin',28,'2024-01-03',0,NULL,NULL),(103,32,'11区','2013-01-01',4,50.4,2,'4.2*12*3','0.0',0,'0.39375','admin',35,'2024-01-03',0,NULL,NULL),(104,32,'12区','2013-01-01',4,49.56,2,'4.2*11.8*3','0.0',0,'5.506666666666667','admin',4,'2024-01-03',0,NULL,NULL),(105,0,'北场区/南场区10分区东','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'6.257142857142857','admin',80,NULL,0,NULL,NULL),(106,0,'北场区/南场区10分区西','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'1.6632911392405063','admin',118,NULL,0,NULL,NULL),(107,0,'北场区/南场区9分区东','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'1.7403973509933777','admin',93,NULL,0,NULL,NULL),(108,0,'北场区/南场区9分区西','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'2.389090909090909','admin',79,NULL,0,NULL,NULL),(111,0,'北场区/南场区7分区东','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'2.053125','admin',94,NULL,0,NULL,NULL),(112,0,'北场区/南场区7分区西','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'1.4282608695652175','admin',151,NULL,0,NULL,NULL),(115,0,'北场区/南场区1分区东','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'2.5764705882352943','admin',89,NULL,0,NULL,NULL),(116,0,'北场区/南场区1分区西','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'4.38','admin',-7,NULL,0,NULL,NULL),(117,0,'北场区/南场区2分区东','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'1.4931818181818182','admin',153,NULL,0,NULL,NULL),(118,0,'北场区/南场区2分区西','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'1.5190751445086705','admin',26,NULL,0,NULL,NULL),(129,0,'北场区/南场区3分区西','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'1.3476923076923075','admin',67,NULL,0,NULL,NULL),(130,0,'北场区/南场区3分区东','2012-01-01',3,87.6,1,'6.1*3*9','8.5*1.1*6',0,'0.689763779527559','admin',107,NULL,0,NULL,NULL),(131,0,'北场区/南场区4分区西','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'0.43799999999999994','admin',-224,NULL,0,NULL,NULL),(132,0,'北场区/南场区4分区东','2012-01-01',3,87.6,1,'6.1*3*9','8.5*1.1*6',0,'0.349003984063745','admin',-142,NULL,0,NULL,NULL),(133,0,'北场区/南场区5分区西','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'1.2338028169014084','admin',694,NULL,0,NULL,NULL),(134,0,'北场区/南场区5分区东','2012-01-01',3,87.6,1,'6.1*3*9','8.5*1.1*6',0,'0.45388601036269427','admin',-105,NULL,0,NULL,NULL),(136,105,'1-3区','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'52.56','admin',11,'2024-01-03',0,NULL,NULL),(137,105,'4-6区','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'43.800000000000004','admin',47,'2024-01-03',0,NULL,NULL),(138,105,'7-8区','2012-01-01',1,175.2,1,'6.1*3*12','8.5*1.1*12',0,'25.02857142857143','admin',6,'2024-01-03',0,NULL,NULL),(139,105,'9-11区','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'52.56','admin',3,'2024-01-03',0,NULL,NULL),(140,106,'1-3区','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'6.409756097560976','admin',41,'2024-01-03',0,NULL,NULL),(141,106,'4-6区','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'7.102702702702703','admin',28,'2024-01-03',0,NULL,NULL),(142,106,'7-8区','2012-01-01',1,175.2,1,'6.1*3*12','8.5*1.1*12',0,'5.651612903225806','admin',28,'2024-01-03',0,NULL,NULL),(143,106,'9-11区','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'5.591489361702128','admin',21,'2024-01-03',0,NULL,NULL),(144,107,'1-3区','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'8.47741935483871','admin',24,'2024-01-03',0,NULL,NULL),(145,107,'4-6区','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'6.257142857142857','admin',3,'2024-01-03',0,NULL,NULL),(146,107,'7-8区','2012-01-01',1,175.2,1,'6.1*3*12','8.5*1.1*12',0,'4.866666666666666','admin',34,'2024-01-03',0,NULL,NULL),(147,107,'9-11区','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'6.409756097560976','admin',31,'2024-01-03',0,NULL,NULL),(148,108,'1-3区','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'11.42608695652174','admin',15,'2024-01-03',0,NULL,NULL),(149,108,'4-6区','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'13.831578947368422','admin',29,'2024-01-03',0,NULL,NULL),(150,108,'7-8区','2012-01-01',1,175.2,1,'6.1*3*12','8.5*1.1*12',0,'7.963636363636363','admin',-1,'2024-01-03',0,NULL,NULL),(151,108,'9-11区','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'9.062068965517241','admin',20,'2024-01-03',0,NULL,NULL),(160,111,'1-3区','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'7.508571428571429','admin',29,'2024-01-03',0,NULL,NULL),(161,111,'4-6区','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'7.963636363636364','admin',24,'2024-01-03',0,NULL,NULL),(162,111,'7-8区','2012-01-01',1,175.2,1,'6.1*3*12','8.5*1.1*12',0,'7.963636363636363','admin',20,'2024-01-03',0,NULL,NULL),(163,111,'9-11区','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'10.512','admin',20,'2024-01-03',0,NULL,NULL),(164,112,'1-3区','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'65.7','admin',4,'2024-01-03',0,NULL,NULL),(165,112,'4-6区','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'7.729411764705882','admin',32,'2024-01-03',0,NULL,NULL),(166,112,'7-8区','2012-01-01',1,175.2,1,'6.1*3*12','8.5*1.1*12',0,'8.342857142857142','admin',12,'2024-01-03',0,NULL,NULL),(167,112,'9-11区','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'6.915789473684211','admin',29,'2024-01-03',0,NULL,NULL),(176,115,'1-3区','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'5.84','admin',68,'2024-01-03',0,NULL,NULL),(177,115,'4-6区','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'10.512','admin',39,'2024-01-03',0,NULL,NULL),(178,115,'7-8区','2012-01-01',1,175.2,1,'6.1*3*12','8.5*1.1*12',0,'7.007999999999999','admin',-1,'2024-01-03',0,NULL,NULL),(179,115,'9-11区','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'8.47741935483871','admin',8,'2024-01-03',0,NULL,NULL),(180,116,'1-3区','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'0','admin',0,'2024-01-03',0,NULL,NULL),(181,116,'4-6区','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'0','admin',-29,'2024-01-03',0,NULL,NULL),(182,116,'7-8区','2012-01-01',1,175.2,1,'6.1*3*12','8.5*1.1*12',0,'5.152941176470588','admin',-3,'2024-01-03',0,NULL,NULL),(183,116,'9-11区','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'12.514285714285714','admin',25,'2024-01-03',0,NULL,NULL),(184,117,'1-3区','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'5.053846153846154','admin',32,'2024-01-03',0,NULL,NULL),(185,117,'4-6区','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'4.308196721311476','admin',55,'2024-01-03',0,NULL,NULL),(186,117,'7-8区','2012-01-01',1,175.2,1,'6.1*3*12','8.5*1.1*12',0,'12.514285714285714','admin',32,'2024-01-03',0,NULL,NULL),(187,117,'9-11区','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'6.409756097560976','admin',34,'2024-01-03',0,NULL,NULL),(188,118,'1-3区','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'7.508571428571429','admin',24,'2024-01-03',0,NULL,NULL),(189,118,'4-6区','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'4.866666666666667','admin',0,'2024-01-03',0,NULL,NULL),(190,118,'7-8区','2012-01-01',1,175.2,1,'6.1*3*12','8.5*1.1*12',0,'7.617391304347826','admin',0,'2024-01-03',0,NULL,NULL),(191,118,'9-11区','2012-01-01',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'5.591489361702128','admin',2,'2024-01-03',0,NULL,NULL),(192,129,'4区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'17.52','admin',10,'2024-01-03',0,NULL,NULL),(193,129,'5区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'17.52','admin',2,'2024-01-03',0,NULL,NULL),(194,129,'6区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'0','admin',-4,'2024-01-03',0,NULL,NULL),(195,129,'7区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'21.9','admin',12,'2024-01-03',0,NULL,NULL),(196,129,'8区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'6.257142857142857','admin',1,'2024-01-03',0,NULL,NULL),(197,129,'9区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'10.95','admin',9,'2024-01-03',0,NULL,NULL),(198,129,'10区','2012-01-01',3,87.6,1,'6.1*3*7','8.5*1.1*6',0,'5.152941176470588','admin',34,'2024-01-03',0,NULL,NULL),(199,129,'11区','2012-01-01',3,87.6,1,'6.1*3*8','8.5*1.1*6',0,'0','admin',0,'2024-01-03',0,NULL,NULL),(200,130,'1区','2012-01-01',3,87.6,1,'6.1*3*9','8.5*1.1*6',0,'7.3','admin',11,'2024-01-03',0,NULL,NULL),(201,130,'2区','2012-01-01',3,87.6,1,'6.1*3*10','8.5*1.1*6',0,'10.95','admin',8,'2024-01-03',0,NULL,NULL),(202,130,'3区','2012-01-01',3,87.6,1,'6.1*3*11','8.5*1.1*6',0,'9.733333333333333','admin',7,'2024-01-03',0,NULL,NULL),(203,130,'4区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'7.963636363636363','admin',22,'2024-01-03',0,NULL,NULL),(204,130,'5区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'6.738461538461538','admin',9,'2024-01-03',0,NULL,NULL),(205,130,'6区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'7.963636363636363','admin',10,'2024-01-03',0,NULL,NULL),(206,130,'7区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'87.6','admin',4,'2024-01-03',0,NULL,NULL),(207,130,'8区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'7.3','admin',6,'2024-01-03',0,NULL,NULL),(208,130,'9区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'7.3','admin',19,'2024-01-03',0,NULL,NULL),(209,130,'10区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'10.95','admin',12,'2024-01-03',0,NULL,NULL),(210,130,'11区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'43.8','admin',-13,'2024-01-03',0,NULL,NULL),(211,131,'1区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'4.866666666666666','admin',-2,'2024-01-03',0,NULL,NULL),(212,131,'2区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'4.38','admin',-1,'2024-01-03',0,NULL,NULL),(213,131,'3区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'9.733333333333333','admin',-4,'2024-01-03',0,NULL,NULL),(214,131,'4区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'5.152941176470588','admin',-2,'2024-01-03',0,NULL,NULL),(215,131,'5区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'5.475','admin',-26,'2024-01-03',0,NULL,NULL),(216,131,'6区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'4.38','admin',11,'2024-01-03',0,NULL,NULL),(217,131,'7区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'3.9818181818181815','admin',-7,'2024-01-03',0,NULL,NULL),(218,131,'8区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'5.84','admin',7,'2024-01-03',0,NULL,NULL),(219,131,'9区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'5.475','admin',-3,'2024-01-03',0,NULL,NULL),(220,131,'10区','2012-01-01',3,87.6,1,'6.1*3*7','8.5*1.1*6',0,'4.610526315789474','admin',-2,'2024-01-03',0,NULL,NULL),(221,131,'11区','2012-01-01',3,87.6,1,'6.1*3*8','8.5*1.1*6',0,'4.610526315789474','admin',0,'2024-01-03',0,NULL,NULL),(222,132,'1区','2012-01-01',3,87.6,1,'6.1*3*9','8.5*1.1*6',0,'3.1285714285714286','admin',-1,'2024-01-03',0,NULL,NULL),(223,132,'2区','2012-01-01',3,87.6,1,'6.1*3*10','8.5*1.1*6',0,'3.5039999999999996','admin',23,'2024-01-03',0,NULL,NULL),(224,132,'3区','2012-01-01',3,87.6,1,'6.1*3*11','8.5*1.1*6',0,'5.84','admin',0,'2024-01-03',0,NULL,NULL),(225,132,'4区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'3.244444444444444','admin',26,'2024-01-03',0,NULL,NULL),(226,132,'5区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'0','admin',17,'2024-01-03',0,NULL,NULL),(227,132,'6区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'3.0206896551724136','admin',-1,'2024-01-03',0,NULL,NULL),(228,132,'7区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'4.610526315789474','admin',2,'2024-01-03',0,NULL,NULL),(229,132,'8区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'1.9909090909090907','admin',37,'2024-01-03',0,NULL,NULL),(230,132,'9区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'2.92','admin',30,'2024-01-03',0,NULL,NULL),(231,132,'10区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'3.1285714285714286','admin',-1,'2024-01-03',0,NULL,NULL),(232,132,'11区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'3.808695652173913','admin',0,'2024-01-03',0,NULL,NULL),(233,133,'1区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'3.65','admin',8,'2024-01-03',0,NULL,NULL),(234,133,'2区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'4.38','admin',4,'2024-01-03',0,NULL,NULL),(235,133,'3区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'4.866666666666666','admin',17,'2024-01-03',0,NULL,NULL),(236,133,'4区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'4.610526315789474','admin',19,'2024-01-03',0,NULL,NULL),(237,133,'5区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'6.257142857142857','admin',14,'2024-01-03',0,NULL,NULL),(238,133,'6区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'4.171428571428571','admin',21,'2024-01-03',0,NULL,NULL),(239,133,'7区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'2.6545454545454543','admin',32,'2024-01-03',0,NULL,NULL),(240,133,'8区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'0','admin',-1,'2024-01-03',0,NULL,NULL),(241,133,'9区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'0','admin',-1,'2024-01-03',0,NULL,NULL),(242,133,'10区','2012-01-01',3,87.6,1,'6.1*3*7','8.5*1.1*6',0,'0','admin',0,'2024-01-03',0,NULL,NULL),(243,133,'11区','2012-01-01',3,87.6,1,'6.1*3*8','8.5*1.1*6',0,'0','admin',0,'2024-01-03',0,NULL,NULL),(244,134,'1区','2012-01-01',3,87.6,1,'6.1*3*9','8.5*1.1*6',0,'3.9818181818181815','admin',17,'2024-01-03',0,NULL,NULL),(245,134,'2区','2012-01-01',3,87.6,1,'6.1*3*10','8.5*1.1*6',0,'4.610526315789474','admin',3,'2024-01-03',0,NULL,NULL),(246,134,'3区','2012-01-01',3,87.6,1,'6.1*3*11','8.5*1.1*6',0,'3.5039999999999996','admin',18,'2024-01-03',0,NULL,NULL),(247,134,'4区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'3.5039999999999996','admin',22,'2024-01-03',0,NULL,NULL),(248,134,'5区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'5.475','admin',16,'2024-01-03',0,NULL,NULL),(249,134,'6区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'6.738461538461538','admin',-29,'2024-01-03',0,NULL,NULL),(250,134,'7区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'6.738461538461538','admin',-6,'2024-01-03',0,NULL,NULL),(251,134,'8区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'2.3675675675675674','admin',34,'2024-01-03',0,NULL,NULL),(252,134,'9区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'3.369230769230769','admin',26,'2024-01-03',0,NULL,NULL),(253,134,'10区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'3.9818181818181815','admin',22,'2024-01-03',0,NULL,NULL),(254,134,'11区','2012-01-01',3,87.6,1,'6.1*3*6','8.5*1.1*6',0,'3.0206896551724136','admin',20,'2024-01-03',0,NULL,NULL),(392,0,'待收分区','2021-04-25',1,262.8,1,'6.1*3*18','8.5*1.1*18',0,'0.9626373626373627','admin',241,NULL,0,NULL,NULL),(393,392,'1区','2021-04-25',1,300,1,'10*10*3','10*10*10',0,'1.5873015873015872','qiao',93,'2024-01-26',0,NULL,NULL),(395,2,'枯草处理','2021-11-18',7,1000,2,'1000','1000',0,'111.11111111111111','管理员',-851,'2024-01-03',0,NULL,NULL),(396,392,'2区','2022-01-01',1,300,1,'10*10*3','10*10*10',0,'23.076923076923077','qiao',4,'2024-01-26',0,NULL,NULL),(397,0,'种草/草株/草地/幼草/母草/种草分区','2023-03-20',5,39,0,'30*13*4','0',0,'0','admin',11,NULL,0,NULL,NULL),(398,397,'1区','2023-03-20',5,39,0,'30*13*4','0',0,'0','admin',3,'2024-01-04',0,NULL,NULL),(399,0,'北场区8分区A栋东','2023-05-15',1,262.8,1,'6*3*8','0',1,'1.6425','admin',161,NULL,0,NULL,NULL),(400,0,'北场区8分区A栋西','2023-05-15',1,262.8,1,'6*3*8','0',1,'1.6528301886792454','admin',127,NULL,0,NULL,NULL),(401,399,'1区','2023-05-15',1,24,0,'4*6','0',1,'0','admin',-1,'2024-01-04',0,NULL,NULL),(402,399,'2区','2023-05-15',1,24,0,'4*6','0',1,'1.8461538461538463','admin',11,'2024-01-04',0,NULL,NULL),(403,399,'3区','2023-05-15',1,24,0,'4*6','0',1,'1.7142857142857142','admin',9,'2024-01-04',0,NULL,NULL),(404,399,'4区','2023-05-15',1,24,0,'4*6','0',1,'2.1818181818181817','admin',11,'2024-01-04',0,NULL,NULL),(405,399,'5区','2023-05-15',1,24,0,'4*6','0',1,'2.4','admin',9,'2024-01-04',0,NULL,NULL),(406,399,'6区','2023-05-15',1,24,0,'4*6','0',1,'2.4','admin',8,'2024-01-04',0,NULL,NULL),(407,399,'7区','2023-05-15',1,24,0,'4*6','0',1,'2.6666666666666665','admin',0,'2024-01-04',0,NULL,NULL),(408,399,'8区','2023-05-15',1,24,0,'4*6','0',1,'2.4','admin',8,'2024-01-04',0,NULL,NULL),(409,399,'9区','2023-05-15',1,24,0,'4*6','0',1,'4.0','admin',6,'2024-01-04',0,NULL,NULL),(410,399,'10区','2023-05-15',1,24,0,'4*6','0',1,'2.1818181818181817','admin',11,'2024-01-04',0,NULL,NULL),(411,399,'11区','2023-05-15',1,24,0,'4*6','0',1,'2.4','admin',23,'2024-01-04',0,NULL,NULL),(415,0,'北场区8分区B栋东','2023-05-15',1,262.8,1,'6*3*8','0',1,'1.4205405405405407','admin',146,NULL,0,NULL,NULL),(416,0,'北场区8分区B栋西','2023-05-15',1,262.8,1,'6*3*8','0',1,'2.5764705882352943','admin',76,NULL,0,NULL,NULL),(417,400,'1区','2023-05-15',1,24,0,'4*6','0',1,'0','admin',0,'2024-01-04',0,NULL,NULL),(418,400,'2区','2023-05-15',1,24,0,'4*6','0',1,'3.0','admin',4,'2024-01-04',0,NULL,NULL),(419,400,'3区','2023-05-15',1,24,0,'4*6','0',1,'0','admin',-1,'2024-01-04',0,NULL,NULL),(420,400,'4区','2023-05-15',1,24,0,'4*6','0',1,'3.0','admin',3,'2024-01-04',0,NULL,NULL),(421,400,'5区','2023-05-15',1,24,0,'4*6','0',1,'2.4','admin',7,'2024-01-04',0,NULL,NULL),(422,400,'6区','2023-05-15',1,24,0,'4*6','0',1,'3.0','admin',7,'2024-01-04',0,NULL,NULL),(423,400,'7区','2023-05-15',1,24,0,'4*6','0',1,'2.1818181818181817','admin',8,'2024-01-04',0,NULL,NULL),(424,400,'8区','2023-05-15',1,24,0,'4*6','0',1,'2.6666666666666665','admin',9,'2024-01-04',0,NULL,NULL),(425,400,'9区','2023-05-15',1,24,0,'4*6','0',1,'1.8461538461538463','admin',10,'2024-01-04',0,NULL,NULL),(426,400,'10区','2023-05-15',1,24,0,'4*6','0',1,'3.4285714285714284','admin',5,'2024-01-04',0,NULL,NULL),(427,400,'11区','2023-05-15',1,24,0,'4*6','0',1,'2.6666666666666665','admin',8,'2024-01-04',0,NULL,NULL),(428,415,'1区','2023-05-15',1,24,0,'4*6','0',1,'0','admin',-9,'2024-01-04',0,NULL,NULL),(429,415,'2区','2023-05-15',1,24,0,'4*6','0',1,'3.0','admin',7,'2024-01-04',0,NULL,NULL),(430,415,'3区','2023-05-15',1,24,0,'4*6','0',1,'2.4','admin',10,'2024-01-04',0,NULL,NULL),(431,415,'4区','2023-05-15',1,24,0,'4*6','0',1,'2.1818181818181817','admin',9,'2024-01-04',0,NULL,NULL),(432,415,'5区','2023-05-15',1,24,0,'4*6','0',1,'2.6666666666666665','admin',2,'2024-01-04',0,NULL,NULL),(433,415,'6区','2023-05-15',1,24,0,'4*6','0',1,'2.0','admin',11,'2024-01-04',0,NULL,NULL),(434,415,'7区','2023-05-15',1,24,0,'4*6','0',1,'2.4','admin',9,'2024-01-04',0,NULL,NULL),(435,415,'8区','2023-05-15',1,24,0,'4*6','0',1,'4.8','admin',4,'2024-01-04',0,NULL,NULL),(436,415,'9区','2023-05-15',1,24,0,'4*6','0',1,'3.0','admin',8,'2024-01-04',0,NULL,NULL),(437,415,'10区','2023-05-15',1,24,0,'4*6','0',1,'2.1818181818181817','admin',10,'2024-01-04',0,NULL,NULL),(438,415,'11区','2023-05-15',1,24,0,'4*6','0',1,'3.0','admin',5,'2024-01-04',0,NULL,NULL),(439,416,'1区','2023-05-15',1,24,0,'4*6','0',1,'12.0','admin',0,'2024-01-04',0,NULL,NULL),(440,416,'2区','2023-05-15',1,24,0,'4*6','0',1,'0','admin',-1,'2024-01-04',0,NULL,NULL),(441,416,'3区','2023-05-15',1,24,0,'4*6','0',1,'0','admin',-1,'2024-01-04',0,NULL,NULL),(442,416,'4区','2023-05-15',1,24,0,'4*6','0',1,'0','admin',-1,'2024-01-04',0,NULL,NULL),(443,416,'5区','2023-05-15',1,24,0,'4*6','0',1,'4.0','admin',5,'2024-01-04',0,NULL,NULL),(444,416,'6区','2023-05-15',1,24,0,'4*6','0',1,'2.1818181818181817','admin',10,'2024-01-04',0,NULL,NULL),(445,416,'7区','2023-05-15',1,24,0,'4*6','0',1,'2.0','admin',12,'2024-01-04',0,NULL,NULL),(446,416,'8区','2023-05-15',1,24,0,'4*6','0',1,'2.6666666666666665','admin',9,'2024-01-04',0,NULL,NULL),(447,416,'9区','2023-05-15',1,24,0,'4*6','0',1,'4.0','admin',6,'2024-01-04',0,NULL,NULL),(448,416,'10区','2023-05-15',1,24,0,'4*6','0',1,'2.1818181818181817','admin',11,'2024-01-04',0,NULL,NULL),(449,416,'11区','2023-05-15',1,24,0,'4*6','0',1,'3.4285714285714284','admin',7,'2024-01-04',0,NULL,NULL),(450,399,'12区','2023-05-15',1,24,0,'4*6','0',1,'4.0','admin',21,'2024-01-04',0,NULL,NULL),(451,399,'13区','2023-05-15',1,24,0,'4*6','0',1,'24.0','admin',-3,'2024-01-04',0,NULL,NULL),(452,399,'14区','2023-05-15',1,24,0,'4*6','0',1,'8.0','admin',2,'2024-01-04',0,NULL,NULL),(453,399,'15区','2023-05-15',1,24,0,'4*6','0',1,'0','admin',-2,'2024-01-04',0,NULL,NULL),(454,399,'16区','2023-05-15',1,24,0,'4*6','0',1,'0','admin',0,'2024-01-04',0,NULL,NULL),(455,399,'17区','2023-05-15',1,24,0,'4*6','0',1,'0','admin',0,'2024-01-04',0,NULL,NULL),(456,400,'12区','2023-05-15',1,24,0,'4*6','0',1,'2.4','admin',9,'2024-01-04',0,NULL,NULL),(457,400,'13区','2023-05-15',1,24,0,'4*6','0',1,'1.7142857142857142','admin',10,'2024-01-04',0,NULL,NULL),(458,400,'15区','2023-05-15',1,24,0,'4*6','0',1,'2.4','admin',10,'2024-01-04',0,NULL,NULL),(459,400,'16区','2023-05-15',1,24,0,'4*6','0',1,'3.0','admin',7,'2024-01-04',0,NULL,NULL),(460,400,'17区','2023-05-15',1,24,0,'4*6','0',1,'0','admin',0,'2024-01-04',0,NULL,NULL),(461,415,'12区','2023-05-15',1,24,0,'4*6','0',1,'2.1818181818181817','admin',11,'2024-01-04',0,NULL,NULL),(462,415,'13区','2023-05-15',1,24,0,'4*6','0',1,'4.0','admin',6,'2024-01-04',0,NULL,NULL),(463,415,'14区','2023-05-15',1,24,0,'4*6','0',1,'2.1818181818181817','admin',8,'2024-01-04',0,NULL,NULL),(464,415,'15区','2023-05-15',1,24,0,'4*6','0',1,'6.0','admin',3,'2024-01-04',0,NULL,NULL),(465,415,'16区','2023-05-15',1,24,0,'4*6','0',1,'2.6666666666666665','admin',6,'2024-01-04',0,NULL,NULL),(466,415,'17区','2023-05-15',1,24,0,'4*6','0',1,'2.1818181818181817','admin',10,'2024-01-04',0,NULL,NULL),(467,416,'12区','2023-05-15',1,24,0,'4*6','0',1,'1.8461538461538463','admin',10,'2024-01-04',0,NULL,NULL),(468,416,'13区','2023-05-15',1,24,0,'4*6','0',1,'2.0','admin',12,'2024-01-04',0,NULL,NULL),(469,416,'14区','2023-05-15',1,24,0,'4*6','0',1,'2.0','admin',12,'2024-01-04',0,NULL,NULL),(470,416,'15区','2023-05-15',1,24,0,'4*6','0',1,'2.0','admin',11,'2024-01-04',0,NULL,NULL),(471,416,'16区','2023-05-15',1,24,0,'4*6','0',1,'2.4','admin',9,'2024-01-04',0,NULL,NULL),(472,416,'17区','2023-05-15',1,24,0,'4*6','0',1,'0','admin',0,'2024-01-04',0,NULL,NULL),(473,111,'12区','2023-12-15',1,92.6,1,'6.1*3*6','8.5*1.1*6',1,'8.418181818181818','admin',10,NULL,0,NULL,NULL),(474,111,'13区','2023-12-15',1,93.5,1,'6.1*3*6','8.5*1.1*6',1,'9.35','admin',12,NULL,0,NULL,NULL),(475,111,'14区','2023-12-15',1,93.6,1,'6.1*3*6','8.5*1.1*6',1,'8.509090909090908','admin',11,NULL,0,NULL,NULL),(476,111,'15区','2023-12-15',1,93.6,1,'6.1*3*6','8.5*1.1*6',1,'7.199999999999999','admin',13,NULL,0,NULL,NULL),(477,111,'16区','2023-12-15',1,93.1,1,'6.1*3*6','8.5*1.1*6',1,'9.309999999999999','admin',13,NULL,0,NULL,NULL),(478,111,'17区','2023-12-15',1,92.6,1,'6.1*3*6','8.5*1.1*6',1,'6.173333333333333','admin',8,NULL,0,NULL,NULL),(479,111,'18区','2023-12-15',1,93.1,1,'6.1*3*6','8.5*1.1*6',1,'0','admin',0,NULL,0,NULL,NULL),(480,400,'14区','2024-01-04',1,24,0,'4*6','0',0,'3.0','admin',7,NULL,0,NULL,NULL),(481,112,'15区','2024-01-03',1,82.6,1,'2*3*6','2.6*1.1*6',1,'5.8999999999999995','admin',14,NULL,0,NULL,NULL),(482,112,'16区','2024-01-03',1,82.6,1,'2*3*6','2.6*1.1*6',1,'5.8999999999999995','admin',13,NULL,0,NULL,NULL),(483,112,'12-14区','2024-01-03',1,262.8,1,'6.1*6*12','8.5*1.1*18',1,'7.729411764705882','admin',35,NULL,0,NULL,NULL),(485,112,'17区','2023-12-20',1,82.6,1,'6.1*3*18','8.58*1.1*18',1,'6.3538461538461535','admin',10,NULL,0,NULL,NULL),(486,0,'桃树地','2024-03-10',4,600,1,'4*3*5','0.0',1,'31.57894736842105','曹立军',0,NULL,0,NULL,NULL),(487,486,'桃树地','2024-04-22',4,600,0,'50*4*3','0.0',1,'0','曹立军',0,NULL,0,NULL,NULL),(488,0,'待转分区','2024-01-01',7,87,1,'4*3*29','0.0',0,'0','admin',0,NULL,0,NULL,NULL),(489,0,'北场区/南场区6分区B东','2024-10-30',3,262.8,1,'6*3*8','3',1,'0','曹立金',-5,NULL,0,NULL,NULL),(490,0,'北场区/南场区6分区B西','2024-10-30',3,262.8,1,'6*3*8','3',1,'0','曹立军',-1,NULL,0,NULL,NULL),(491,0,'北场区/南场区6分区A东','2024-10-30',3,262.8,1,'6*3*8','3',1,'0','曹立军',-36,NULL,0,NULL,NULL),(492,0,'北场区/南场区6分区A西','2024-10-30',3,262.8,1,'6*3*8','3',1,'0','曹立军',-8,NULL,0,NULL,NULL),(493,492,'1区','2024-10-30',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(494,492,'2区','2024-10-30',3,8,1,'8','8',1,'0','cc',0,NULL,0,NULL,NULL),(495,492,'3区','2024-10-30',3,1,1,'1','1',1,'0','c',0,NULL,0,NULL,NULL),(496,492,'4区','2024-10-30',3,8,1,'8','8',1,'0','曹立军',-4,NULL,0,NULL,NULL),(497,492,'5区','2024-11-21',3,8,1,'8','8',1,'0','c',-1,NULL,0,NULL,NULL),(498,492,'6区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',-2,NULL,0,NULL,NULL),(499,492,'7区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(500,492,'8区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',-2,NULL,0,NULL,NULL),(501,492,'9区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',-1,NULL,0,NULL,NULL),(502,492,'10区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(503,492,'11区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',-1,NULL,0,NULL,NULL),(504,492,'12区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',3,NULL,0,NULL,NULL),(505,492,'13区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(506,492,'14区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',2,NULL,0,NULL,NULL),(507,492,'15区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(508,492,'16区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',-1,NULL,0,NULL,NULL),(509,492,'17区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(510,492,'18区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',-1,NULL,0,NULL,NULL),(511,492,'19区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(512,491,'1区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',-4,NULL,0,NULL,NULL),(513,491,'2区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',-1,NULL,0,NULL,NULL),(514,491,'3区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',-4,NULL,0,NULL,NULL),(515,491,'4区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',-3,NULL,0,NULL,NULL),(516,491,'5区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',-1,NULL,0,NULL,NULL),(517,491,'6区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',-1,NULL,0,NULL,NULL),(518,491,'7区','2024-11-21',3,8,1,'8','8',1,'0','曹立金',-1,NULL,0,NULL,NULL),(519,491,'8区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(520,491,'9区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',-1,NULL,0,NULL,NULL),(521,491,'10区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',-6,NULL,0,NULL,NULL),(522,491,'11区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',-3,NULL,0,NULL,NULL),(523,491,'12区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',-1,NULL,0,NULL,NULL),(524,491,'13区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',-4,NULL,0,NULL,NULL),(525,491,'14区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',-1,NULL,0,NULL,NULL),(526,491,'15区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(527,491,'16区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',-2,NULL,0,NULL,NULL),(528,491,'17区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',-2,NULL,0,NULL,NULL),(529,491,'18区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',-1,NULL,0,NULL,NULL),(530,489,'1区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(531,489,'2区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(532,489,'3区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',-1,NULL,0,NULL,NULL),(533,489,'4区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(534,489,'5区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(535,489,'6区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(536,489,'7区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(537,489,'8区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(538,489,'9区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(539,489,'10区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(540,489,'11区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(541,489,'12区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(542,489,'13区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(543,489,'14区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(544,489,'15区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(545,489,'16区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(546,489,'17区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(547,489,'18区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',-1,NULL,0,NULL,NULL),(548,489,'19区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',-3,NULL,0,NULL,NULL),(549,490,'1区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(550,490,'2区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(551,490,'3区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(552,490,'4区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(553,490,'5区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(554,490,'6区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(555,490,'7区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(556,490,'8区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(557,490,'9区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(558,490,'10区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(559,490,'11区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(560,490,'12区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(561,490,'13区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(562,490,'14区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(563,490,'15区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(564,490,'16区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(565,490,'17区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',-1,NULL,0,NULL,NULL),(566,490,'18区','2024-11-21',3,8,1,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(567,0,'北场区/南场区11分区东','2024-11-30',3,22,1,'22','22',1,'0','曹立军',8,NULL,0,NULL,NULL),(568,0,'北场区/南场区11分区西','2024-11-30',3,22,1,'22','22',1,'0','曹立军',-15,NULL,0,NULL,NULL),(569,567,'1区','2024-12-01',3,8,0,'8','8',1,'0','曹立军',-2,NULL,0,NULL,NULL),(570,567,'2区','2024-12-01',3,8,1,'8','8',1,'0','曹立军',-2,NULL,0,NULL,NULL),(571,567,'3区','2024-12-01',3,8,0,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(572,567,'4区','2024-12-01',3,8,0,'8','8',1,'0','曹立军',-2,NULL,0,NULL,NULL),(573,567,'5区','2024-12-01',3,8,0,'8','8',1,'0','曹立军',-1,NULL,0,NULL,NULL),(574,567,'6区','2024-12-01',3,8,0,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(575,567,'7区','2024-12-01',3,8,0,'8','8',1,'0','曹立军',-5,NULL,0,NULL,NULL),(576,567,'8区','2024-12-01',3,8,0,'8','8',1,'0','曹立军',5,NULL,0,NULL,NULL),(577,567,'9区','2024-12-01',3,8,0,'8','8',1,'0','曹立军',5,NULL,0,NULL,NULL),(578,567,'10区','2024-12-01',3,8,0,'8','8',1,'0','曹立军',4,NULL,0,NULL,NULL),(579,567,'11区','2024-12-01',3,8,0,'8','8',1,'0','曹立军',5,NULL,0,NULL,NULL),(580,567,'12区','2024-12-01',3,8,0,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(581,567,'13区','2024-12-01',3,8,0,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(582,567,'14区','2024-12-01',3,8,0,'8','8',1,'0','曹立军',1,NULL,0,NULL,NULL),(583,567,'15区','2024-12-01',3,8,0,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(584,567,'16区','2024-12-01',3,8,0,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(585,567,'17区','2024-12-01',3,8,0,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(586,568,'1区','2024-12-01',3,8,0,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(587,568,'2区','2024-12-01',3,8,0,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(588,568,'3区','2024-12-01',3,8,0,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(589,568,'4区','2024-12-01',3,8,0,'8','8',1,'0','曹立军',-5,NULL,0,NULL,NULL),(590,568,'5区','2024-12-01',3,8,0,'8','8',1,'0','曹立军',-1,NULL,0,NULL,NULL),(591,568,'6区','2024-12-01',3,8,0,'8','8',1,'0','曹立军',-2,NULL,0,NULL,NULL),(592,568,'7区','2024-12-02',3,8,0,'8','8',1,'0','曹立军',-2,NULL,0,NULL,NULL),(593,568,'8区','2024-12-01',3,8,0,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(594,568,'9区','2024-12-01',3,8,0,'8','8',1,'0','曹立军',-1,NULL,0,NULL,NULL),(595,568,'10区','2024-12-01',3,8,0,'8','8',1,'0','曹立军',-1,NULL,0,NULL,NULL),(596,568,'11区','2024-12-01',3,8,0,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(597,568,'12区','2024-12-01',3,8,0,'8','8',1,'0','曹立军',-2,NULL,0,NULL,NULL),(598,568,'13区','2024-12-01',3,8,0,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(599,568,'14区','2024-12-01',3,8,0,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(600,568,'15区','2024-12-01',3,8,0,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(601,568,'16区','2024-12-01',3,8,0,'8','8',1,'0','曹立军',0,NULL,0,NULL,NULL),(602,568,'17区','2024-12-01',3,8,0,'8','8',1,'0','曹立军',-1,NULL,0,NULL,NULL),(603,2,'死亡区','2017-01-01',6,0,0,'0','0',NULL,'0.0000000000','system',1,NULL,0,NULL,NULL),(604,2,'收割/出圃区','2017-01-01',6,0,0,'0','0',NULL,'0','system',1,NULL,0,NULL,NULL),(605,2,'淘汰区','2017-01-01',6,0,0,'0','0',NULL,'0','system',0,NULL,0,NULL,NULL);
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
