#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 supply_commodityinfo explain 字段双重编码乱码（完整版）
原理：原始 UTF-8 字节被 cp1252/latin1 解码后再 UTF-8 编码
修复：使用 cp1252 + latin1 混合编码还原原始字节，再 UTF-8 解码
"""
import pymysql
import re

# cp1252 中 Windows 特有的字符映射（解码用）
# 注意：Python 的 cp1252 decoder 在 Linux 上对 0x81/0x8D/0x8F/0x90/0x9D 返回控制字符
# 但 cp1252 encoder 对这些 Unicode 控制字符不支持，所以需要用 latin1 编码

def mixed_encode(text):
    """尝试用 cp1252 编码，对失败的字符用 latin1 编码"""
    result = []
    for ch in text:
        code = ord(ch)
        if code <= 0x7F:
            # ASCII，直接编码
            result.append(code)
        elif 0x80 <= code <= 0x9F:
            # C1 控制字符，使用 latin1 编码（0x80-0x9F 映射到自身）
            result.append(code)
        elif 0xA0 <= code <= 0xFF:
            # Latin-1 补充字符，cp1252 和 latin1 编码相同
            result.append(code)
        else:
            # U+0100 以上字符，需要使用 cp1252 的反向映射
            # 常见 cp1252 扩展字符的编码
            cp1252_map = {
                0x0152: 0x8C,  # Œ
                0x0153: 0x9C,  # œ
                0x0160: 0x8A,  # Š
                0x0161: 0x9A,  # š
                0x017D: 0x8E,  # Ž
                0x017E: 0x9E,  # ž
                0x0178: 0x9F,  # Ÿ
                0x0192: 0x83,  # ƒ
                0x02C6: 0x88,  # ˆ
                0x02DC: 0x98,  # ˜
                0x2013: 0x96,  # –
                0x2014: 0x97,  # —
                0x2018: 0x91,  # '
                0x2019: 0x92,  # '
                0x201A: 0x82,  # ‚
                0x201C: 0x93,  # "
                0x201D: 0x94,  # "
                0x201E: 0x84,  # „
                0x2020: 0x86,  # †
                0x2021: 0x87,  # ‡
                0x2022: 0x95,  # •
                0x2026: 0x85,  # …
                0x2030: 0x89,  # ‰
                0x2039: 0x8B,  # ‹
                0x203A: 0x9B,  # ›
                0x20AC: 0x80,  # €
                0x2122: 0x99,  # ™
            }
            if code in cp1252_map:
                result.append(cp1252_map[code])
            else:
                # 无法映射的字符，跳过
                return None
    return bytes(result)

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
    
    # 如果已经是正常中文（包含中文字符），跳过
    if re.search(r'[\u4e00-\u9fff]', explain_val):
        skip_count += 1
        continue
    
    try:
        original_bytes = mixed_encode(explain_val)
        if original_bytes is None:
            skip_count += 1
            continue
        fixed = original_bytes.decode('utf-8')
        
        # 验证修复结果：应包含中文字符
        if re.search(r'[\u4e00-\u9fff]', fixed) and fixed != explain_val:
            cursor.execute('UPDATE supply_commodityinfo SET `explain` = %s WHERE id = %s', (fixed, id_))
            fixed_count += 1
            print(f'Fixed id={id_}: {explain_val!r} -> {fixed!r}')
        else:
            skip_count += 1
    except Exception as e:
        skip_count += 1
        print(f'Skip id={id_}: {explain_val!r} (error: {e})')

conn.commit()
print(f'\nTotal fixed: {fixed_count} records, skipped: {skip_count} records')
conn.close()
