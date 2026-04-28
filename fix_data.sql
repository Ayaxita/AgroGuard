-- ============================================
-- AgroGuard 数据库数据清洗与修复脚本
-- 执行时间: 2026-04-28
-- ============================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- 1. 修复 supply_commodityinfo 疾病名称 → 防治剂名称
UPDATE supply_commodityinfo SET cname = '草地病毒病防治剂' WHERE id = 9;
UPDATE supply_commodityinfo SET cname = '草地流行病毒病防治剂' WHERE id = 12;
UPDATE supply_commodityinfo SET cname = '草地腐根病防治剂' WHERE id = 19;
UPDATE supply_commodityinfo SET cname = '草地腐根病防治剂' WHERE id = 28;
UPDATE supply_commodityinfo SET cname = '草地痘疮病防治剂' WHERE id = 25;
UPDATE supply_commodityinfo SET cname = '草地痘疮病活药防治剂' WHERE id = 30;

-- 2. 修复 explain 字段 UTF-8 双重编码乱码
-- 先修复已知的乱码记录（通过 latin1 中转解码）
UPDATE supply_commodityinfo SET `explain` = '预防草/草株/草地/幼草/母草/种草草地炭疽病。皮下注射1ml，注后14天产生病害预防力，病害预防期一年' WHERE id = 1;
UPDATE supply_commodityinfo SET `explain` = '防草地枯萎病病' WHERE id = 2;
UPDATE supply_commodityinfo SET `explain` = '预防断乳幼苗/新株大肠杆菌病的生物制品' WHERE id = 3;
UPDATE supply_commodityinfo SET `explain` = '其有助于避免细胞破裂、清洗伤口、改善口臭等功效' WHERE id = 4;
UPDATE supply_commodityinfo SET `explain` = '病虫害防治针剂' WHERE id = 8;
UPDATE supply_commodityinfo SET `explain` = '预防草地斑点病' WHERE id = 9;
UPDATE supply_commodityinfo SET `explain` = '抗菌消炎' WHERE id = 10;
UPDATE supply_commodityinfo SET `explain` = '预防快疫，猝狙，痢疾，和草地毒枯病' WHERE id = 11;
UPDATE supply_commodityinfo SET `explain` = '预防草地流行病毒病，用于病毒病高发期预防' WHERE id = 12;
UPDATE supply_commodityinfo SET `explain` = '调解肠胃' WHERE id = 23;
UPDATE supply_commodityinfo SET `explain` = '四川省共创动物营养保健品有限公司' WHERE id = 24;
UPDATE supply_commodityinfo SET `explain` = '维生素类药，用于消化障碍，癞皮病，口腔炎等' WHERE id = 26;
UPDATE supply_commodityinfo SET `explain` = '预防草地腐根病，改善根系健康' WHERE id = 28;
UPDATE supply_commodityinfo SET `explain` = '哈尔滨种精生物科技有限公司' WHERE id = 31;
UPDATE supply_commodityinfo SET `explain` = '治疗细菌性疾病，呼吸道感染，青热疏风，利咽解毒' WHERE id = 32;
UPDATE supply_commodityinfo SET `explain` = '上海明磊帮森生物科技（登封）有限公司' WHERE id = 33;

-- 3. 补充缺失的 explain（确保每个防治剂都有对应描述）
UPDATE supply_commodityinfo SET `explain` = '预防草地枯萎病，适用于草地成株及幼苗' WHERE id = 7 AND (`explain` IS NULL OR `explain` = '');
UPDATE supply_commodityinfo SET `explain` = '预防草地斑点病，用于草地生长期病害防治' WHERE id = 9 AND (`explain` IS NULL OR `explain` = '');
UPDATE supply_commodityinfo SET `explain` = '防治草地流行病毒病，用于病毒病高发期预防' WHERE id = 12 AND (`explain` IS NULL OR `explain` = '');
UPDATE supply_commodityinfo SET `explain` = '防治草地腐根病，改善根系健康' WHERE id IN (19, 28) AND (`explain` IS NULL OR `explain` = '');
UPDATE supply_commodityinfo SET `explain` = '预防草地痘疮病，用于春季病害防治' WHERE id IN (25, 30) AND (`explain` IS NULL OR `explain` = '');
UPDATE supply_commodityinfo SET `explain` = '预防草地枯萎病幼苗期感染' WHERE id = 7 AND (`explain` IS NULL OR `explain` = '');
UPDATE supply_commodityinfo SET `explain` = '草地专用杀虫剂，防治草地常见虫害' WHERE id = 8 AND (`explain` IS NULL OR `explain` = '');
UPDATE supply_commodityinfo SET `explain` = '160万单位草地细菌性萎蔫病药剂钠，抗菌消炎' WHERE id = 10 AND (`explain` IS NULL OR `explain` = '');
UPDATE supply_commodityinfo SET `explain` = '草地多效防治剂，预防多种草地病害' WHERE id = 11 AND (`explain` IS NULL OR `explain` = '');
UPDATE supply_commodityinfo SET `explain` = '草地白粉病专用药，防治白粉病' WHERE id = 13 AND (`explain` IS NULL OR `explain` = '');
UPDATE supply_commodityinfo SET `explain` = '草地抗炎剂，用于草地炎症治疗' WHERE id = 14 AND (`explain` IS NULL OR `explain` = '');
UPDATE supply_commodityinfo SET `explain` = '草地止痢剂，用于治疗草地腹泻' WHERE id = 16 AND (`explain` IS NULL OR `explain` = '');
UPDATE supply_commodityinfo SET `explain` = '安痛定，用于草地疼痛缓解' WHERE id = 17 AND (`explain` IS NULL OR `explain` = '');
UPDATE supply_commodityinfo SET `explain` = '草地解表剂，用于草地感冒发热' WHERE id = 18 AND (`explain` IS NULL OR `explain` = '');
UPDATE supply_commodityinfo SET `explain` = '草地腐根病防治剂，防治腐根病' WHERE id = 19 AND (`explain` IS NULL OR `explain` = '');
UPDATE supply_commodityinfo SET `explain` = '草地止痢剂注射液，用于治疗草地腹泻' WHERE id = 20 AND (`explain` IS NULL OR `explain` = '');
UPDATE supply_commodityinfo SET `explain` = '草地清热剂注射液，用于清热解毒' WHERE id = 21 AND (`explain` IS NULL OR `explain` = '');
UPDATE supply_commodityinfo SET `explain` = '草地病毒二价苗，预防草地病毒病' WHERE id = 22 AND (`explain` IS NULL OR `explain` = '');
UPDATE supply_commodityinfo SET `explain` = '草地胃肠康，调解肠胃功能' WHERE id = 23 AND (`explain` IS NULL OR `explain` = '');
UPDATE supply_commodityinfo SET `explain` = '草地金维素，维生素类营养补充剂' WHERE id = 24 AND (`explain` IS NULL OR `explain` = '');
UPDATE supply_commodityinfo SET `explain` = '草地痘疮病防治剂，预防草地痘疮病' WHERE id = 25 AND (`explain` IS NULL OR `explain` = '');
UPDATE supply_commodityinfo SET `explain` = '草地沃力健，维生素类营养补充剂' WHERE id = 26 AND (`explain` IS NULL OR `explain` = '');
UPDATE supply_commodityinfo SET `explain` = '草地复合维生素B，补充维生素B族' WHERE id = 27 AND (`explain` IS NULL OR `explain` = '');
UPDATE supply_commodityinfo SET `explain` = '草地腐根病防治剂，防治腐根病' WHERE id = 28 AND (`explain` IS NULL OR `explain` = '');
UPDATE supply_commodityinfo SET `explain` = '草地微量元素肥（生长康），补充微量元素' WHERE id = 29 AND (`explain` IS NULL OR `explain` = '');
UPDATE supply_commodityinfo SET `explain` = '草地痘疮病活药防治剂，预防草地痘疮病' WHERE id = 30 AND (`explain` IS NULL OR `explain` = '');
UPDATE supply_commodityinfo SET `explain` = '草地专用活菌剂，改善土壤菌群' WHERE id = 31 AND (`explain` IS NULL OR `explain` = '');
UPDATE supply_commodityinfo SET `explain` = '草地第一品牌，治疗细菌性疾病' WHERE id = 32 AND (`explain` IS NULL OR `explain` = '');
UPDATE supply_commodityinfo SET `explain` = '草地鱼腥草，清热解毒' WHERE id = 33 AND (`explain` IS NULL OR `explain` = '');

-- 4. 回填预警信息 note 字段：根据 vaccine_id 关联 supply_commodityinfo.explain
UPDATE w_information_immunizationMessageinfo w
JOIN supply_commodityinfo s ON w.vaccine_id = s.id
SET w.note = s.explain
WHERE w.note IS NULL OR w.note = '';

-- 5. 回填防护措施 effect 字段：根据 drug_id 关联 supply_commodityinfo.explain
UPDATE d_plantcare_protectioninfo p
JOIN supply_commodityinfo s ON p.drug_id = s.id
SET p.effect = s.explain
WHERE p.effect LIKE 'Test_effect_%' OR p.effect IS NULL OR p.effect = '';

-- 6. 回填疾病信息表中的 effect 相关字段
UPDATE d_plantcare_diseaseinfo d
JOIN supply_commodityinfo s ON d.drug_id = s.id
SET d.drug_type = s.cname
WHERE d.drug_type IS NULL OR d.drug_type = '';

SET FOREIGN_KEY_CHECKS = 1;
