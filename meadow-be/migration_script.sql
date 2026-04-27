-- ============================================================
-- AgroGuard Meadow Database Migration & Data Filling Script
-- Generated: 2026-04-27
-- Target Database: meadow_test
-- ============================================================
-- PURPOSE:
--   1. Migrate data from old backup table names to current names
--      (only if old tables still exist in the target DB).
--   2. Fill empty tables with >= 5 rows of realistic test data.
-- ============================================================
-- SAFETY: This script disables FK checks during migration.
--         All migration INSERTs use LEFT JOIN / NOT EXISTS
--         to avoid duplicates. Data-filling uses row-count
--         guards so it will NOT add rows to tables that
--         already contain data.
-- ============================================================
-- DO NOT execute blindly on production. Review & test first.
-- ============================================================

SET FOREIGN_KEY_CHECKS = 0;
SET UNIQUE_CHECKS = 0;
SET NAMES utf8mb4;

-- ============================================================
-- PART 1: MIGRATE OLD TABLE NAMES -> CURRENT TABLE NAMES
-- ============================================================
-- Only runs when the OLD table exists and the NEW table
-- does not already contain the same PK rows.
-- ------------------------------------------------------------

-- 1.1 colony_houseinfo -> field_houseinfo
-- Schemas are identical.
INSERT INTO field_houseinfo
SELECT c.* FROM colony_houseinfo c
LEFT JOIN field_houseinfo f ON c.id = f.id
WHERE f.id IS NULL;

-- 1.2 colony_disinfectioninfo -> field_disinfectioninfo
-- Schemas are identical.
INSERT INTO field_disinfectioninfo
SELECT c.* FROM colony_disinfectioninfo c
LEFT JOIN field_disinfectioninfo f ON c.id = f.id
WHERE f.id IS NULL;

-- 1.3 colony_maintenanceinfo -> field_maintenanceinfo
-- Schemas are identical.
INSERT INTO field_maintenanceinfo
SELECT c.* FROM colony_maintenanceinfo c
LEFT JOIN field_maintenanceinfo f ON c.id = f.id
WHERE f.id IS NULL;

-- 1.4 colony_transferinfo -> field_transferinfo
-- Schemas are identical.
INSERT INTO field_transferinfo
SELECT c.* FROM colony_transferinfo c
LEFT JOIN field_transferinfo f ON c.id = f.id
WHERE f.id IS NULL;

-- 1.5 basic_breederconditioninfo -> basic_fieldconditioninfo
-- Column rename mapping:
--   testis_shape      -> root_shape
--   with_births       -> with_plantings
--   (all other columns are identical)
INSERT INTO basic_fieldconditioninfo
  (id, date, basic_id, age, high, weight, Llong, bust,
   root_shape, t_staff, AE, performance_traits,
   with_plantings, wea_weight, June_heavy, health,
   f_date, f_staff, notes, belong, color, mon_age, rank,
   back_fat, eye)
SELECT
  c.id, c.date, c.basic_id, c.age, c.high, c.weight, c.Llong, c.bust,
  c.testis_shape, c.t_staff, c.AE, c.performance_traits,
  c.with_births, c.wea_weight, c.June_heavy, c.health,
  c.f_date, c.f_staff, c.notes, c.belong, c.color, c.mon_age, c.rank,
  c.back_fat, c.eye
FROM basic_breederconditioninfo c
LEFT JOIN basic_fieldconditioninfo f ON c.id = f.id
WHERE f.id IS NULL;

-- 1.6 basic_cutinfo -> basic_harvestinfo
-- Column rename mapping:
--   cut_time  -> harvest_time
--   cut_num   -> harvest_num
--   (all other columns are identical)
INSERT INTO basic_harvestinfo
  (id, house_id, ele_quantity, variety, harvest_time,
   rank, color, weight, staff, notes, belong, f_date, harvest_num)
SELECT
  c.id, c.house_id, c.ele_quantity, c.variety, c.cut_time,
  c.rank, c.color, c.weight, c.staff, c.notes, c.belong, c.f_date, c.cut_num
FROM basic_cutinfo c
LEFT JOIN basic_harvestinfo f ON c.id = f.id
WHERE f.id IS NULL;

-- 1.7 basic_manureinfo -> basic_fertilizerinfo
-- Schemas are identical (table renamed only).
INSERT INTO basic_fertilizerinfo
SELECT c.* FROM basic_manureinfo c
LEFT JOIN basic_fertilizerinfo f ON c.id = f.id
WHERE f.id IS NULL;


-- ============================================================
-- PART 2: FILL EMPTY TABLES WITH REALISTIC TEST DATA
-- ============================================================
-- Uses a stored-procedure guard so rows are only inserted
-- when the table currently has < 5 rows.
-- ------------------------------------------------------------

DELIMITER $$

CREATE PROCEDURE IF NOT EXISTS agroguard_fill_empty_tables()
BEGIN

  -- ----------------------------------------------------------
  -- 2.1 field_* group
  -- ----------------------------------------------------------

  -- field_houseinfo
  IF (SELECT COUNT(*) FROM field_houseinfo) < 5 THEN
    INSERT INTO field_houseinfo
      (pid, name, build_time, function, area, h_type, h_lwh, sports_lwh,
       grass_type, area_pro, staff, grass_quantity, difinfect_time, belong, f_staff, add_area)
    VALUES
      (0, 'A区种植棚', '2023-03-15', 1, 260.0, 1, '6.1*3*18', '8.5*1.1*18', 1, '3.5', '张伟', 120, '2025-04-20', 0, 'system', NULL),
      (0, 'B区种植棚', '2023-03-15', 1, 260.0, 1, '6.1*3*18', '8.5*1.1*18', 1, '2.8', '李强', 98, '2025-04-21', 0, 'system', NULL),
      (0, 'C区育苗棚', '2023-04-10', 3, 87.6, 1, '6.1*3*6', '8.5*1.1*6', 2, '1.2', '王芳', 45, '2025-04-22', 0, 'system', NULL),
      (0, 'D区生产棚', '2022-06-01', 4, 600.0, 2, '5*11.5*3', '0.0', 0, '5.6', '赵敏', 220, '2025-04-23', 0, 'system', NULL),
      (0, 'E区暂存区', '2020-08-10', 2, 100.0, 0, '6', '7', 1, '16.7', '刘洋', 80, '2025-04-24', 0, 'system', NULL),
      (0, 'F区收割区', '2021-04-25', 7, 1000.0, 2, '1000', '1000', 0, '111.1', '陈刚', 60, '2025-04-25', 0, 'system', NULL);
  END IF;

  -- field_disinfectioninfo
  IF (SELECT COUNT(*) FROM field_disinfectioninfo) < 5 THEN
    INSERT INTO field_disinfectioninfo
      (house_id, date, staff, drug, dose, method, notes, belong)
    VALUES
      (5, '2025-04-01', '张伟', '百菌清', 500.0, 1, '春季常规消毒，喷洒均匀', 0),
      (5, '2025-04-08', '李强', '多菌灵', 300.0, 0, '土壤表面喷雾处理', 0),
      (7, '2025-04-10', '王芳', '甲基托布津', 400.0, 1, '棚内全面消毒', 0),
      (12, '2025-04-15', '赵敏', '代森锰锌', 250.0, 0, '预防性消毒', 0),
      (27, '2025-04-18', '刘洋', '福美双', 600.0, 1, '入口及通道重点消毒', 0),
      (28, '2025-04-20', '陈刚', '三唑酮', 350.0, 1, '春季返青期消毒', 0);
  END IF;

  -- field_maintenanceinfo
  IF (SELECT COUNT(*) FROM field_maintenanceinfo) < 5 THEN
    INSERT INTO field_maintenanceinfo
      (house_id, M_condition, M_details, M_time, M_cost, f_date, f_staff, belong)
    VALUES
      (5, '通风系统故障', '更换风机电机，清理风道积尘', '2025-03-10', 850.50, '2025-03-10', '张伟', 0),
      (7, '灌溉管道漏水', '更换老化PVC管接头，压力测试', '2025-03-15', 320.00, '2025-03-15', '李强', 0),
      (12, '遮阳网破损', '更换东侧遮阳网，加固拉绳', '2025-03-20', 1200.00, '2025-03-20', '王芳', 0),
      (27, '温控传感器失灵', '校准温湿度传感器，更换探头', '2025-03-25', 580.00, '2025-03-25', '赵敏', 0),
      (28, '卷帘机异响', '润滑传动链条，调整限位开关', '2025-03-28', 260.00, '2025-03-28', '刘洋', 0),
      (5, '补光灯损坏', '更换LED补光灯条，检测电路', '2025-04-02', 450.00, '2025-04-02', '陈刚', 0);
  END IF;

  -- field_transferinfo
  IF (SELECT COUNT(*) FROM field_transferinfo) < 5 THEN
    INSERT INTO field_transferinfo
      (basic_id, new_house_id, old_house_id, reason, trans_time, grass_type, f_date, f_staff, belong)
    VALUES
      (101, 5, 27, 1, '2025-04-01', '高羊茅', '2025-04-01', '张伟', 0),
      (102, 7, 28, 2, '2025-04-03', '黑麦草', '2025-04-03', '李强', 0),
      (103, 12, 29, 3, '2025-04-05', '早熟禾', '2025-04-05', '王芳', 0),
      (104, 27, 30, 1, '2025-04-08', '紫花苜蓿', '2025-04-08', '赵敏', 0),
      (105, 28, 31, 4, '2025-04-10', '白三叶', '2025-04-10', '刘洋', 0),
      (106, 5, 32, 2, '2025-04-12', '红三叶', '2025-04-12', '陈刚', 0);
  END IF;


  -- ----------------------------------------------------------
  -- 2.2 d_plantcare_* group
  -- ----------------------------------------------------------

  -- d_plantcare_damageinfo
  IF (SELECT COUNT(*) FROM d_plantcare_damageinfo) < 5 THEN
    INSERT INTO d_plantcare_damageinfo
      (basic_id, notes, method, staff, date, f_staff, f_date, belong)
    VALUES
      (101, '叶片机械损伤', '修剪受损叶片，喷洒修复剂', '张伟', '2025-04-01', 'system', '2025-04-01', 0),
      (102, '根系挤压伤', '松土透气，减少灌溉', '李强', '2025-04-03', 'system', '2025-04-03', 0),
      (103, '茎秆折裂', '支撑固定，涂抹愈合剂', '王芳', '2025-04-05', 'system', '2025-04-05', 0),
      (104, '日灼伤害', '增加遮阳，早晚喷水降温', '赵敏', '2025-04-08', 'system', '2025-04-08', 0),
      (105, '冻害损伤', '覆盖保温，喷施抗冻剂', '刘洋', '2025-04-10', 'system', '2025-04-10', 0),
      (106, '虫害啃食', '清除害虫，喷洒生物农药', '陈刚', '2025-04-12', 'system', '2025-04-12', 0);
  END IF;

  -- d_plantcare_diseaseinfo
  IF (SELECT COUNT(*) FROM d_plantcare_diseaseinfo) < 5 THEN
    INSERT INTO d_plantcare_diseaseinfo
      (basic_id, disease_time, age, disease, treatment_time, m_staff, drug_id, drug_type, WDT,
       cur_effect, cur_time, out_time, out_no, f_staff, belong)
    VALUES
      (101, '2025-04-01', 6, '锈病', '2025-04-02', '张伟', 1, '三唑酮', '15-20', 1, '2025-04-05', '2025-04-10', 1, 'system', 0),
      (102, '2025-04-03', 8, '白粉病', '2025-04-04', '李强', 2, '甲基托布津', '12-18', 1, '2025-04-07', '2025-04-12', 2, 'system', 0),
      (103, '2025-04-05', 4, '褐斑病', '2025-04-06', '王芳', 3, '百菌清', '10-15', 0, NULL, '2025-04-15', 3, 'system', 0),
      (104, '2025-04-08', 10, '枯萎病', '2025-04-09', '赵敏', 4, '多菌灵', '8-12', 1, '2025-04-12', '2025-04-18', 4, 'system', 0),
      (105, '2025-04-10', 5, '炭疽病', '2025-04-11', '刘洋', 5, '代森锰锌', '14-20', 1, '2025-04-14', '2025-04-20', 5, 'system', 0),
      (106, '2025-04-12', 7, '叶斑病', '2025-04-13', '陈刚', 6, '福美双', '10-16', 0, NULL, '2025-04-22', 6, 'system', 0);
  END IF;

  -- d_plantcare_immunizationinfo
  IF (SELECT COUNT(*) FROM d_plantcare_immunizationinfo) < 5 THEN
    INSERT INTO d_plantcare_immunizationinfo
      (basic_id, imm_age, imm_date, vaccine_id, maker_id, dose, anti_level, post_stage,
       out_time, f_date, operators, belong, f_staff)
    VALUES
      (101, 3.0, '2025-04-01', 1, 1, '0.5ml', '高', '幼苗期', '2025-04-10', '2025-04-01', '张伟', 0, 'system'),
      (102, 6.0, '2025-04-03', 2, 2, '1.0ml', '中', '生长期', '2025-04-12', '2025-04-03', '李强', 0, 'system'),
      (103, 12.0, '2025-04-05', 3, 1, '1.5ml', '高', '成熟期', '2025-04-15', '2025-04-05', '王芳', 0, 'system'),
      (104, 2.5, '2025-04-08', 1, 3, '0.5ml', '低', '幼苗期', '2025-04-18', '2025-04-08', '赵敏', 0, 'system'),
      (105, 8.0, '2025-04-10', 4, 2, '1.0ml', '中', '开花期', '2025-04-20', '2025-04-10', '刘洋', 0, 'system'),
      (106, 4.0, '2025-04-12', 2, 1, '0.8ml', '高', '生长期', '2025-04-22', '2025-04-12', '陈刚', 0, 'system');
  END IF;

  -- d_plantcare_nursinginfo
  IF (SELECT COUNT(*) FROM d_plantcare_nursinginfo) < 5 THEN
    INSERT INTO d_plantcare_nursinginfo
      (basic_id, age, nurse, nur_time, root_shape, prenatal_paralysi, uterus_fall,
       swelling, Ab_color, Ab_smell, information, f_date, belong, f_staff)
    VALUES
      (101, 6, '张伟', '2025-04-01', 1, 0, 0, 0, 1, 0, '根系发育良好，无需特殊护理', '2025-04-01', 0, 'system'),
      (102, 8, '李强', '2025-04-03', 2, 0, 0, 1, 0, 0, '轻微肿胀，已做标记观察', '2025-04-03', 0, 'system'),
      (103, 4, '王芳', '2025-04-05', 1, 0, 0, 0, 1, 1, '有异味，已更换培养基质', '2025-04-05', 0, 'system'),
      (104, 10, '赵敏', '2025-04-08', 3, 0, 1, 0, 0, 0, '发现倒伏，已支撑固定', '2025-04-08', 0, 'system'),
      (105, 5, '刘洋', '2025-04-10', 1, 0, 0, 0, 1, 0, '生长状态正常，常规巡查', '2025-04-10', 0, 'system'),
      (106, 7, '陈刚', '2025-04-12', 2, 0, 0, 0, 0, 0, '叶片发黄，补充微量元素', '2025-04-12', 0, 'system');
  END IF;

  -- d_plantcare_protectioninfo
  IF (SELECT COUNT(*) FROM d_plantcare_protectioninfo) < 5 THEN
    INSERT INTO d_plantcare_protectioninfo
      (basic_id, protection_age, take_time, drug_id, vac_maker, effect, timing, IR_bath,
       out_time, f_date, operators, belong, f_staff)
    VALUES
      (101, 3.0, '2025-04-01', 1, 1, '有效', '上午', '叶面喷雾', '2025-04-10', '2025-04-01', '张伟', 0, 'system'),
      (102, 6.0, '2025-04-03', 2, 2, '良好', '下午', '根部灌注', '2025-04-12', '2025-04-03', '李强', 0, 'system'),
      (103, 12.0, '2025-04-05', 3, 1, '显著', '上午', '全面喷洒', '2025-04-15', '2025-04-05', '王芳', 0, 'system'),
      (104, 2.5, '2025-04-08', 1, 3, '一般', '傍晚', '局部处理', '2025-04-18', '2025-04-08', '赵敏', 0, 'system'),
      (105, 8.0, '2025-04-10', 4, 2, '有效', '上午', '叶面喷雾', '2025-04-20', '2025-04-10', '刘洋', 0, 'system'),
      (106, 4.0, '2025-04-12', 2, 1, '良好', '下午', '土壤处理', '2025-04-22', '2025-04-12', '陈刚', 0, 'system');
  END IF;

  -- d_plantcare_quarantineinfo
  IF (SELECT COUNT(*) FROM d_plantcare_quarantineinfo) < 5 THEN
    INSERT INTO d_plantcare_quarantineinfo
      (basic_id, quarantine_time, quarantine_age, quarantine_result, quarantine_type,
       quarantine_num, quarantine_staff, quarantine_method, quarantine_reason, f_date, belong, f_staff)
    VALUES
      (101, '2025-04-01', 6, 1, '入棚检疫', 'Q2025040101', '张伟', '目视+采样', '新批次入棚', '2025-04-01', 0, 'system'),
      (102, '2025-04-03', 8, 1, '常规巡检', 'Q2025040301', '李强', '目视检查', '月度巡检', '2025-04-03', 0, 'system'),
      (103, '2025-04-05', 4, 0, '疫情排查', 'Q2025040501', '王芳', '采样检测', '邻近棚发现病害', '2025-04-05', 0, 'system'),
      (104, '2025-04-08', 10, 1, '出棚检疫', 'Q2025040801', '赵敏', '全面检测', '准备移栽', '2025-04-08', 0, 'system'),
      (105, '2025-04-10', 5, 1, '入棚检疫', 'Q2025041001', '刘洋', '目视+采样', '新批次入棚', '2025-04-10', 0, 'system'),
      (106, '2025-04-12', 7, 0, '异常排查', 'Q2025041201', '陈刚', '采样检测', '叶片出现黄斑', '2025-04-12', 0, 'system');
  END IF;

  -- d_plantcare_witherinfo
  IF (SELECT COUNT(*) FROM d_plantcare_witherinfo) < 5 THEN
    INSERT INTO d_plantcare_witherinfo
      (basic_id, wither_age, wither_time, wither_reason, wither_result, f_date, belong, f_staff)
    VALUES
      (101, 6, '2025-04-01', '自然枯萎', '正常淘汰', '2025-04-01', 0, 'system'),
      (102, 8, '2025-04-03', '缺水干旱', '抢救成功', '2025-04-03', 0, 'system'),
      (103, 4, '2025-04-05', '病害枯萎', '已清理', '2025-04-05', 0, 'system'),
      (104, 10, '2025-04-08', '自然老化', '正常淘汰', '2025-04-08', 0, 'system'),
      (105, 5, '2025-04-10', '肥害烧根', '已换土', '2025-04-10', 0, 'system'),
      (106, 7, '2025-04-12', '涝害烂根', '改善排水', '2025-04-12', 0, 'system');
  END IF;


  -- ----------------------------------------------------------
  -- 2.3 e_cultivation_* group
  -- ----------------------------------------------------------

  -- e_cultivation_cultivationinfo
  IF (SELECT COUNT(*) FROM e_cultivation_cultivationinfo) < 5 THEN
    INSERT INTO e_cultivation_cultivationinfo
      (cultivation_date, pre_harvest_date, cultivation_way, mother_id, mother_variety,
       father_id, father_variety, cultivation_state, staff, f_staff, f_date, belong, growth_period, single_success)
    VALUES
      ('2025-04-01', '2025-08-01', 1, 1001, 1, 2001, 2, 1, '张伟', 'system', '2025-04-01', 0, 120, '是'),
      ('2025-04-03', '2025-08-15', 2, 1002, 1, 2002, 2, 1, '李强', 'system', '2025-04-03', 0, 135, '是'),
      ('2025-04-05', '2025-09-01', 1, 1003, 3, 2003, 4, 0, '王芳', 'system', '2025-04-05', 0, 150, '否'),
      ('2025-04-08', '2025-08-20', 3, 1004, 2, 2004, 1, 1, '赵敏', 'system', '2025-04-08', 0, 130, '是'),
      ('2025-04-10', '2025-09-10', 1, 1005, 4, 2005, 3, 1, '刘洋', 'system', '2025-04-10', 0, 145, '是'),
      ('2025-04-12', '2025-08-25', 2, 1006, 2, 2006, 2, 0, '陈刚', 'system', '2025-04-12', 0, 125, '否');
  END IF;

  -- e_cultivation_floweringinfo
  IF (SELECT COUNT(*) FROM e_cultivation_floweringinfo) < 5 THEN
    INSERT INTO e_cultivation_floweringinfo
      (check_type, cultivation_id, flowering_status, f_staff, f_date, notes, belong)
    VALUES
      ('目测检查', 1, '初花期', 'system', '2025-05-01', '花序分化正常，花粉活力良好', 0),
      ('仪器检测', 2, '盛花期', 'system', '2025-05-10', '花粉量充足，授粉条件佳', 0),
      ('目测检查', 3, '末花期', 'system', '2025-05-15', '部分花朵已凋谢，开始结籽', 0),
      ('仪器检测', 4, '初花期', 'system', '2025-05-05', '花穗整齐，颜色正常', 0),
      ('目测检查', 5, '盛花期', 'system', '2025-05-12', '蜜蜂授粉活跃，坐果率高', 0),
      ('仪器检测', 6, '初花期', 'system', '2025-05-08', '花药饱满，散粉正常', 0);
  END IF;

  -- e_cultivation_germinationinfo
  IF (SELECT COUNT(*) FROM e_cultivation_germinationinfo) < 5 THEN
    INSERT INTO e_cultivation_germinationinfo
      (sprout_id, Delivery_date, cultivation_way, Seedling_weight, wea_weight, belong, f_staff, rank)
    VALUES
      (1, '2025-04-05', 1, 12.5, 10.2, 0, 'system', 1),
      (2, '2025-04-08', 2, 15.0, 13.5, 0, 'system', 1),
      (3, '2025-04-10', 1, 8.5, 7.0, 0, 'system', 2),
      (4, '2025-04-12', 3, 18.0, 16.5, 0, 'system', 1),
      (5, '2025-04-15', 2, 11.0, 9.8, 0, 'system', 2),
      (6, '2025-04-18', 1, 14.5, 13.0, 0, 'system', 1);
  END IF;

  -- e_cultivation_irrigationinfo
  IF (SELECT COUNT(*) FROM e_cultivation_irrigationinfo) < 5 THEN
    INSERT INTO e_cultivation_irrigationinfo
      (sprout_id, delivery_date, BW, reason, feeding_material, mcal, health, help, dose,
       feeding_staff, belong, f_staff)
    VALUES
      (1, '2025-04-05', '正常', '春季返青', '复合肥', '12-8-10', '良好', '无', '15kg/亩', '张伟', 0, 'system'),
      (2, '2025-04-08', '偏湿', '连续降雨', '有机肥', '5-3-2', '良好', '排水', '10kg/亩', '李强', 0, 'system'),
      (3, '2025-04-10', '正常', '拔节期需水', '尿素', '46-0-0', '良好', '无', '8kg/亩', '王芳', 0, 'system'),
      (4, '2025-04-12', '偏干', '干旱少雨', '水溶肥', '20-20-20', '一般', '补水', '12kg/亩', '赵敏', 0, 'system'),
      (5, '2025-04-15', '正常', '孕穗期', '磷酸二氢钾', '0-52-34', '良好', '无', '5kg/亩', '刘洋', 0, 'system'),
      (6, '2025-04-18', '正常', '灌浆期', '微量元素肥', '多元', '良好', '无', '3kg/亩', '陈刚', 0, 'system');
  END IF;

  -- e_cultivation_maturationinfo
  IF (SELECT COUNT(*) FROM e_cultivation_maturationinfo) < 5 THEN
    INSERT INTO e_cultivation_maturationinfo
      (cultivation_id, cultivation_date, delivery_date, father_id, mother_id, Booroola,
       mother_health, mother_condition, sprout_ele_num, sprout_state, sprout_weight,
       live_seedling_num, planting_attendants, f_staff, f_date, notes, belong)
    VALUES
      (1, '2025-04-01', '2025-04-05', 2001, 1001, 1.2, 1, 1, 'SE001', 1, 15.5, 85, '张伟', 'system', '2025-04-05', '出苗整齐，成活率达标', 0),
      (2, '2025-04-03', '2025-04-08', 2002, 1002, 1.5, 1, 1, 'SE002', 1, 18.0, 92, '李强', 'system', '2025-04-08', '苗情健壮，无病虫害', 0),
      (3, '2025-04-05', '2025-04-10', 2003, 1003, 1.0, 0, 1, 'SE003', 2, 12.5, 78, '王芳', 'system', '2025-04-10', '部分弱苗，已标记', 0),
      (4, '2025-04-08', '2025-04-12', 2004, 1004, 1.3, 1, 1, 'SE004', 1, 16.8, 88, '赵敏', 'system', '2025-04-12', '生长均衡，符合标准', 0),
      (5, '2025-04-10', '2025-04-15', 2005, 1005, 1.4, 1, 0, 'SE005', 1, 17.2, 90, '刘洋', 'system', '2025-04-15', '基质养分充足，根系发达', 0),
      (6, '2025-04-12', '2025-04-18', 2006, 1006, 1.1, 1, 1, 'SE006', 2, 14.0, 82, '陈刚', 'system', '2025-04-18', '湿度略高，注意通风', 0);
  END IF;

  -- e_cultivation_polleninfo
  IF (SELECT COUNT(*) FROM e_cultivation_polleninfo) < 5 THEN
    INSERT INTO e_cultivation_polleninfo
      (pollen_date, cultivation_id, pollen_type, pollen_num, pollen_staff, f_staff, f_date, belong)
    VALUES
      ('2025-05-01', 1, 1, 50, '张伟', 'system', '2025-05-01', 0),
      ('2025-05-05', 2, 2, 80, '李强', 'system', '2025-05-05', 0),
      ('2025-05-08', 3, 1, 45, '王芳', 'system', '2025-05-08', 0),
      ('2025-05-10', 4, 3, 65, '赵敏', 'system', '2025-05-10', 0),
      ('2025-05-12', 5, 2, 75, '刘洋', 'system', '2025-05-12', 0),
      ('2025-05-15', 6, 1, 55, '陈刚', 'system', '2025-05-15', 0);
  END IF;

  -- e_cultivation_seedinginfo
  IF (SELECT COUNT(*) FROM e_cultivation_seedinginfo) < 5 THEN
    INSERT INTO e_cultivation_seedinginfo
      (seeding_date, seed_num, seed_weight, seed_type, seed_source, seed_batch,
       seed_purity, seed_germination, seed_moisture, seed_viability, f_staff, f_date, belong)
    VALUES
      ('2025-03-01', 500, 2.5, 1, '自繁', 'B20250301', 98.5, 92.0, 8.5, 95.0, 'system', '2025-03-01', 0),
      ('2025-03-05', 800, 4.0, 2, '外购', 'B20250305', 99.0, 95.0, 7.8, 96.0, 'system', '2025-03-05', 0),
      ('2025-03-10', 600, 3.2, 1, '自繁', 'B20250310', 97.8, 90.0, 9.0, 94.0, 'system', '2025-03-10', 0),
      ('2025-03-15', 1000, 5.5, 3, '合作基地', 'B20250315', 98.0, 93.0, 8.2, 95.5, 'system', '2025-03-15', 0),
      ('2025-03-20', 450, 2.8, 2, '外购', 'B20250320', 99.2, 96.0, 7.5, 97.0, 'system', '2025-03-20', 0),
      ('2025-03-25', 700, 3.8, 1, '自繁', 'B20250325', 98.8, 94.0, 8.0, 96.0, 'system', '2025-03-25', 0);
  END IF;

  -- e_cultivation_sproutinfo
  IF (SELECT COUNT(*) FROM e_cultivation_sproutinfo) < 5 THEN
    INSERT INTO e_cultivation_sproutinfo
      (sprout_date, seed_id, sprout_num, sprout_rate, sprout_staff, f_staff, f_date, belong)
    VALUES
      ('2025-04-01', 1, 460, 92.0, '张伟', 'system', '2025-04-01', 0),
      ('2025-04-05', 2, 760, 95.0, '李强', 'system', '2025-04-05', 0),
      ('2025-04-10', 3, 540, 90.0, '王芳', 'system', '2025-04-10', 0),
      ('2025-04-15', 4, 930, 93.0, '赵敏', 'system', '2025-04-15', 0),
      ('2025-04-20', 5, 432, 96.0, '刘洋', 'system', '2025-04-20', 0),
      ('2025-04-25', 6, 658, 94.0, '陈刚', 'system', '2025-04-25', 0);
  END IF;


  -- ----------------------------------------------------------
  -- 2.4 g_harvest_* group
  -- ----------------------------------------------------------

  -- g_harvest_binformationinfo
  IF (SELECT COUNT(*) FROM g_harvest_binformationinfo) < 5 THEN
    INSERT INTO g_harvest_binformationinfo
      (belong, date, month, basic_id, variety, source, back_fat_thickness, net_meat_ratio,
       CWT, emuscle_area, back_thickness, level, recorder, notes, f_staff)
    VALUES
      (0, '2025-04-01', 4.0, 'GH001', 1, '本场', 2.5, 52.0, 18.5, 12.5, 3.2, '优', '张伟', '草质鲜嫩，色泽正常', 'system'),
      (0, '2025-04-03', 4.0, 'GH002', 2, '本场', 2.8, 50.0, 17.8, 11.8, 3.5, '良', '李强', '茎秆略粗，适口性一般', 'system'),
      (0, '2025-04-05', 4.0, 'GH003', 1, '合作场', 2.2, 54.0, 19.2, 13.0, 2.9, '优', '王芳', '叶片完整，无病虫害', 'system'),
      (0, '2025-04-08', 4.0, 'GH004', 3, '本场', 3.0, 48.0, 17.0, 11.0, 3.8, '中', '赵敏', '部分枯黄，需改进', 'system'),
      (0, '2025-04-10', 4.0, 'GH005', 2, '外购', 2.6, 51.0, 18.0, 12.0, 3.3, '良', '刘洋', '包装完好，运输无损', 'system'),
      (0, '2025-04-12', 4.0, 'GH006', 1, '本场', 2.3, 53.0, 19.0, 12.8, 3.0, '优', '陈刚', '达到一级草标准', 'system');
  END IF;

  -- g_harvest_economicinfo
  IF (SELECT COUNT(*) FROM g_harvest_economicinfo) < 5 THEN
    INSERT INTO g_harvest_economicinfo
      (belong, basic_id, age, house_id, in_weight, in_1_5, in_3, in_4_5, out_weight,
       put_volume, intake, menu, cost, FCR, ADG, f_staff)
    VALUES
      ('A区', 'GH001', 6.0, 5, 1200.0, 800.0, 300.0, 100.0, 3500.0, 4200.0, 3800.0, 3200.0, 2.8, 4.2, 12.5, 'system'),
      ('B区', 'GH002', 8.0, 7, 1500.0, 1000.0, 400.0, 100.0, 4200.0, 5100.0, 4600.0, 3900.0, 3.0, 4.5, 11.0, 'system'),
      ('C区', 'GH003', 4.0, 12, 800.0, 500.0, 200.0, 100.0, 2400.0, 2900.0, 2600.0, 2200.0, 2.5, 4.0, 13.5, 'system'),
      ('D区', 'GH004', 10.0, 27, 2000.0, 1300.0, 500.0, 200.0, 5500.0, 6800.0, 6100.0, 5200.0, 3.2, 4.8, 10.5, 'system'),
      ('E区', 'GH005', 5.0, 28, 1000.0, 650.0, 250.0, 100.0, 3000.0, 3600.0, 3200.0, 2700.0, 2.7, 4.3, 12.0, 'system'),
      ('F区', 'GH006', 7.0, 5, 1300.0, 850.0, 350.0, 100.0, 3800.0, 4600.0, 4100.0, 3500.0, 2.9, 4.4, 11.8, 'system');
  END IF;

  -- g_harvest_g_salesinfo
  IF (SELECT COUNT(*) FROM g_harvest_g_salesinfo) < 5 THEN
    INSERT INTO g_harvest_g_salesinfo
      (belong, sales_date, sales_order, type, billing_unit, unit_price, weight, total_price,
       transportation, img_trans, sales_site, name, buyer, buyer_phone, selling_type, notes, f_staff)
    VALUES
      (0, '2025-04-01', 'SO250401', 1, '公斤', 3.5, 5000.0, 17500.0, '物流', '/img/trans01.jpg', '河北省保定市', '高羊茅', '王经理', '13800138000', 1, '现款现货', 'system'),
      (0, '2025-04-05', 'SO250405', 2, '公斤', 4.2, 3000.0, 12600.0, '自提', '/img/trans02.jpg', '北京市大兴区', '黑麦草', '李老板', '13900139000', 2, '赊销30天', 'system'),
      (0, '2025-04-10', 'SO250410', 1, '公斤', 3.8, 4500.0, 17100.0, '物流', '/img/trans03.jpg', '天津市武清区', '早熟禾', '张采购', '13700137000', 1, '现款现货', 'system'),
      (0, '2025-04-12', 'SO250412', 3, '公斤', 5.0, 2000.0, 10000.0, '冷链', '/img/trans04.jpg', '上海市浦东新区', '紫花苜蓿', '赵总', '13600136000', 1, '优质优价', 'system'),
      (0, '2025-04-15', 'SO250415', 1, '公斤', 3.2, 6000.0, 19200.0, '物流', '/img/trans05.jpg', '山东省济南市', '白三叶', '陈经理', '13500135000', 2, '月结', 'system'),
      (0, '2025-04-18', 'SO250418', 2, '公斤', 4.5, 2500.0, 11250.0, '自提', '/img/trans06.jpg', '河南省郑州市', '红三叶', '刘主任', '13400134000', 1, '现款现货', 'system');
  END IF;

  -- g_harvest_s_salesinfo
  IF (SELECT COUNT(*) FROM g_harvest_s_salesinfo) < 5 THEN
    INSERT INTO g_harvest_s_salesinfo
      (belong, sales_date, sales_order, type, quarantine_coding, ele_num, age, medical_leave,
       billing_unit, unit_price, weight, total_price, transportation, img_trans, sales_site,
       name, buyer, buyer_phone, selling_type, basic_id, notes, f_staff)
    VALUES
      (0, '2025-04-01', 'SO250401S', 1, 'Q20250401', 'EL001', 6.0, 0, '公斤', 3.5, 500.0, 1750.0, '物流', '/img/s01.jpg', '保定', '高羊茅草捆', '王经理', '13800138000', 1, 101, '一级品', 'system'),
      (0, '2025-04-05', 'SO250405S', 2, 'Q20250405', 'EL002', 8.0, 0, '公斤', 4.2, 300.0, 1260.0, '自提', '/img/s02.jpg', '北京', '黑麦草草捆', '李老板', '13900139000', 2, 102, '特级品', 'system'),
      (0, '2025-04-10', 'SO250410S', 1, 'Q20250410', 'EL003', 4.0, 0, '公斤', 3.8, 450.0, 1710.0, '物流', '/img/s03.jpg', '天津', '早熟禾草捆', '张采购', '13700137000', 1, 103, '一级品', 'system'),
      (0, '2025-04-12', 'SO250412S', 3, 'Q20250412', 'EL004', 10.0, 0, '公斤', 5.0, 200.0, 1000.0, '冷链', '/img/s04.jpg', '上海', '苜蓿草捆', '赵总', '13600136000', 1, 104, '有机认证', 'system'),
      (0, '2025-04-15', 'SO250415S', 1, 'Q20250415', 'EL005', 5.0, 0, '公斤', 3.2, 600.0, 1920.0, '物流', '/img/s05.jpg', '济南', '白三叶草捆', '陈经理', '13500135000', 2, 105, '一级品', 'system'),
      (0, '2025-04-18', 'SO250418S', 2, 'Q20250418', 'EL006', 7.0, 0, '公斤', 4.5, 250.0, 1125.0, '自提', '/img/s06.jpg', '郑州', '红三叶草捆', '刘主任', '13400134000', 1, 106, '特级品', 'system');
  END IF;

  -- g_harvest_segmentinfo
  IF (SELECT COUNT(*) FROM g_harvest_segmentinfo) < 5 THEN
    INSERT INTO g_harvest_segmentinfo
      (belong, basic_id, age, source, in_weight, CWT, net_meat_weight, spine, chops_weight,
       stick_bone_weight, others_weight, head_weight, blood_weight, skin_weight, heart_weight,
       liver_weight, lungs_weight, tripe_weight, hoof_weight, L_intestine_weight, S_intestine_weight,
       kidney_weight, white_weight, date, f_staff)
    VALUES
      (0, 'GH001', 6.0, '本场', 1200.0, 18.5, 52.0, 8.5, 12.0, 5.5, 3.2, 2.8, 1.5, 8.0, 0.8, 1.2, 1.5, 2.0, 1.8, 3.5, 2.2, 0.6, 0.4, '2025-04-01', 'system'),
      (0, 'GH002', 8.0, '本场', 1500.0, 17.8, 50.0, 8.2, 11.5, 5.2, 3.0, 2.6, 1.4, 7.8, 0.7, 1.1, 1.4, 1.9, 1.7, 3.3, 2.0, 0.5, 0.3, '2025-04-03', 'system'),
      (0, 'GH003', 4.0, '合作场', 800.0, 19.2, 54.0, 8.8, 12.5, 5.8, 3.5, 3.0, 1.6, 8.5, 0.9, 1.3, 1.6, 2.2, 2.0, 3.8, 2.4, 0.7, 0.5, '2025-04-05', 'system'),
      (0, 'GH004', 10.0, '本场', 2000.0, 17.0, 48.0, 7.8, 11.0, 5.0, 2.8, 2.4, 1.3, 7.5, 0.6, 1.0, 1.3, 1.8, 1.6, 3.0, 1.8, 0.5, 0.3, '2025-04-08', 'system'),
      (0, 'GH005', 5.0, '外购', 1000.0, 18.0, 51.0, 8.3, 11.8, 5.4, 3.1, 2.7, 1.5, 7.9, 0.8, 1.2, 1.5, 2.0, 1.8, 3.4, 2.1, 0.6, 0.4, '2025-04-10', 'system'),
      (0, 'GH006', 7.0, '本场', 1300.0, 19.0, 53.0, 8.6, 12.2, 5.6, 3.3, 2.9, 1.5, 8.2, 0.8, 1.2, 1.5, 2.1, 1.9, 3.6, 2.3, 0.6, 0.4, '2025-04-12', 'system');
  END IF;


  -- ----------------------------------------------------------
  -- 2.5 h_store_* group
  -- ----------------------------------------------------------

  -- h_store_feedingin
  IF (SELECT COUNT(*) FROM h_store_feedingin) < 5 THEN
    INSERT INTO h_store_feedingin
      (type, f_name, ingredientsType, warehouse_num, nutrients, buy_time, billing_unit, quantity,
       unit_price, total_price, specifications, purpose, water_content, mildew, impurity_content,
       maker_id, notes, f_date, operation, keep_amount, belong, f_staff, fare, avg_price)
    VALUES
      (1, '玉米秸秆', 1, 1, '粗纤维', '2025-03-01', '吨', 50.0, 800.0, 40000.0, '切碎', '基肥', '12', '无', '2', 1, '颜色金黄，无霉变', '2025-03-01', '入库', 50.0, 0, 'system', 500.0, 810.0),
      (2, '豆粕', 2, 2, '粗蛋白', '2025-03-05', '吨', 30.0, 3500.0, 105000.0, '颗粒', '追肥', '10', '无', '1', 2, '蛋白含量达标', '2025-03-05', '入库', 30.0, 0, 'system', 300.0, 3510.0),
      (1, '羊草', 1, 3, '粗纤维', '2025-03-10', '吨', 40.0, 1200.0, 48000.0, '捆装', '基肥', '11', '无', '2', 3, '本地优质羊草', '2025-03-10', '入库', 40.0, 0, 'system', 400.0, 1210.0),
      (2, '磷酸二铵', 3, 4, '磷氮', '2025-03-15', '吨', 20.0, 4200.0, 84000.0, '袋装', '追肥', '8', '无', '0', 4, '缓释型，肥效持久', '2025-03-15', '入库', 20.0, 0, 'system', 200.0, 4210.0),
      (1, '苜蓿干草', 1, 5, '粗蛋白', '2025-03-20', '吨', 25.0, 2800.0, 70000.0, '捆装', '基肥', '10', '无', '1', 5, '紫花苜蓿，蛋白高', '2025-03-20', '入库', 25.0, 0, 'system', 250.0, 2810.0),
      (2, '尿素', 3, 6, '氮', '2025-03-25', '吨', 15.0, 2200.0, 33000.0, '袋装', '追肥', '5', '无', '0', 6, '含氮量46%', '2025-03-25', '入库', 15.0, 0, 'system', 150.0, 2210.0);
  END IF;

  -- h_store_feeding_out
  IF (SELECT COUNT(*) FROM h_store_feeding_out) < 5 THEN
    INSERT INTO h_store_feeding_out
      (outbound_no, type, f_name, ingredientsType, warehouse_num, delivery_time, out_purposes,
       num, out_price, out_staff, maker_id, contact_phone, notes, belong, f_staff)
    VALUES
      ('FO250401', 1, '玉米秸秆', 1, 1, '2025-04-01', 'A区施肥', 5, 810.0, '张伟', 1, '13800138000', '基肥使用', 0, 'system'),
      ('FO250403', 2, '豆粕', 2, 2, '2025-04-03', 'B区追肥', 3, 3510.0, '李强', 2, '13900139000', '蛋白补充', 0, 'system'),
      ('FO250405', 1, '羊草', 1, 3, '2025-04-05', 'C区基肥', 4, 1210.0, '王芳', 3, '13700137000', '常规施肥', 0, 'system'),
      ('FO250408', 3, '磷酸二铵', 3, 4, '2025-04-08', 'D区追肥', 2, 4210.0, '赵敏', 4, '13600136000', '磷肥补充', 0, 'system'),
      ('FO250410', 1, '苜蓿干草', 1, 5, '2025-04-10', 'E区基肥', 2, 2810.0, '刘洋', 5, '13500135000', '高蛋白基肥', 0, 'system'),
      ('FO250412', 3, '尿素', 3, 6, '2025-04-12', 'F区追肥', 1, 2210.0, '陈刚', 6, '13400134000', '快速补氮', 0, 'system');
  END IF;

  -- h_store_inventory
  IF (SELECT COUNT(*) FROM h_store_inventory) < 5 THEN
    INSERT INTO h_store_inventory
      (type, goods, maker_id, ingredientsType, quantity, stockPrice, totalCost, alert, f_date,
       operation, belong, out_time, f_staff)
    VALUES
      (1, '玉米秸秆', 1, 1, 45.0, 810.0, 36450.0, 10.0, '2025-04-01', '库存盘点', 0, NULL, 'system'),
      (2, '豆粕', 2, 2, 27.0, 3510.0, 94770.0, 5.0, '2025-04-01', '库存盘点', 0, NULL, 'system'),
      (1, '羊草', 3, 1, 36.0, 1210.0, 43560.0, 8.0, '2025-04-01', '库存盘点', 0, NULL, 'system'),
      (3, '磷酸二铵', 4, 3, 18.0, 4210.0, 75780.0, 3.0, '2025-04-01', '库存盘点', 0, NULL, 'system'),
      (1, '苜蓿干草', 5, 1, 23.0, 2810.0, 64630.0, 5.0, '2025-04-01', '库存盘点', 0, NULL, 'system'),
      (3, '尿素', 6, 3, 14.0, 2210.0, 30940.0, 3.0, '2025-04-01', '库存盘点', 0, NULL, 'system');
  END IF;

  -- h_store_protection_in
  IF (SELECT COUNT(*) FROM h_store_protection_in) < 5 THEN
    INSERT INTO h_store_protection_in
      (v_name, type, ingredientsType, maker_id, purpose, produce_date, expiration_date, produce_num,
       billing_unit, in_amount, unit_price, total_price, in_time, keep_amount, f_date, operation,
       belong, f_staff, fare, avg_price)
    VALUES
      ('百菌清', 1, 4, 1, '杀菌', '2024-06-01', '2026-06-01', 'BN20240601', '瓶', 100, 25.0, 2500.0, '2025-03-01', 100.0, '2025-03-01', '入库', 0, 'system', 50.0, 25.5),
      ('多菌灵', 2, 4, 2, '杀菌', '2024-08-15', '2026-08-15', 'DJ20240815', '袋', 80, 35.0, 2800.0, '2025-03-05', 80.0, '2025-03-05', '入库', 0, 'system', 40.0, 35.5),
      ('吡虫啉', 3, 5, 3, '杀虫', '2024-09-10', '2026-09-10', 'BC20240910', '瓶', 60, 45.0, 2700.0, '2025-03-10', 60.0, '2025-03-10', '入库', 0, 'system', 30.0, 45.5),
      ('草甘膦', 1, 5, 4, '除草', '2024-10-20', '2026-10-20', 'CG20241020', '桶', 40, 120.0, 4800.0, '2025-03-15', 40.0, '2025-03-15', '入库', 0, 'system', 80.0, 122.0),
      ('阿维菌素', 2, 5, 5, '杀虫', '2024-11-05', '2026-11-05', 'AW20241105', '瓶', 50, 55.0, 2750.0, '2025-03-20', 50.0, '2025-03-20', '入库', 0, 'system', 35.0, 55.7),
      ('代森锰锌', 3, 4, 6, '杀菌', '2024-12-01', '2026-12-01', 'DS20241201', '袋', 70, 30.0, 2100.0, '2025-03-25', 70.0, '2025-03-25', '入库', 0, 'system', 25.0, 30.4);
  END IF;

  -- h_store_protection_out
  IF (SELECT COUNT(*) FROM h_store_protection_out) < 5 THEN
    INSERT INTO h_store_protection_out
      (outbound_no, v_name, type, ingredientsType, delivery_time, out_purposes, num, out_price,
       maker_id, out_staff, contact_phone, notes, belong, f_staff)
    VALUES
      ('PO250401', '百菌清', 1, 4, '2025-04-01', 'A区杀菌', 10, 25.5, 1, '张伟', '13800138000', '预防性喷药', 0, 'system'),
      ('PO250403', '多菌灵', 2, 4, '2025-04-03', 'B区杀菌', 8, 35.5, 2, '李强', '13900139000', '病害防治', 0, 'system'),
      ('PO250405', '吡虫啉', 3, 5, '2025-04-05', 'C区杀虫', 6, 45.5, 3, '王芳', '13700137000', '蚜虫防治', 0, 'system'),
      ('PO250408', '草甘膦', 1, 5, '2025-04-08', 'D区除草', 4, 122.0, 4, '赵敏', '13600136000', '行间除草', 0, 'system'),
      ('PO250410', '阿维菌素', 2, 5, '2025-04-10', 'E区杀虫', 5, 55.7, 5, '刘洋', '13500135000', '螨类防治', 0, 'system'),
      ('PO250412', '代森锰锌', 3, 4, '2025-04-12', 'F区杀菌', 7, 30.4, 6, '陈刚', '13400134000', '霜霉病预防', 0, 'system');
  END IF;


  -- ----------------------------------------------------------
  -- 2.6 supply_* group
  -- ----------------------------------------------------------

  -- supply_commodityinfo
  IF (SELECT COUNT(*) FROM supply_commodityinfo) < 5 THEN
    INSERT INTO supply_commodityinfo
      (type, cname, explain, belong, f_staff)
    VALUES
      (1, '玉米秸秆', '优质青贮玉米秸秆，适口性好', 0, 'system'),
      (2, '豆粕', '高蛋白豆粕，适合追肥', 0, 'system'),
      (3, '百菌清', '广谱杀菌剂，预防真菌病害', 0, 'system'),
      (4, '尿素', '高氮肥料，快速补充氮素', 0, 'system'),
      (5, '苜蓿种子', '紫花苜蓿，蛋白含量高', 0, 'system'),
      (1, '羊草', '本地优质羊草，粗纤维丰富', 0, 'system');
  END IF;

  -- supply_f_suppliersinfo
  IF (SELECT COUNT(*) FROM supply_f_suppliersinfo) < 5 THEN
    INSERT INTO supply_f_suppliersinfo
      (belong, supplier_name, sale_type, sup_linkman, sup_contact, contact, mail, address, f_date, operation, f_staff)
    VALUES
      (0, '绿源饲料有限公司', '饲料原料', '张经理', '13800138000', '13800138000', 'ly@feed.com', '河北省石家庄市', '2024-01-01', '长期合作', 'system'),
      (0, '丰收农资合作社', '化肥农药', '李主任', '13900139000', '13900139000', 'fs@nongzi.com', '河北省保定市', '2024-02-01', '年度采购', 'system'),
      (0, '华北种业集团', '草种', '王科长', '13700137000', '13700137000', 'hb@seed.com', '北京市大兴区', '2024-03-01', '种子供应', 'system'),
      (0, '恒通物流有限公司', '运输', '赵经理', '13600136000', '13600136000', 'ht@wuliu.com', '天津市武清区', '2024-04-01', '物流合作', 'system'),
      (0, '金盾植保服务站', '农药', '陈站长', '13500135000', '13500135000', 'jd@zhibao.com', '河北省唐山市', '2024-05-01', '农药供应', 'system'),
      (0, '绿洲有机肥厂', '有机肥', '刘厂长', '13400134000', '13400134000', 'lz@youji.com', '河北省沧州市', '2024-06-01', '基肥供应', 'system');
  END IF;

  -- supply_insuranceinfo
  IF (SELECT COUNT(*) FROM supply_insuranceinfo) < 5 THEN
    INSERT INTO supply_insuranceinfo
      (belong, in_name, contact, mail, handler, link, f_date, f_staff)
    VALUES
      (0, '人保财险', '95518', 'picc@picc.com.cn', '张经理', '13800138000', '2024-01-01', 'system'),
      (0, '平安财险', '95511', 'pa@pingan.com', '李主任', '13900139000', '2024-02-01', 'system'),
      (0, '太平洋财险', '95500', 'cpic@cpic.com.cn', '王科长', '13700137000', '2024-03-01', 'system'),
      (0, '中华联合财险', '95585', 'zh@zhlianhe.com', '赵经理', '13600136000', '2024-04-01', 'system'),
      (0, '国寿财险', '95519', 'gi@chinalife.com', '陈站长', '13500135000', '2024-05-01', 'system'),
      (0, '阳光财险', '95510', 'yg@sinosig.com', '刘厂长', '13400134000', '2024-06-01', 'system');
  END IF;

  -- supply_v_suppliersinfo
  IF (SELECT COUNT(*) FROM supply_v_suppliersinfo) < 5 THEN
    INSERT INTO supply_v_suppliersinfo
      (belong, supplier_name, sale_type, sup_linkman, sup_contact, contact, mail, address, f_date, operation, f_staff)
    VALUES
      (0, '中牧实业', '疫苗', '张经理', '13800138000', '13800138000', 'zm@cam.com', '北京市海淀区', '2024-01-01', '疫苗供应', 'system'),
      (0, '大华农生物', '兽药', '李主任', '13900139000', '13900139000', 'dh@dhn.com', '广东省佛山市', '2024-02-01', '药品供应', 'system'),
      (0, '瑞普生物', '疫苗', '王科长', '13700137000', '13700137000', 'rp@ringpu.com', '天津市滨海新区', '2024-03-01', '疫苗供应', 'system'),
      (0, '齐鲁动保', '兽药', '赵经理', '13600136000', '13600136000', 'ql@qilu.com', '山东省济南市', '2024-04-01', '药品供应', 'system'),
      (0, '金宇生物', '疫苗', '陈站长', '13500135000', '13500135000', 'jy@jinyu.com', '内蒙古呼和浩特市', '2024-05-01', '疫苗供应', 'system'),
      (0, '勃林格殷格翰', '兽药', '刘厂长', '13400134000', '13400134000', 'bh@boehringer.com', '上海市浦东新区', '2024-06-01', '进口药品', 'system');
  END IF;


  -- ----------------------------------------------------------
  -- 2.7 basic_* group
  -- ----------------------------------------------------------

  -- basic_canopyperformance
  IF (SELECT COUNT(*) FROM basic_canopyperformance) < 5 THEN
    INSERT INTO basic_canopyperformance
      (basic_id, skin_area, skin_thick, date, f_staff, belong)
    VALUES
      (101, 12.5, 0.8, '2025-04-01', 'system', 0),
      (102, 14.0, 0.9, '2025-04-03', 'system', 0),
      (103, 11.0, 0.7, '2025-04-05', 'system', 0),
      (104, 15.5, 1.0, '2025-04-08', 'system', 0),
      (105, 13.0, 0.85, '2025-04-10', 'system', 0),
      (106, 12.0, 0.75, '2025-04-12', 'system', 0);
  END IF;

  -- basic_fertilizerinfo
  IF (SELECT COUNT(*) FROM basic_fertilizerinfo) < 5 THEN
    INSERT INTO basic_fertilizerinfo
      (house_id, num, weight, notes, f_staff, f_date, belong)
    VALUES
      (5, 10, 500.0, 'A区春季基肥，有机肥为主', '张伟', '2025-04-01', 0),
      (7, 8, 400.0, 'B区追肥，复合肥补充', '李强', '2025-04-03', 0),
      (12, 12, 600.0, 'C区基肥，羊草与有机肥混施', '王芳', '2025-04-05', 0),
      (27, 15, 750.0, 'D区大肥量，满足生产需求', '赵敏', '2025-04-08', 0),
      (28, 9, 450.0, 'E区常规施肥', '刘洋', '2025-04-10', 0),
      (5, 6, 300.0, 'A区补肥，针对弱苗区域', '陈刚', '2025-04-12', 0);
  END IF;

  -- basic_groupmalecapacity
  IF (SELECT COUNT(*) FROM basic_groupmalecapacity) < 5 THEN
    INSERT INTO basic_groupmalecapacity
      (one_year_ram, two_year_ram, three_year_ram, four_year_ram, five_year_ram, six_year_ram, belong, capa_ram)
    VALUES
      (85.0, 92.0, 95.0, 90.0, 88.0, 85.0, 0, '一龄85 二龄92 三龄95'),
      (80.0, 88.0, 93.0, 91.0, 87.0, 82.0, 0, '一龄80 二龄88 三龄93'),
      (88.0, 94.0, 96.0, 92.0, 89.0, 86.0, 0, '一龄88 二龄94 三龄96'),
      (82.0, 90.0, 94.0, 93.0, 90.0, 87.0, 0, '一龄82 二龄90 三龄94'),
      (86.0, 93.0, 97.0, 94.0, 91.0, 88.0, 0, '一龄86 二龄93 三龄97'),
      (84.0, 91.0, 95.0, 93.0, 89.0, 85.0, 0, '一龄84 二龄91 三龄95');
  END IF;

  -- basic_harvestinfo
  IF (SELECT COUNT(*) FROM basic_harvestinfo) < 5 THEN
    INSERT INTO basic_harvestinfo
      (house_id, ele_quantity, variety, harvest_time, rank, color, weight, staff, notes, belong, f_date, harvest_num)
    VALUES
      (5, 120, 1, '2025-04-01', 1, 1, 3500.0, '张伟', 'A区首批收割，草质优良', 0, '2025-04-01', 1),
      (7, 98, 2, '2025-04-03', 2, 0, 2800.0, '李强', 'B区二次收割，产量稳定', 0, '2025-04-03', 2),
      (12, 150, 1, '2025-04-05', 1, 1, 4200.0, '王芳', 'C区大丰收，达到预期', 0, '2025-04-05', 3),
      (27, 200, 3, '2025-04-08', 2, 1, 5500.0, '赵敏', 'D区刈割，留茬高度合适', 0, '2025-04-08', 4),
      (28, 110, 2, '2025-04-10', 1, 0, 3100.0, '刘洋', 'E区适时收割，营养丰富', 0, '2025-04-10', 5),
      (5, 85, 1, '2025-04-12', 2, 1, 2400.0, '陈刚', 'A区尾茬收割，质量尚可', 0, '2025-04-12', 6);
  END IF;

  -- basic_productivityinfo
  IF (SELECT COUNT(*) FROM basic_productivityinfo) < 5 THEN
    INSERT INTO basic_productivityinfo
      (basic_id, weight, high, Llong, bust, month_age, fecundity, per_meat, per_milk, per_hair,
       per_skin, growth_rate, FCR, belong)
    VALUES
      (101, 85.0, 65.0, 78.0, 82.0, 6.0, 85, 52, 0, 0, 12, '快', 4.2, 0),
      (102, 92.0, 68.0, 82.0, 85.0, 8.0, 90, 55, 0, 0, 13, '快', 4.5, 0),
      (103, 78.0, 62.0, 75.0, 80.0, 4.0, 80, 48, 0, 0, 11, '中', 4.0, 0),
      (104, 95.0, 70.0, 85.0, 88.0, 10.0, 92, 58, 0, 0, 14, '快', 4.8, 0),
      (105, 88.0, 66.0, 80.0, 83.0, 5.0, 87, 53, 0, 0, 12, '快', 4.3, 0),
      (106, 82.0, 64.0, 77.0, 81.0, 7.0, 83, 50, 0, 0, 11, '中', 4.1, 0);
  END IF;

  -- basic_sportsinfo
  IF (SELECT COUNT(*) FROM basic_sportsinfo) < 5 THEN
    INSERT INTO basic_sportsinfo
      (basic_id, exercise_time, exercise, belong, date)
    VALUES
      (101, '30min', 2.5, 0, '2025-04-01'),
      (102, '45min', 3.8, 0, '2025-04-03'),
      (103, '20min', 1.5, 0, '2025-04-05'),
      (104, '60min', 5.0, 0, '2025-04-08'),
      (105, '35min', 2.8, 0, '2025-04-10'),
      (106, '25min', 2.0, 0, '2025-04-12');
  END IF;

  -- basic_yieldperformance
  IF (SELECT COUNT(*) FROM basic_yieldperformance) < 5 THEN
    INSERT INTO basic_yieldperformance
      (basic_id, milk_volume, lamb_num, date, f_staff, belong)
    VALUES
      (101, '3.5kg/天', 2, '2025-04-01', 'system', 0),
      (102, '4.2kg/天', 3, '2025-04-03', 'system', 0),
      (103, '2.8kg/天', 1, '2025-04-05', 'system', 0),
      (104, '4.8kg/天', 3, '2025-04-08', 'system', 0),
      (105, '3.9kg/天', 2, '2025-04-10', 'system', 0),
      (106, '3.2kg/天', 2, '2025-04-12', 'system', 0);
  END IF;

  -- basic_yield_capacity
  IF (SELECT COUNT(*) FROM basic_yield_capacity) < 5 THEN
    INSERT INTO basic_yield_capacity
      (belong, yield_one_year, yield_two_year, yield_three_year, yield_four_year, yield_five_year, yield_six_year, capa_yield)
    VALUES
      (0, 3500.0, 4200.0, 4800.0, 4500.0, 4000.0, 3500.0, '一龄3500 二龄4200 三龄4800'),
      (0, 3200.0, 4000.0, 4600.0, 4400.0, 3900.0, 3400.0, '一龄3200 二龄4000 三龄4600'),
      (0, 3800.0, 4500.0, 5000.0, 4700.0, 4200.0, 3700.0, '一龄3800 二龄4500 三龄5000'),
      (0, 3000.0, 3800.0, 4400.0, 4200.0, 3700.0, 3200.0, '一龄3000 二龄3800 三龄4400'),
      (0, 3600.0, 4300.0, 4900.0, 4600.0, 4100.0, 3600.0, '一龄3600 二龄4300 三龄4900'),
      (0, 3400.0, 4100.0, 4700.0, 4500.0, 4000.0, 3500.0, '一龄3400 二龄4100 三龄4700');
  END IF;


  -- ----------------------------------------------------------
  -- 2.8 grass_assetinfo & grass_asset_standardinfo
  -- ----------------------------------------------------------

  -- grass_assetinfo
  IF (SELECT COUNT(*) FROM grass_assetinfo) < 5 THEN
    INSERT INTO grass_assetinfo
      (variety, sex, purpose, number, sum_value, sum_weight, f_date, notes, belong)
    VALUES
      (1, 0, 1, 120, 360000.0, 420000.0, '2025-04-01', 'A区高羊茅资产', 0),
      (2, 0, 1, 98, 294000.0, 343000.0, '2025-04-01', 'B区黑麦草资产', 0),
      (1, 0, 2, 150, 450000.0, 525000.0, '2025-04-01', 'C区早熟禾资产', 0),
      (3, 0, 1, 200, 600000.0, 700000.0, '2025-04-01', 'D区苜蓿资产', 0),
      (2, 0, 2, 110, 330000.0, 385000.0, '2025-04-01', 'E区白三叶资产', 0),
      (1, 0, 1, 85, 255000.0, 297500.0, '2025-04-01', 'F区红三叶资产', 0);
  END IF;

  -- grass_asset_standardinfo
  IF (SELECT COUNT(*) FROM grass_asset_standardinfo) < 5 THEN
    INSERT INTO grass_asset_standardinfo
      (variety, sex, purpose, unit_price, rank_0, rank_1, rank_2, rank_3, rank_9, f_staff, f_date, notes, belong)
    VALUES
      (1, 0, 1, 3000.0, 3500.0, 3200.0, 2800.0, 2500.0, 2000.0, 'system', '2025-04-01', '高羊茅等级标准', 0),
      (2, 0, 1, 3000.0, 3600.0, 3300.0, 2900.0, 2600.0, 2100.0, 'system', '2025-04-01', '黑麦草等级标准', 0),
      (1, 0, 2, 3000.0, 3700.0, 3400.0, 3000.0, 2700.0, 2200.0, 'system', '2025-04-01', '早熟禾等级标准', 0),
      (3, 0, 1, 3000.0, 3800.0, 3500.0, 3100.0, 2800.0, 2300.0, 'system', '2025-04-01', '苜蓿等级标准', 0),
      (2, 0, 2, 3000.0, 3400.0, 3100.0, 2700.0, 2400.0, 1900.0, 'system', '2025-04-01', '白三叶等级标准', 0),
      (1, 0, 1, 3000.0, 3300.0, 3000.0, 2600.0, 2300.0, 1800.0, 'system', '2025-04-01', '红三叶等级标准', 0);
  END IF;


  -- ----------------------------------------------------------
  -- 2.9 w_information_immunizationMessageinfo
  -- ----------------------------------------------------------

  IF (SELECT COUNT(*) FROM w_information_immunizationMessageinfo) < 5 THEN
    INSERT INTO w_information_immunizationMessageinfo
      (basic_id, ele_num, pre_num, sex, variety, mon_age, house, hurdle_name, vaccine_id,
       birth, imm_date, distance_date, dead_date, state, f_staff, f_date, note, belong)
    VALUES
      (101, 'EL001', 'PR001', 1, 1, 6.0, 'A区种植棚', '1号围栏', 1, '2024-10-01', '2025-04-01', '2025-07-01', NULL, 1, 'system', '2025-04-01', '首次免疫，状态良好', 0),
      (102, 'EL002', 'PR002', 0, 2, 8.0, 'B区种植棚', '2号围栏', 2, '2024-08-01', '2025-04-03', '2025-07-03', NULL, 1, 'system', '2025-04-03', '二次免疫，抗体合格', 0),
      (103, 'EL003', 'PR003', 1, 1, 4.0, 'C区育苗棚', '3号围栏', 1, '2024-12-01', '2025-04-05', '2025-07-05', NULL, 1, 'system', '2025-04-05', '幼苗期免疫，需观察', 0),
      (104, 'EL004', 'PR004', 0, 3, 10.0, 'D区生产棚', '4号围栏', 3, '2024-06-01', '2025-04-08', '2025-07-08', NULL, 1, 'system', '2025-04-08', '成年期加强免疫', 0),
      (105, 'EL005', 'PR005', 1, 2, 5.0, 'E区暂存区', '5号围栏', 2, '2024-11-01', '2025-04-10', '2025-07-10', NULL, 1, 'system', '2025-04-10', '常规免疫程序', 0),
      (106, 'EL006', 'PR006', 0, 1, 7.0, 'F区收割区', '6号围栏', 1, '2024-09-01', '2025-04-12', '2025-07-12', NULL, 1, 'system', '2025-04-12', '免疫后无明显反应', 0);
  END IF;

END$$

DELIMITER ;

-- Execute the data-filling procedure
CALL agroguard_fill_empty_tables();

-- Clean up
DROP PROCEDURE IF EXISTS agroguard_fill_empty_tables;

-- Re-enable checks
SET FOREIGN_KEY_CHECKS = 1;
SET UNIQUE_CHECKS = 1;

-- ============================================================
-- END OF SCRIPT
-- ============================================================
