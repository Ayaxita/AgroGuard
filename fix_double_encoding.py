#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 supply_commodityinfo explain 字段双重编码乱码
原理：UTF-8字节被错误地当作latin1解码，然后再以UTF-8存储
修复：将当前字符串encode为latin1（还原原始UTF-8字节），再decode为utf-8
"""
import pymysql

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
for row in rows:
    id_, cname, explain_val = row
    try:
        # 尝试双重解码修复
        # 当前 explain_val 是 Unicode 字符串，它实际上是 UTF-8 字节被当作 latin1 解码后的结果
        # encode('latin1') 还原原始 UTF-8 字节，然后 decode('utf-8') 得到正确中文
        fixed = explain_val.encode('latin1').decode('utf-8')
        if fixed != explain_val:
            cursor.execute('UPDATE supply_commodityinfo SET `explain` = %s WHERE id = %s', (fixed, id_))
            fixed_count += 1
            print(f'Fixed id={id_}: {explain_val!r} -> {fixed!r}')
    except (UnicodeEncodeError, UnicodeDecodeError) as e:
        # 无法修复的记录，跳过
        print(f'Skip id={id_}: {explain_val!r} (error: {e})')

conn.commit()
print(f'\nTotal fixed: {fixed_count} records')
conn.close()
