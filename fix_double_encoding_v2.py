#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 supply_commodityinfo explain 字段双重编码乱码
原理：UTF-8字节被错误地当作latin1/cp1252解码，然后再以UTF-8存储
修复：将当前字符串用 cp1252 编码还原原始 UTF-8 字节，再用 utf-8 解码
"""
import pymysql
import re

conn = pymysql.connect(
    host='localhost',
    port=5010,
    user='root',
    password='meadow123',
    database='meadow_test',
    charset='utf8mb4'
)
cursor = conn.cursor()

# 获取所有 explain 非空记录
cursor.execute('SELECT id, cname, `explain` FROM supply_commodityinfo WHERE `explain` IS NOT NULL AND `explain` != ""')
rows = cursor.fetchall()

fixed_count = 0
skip_count = 0
for row in rows:
    id_, cname, explain_val = row
    original = explain_val
    
    # 如果 explain 已经是正常中文（包含中文字符），跳过
    # 使用正则匹配中文字符范围
    if re.search(r'[\u4e00-\u9fff]', explain_val):
        skip_count += 1
        continue
    
    try:
        # 尝试用 cp1252 编码还原原始 UTF-8 字节，再用 utf-8 解码
        original_bytes = explain_val.encode('cp1252')
        fixed = original_bytes.decode('utf-8')
        
        # 如果修复后包含中文字符，说明修复成功
        if re.search(r'[\u4e00-\u9fff]', fixed) and fixed != explain_val:
            cursor.execute('UPDATE supply_commodityinfo SET `explain` = %s WHERE id = %s', (fixed, id_))
            fixed_count += 1
            print(f'Fixed id={id_}: {explain_val!r} -> {fixed!r}')
        else:
            skip_count += 1
    except (UnicodeEncodeError, UnicodeDecodeError) as e:
        skip_count += 1
        print(f'Skip id={id_}: {explain_val!r} (error: {e})')

conn.commit()
print(f'\nTotal fixed: {fixed_count} records, skipped: {skip_count} records')
conn.close()
