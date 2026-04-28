-- 修复 supply_commodityinfo explain 字段双重编码乱码
SET NAMES utf8mb4;

-- 针对所有 explain 包含乱码特征字节（UTF-8字节被误读为latin1）的记录进行解码修复
UPDATE supply_commodityinfo
SET `explain` = CONVERT(CAST(CONVERT(`explain` USING latin1) AS BINARY) USING utf8mb4)
WHERE `explain` IS NOT NULL
  AND `explain` != ''
  AND `explain` LIKE '%Ã%';
