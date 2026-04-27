from datetime import datetime, timedelta, date
import random
import os
import traceback
import json
import calendar

from flask import Blueprint, render_template, request, make_response, Response, redirect, url_for, session, jsonify, \
    send_file
from sqlalchemy import desc, and_, or_, not_, text, func, asc
import pandas as pd

from ..modelsReverse import *
from ..utils.AlchemyEncoder import AlchemyEncoder
from decimal import Decimal
import itertools
from io import BytesIO

analysis = Blueprint('analysis', __name__)
# today = datetime(2025, 1, 2).date()

@analysis.route('/analysis/standardinfo', methods=['POST'])#  获取草资产评价标准
def get_standardinfo():

    # pageNum = int(request.json.get('pageNum'))
    # pageNum = 1
    # # pageNum = int(request.form.get('pageNum'))
    # # pageSize = int(request.json.get('pageSize'))
    # pageSize = 12
    # 分页不用了，只返回数据
    conditions = []
    search_params = {
        'variety': GrassAssetStandardinfo.variety,
        'sex': GrassAssetStandardinfo.sex,
        'purpose': GrassAssetStandardinfo.purpose,
        'unit_price': GrassAssetStandardinfo.unit_price,
        'f_date': GrassAssetStandardinfo.f_date,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            conditions.append(column == value)

        # 使用 and_() 组合条件
    if conditions:
        query = GrassAssetStandardinfo.query.filter(and_(*conditions))
    else:
        query = GrassAssetStandardinfo.query  # 如果没有条件，查询所有

    # 筛选出没有被移除的草(状态-1)和没有枯萎的草(状态0)
    # 并且根据id降序排列

    # 并且根据id降序排列

    query = query.filter(GrassAssetStandardinfo.belong == 0)
    infos = query.order_by(asc(GrassAssetStandardinfo.id)).paginate(error_out=False)
    # total = query.count()

    list = []
    for info in infos:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        data = json.loads(data)
        list.append(data)
    result = {
        "code": 200,
        "data": {
            "list": list,
            # "pageNum": pageNum,
            # "pageSize": pageSize,
            # "total": total
        },
        "msg": '成功'
    }
    return jsonify(result)

@analysis.route('/analysis/standardinfo/add', methods=['POST'])#  新增草资产评价标准
def add_standardinfo():
    data = request.get_json()

    ctime = datetime.now()
    data['belong'] = 0
    data['f_date'] = ctime


    data_info= GrassAssetStandardinfo()

    for key, value in data.items():#将data字典里的数据添加到实例对象中
        setattr(data_info, key, value)
    try:
        db.session.add(data_info)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        result = {
            "code": 500,
            "msg": f'添加失败 {str(e)}'
        }
        return jsonify(result)
    result = {
        "code": 200,
        "msg": '添加成功'
    }
    return jsonify(result)

@analysis.route('/analysis/standardinfo/edit', methods=['POST'])#  编辑草资产评价标准
def edit_standardinfo():
    data = request.get_json()
    print("--data-->", data)
    id = data['id']

    # BasicBasicinfo.query.filter_by(ele_id = ele_id,pre_id = pre_id).update(data)
    try:
        # 更新
        GrassAssetStandardinfo.query.filter_by(id=id).update(data)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        result = {
            "code": 500,
            "msg": f'修改失败 {str(e)}'
        }
        return jsonify(result)
    result = {
        "code": 200,
        "msg": '修改成功'
    }
    return jsonify(result)


@analysis.route('/analysis/grass_assetinfo', methods=['POST'])#  获取草资产表
def get_grass_assetinfo():

    pageNum = int(request.json.get('pageNum'))
    # pageNum = int(request.form.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        'variety': GrassAssetinfo.variety,
        'sex': GrassAssetinfo.sex,
        'purpose': GrassAssetinfo.purpose,
        # 'unit_price': GrassAssetStandardinfo.unit_price,
        'f_date': GrassAssetStandardinfo.f_date,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        print(value)
        if value is not None:  # 检查值不为 None
            # conditions.append(column == value)
            if isinstance(value, list) and len(value) == 2:  # 处理日期范围
                conditions.append(column.between(value[0], value[1]))
            else:  # 单个值，使用 == 比较
                conditions.append(column == value)

        # 使用 and_() 组合条件
    if conditions:
        query = GrassAssetinfo.query.filter(and_(*conditions))
    else:
        query = GrassAssetinfo.query  # 如果没有条件，查询所有

    # 筛选出没有被移除的草(状态-1)和没有枯萎的草(状态0)
    # 并且根据id降序排列

    # 并且根据id降序排列

    query = query.filter(GrassAssetinfo.belong == 0)
    # infos = query.order_by(desc(GrassAssetinfo.id)).paginate(error_out=False)
    infos = query.order_by(desc(GrassAssetinfo.id)).paginate(page=pageNum, per_page=pageSize,
                                                                  error_out=False)
    total = query.count()

    list1 = []
    for info in infos:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        data = json.loads(data)
        list1.append(data)
    result = {
        "code": 200,
        "data": {
            "list": list1,
            "pageNum": pageNum,
            "pageSize": pageSize,
            "total": total
        },
        "msg": '成功'
    }
    return jsonify(result)

@analysis.route('/analysis/grass_assetinfo/update', methods=['POST'])#  手动更新草库存资产表
def update_grass_assetinfo():
    """更新草资产统计信息路由"""
    try:
        # 获取当前日期
        today = datetime.now().date()
        # today = datetime(2025, 1, 1).date()

        # -------------------------- 步骤1：检查现有记录 --------------------------
        existing_records = db.session.query(GrassAssetinfo).filter(
            GrassAssetinfo.f_date == today
        ).all()

        # 转换为字典方便查找 {(品种, 用途, 性别): 记录}
        existing_map = {
            (rec.variety, rec.purpose, rec.sex): rec
            for rec in existing_records
        }
        print(f'existing_map{existing_map}')

        # -------------------------- 步骤2：执行计算逻辑 --------------------------
        # stats = _calculate_asset_stats()
        stats, missing_weight_data = _calculate_asset_stats()  # 修改返回值为统计数据和缺失数据


        # -------------------------- 步骤3：准备批量操作 --------------------------
        to_update = []
        to_insert = []

        for key, values in stats.items():
            composite_key = (key[0], key[1], key[2])

            if composite_key in existing_map:
                # 更新现有记录
                to_update.append({
                    'id': existing_map[composite_key].id,
                    'sum_value': values['sum_value'],
                    'sum_weight': values['sum_weight'],
                    'number': values['count']
                })
            else:
                # 插入新记录
                to_insert.append({
                    'variety': key[0],
                    'purpose': key[1],
                    'sex': key[2],
                    'sum_value': values['sum_value'],
                    'sum_weight': values['sum_weight'],
                    'number': values['count'],
                    'f_date': today,
                    'belong': 0
                })

        # -------------------------- 执行数据库操作 --------------------------
        if to_update:
            db.session.bulk_update_mappings(GrassAssetinfo, to_update)
            print(f"更新 {len(to_update)} 条记录")

        if to_insert:
            db.session.bulk_insert_mappings(GrassAssetinfo, to_insert)
            print(f"插入 {len(to_insert)} 条新记录")

        db.session.commit()

        return jsonify({
            'code': '200',
            'msg': '更新草库存资产成功'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': '500',
            'msg': f'处理失败: {str(e)}'
        }), 500


def _calculate_asset_stats():
    """核心计算函数"""
    stats = {}
    log_filename = 'missing_weight.log'
    missing_weight_data = []  # 用于存储缺失体重记录

    # -------------------------- 第一部分：处理非人工养护幼苗记录（除了purpose=2的） --------------------------
    # 子查询获取每个basic_id的最新体重记录日期
    # 子查询 1：找到每个 basic_id 对应的最大日期
    latest_date_subquery = (
        db.session.query(
            BasicFieldconditioninfo.basic_id,
            func.max(BasicFieldconditioninfo.date).label('max_date')
        )
            .group_by(BasicFieldconditioninfo.basic_id)
            .subquery()
    )

    # 子查询 2：在每个 basic_id 对应的最大日期下，找到 id 最大的记录
    latest_condition_subquery = (
        db.session.query(
            BasicFieldconditioninfo.basic_id,
            func.max(BasicFieldconditioninfo.id).label('max_id')
        )
            .join(
            latest_date_subquery,
            and_(
                BasicFieldconditioninfo.basic_id == latest_date_subquery.c.basic_id,
                BasicFieldconditioninfo.date == latest_date_subquery.c.max_date
            )
        )
            .group_by(BasicFieldconditioninfo.basic_id)
            .subquery()
    )

    # 主查询：以BasicBasicinfo为主表，左连接获取最新体重
    normal_query = (
        db.session.query(
            BasicBasicinfo.id.label('basic_id'),
            BasicBasicinfo.ele_num,
            BasicBasicinfo.house_name,
            BasicBasicinfo.hurdle_name,
            BasicBasicinfo.state,  # 添加这行
            BasicBasicinfo.variety,
            BasicBasicinfo.sex,
            BasicBasicinfo.purpose,
            BasicBasicinfo.mon_age,
            BasicBasicinfo.rank,
            func.coalesce(BasicFieldconditioninfo.weight, 0).label('weight'),
            BasicFieldconditioninfo.basic_id.is_(None).label('has_no_weight')
        )
            .outerjoin(
            latest_condition_subquery,
            BasicBasicinfo.id == latest_condition_subquery.c.basic_id
        )
            .outerjoin(
            BasicFieldconditioninfo,
            and_(
                BasicFieldconditioninfo.id == latest_condition_subquery.c.max_id
            )
        )
            .filter(
                    or_(
                        (BasicBasicinfo.state == 1) & (BasicBasicinfo.purpose != 2),
                        (BasicBasicinfo.state == -1)
                    )# 排除purpose=2的记录，由第二部分处理

            # BasicBasicinfo.birth <= today  # 新增的过滤条件
        )
            .distinct()  # 添加去重操作
    )

    page_size = 1000
    with open(log_filename, 'w') as log_file:
        for page in itertools.count(start=0):
            records = normal_query.offset(page * page_size).limit(page_size).all()
            if not records:
                break

            for record in records:
                # 记录无体重信息的basic_id
                # 收集缺失体重信息
                if record.has_no_weight:
                    missing_weight_data.append({
                        'basic_id': record.basic_id,
                        '耳号': record.ele_num,  # 添加中文列名
                        '所属草地区块': record.house_name,
                        '所属栏位': record.hurdle_name
                    })

                    log_file.write(f"{record.basic_id,record.ele_num,record.house_name,record.hurdle_name}\n")

                else:
                    # 更新BasicBasicinfo的weight字段
                    basic_info = db.session.query(BasicBasicinfo).filter(
                        BasicBasicinfo.id == record.basic_id
                    ).first()
                    if basic_info:
                        basic_info.weight = record.weight
                        db.session.commit()  # 提交更新

                # -------------------------- 用途调整逻辑 --------------------------
                # 处理state=-1的情况：强制设置purpose=1
                if record.state == -1:
                    adjusted_purpose = 1
                else:

                    adjusted_purpose = record.purpose
                    # 原用途为5、6转为草种（0），8转为育成（1）
                    if record.purpose in (5, 6):
                        adjusted_purpose = 0
                    elif record.purpose == 8:
                        adjusted_purpose = 1

                # -------------------------- 价值计算 --------------------------
                standard = _get_standard_info(
                    variety=record.variety,
                    sex=record.sex,
                    purpose=adjusted_purpose
                )
                if not standard:
                    continue

                # 计算单只价值（根据是否有体重）
                if record.has_no_weight:
                    value = Decimal(0)  # 无体重记录，价值为0
                    effective_weight = 0  # 不计入重量总和
                else:
                    value = _calculate_value_with_weight(
                        weight=record.weight,
                        standard=standard,
                        rank=record.rank
                    )
                    effective_weight = record.weight

                # 更新统计信息
                _update_stats(
                    stats_dict=stats,
                    variety=record.variety,
                    purpose=adjusted_purpose,
                    sex=record.sex,
                    value=value,
                    weight=effective_weight  # 无体重记录时传0
                )

    # -------------------------- 处理人工养护幼苗记录 (purpose=2) --------------------------
    special_query = db.session.query(
        BasicBasicinfo.variety,
        BasicBasicinfo.sex,
        BasicBasicinfo.mon_age,
        BasicBasicinfo.rank
    ).filter(
        BasicBasicinfo.purpose == 2,
        BasicBasicinfo.state == 1,
        # BasicBasicinfo.birth <= today  # 新增的过滤条件
    )

    for page in range(0, 100000):
        records = special_query.offset(page * page_size).limit(page_size).all()
        if not records:
            break

        for record in records:
            # 调整用途
            adjusted_purpose = 3 if record.mon_age > 1 else 2

            # 获取标准
            standard = _get_standard_info(record.variety, record.sex, adjusted_purpose)
            if not standard:
                continue

            # 计算价值
            value = _calculate_value_without_weight(standard, record.rank)

            # 更新统计
            _update_stats(
                stats,
                variety=record.variety,
                purpose=adjusted_purpose,
                sex=record.sex,
                value=value,
                weight=0  # 不计入重量
            )

    # return stats
    return stats, missing_weight_data  # 返回统计数据和缺失数据


def _adjust_purpose(original_purpose, mon_age):
    """调整用途逻辑"""
    # 规则1：原用途为2且月龄>1时调整为3
    if original_purpose == 2 and mon_age > 1:
        return 3

    # 规则2：特殊用途转换
    if original_purpose in (5, 6):
        return 0
    elif original_purpose == 8:
        return 1

    return original_purpose


def _get_standard_info(variety, sex, purpose):
    """获取最新标准信息"""
    return db.session.query(GrassAssetStandardinfo).filter(
        GrassAssetStandardinfo.variety == variety,
        GrassAssetStandardinfo.sex == sex,
        GrassAssetStandardinfo.purpose == purpose
    ).order_by(
        GrassAssetStandardinfo.f_date.desc()
    ).first()


def _calculate_value_with_weight(weight, standard, rank):
    """带体重的价值计算"""
    try:
        rank_value = Decimal(getattr(standard, f'rank_{rank}', '1.0'))
        return Decimal(weight) * 2 * Decimal(standard.unit_price) * rank_value
    except:
        return Decimal(0)


def _calculate_value_without_weight(standard, rank):
    """不带体重的价值计算"""
    try:
        rank_value = Decimal(getattr(standard, f'rank_{rank}', '1.0'))
        return Decimal(standard.unit_price) * rank_value
    except:
        return Decimal(0)


def _update_stats(stats_dict, variety, purpose, sex, value, weight):
    """更新统计字典"""
    key = (variety, purpose, sex)
    if key not in stats_dict:
        stats_dict[key] = {
            'sum_value': Decimal(0),
            'sum_weight': Decimal(0),
            'count': 0
        }

    stats_dict[key]['sum_value'] += value
    stats_dict[key]['sum_weight'] += Decimal(weight)
    stats_dict[key]['count'] += 1




@analysis.route('/analysis/grass_assetinfo/commit_update', methods=['POST'])# 已交完销售记录之后手动更新草库存资产表
def commit_update_asset():

    """提交销售后更新资产表路由"""
    try:
            data = request.get_json()
            print(data)

            update_time_str = data[0].get('sales_date')
            update_date = datetime.strptime(update_time_str, '%Y-%m-%d').date()
            print(update_date)


            # [{'sales_date': '2025-03-04', 'sales_order': '1', 'billing_unit': '1', 'unit_price': '11', 'total_price': '1',
            #   'type': 3, 'transportation': '1', 'sales_site': '1', 'name': '1', 'buyer': '1', 'buyer_phone': '1',
            #   'selling_type': 6, 'quarantine_coding': '1', 'age': None, 'medical_leave': 1, 'notes': '1', 'basic_id': 20892},
            #  {'sales_date': '2025-03-04', 'sales_order': '1', 'billing_unit': '1', 'unit_price': '11', 'total_price': '1',
            #   'type': 3, 'transportation': '1', 'sales_site': '1', 'name': '1', 'buyer': '1', 'buyer_phone': '1',
            #   'selling_type': 6, 'quarantine_coding': '1', 'age': None, 'medical_leave': 1, 'notes': '1', 'basic_id': 20891}]
            # for i in data:
            #     basic_id = i.get('basic_id')
            #     print(basic_id)
            basic_ids = [item.get('basic_id') for item in data if item.get('basic_id') is not None]

            print(basic_ids)

            stats, missing_weight_data = Commit_calculate_asset_stats(basic_ids)

            print(stats)

            # -------------------------- 构建更新操作 --------------------------
            to_update = []

            # 遍历每个分类统计结果
            for key, values in stats.items():
                variety, purpose, sex = key
                # 查询需要更新的历史记录
                history_records = db.session.query(GrassAssetinfo).filter(
                    GrassAssetinfo.f_date >= update_date,
                    GrassAssetinfo.variety == variety,
                    GrassAssetinfo.purpose == purpose,
                    GrassAssetinfo.sex == sex
                ).all()

                # 对每条历史记录进行扣减
                for record in history_records:
                    # 计算新值（使用Decimal保证精度）
                    new_sum_value = Decimal(record.sum_value) - values['sum_value']
                    new_sum_weight = Decimal(record.sum_weight) - values['sum_weight']
                    new_number = record.number - values['count']

                    # 有效性检查（数量不能为负）
                    if new_number < 0:
                        raise ValueError(f"品种{variety}-用途{purpose}-性别{sex}的数量出现负数")

                    to_update.append({
                        'id': record.id,
                        'sum_value': float(new_sum_value),  # 根据实际字段类型调整
                        'sum_weight': float(new_sum_weight),
                        'number': new_number
                    })

            # -------------------------- 执行数据库更新 --------------------------
            if to_update:
                db.session.bulk_update_mappings(GrassAssetinfo, to_update)
                print(f"成功更新 {len(to_update)} 条历史资产记录")

            db.session.commit()
            update_select_grass_asset(update_date)
            return jsonify({
                'code': '200',
                'msg': '资产表更新成功',
                'updated_records': len(to_update),
                'missing_weight': len(missing_weight_data)
            }), 200

    except ValueError as ve:
        db.session.rollback()
        return jsonify({'code': '400', 'msg': str(ve)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': '500',
            'msg': f'更新失败: {str(e)}',
            'traceback': traceback.format_exc()#包含回溯信息的字典
        }), 500


def Commit_calculate_asset_stats(basic_ids):
    """核心计算函数"""
    stats = {}
    log_filename = 'commit_missing_weight.log'
    missing_weight_data = []  # 用于存储缺失体重记录

    # -------------------------- 第一部分：处理非人工养护幼苗记录（除了purpose=2的） --------------------------
    # 子查询获取每个basic_id的最新体重记录日期
    latest_condition_subquery = (
        db.session.query(
            BasicFieldconditioninfo.basic_id,
            func.max(BasicFieldconditioninfo.date).label('max_date')
        )
            .filter(BasicFieldconditioninfo.basic_id.in_(basic_ids))
            .group_by(BasicFieldconditioninfo.basic_id)
            .subquery()
    )

    # 主查询：以BasicBasicinfo为主表，左连接获取最新体重
    normal_query = (
        db.session.query(
            BasicBasicinfo.id.label('basic_id'),
            BasicBasicinfo.ele_num,
            BasicBasicinfo.house_name,
            BasicBasicinfo.hurdle_name,
            BasicBasicinfo.state,  # 添加这行
            BasicBasicinfo.variety,
            BasicBasicinfo.sex,
            BasicBasicinfo.purpose,
            BasicBasicinfo.mon_age,
            BasicBasicinfo.rank,
            func.coalesce(BasicFieldconditioninfo.weight, 0).label('weight'),
            BasicFieldconditioninfo.basic_id.is_(None).label('has_no_weight')
        )
            .outerjoin(
            latest_condition_subquery,
            BasicBasicinfo.id == latest_condition_subquery.c.basic_id
        )
            .outerjoin(
            BasicFieldconditioninfo,
            and_(
                BasicFieldconditioninfo.basic_id == latest_condition_subquery.c.basic_id,
                BasicFieldconditioninfo.date == latest_condition_subquery.c.max_date
            )
        )
            .filter(
                    (BasicBasicinfo.id.in_(basic_ids))  # 只查询传入的 basic_id
        )
    )

    page_size = 1000
    with open(log_filename, 'w') as log_file:
        for page in itertools.count(start=0):
            records = normal_query.offset(page * page_size).limit(page_size).all()
            if not records:
                break

            for record in records:
                # 记录无体重信息的basic_id
                # 收集缺失体重信息
                if record.has_no_weight:
                    missing_weight_data.append({
                        'basic_id': record.basic_id,
                        '耳号': record.ele_num,  # 添加中文列名
                        '所属草地区块': record.house_name,
                        '所属栏位': record.hurdle_name
                    })

                    log_file.write(f"{record.basic_id,record.ele_num,record.house_name,record.hurdle_name}\n")

                else:
                    # 更新BasicBasicinfo的weight字段
                    basic_info = db.session.query(BasicBasicinfo).filter(
                        BasicBasicinfo.id == record.basic_id
                    ).first()
                    if basic_info:
                        basic_info.weight = record.weight
                        db.session.commit()  # 提交更新

                # -------------------------- 用途调整逻辑 --------------------------
                # 处理state=-1的情况：强制设置purpose=1
                if record.state == -1:
                    adjusted_purpose = 1
                else:

                    adjusted_purpose = record.purpose
                    # 原用途为5、6转为草种（0），8转为育成（1）
                    if record.purpose in (5, 6):
                        adjusted_purpose = 0
                    elif record.purpose == 8:
                        adjusted_purpose = 1

                # -------------------------- 价值计算 --------------------------
                standard = _get_standard_info(
                    variety=record.variety,
                    sex=record.sex,
                    purpose=adjusted_purpose
                )
                if not standard:
                    continue

                # 计算单只价值（根据是否有体重）
                if record.has_no_weight:
                    value = Decimal(0)  # 无体重记录，价值为0
                    effective_weight = 0  # 不计入重量总和
                else:
                    value = _calculate_value_with_weight(
                        weight=record.weight,
                        standard=standard,
                        rank=record.rank
                    )
                    effective_weight = record.weight

                # 更新统计信息
                _update_stats(
                    stats_dict=stats,
                    variety=record.variety,
                    purpose=adjusted_purpose,
                    sex=record.sex,
                    value=value,
                    weight=effective_weight  # 无体重记录时传0
                )

    # -------------------------- 处理人工养护幼苗记录 (purpose=2) --------------------------
    special_query = db.session.query(
        BasicBasicinfo.variety,
        BasicBasicinfo.sex,
        BasicBasicinfo.mon_age,
        BasicBasicinfo.rank
    ).filter(
        BasicBasicinfo.purpose == 2,
        BasicBasicinfo.state == 1,
        BasicBasicinfo.id.in_(basic_ids)  # 只处理传入的 basic_id 中人工养护幼苗记录
    )

    for page in range(0, 100000):
        records = special_query.offset(page * page_size).limit(page_size).all()
        if not records:
            break

        for record in records:
            # 调整用途
            adjusted_purpose = 3 if record.mon_age > 1 else 2

            # 获取标准
            standard = _get_standard_info(record.variety, record.sex, adjusted_purpose)
            if not standard:
                continue

            # 计算价值
            value = _calculate_value_without_weight(standard, record.rank)

            # 更新统计
            _update_stats(
                stats,
                variety=record.variety,
                purpose=adjusted_purpose,
                sex=record.sex,
                value=value,
                weight=0  # 不计入重量
            )

    # return stats
    return stats, missing_weight_data  # 返回统计数据和缺失数据



def update_select_grass_asset(date):
    try:


        # 查询今日所有的GrassAssetinfo记录
        today_assets = GrassAssetinfo.query.filter(
            db.func.date(GrassAssetinfo.f_date) == date
        ).all()

        # 初始化分析记录字段字典
        analysis_fields = {
            # 初始化hu系列字段
            **{f'hu_{p}_{s}': 0 for p in range(4) for s in range(2)},
            # 初始化xw系列字段
            **{f'xw_{p}_{s}': 0 for p in range(4) for s in range(2)},
            'other': 0
        }

        # 填充数据
        for asset in today_assets:
            # 只处理variety为0或1的有效数据
            if asset.variety not in [0, 1]:
                analysis_fields['other'] += asset.sum_value  # 使用累加而非覆盖
                continue

            # 确定字段前缀
            prefix = 'hu' if asset.variety == 0 else 'xw'

            # 只处理purpose在0-3范围内的有效数据
            if 0 <= asset.purpose <= 3 and asset.sex in [0, 1]:
                field_name = f"{prefix}_{asset.purpose}_{asset.sex}"
                if field_name in analysis_fields:
                    analysis_fields[field_name] = asset.sum_value

        # 查询或创建分析记录
        analysis_record = AnalysisGrassAsset.query.filter_by(
            f_date=date,
            belong=0
        ).first()
        # 更新或新建记录
        if analysis_record:
            # 更新现有记录
            for field, value in analysis_fields.items():
                setattr(analysis_record, field, value)
            analysis_record.update_time = datetime.now()
        else:
            # 创建新记录
            analysis_record = AnalysisGrassAsset(
                f_date=date,
                belong=0,
                # create_time=datetime.now(),
                **analysis_fields
            )
            db.session.add(analysis_record)

        db.session.commit()


        # # 创建新分析记录
        # new_analysis = AnalysisGrassAsset(
        #     f_date=today,
        #     belong=0,
        #     **analysis_fields
        # )
        #
        # # 添加到数据库并提交
        # db.session.add(new_analysis)
        # db.session.commit()

        return jsonify({
            'code': 200,
            'msg': '更新成功',
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'msg': f'更新失败: {str(e)}'
        })




@analysis.route('/analysis/daily_income', methods=['POST'])#  获取日收入报表
def get_daily_income():

        pageNum = int(request.json.get('pageNum'))
        # pageNum = int(request.form.get('pageNum'))
        pageSize = int(request.json.get('pageSize'))

        conditions = []
        search_params = {

            'f_date': AnalysisDailyIncome.f_date,
        }
        for param, column in search_params.items():
            value = request.json.get(param)
            print(value)
            if value is not None:  # 检查值不为 None
                # conditions.append(column == value)
                if isinstance(value, list) and len(value) == 2:  # 处理日期范围
                    conditions.append(column.between(value[0], value[1]))
                else:  # 单个值，使用 == 比较
                    conditions.append(column == value)
            # 使用 and_() 组合条件
        if conditions:
            query = AnalysisDailyIncome.query.filter(and_(*conditions))
        else:
            query = AnalysisDailyIncome.query  # 如果没有条件，查询所有

        # 筛选出没有被移除的草(状态-1)和没有枯萎的草(状态0)
        # 并且根据id降序排列

        # 并且根据id降序排列

        query = query.filter(AnalysisDailyIncome.belong == 0)
        # infos = query.order_by(desc(AnalysisDailyIncome.id)).paginate(error_out=False)
        infos = query.order_by(desc(AnalysisDailyIncome.id)).paginate(page=pageNum, per_page=pageSize,
                                                                     error_out=False)
        total = query.count()

        list1 = []
        for info in infos:
            data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
            data = json.loads(data)
            list1.append(data)
        result = {
            "code": 200,
            "data": {
                "list": list1,
                "pageNum": pageNum,
                "pageSize": pageSize,
                "total": total
            },
            "msg": '成功'
        }
        return jsonify(result)

@analysis.route('/analysis/daily_income/export', methods=['POST'])
def export_daily_income():
    try:
        selected_ids = request.get_json()
        _dict = {
            1: "是",
            0: "否"
        }

        if selected_ids:
            info = (
                db.session.query(AnalysisDailyIncome)
                    .filter(AnalysisDailyIncome.id.in_(selected_ids))
                    .all()
            )
        else:
            info = (db.session.query(AnalysisDailyIncome).all())

        data_list = []
        for info1 in info:
            data_list.append({
                '粮食作物损失面积': round(info1.number_0, 2) if info1.number_0 is not None else None,
                '粮食作物损失金额': round(info1.value_0, 2) if info1.value_0 is not None else None,
                '经济作物损失面积': round(info1.number_1, 2) if info1.number_1 is not None else None,
                '经济作物损失金额': round(info1.value_1, 2) if info1.value_1 is not None else None,
                '饲草作物损失面积': round(info1.number_2, 2) if info1.number_2 is not None else None,
                '饲草作物损失金额': round(info1.value_2, 2) if info1.value_2 is not None else None,
                '已淘汰田块面积': round(info1.number_3, 2) if info1.number_3 is not None else None,
                '已淘汰田块金额': round(info1.value_3, 2) if info1.value_3 is not None else None,
                '其他作物损失面积': round(info1.number_9, 2) if info1.number_9 is not None else None,
                '其他作物损失金额': round(info1.value_9, 2) if info1.value_9 is not None else None,
                '农药费用': round(info1.dung_value, 2) if info1.dung_value is not None else None,
                '人工防治费': round(info1.wool_value, 2) if info1.wool_value is not None else None,
                '生物防治费': round(info1.skin_value, 2) if info1.skin_value is not None else None,
                '有机肥补充费': round(info1.manure_value, 2) if info1.manure_value is not None else None,
                '补种费用': round(info1.feed_value, 2) if info1.feed_value is not None else None,
                '残株处理费': round(info1.producted_value, 2) if info1.producted_value is not None else None,
                '其他处理费': round(info1.other_value, 2) if info1.other_value is not None else None,
                '日期': info1.f_date.isoformat() if info1.f_date else None,
            })
        df = pd.DataFrame(data_list)

        export_path = os.path.join(os.getcwd(), 'App', 'analysis', 'export_excel', 'income_info.xlsx')
        df.to_excel(export_path, index=False)

        return send_file(export_path, as_attachment=True)
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'导出失败 {str(e)}'})




@analysis.route('/analysis/daily_income/update', methods=['POST'])#  手动更新日收入
# 用类型去分，计算总价，有问题，先注释掉，以防后续有用
# def update_daily_income():
#     try:
#
#         # 获取今天日期
#         # today = datetime.now().date()
#         today = datetime.now().strftime('%Y-%m-%d')
#
#         # 初始化分析数据字典
#         analysis_data = {
#             'f_date': today,
#             'belong': 0,
#             # 初始化SSalesinfo相关字段
#             'number_0': 0, 'value_0': 0.0,
#             'number_1': 0, 'value_1': 0.0,
#             'number_2': 0, 'value_2': 0.0,
#             'number_3': 0, 'value_3': 0.0,
#             'number_9': 0, 'value_9': 0.0,
#             # 初始化GSalesinfo相关字段
#             'dung_value': 0.0,
#             'wool_value': 0.0,
#             'skin_value': 0.0,
#             'manure_value': 0.0,
#             'feed_value': 0.0,
#             'producted_value': 0.0,
#             'other_value': 0.0
#         }
#
#         # 处理GHarvestSSalesinfo数据(草只销售)
#         ssales_records = db.session.query(
#             GHarvestSSalesinfo.type,
#             GHarvestSSalesinfo.total_price
#         ).filter(
#             GHarvestSSalesinfo.sales_date == today
#         ).all()
#
#         # 按type分组处理
#         ssales_groups = {}
#         for record in ssales_records:
#             if record.type not in ssales_groups:
#                 ssales_groups[record.type] = []
#             ssales_groups[record.type].append(record.total_price)
#
#         # 计算每个type的数值
#         for type_, prices in ssales_groups.items():
#             total = sum(prices)
#             count = len(prices) #确定只数
#
#             # 检查价格是否一致
#             # 检查价格是否一致
#             unique_prices = set(prices)   #确定这些草是不是同一批，因为一批草只录入一个总价
#             # unique_prices = len(set(prices))
#             if len(unique_prices) == 1:
#                 total = list(unique_prices)[0]  # 直接取唯一值
#                 # total = prices[0]  # 如果价格一致，只取一个
#             else:
#                 total = sum(unique_prices)  # 只加不同的价格
#
#             # 确定字段后缀
#             field_suffix = str(type_) if 0 <= type_ <= 3 else '9'
#
#             analysis_data[f'number_{field_suffix}'] = count
#             analysis_data[f'value_{field_suffix}'] = total
#
#         # 处理GHarvestGSalesinfo数据
#         gsales_totals = db.session.query(
#             GHarvestGSalesinfo.type,
#             func.sum(GHarvestGSalesinfo.total_price).label('total')
#         ).filter(
#             GHarvestGSalesinfo.sales_date == today
#         ).group_by(GHarvestGSalesinfo.type).all()
#         print(gsales_totals)
#
#
#         # 映射type到不同字段
#         type_mapping = {
#             0: 'dung_value',
#             1: 'wool_value',
#             2: 'skin_value',
#             3: 'manure_value',
#             4: 'feed_value',
#             5: 'producted_value'
#         }
#
#         for type_, total in gsales_totals:
#             field = type_mapping.get(type_, 'other_value')
#             analysis_data[field] = total or 0.0
#
#         # 创建或更新记录
#         existing_record = AnalysisDailyIncome.query.filter_by(f_date=today).first()
#
#         if existing_record:
#             # 更新现有记录
#             for key, value in analysis_data.items():
#                 setattr(existing_record, key, value)
#         else:
#             # 创建新记录
#             new_record = AnalysisDailyIncome(**analysis_data)
#             db.session.add(new_record)
#
#         db.session.commit()
#         return jsonify({'code': 200, 'message': '更新成功'})
#
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({
#             'code': 500,
#             'message': f'更新失败: {str(e)}'
#         }), 500

def update_daily_income():#按照总价去分，再根据类型去分
    try:
        today = datetime.now().strftime('%Y-%m-%d')

        analysis_data = {
            'f_date': today,
            'belong': 0,
            'number_0': 0, 'value_0': 0.0,
            'number_1': 0, 'value_1': 0.0,
            'number_2': 0, 'value_2': 0.0,
            'number_3': 0, 'value_3': 0.0,
            'number_9': 0, 'value_9': 0.0,
            'dung_value': 0.0,
            'wool_value': 0.0,
            'skin_value': 0.0,
            'manure_value': 0.0,
            'feed_value': 0.0,
            'producted_value': 0.0,
            'other_value': 0.0
        }

        # 处理GHarvestSSalesinfo数据（草只销售）
        ssales_records = db.session.query(
            GHarvestSSalesinfo.type,
            GHarvestSSalesinfo.total_price
        ).filter(
            GHarvestSSalesinfo.sales_date == today
        ).all()

        # 按total_price分组
        from collections import defaultdict
        price_groups = defaultdict(list)
        for record in ssales_records:
            price_groups[record.total_price].append(record.type)
        print('-----------------------------')
        print(f'price_groups{price_groups}')
        # 处理每个价格组
        for total_price, types in price_groups.items():
            # 统计类型数量
            type_counts = defaultdict(int)
            for type_ in types:
                type_counts[type_] += 1

            total_records = len(types)
            if total_records == 0:
                continue
            # 将 Decimal 转换为浮点数
            total_price_float = float(total_price)  # 关键转换
            # 计算每个类型的占比并分配金额
            for type_, count in type_counts.items():
                ratio = count / total_records
                allocated_value = total_price_float * ratio

                # 确定字段后缀
                if type_ in {0, 1, 2, 3}:
                    field_suffix = str(type_)
                else:
                    field_suffix = '9'

                # 累加统计结果
                analysis_data[f'number_{field_suffix}'] += count
                analysis_data[f'value_{field_suffix}'] += allocated_value

        # 处理GHarvestGSalesinfo数据（其他产品销售）
        gsales_totals = db.session.query(
            GHarvestGSalesinfo.type,
            func.sum(GHarvestGSalesinfo.total_price).label('total')
        ).filter(
            GHarvestGSalesinfo.sales_date == today
        ).group_by(GHarvestGSalesinfo.type).all()

        type_mapping = {
            0: 'dung_value',
            1: 'wool_value',
            2: 'skin_value',
            3: 'manure_value',
            4: 'feed_value',
            5: 'producted_value'
        }

        for type_, total in gsales_totals:
            field = type_mapping.get(type_, 'other_value')
            analysis_data[field] = total or 0.0

        # 创建或更新记录
        existing_record = AnalysisDailyIncome.query.filter_by(f_date=today).first()

        if existing_record:
            for key, value in analysis_data.items():
                setattr(existing_record, key, value)
        else:
            new_record = AnalysisDailyIncome(**analysis_data)
            db.session.add(new_record)

        db.session.commit()
        return jsonify({'code': 200, 'message': '更新成功'})

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'message': f'更新失败: {str(e)}'
        }), 500


@analysis.route('/analysis/daily_income/selectupdate', methods=['POST'])#  手动更新日收入
def update_select__daily_income():
    try:
        print('=====================================')
        request_date = request.get_json()
        print(request_date)
        # [{'belong': 0, 'dung_value': '0.00', 'f_date': '2025-03-03', 'feed_value': '0.00', 'id': 63, 'manure_value': '0.00', 'number_0': '0.00', 'number_1': '0.00', 'number_2': '0.00', 'number_3': '0.00', 'number_9': '0.00', 'other_value': '0.00', 'producted_value': '0.00', 'skin_value': '0.00', 'value_0': '0.00', 'value_1': '0.00', 'value_2': '0.00', 'value_3': '0.00', 'value_9': '0.00', 'weight_0': None, 'weight_1': None, 'weight_2': None, 'weight_3': None, 'weight_9': None, 'wool_value': '0.00'}]
        # 我进来了
        # 2025-03-03
        # 2025-03-03
        # print(request_date[0].get('f_date'))
        if request_date:
            print("我进来了")
            date = request_date[0].get('f_date')
            print(date)
            if not date:
                # 如果请求数据中没有 f_date 字段，使用当前日期
                date = datetime.now().strftime('%Y-%m-%d')
        else:
            date = datetime.now().strftime('%Y-%m-%d')
        print(date)
        # 获取今天日期
        # today = datetime.now().date()
        # today = datetime.now().strftime('%Y-%m-%d')

        # 初始化分析数据字典
        analysis_data = {
            'f_date': date,
            'belong': 0,
            'number_0': 0, 'value_0': 0.0,
            'number_1': 0, 'value_1': 0.0,
            'number_2': 0, 'value_2': 0.0,
            'number_3': 0, 'value_3': 0.0,
            'number_9': 0, 'value_9': 0.0,
            'dung_value': 0.0,
            'wool_value': 0.0,
            'skin_value': 0.0,
            'manure_value': 0.0,
            'feed_value': 0.0,
            'producted_value': 0.0,
            'other_value': 0.0
        }

        # 处理GHarvestSSalesinfo数据（草只销售）
        ssales_records = db.session.query(
            GHarvestSSalesinfo.type,
            GHarvestSSalesinfo.total_price
        ).filter(
            GHarvestSSalesinfo.sales_date == date
        ).all()

        # 按total_price分组
        from collections import defaultdict
        price_groups = defaultdict(list)
        for record in ssales_records:
            price_groups[record.total_price].append(record.type)
        print('-----------------------------')
        print(f'price_groups{price_groups}')
        # 处理每个价格组
        for total_price, types in price_groups.items():
            # 统计类型数量
            type_counts = defaultdict(int)
            for type_ in types:
                type_counts[type_] += 1

            total_records = len(types)
            if total_records == 0:
                continue
            # 将 Decimal 转换为浮点数
            total_price_float = float(total_price)  # 关键转换
            # 计算每个类型的占比并分配金额
            for type_, count in type_counts.items():
                ratio = count / total_records
                allocated_value = total_price_float * ratio

                # 确定字段后缀
                if type_ in {0, 1, 2, 3}:
                    field_suffix = str(type_)
                else:
                    field_suffix = '9'

                # 累加统计结果
                analysis_data[f'number_{field_suffix}'] += count
                analysis_data[f'value_{field_suffix}'] += allocated_value
        print('我处理完了')


        # 处理GHarvestGSalesinfo数据
        gsales_totals = db.session.query(
            GHarvestGSalesinfo.type,
            func.sum(GHarvestGSalesinfo.total_price).label('total')
        ).filter(
            GHarvestGSalesinfo.sales_date == date
        ).group_by(GHarvestGSalesinfo.type).all()
        print(gsales_totals)


        # 映射type到不同字段
        type_mapping = {
            0: 'dung_value',
            1: 'wool_value',
            2: 'skin_value',
            3: 'manure_value',
            4: 'feed_value',
            5: 'producted_value'
        }

        for type_, total in gsales_totals:
            field = type_mapping.get(type_, 'other_value')
            analysis_data[field] = total or 0.0

        # 创建或更新记录
        existing_record = AnalysisDailyIncome.query.filter_by(f_date=date).first()

        if existing_record:
            # 更新现有记录
            for key, value in analysis_data.items():
                setattr(existing_record, key, value)
        else:
            # 创建新记录
            new_record = AnalysisDailyIncome(**analysis_data)
            db.session.add(new_record)

        db.session.commit()
        return jsonify({'code': 200, 'message': '更新成功'})

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'message': f'更新失败: {str(e)}'
        }), 500

@analysis.route('/analysis/daily_income/commit_update', methods=['POST'])#  在添加完销售记录之后更新日收入
def commit_update__daily_income():
    try:
        print('=====================================')
        request_date = request.get_json()
        print(request_date)
        # == == == == == == == == == == == == == == == == == == =
        # [{'sales_date': '2025-03-04', 'sales_order': '1', 'billing_unit': '1', 'unit_price': '1', 'total_price': '1',
        #   'type': 1, 'transportation': '1', 'sales_site': '1', 'name': '1', 'buyer': '1', 'buyer_phone': '1',
        #   'selling_type': 6, 'quarantine_coding': '1', 'age': None, 'medical_leave': 0, 'notes': None,
        #   'basic_id': 20871},
        #  {'sales_date': '2025-03-04', 'sales_order': '1', 'billing_unit': '1', 'unit_price': '1', 'total_price': '1',
        #   'type': 1, 'transportation': '1', 'sales_site': '1', 'name': '1', 'buyer': '1', 'buyer_phone': '1',
        #   'selling_type': 6, 'quarantine_coding': '1', 'age': None, 'medical_leave': 0, 'notes': None,
        #   'basic_id': 20870}]


        if request_date:
            print("我进来了")
            date = request_date[0].get('sales_date')
            print(date)
            if not date:
                # 如果请求数据中没有 f_date 字段，使用当前日期
                date = datetime.now().strftime('%Y-%m-%d')
        else:
            date = datetime.now().strftime('%Y-%m-%d')
        print(date)
        # 获取今天日期
        # today = datetime.now().date()
        # today = datetime.now().strftime('%Y-%m-%d')

        # 初始化分析数据字典
        analysis_data = {
            'f_date': date,
            'belong': 0,
            'number_0': 0, 'value_0': 0.0,
            'number_1': 0, 'value_1': 0.0,
            'number_2': 0, 'value_2': 0.0,
            'number_3': 0, 'value_3': 0.0,
            'number_9': 0, 'value_9': 0.0,
            'dung_value': 0.0,
            'wool_value': 0.0,
            'skin_value': 0.0,
            'manure_value': 0.0,
            'feed_value': 0.0,
            'producted_value': 0.0,
            'other_value': 0.0
        }

        # 处理GHarvestSSalesinfo数据（草只销售）
        ssales_records = db.session.query(
            GHarvestSSalesinfo.type,
            GHarvestSSalesinfo.total_price
        ).filter(
            GHarvestSSalesinfo.sales_date == date
        ).all()

        # 按total_price分组
        from collections import defaultdict
        price_groups = defaultdict(list)
        for record in ssales_records:
            price_groups[record.total_price].append(record.type)
        print('-----------------------------')
        print(f'price_groups{price_groups}')
        # 处理每个价格组
        for total_price, types in price_groups.items():
            # 统计类型数量
            type_counts = defaultdict(int)
            for type_ in types:
                type_counts[type_] += 1

            total_records = len(types)
            if total_records == 0:
                continue
            # 将 Decimal 转换为浮点数
            total_price_float = float(total_price)  # 关键转换
            # 计算每个类型的占比并分配金额
            for type_, count in type_counts.items():
                ratio = count / total_records
                allocated_value = total_price_float * ratio

                # 确定字段后缀
                if type_ in {0, 1, 2, 3}:
                    field_suffix = str(type_)
                else:
                    field_suffix = '9'

                # 累加统计结果
                analysis_data[f'number_{field_suffix}'] += count
                analysis_data[f'value_{field_suffix}'] += allocated_value
        print('我处理完了')


        # 处理GHarvestGSalesinfo数据
        gsales_totals = db.session.query(
            GHarvestGSalesinfo.type,
            func.sum(GHarvestGSalesinfo.total_price).label('total')
        ).filter(
            GHarvestGSalesinfo.sales_date == date
        ).group_by(GHarvestGSalesinfo.type).all()
        print(gsales_totals)


        # 映射type到不同字段
        type_mapping = {
            0: 'dung_value',
            1: 'wool_value',
            2: 'skin_value',
            3: 'manure_value',
            4: 'feed_value',
            5: 'producted_value'
        }

        for type_, total in gsales_totals:
            field = type_mapping.get(type_, 'other_value')
            analysis_data[field] = total or 0.0

        # 创建或更新记录
        existing_record = AnalysisDailyIncome.query.filter_by(f_date=date).first()

        if existing_record:
            # 更新现有记录
            for key, value in analysis_data.items():
                setattr(existing_record, key, value)
        else:
            # 创建新记录
            new_record = AnalysisDailyIncome(**analysis_data)
            db.session.add(new_record)

        db.session.commit()
        return jsonify({'code': 200, 'message': '更新成功'})

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'message': f'更新失败: {str(e)}'
        }), 500




@analysis.route('/analysis/daily_grass_asset', methods=['POST'])# 获取草库存资产报表
def get_daily_grass_asset():

        pageNum = int(request.json.get('pageNum'))
        # pageNum = int(request.form.get('pageNum'))
        pageSize = int(request.json.get('pageSize'))

        conditions = []
        search_params = {

            'f_date': AnalysisGrassAsset.f_date,
        }
        for param, column in search_params.items():
            value = request.json.get(param)
            print(value)
            if value is not None:  # 检查值不为 None
                # conditions.append(column == value)
                if isinstance(value, list) and len(value) == 2:  # 处理日期范围
                    conditions.append(column.between(value[0], value[1]))
                else:  # 单个值，使用 == 比较
                    conditions.append(column == value)
            # 使用 and_() 组合条件
        if conditions:
            query = AnalysisGrassAsset.query.filter(and_(*conditions))
        else:
            query = AnalysisGrassAsset.query  # 如果没有条件，查询所有

        # 筛选出没有被移除的草(状态-1)和没有枯萎的草(状态0)
        # 并且根据id降序排列

        # 并且根据id降序排列

        query = query.filter(AnalysisGrassAsset.belong == 0)
        # infos = query.order_by(desc(AnalysisGrassAsset.id)).paginate(error_out=False)
        infos = query.order_by(desc(AnalysisGrassAsset.id)).paginate(page=pageNum, per_page=pageSize,
                                                                 error_out=False)

        total = query.count()

        list1 = []
        for info in infos:
            data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
            data = json.loads(data)
            list1.append(data)
        result = {
            "code": 200,
            "data": {
                "list": list1,
                "pageNum": pageNum,
                "pageSize": pageSize,
                "total": total
            },
            "msg": '成功'
        }
        return jsonify(result)


@analysis.route('/analysis/daily_grass_asset/export', methods=['POST'])
def export_daily_grass_asset():
    try:
        selected_ids = request.get_json()
        _dict = {
            1: "是",
            0: "否"
        }

        if selected_ids:
            info = (
                db.session.query(AnalysisGrassAsset)
                    .filter(AnalysisGrassAsset.id.in_(selected_ids))
                    .all()
            )
        else:
            info = (db.session.query(AnalysisGrassAsset).all())

        data_list = []
        for info1 in info:
            data_list.append({
                '草地繁殖父本价值': round(info1.hu_0_0, 2) if info1.hu_0_0 is not None else None,
                '草地繁殖母系价值': round(info1.hu_0_1, 2) if info1.hu_0_1 is not None else None,
                '草地育肥父本价值': round(info1.hu_1_0, 2) if info1.hu_1_0 is not None else None,
                '草地育肥母系价值': round(info1.hu_1_1, 2) if info1.hu_1_1 is not None else None,
                '草地幼株父系(1月)价值': round(info1.hu_2_0, 2) if info1.hu_2_0 is not None else None,
                '草地幼株母系(1月)价值': round(info1.hu_2_1, 2) if info1.hu_2_1 is not None else None,
                '草地幼株父系(2月)价值': round(info1.hu_3_0, 2) if info1.hu_3_0 is not None else None,
                '草地幼株母系(2月)价值': round(info1.hu_3_1, 2) if info1.hu_3_1 is not None else None,
                '小麦繁殖父本价值': round(info1.xw_0_0, 2) if info1.xw_0_0 is not None else None,
                '小麦繁殖母系价值': round(info1.xw_0_1, 2) if info1.xw_0_1 is not None else None,
                '小麦育肥父本价值': round(info1.xw_1_0, 2) if info1.xw_1_0 is not None else None,
                '小麦育肥母系价值': round(info1.xw_1_1, 2) if info1.xw_1_1 is not None else None,
                '小麦幼株父系(1月)价值': round(info1.xw_2_0, 2) if info1.xw_2_0 is not None else None,
                '小麦幼株母系(1月)价值': round(info1.xw_2_1, 2) if info1.xw_2_1 is not None else None,
                '小麦幼株父系(2月)价值': round(info1.xw_3_0, 2) if info1.xw_3_0 is not None else None,
                '小麦幼株母系(2月)价值': round(info1.xw_3_1, 2) if info1.xw_3_1 is not None else None,
                '日期': info1.f_date.isoformat() if info1.f_date else None,
            })
        df = pd.DataFrame(data_list)

        export_path = os.path.join(os.getcwd(), 'App', 'analysis', 'export_excel', 'grass_asset_info.xlsx')
        df.to_excel(export_path, index=False)

        return send_file(export_path, as_attachment=True)
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'导出失败 {str(e)}'})

@analysis.route('/analysis/daily_grass_asset/update', methods=['POST'])# 更新草库存资产报表
def update_daily_grass_asset():
    try:
        # 获取今天的日期
        today = datetime.now().date()

        # 查询今日所有的GrassAssetinfo记录
        today_assets = GrassAssetinfo.query.filter(
            db.func.date(GrassAssetinfo.f_date) == today
        ).all()

        # 初始化分析记录字段字典
        analysis_fields = {
            # 初始化hu系列字段
            **{f'hu_{p}_{s}': 0 for p in range(4) for s in range(2)},
            # 初始化xw系列字段
            **{f'xw_{p}_{s}': 0 for p in range(4) for s in range(2)},
            'other': 0
        }

        # 填充数据
        for asset in today_assets:
            # 只处理variety为0或1的有效数据
            if asset.variety not in [0, 1]:
                analysis_fields['other'] += asset.sum_value  # 使用累加而非覆盖
                continue

            # 确定字段前缀
            prefix = 'hu' if asset.variety == 0 else 'xw'

            # 只处理purpose在0-3范围内的有效数据
            if 0 <= asset.purpose <= 3 and asset.sex in [0, 1]:
                field_name = f"{prefix}_{asset.purpose}_{asset.sex}"
                if field_name in analysis_fields:
                    analysis_fields[field_name] = asset.sum_value

        # 查询或创建分析记录
        analysis_record = AnalysisGrassAsset.query.filter_by(
            f_date=today,
            belong=0
        ).first()
        # 更新或新建记录
        if analysis_record:
            # 更新现有记录
            for field, value in analysis_fields.items():
                setattr(analysis_record, field, value)
            analysis_record.update_time = datetime.now()
        else:
            # 创建新记录
            analysis_record = AnalysisGrassAsset(
                f_date=today,
                belong=0,
                # create_time=datetime.now(),
                **analysis_fields
            )
            db.session.add(analysis_record)

        db.session.commit()


        # # 创建新分析记录
        # new_analysis = AnalysisGrassAsset(
        #     f_date=today,
        #     belong=0,
        #     **analysis_fields
        # )
        #
        # # 添加到数据库并提交
        # db.session.add(new_analysis)
        # db.session.commit()

        return jsonify({
            'code': 200,
            'msg': '更新成功',
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'msg': f'更新失败: {str(e)}'
        })










# =========================================


# 辅助函数：根据模型类生成字段字典
def generate_field_dict(model_class, patterns):
    """
    根据字段名称模式生成字段字典
    :param model_class: SQLAlchemy模型类
    :param patterns: 包含的字段模式列表（支持字符串匹配或正则表达式）
    :return: 字段名称列表
    """
    fields = []
    for column in model_class.__table__.columns:
        col_name = column.name
        if any(pattern in col_name for pattern in patterns):
            fields.append(col_name)
    return fields


# 定义各模型需要计算的字段模式
CALCULATION_PATTERNS = {
    'expense': {
        'exclude': ['id', 'date', 'food_fees', 'drug_fees', 'f_date', 'f_staff', 'belong', 'day_compute',
                    'directtotal_fees', 'indirecttotal_fees', 'total_fees', 'other_text']
    },
    'income': {'include': ['value']},
    'grass_asset': {'exclude': ['id', 'f_date', 'belong']},
    'stock_asset': {'include': ['_val']}
}


@analysis.route('/analysis/daily_report/searchDate', methods=['POST'])  # 日支出报表编辑 后端接口
def search_Date():
    data = request.get_json()
    print(data)
    sheet = Analysisdailysheet.query.filter_by(date=data['date']).all()
    if (sheet):
        result = {
            "code": 200,
            "msg": '经查询得知相同日期已经存在一次记录，继续增加则在之前基础上累加！'
        }
        return jsonify(result)
    else:
        result = {
            "code": 200,
            "msg": '未查询到相同日期的记录，请继续添加！'
        }
        return jsonify(result)


@analysis.route('/analysis/daily_report', methods=['POST'])  # 病虫害日防治报表 后端接口
def get_dailyReport():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        # 'basic_id': DHealthDeathinfo.basic_id,
        'date': Analysisdailysheet.date,
        'f_date': Analysisdailysheet.f_date,
        'f_staff': Analysisdailysheet.f_staff
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'date' or param == 'f_date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        print(conditions)
        query = Analysisdailysheet.query.filter(and_(*conditions))
    else:
        query = Analysisdailysheet.query  # 如果没有条件，查询所有

    # 并且根据id降序排列

    query = query.filter(Analysisdailysheet.belong == 0)
    infos = query.order_by(desc(Analysisdailysheet.date)).paginate(page=pageNum, per_page=pageSize,
                                                                   error_out=False)
    total = query.count()

    list = []
    for info in infos:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        data = json.loads(data)
        list.append(data)
    result = {
        "code": 200,
        "data": {
            "list": list,
            "pageNum": pageNum,
            "pageSize": pageSize,
            "total": total
        },
        "msg": '成功'
    }
    return jsonify(result)


@analysis.route('/analysis/daily_report/add', methods=['POST'])  # 增加日支出报表 后端接口
def add_dailyReport():
    data = request.get_json()

    ctime = datetime.now()
    # 初始化创建时间
    data['f_date'] = ctime
    # 默认belong为0
    data['belong'] = 0
    print(data)
    # 将日期字符串转换为 datetime 对象
    date_obj = datetime.strptime(data['date'], '%Y-%m-%d')
    if date_obj > ctime:
        result = {
            "code": 500,
            "msg": '日报表日期不可以大于当天日期'
        }
        return jsonify(result)
    # 构造完数据后应该对数据进行判断, 如果存在则直接累加
    object = Analysisdailysheet.query.filter_by(date=data['date']).first()  # 获取可能数据库存在的相同的日期记录
    if object:
        # 如果存在
        sheet = object
        # 遍历数据字典，对数值类型的属性进行累加
        for key, value in data.items():
            if key == 'date' or key == 'f_date' or key == 'belong' or key == 'f_staff' or key == 'other_text':
                if key == 'other_text':  # 备注需要在后面直接字符串链接
                    current_value = getattr(sheet, key)
                    if current_value is None:
                        setattr(sheet, key, value)
                    else:
                        setattr(sheet, key, current_value + value)
                continue
            else:
                # if key in ['buygrass_fees', 'foods_fees', 'drug_fees', 'test_fees', 'labor_fees',
                #            'waterEle_fees', 'land_fees', 'maintenance_fees']:  # 如果是直接费用的字典
                #     setattr(sheet, 'directtotal_fees', value + sheet.directtotal_fees)  # 计算直接费用总花费
                # elif key in ['cheep_fees', 'manage_fees', 'research_fees', 'other_fees']:  # 如果是间接费用的字典
                #     setattr(sheet, 'indirecttotal_fees', value + sheet.indirecttotal_fees)  # 计算间接费用总花费
                current_value = getattr(sheet, key)
                # setattr(sheet, 'total_fees', value + sheet.directtotal_fees)  # 计算总花费
                if current_value is None:
                    current_value = 0
                setattr(sheet, key, current_value + Decimal(str(value)))

        # 将日期字符串转换为 datetime 对象
        date_obj = datetime.strptime(data['date'], '%Y-%m-%d')
        # 计算上一天的日期
        previous_day = date_obj - timedelta(days=1)
        # 将上一天的日期转换为字符串
        previous_day_str = previous_day.strftime('%Y-%m-%d')
        pre_day = Analysisdailysheet.query.filter_by(date=previous_day_str).first()
        # if (pre_day):
        #     setattr(sheet, 'directtotal_fees', sheet.directtotal_fees + pre_day.directtotal_fees)
        #     setattr(sheet, 'indirecttotal_fees', sheet.indirecttotal_fees + pre_day.indirecttotal_fees)
        #     setattr(sheet, 'total_fees', sheet.total_fees + pre_day.total_fees)


    else:
        # 创建Analysisdailysheet对象，并进行对前端传过来的信息构造数据
        sheet = Analysisdailysheet()
        sheet.directtotal_fees = 0
        sheet.indirecttotal_fees = 0
        sheet.total_fees = 0
        for key, value in data.items():
            if key == 'date' or key == 'f_date' or key == 'belong' or key == 'f_staff' or key == 'other_text':
                setattr(sheet, key, value)
                continue
            elif value is None:
                value = 0
            # if key in ['buygrass_fees', 'foods_fees', 'drug_fees', 'test_fees', 'labor_fees',
            #            'waterEle_fees', 'land_fees', 'maintenance_fees']:  # 如果是直接费用的字典
            #     setattr(sheet, 'directtotal_fees', value + sheet.directtotal_fees)  # 计算直接费用总花费
            # elif key in ['cheep_fees', 'manage_fees', 'research_fees', 'other_fees']:  # 如果是间接费用的字典
            #     setattr(sheet, 'indirecttotal_fees', value + sheet.indirecttotal_fees)  # 计算间接费用总花费
            # setattr(sheet, 'total_fees', value + sheet.directtotal_fees)  # 计算总花费
            setattr(sheet, key, value)
        # 将日期字符串转换为 datetime 对象
        date_obj = datetime.strptime(data['date'], '%Y-%m-%d')
        # 计算上一天的日期
        previous_day = date_obj - timedelta(days=1)
        # 将上一天的日期转换为字符串
        previous_day_str = previous_day.strftime('%Y-%m-%d')
        pre_day = Analysisdailysheet.query.filter_by(date=previous_day_str).first()
    # 提交到数据库
    try:
        db.session.add(sheet)
        db.session.commit()
    # 处理报错
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        result = {
            "code": 500,
            "msg": f'添加失败 {str(e)}'
        }
        return jsonify(result)
    # 返回结果
    result = {
        "code": 200,
        "msg": '添加成功'
    }
    return jsonify(result)


@analysis.route('/analysis/daily_report/edit', methods=['POST'])  # 日支出报表编辑 后端接口
def edit_dailyReport():
    data = request.get_json()
    '''
    编辑逻辑：在一个费用发生改变的时候，同时需要计算他的总花费，直接总花费和间接总花费的变化，同时在当下日期改变
    的时候，在大于这个日期的所有记录也同时需要改变总花费，直接总花费和简介总花费。
    '''

    # try:
    record = Analysisdailysheet.query.get(data['id'])
    if not record:
        result = {
            "code": 404,
            "msg": "未找到对应的记录"
        }
        return jsonify(result)
    # 获取数据库中最新的日期
    latest_date = db.session.query(func.max(Analysisdailysheet.date)).scalar()
    # 直接费用字段列表
    direct_fees_fields = [
        'buygrass_fees', 'test_fees',
        'labor_fees', 'waterEle_fees', 'land_fees', 'maintenance_fees'
    ]
    # 间接费用字段列表
    indirect_fees_fields = [
        'cheep_fees', 'manage_fees', 'research_fees', 'other_fees'
    ]
    direct_total_diff = Decimal('0')
    indirect_total_diff = Decimal('0')
    # 更新记录的字段并计算差值
    for key, new_value in data.items():
        if hasattr(record, key):
            old_value = getattr(record, key)
            if (key in direct_fees_fields or key in indirect_fees_fields):
                if isinstance(new_value, str):
                    try:
                        # 尝试将字符串转换为 Decimal 类型
                        print(new_value)
                        num_value = Decimal(new_value)
                        new_value = num_value
                    except ValueError:
                        result = {
                            "code": 400,
                            "msg": f"字段 {key} 的值 {new_value} 无法转换为数字"
                        }
                        return jsonify(result)
            if key in direct_fees_fields:
                direct_total_diff += (Decimal(str(new_value)) - Decimal(str(old_value)))
            elif key in indirect_fees_fields:
                indirect_total_diff += (Decimal(str(new_value)) - Decimal(str(old_value)))
            setattr(record, key, new_value)
    # 更新直接总花费、间接总花费和总花费
    # record.directtotal_fees = Decimal(str(record.directtotal_fees)) + direct_total_diff
    # record.indirecttotal_fees = Decimal(str(record.indirecttotal_fees)) + indirect_total_diff
    # record.total_fees = Decimal(str(record.total_fees)) + direct_total_diff + indirect_total_diff
    # 如果更新信息的日期不是最新日期，更新大于该日期的所有记录
    # 确保 record.date 是 datetime.date 类型
    # if isinstance(record.date, str):
    #     record.date = datetime.strptime(record.date, '%Y-%m-%d').date()
    # # 确保 latest_date 是 datetime.date 类型
    # if isinstance(latest_date, str):
    #     latest_date = datetime.strptime(latest_date, '%Y-%m-%d').date()
    # if record.date < latest_date:
    #     later_records = Analysisdailysheet.query.filter(Analysisdailysheet.date > record.date).all()
    #     for later_record in later_records:
    #         later_record.directtotal_fees = Decimal(str(later_record.directtotal_fees)) + direct_total_diff
    #         later_record.indirecttotal_fees = Decimal(str(later_record.indirecttotal_fees)) + indirect_total_diff
    #         later_record.total_fees = Decimal(str(later_record.total_fees)) + direct_total_diff + indirect_total_diff
    db.session.commit()
    # except Exception as e:
    #     db.session.rollback()
    #     db.session.flush()
    #     result = {
    #         "code": 500,
    #         "msg": f'修改失败 {str(e)}'
    #     }
    #     return jsonify(result)
    result = {
        "code": 200,
        "msg": '修改成功'
    }
    return jsonify(result)


@analysis.route('/analysis/daily_report/export', methods=['POST'])  # 日支出报表导出 后端接口
def export_dailyReport():
    try:
        selected_ids = request.get_json()

        if selected_ids:
            daily_report_info = Analysisdailysheet.query.filter(Analysisdailysheet.id.in_(selected_ids)).all()
        else:
            daily_report_info = Analysisdailysheet.query.all()

        data_list = []
        for info in daily_report_info:
            data_list.append({
                '日期': info.date.isoformat() if info.date else None,
                '种苗购置费用': round(info.buygrass_fees, 2) if info.buygrass_fees is not None else None,
                '草料费用': round(info.caoliao_fees, 2) if info.caoliao_fees is not None else None,
                '精料费用': round(info.jingliao_fees, 2) if info.jingliao_fees is not None else None,
                '疫苗费用': round(info.yimiao_fees, 2) if info.yimiao_fees is not None else None,
                '药品费用': round(info.yaopin_fees, 2) if info.yaopin_fees is not None else None,
                '检测检验费用': round(info.test_fees, 2) if info.test_fees is not None else None,
                '人工费用': round(info.labor_fees, 2) if info.labor_fees is not None else None,
                '水电费用': round(info.waterEle_fees, 2) if info.waterEle_fees is not None else None,
                '地租': round(info.land_fees, 2) if info.land_fees is not None else None,
                '维修费用': round(info.maintenance_fees, 2) if info.maintenance_fees is not None else None,
                '低值易耗品费用': round(info.cheep_fees, 2) if info.cheep_fees is not None else None,
                '管理费用': round(info.manage_fees, 2) if info.manage_fees is not None else None,
                '研究费用': round(info.research_fees, 2) if info.research_fees is not None else None,
                '其他费用': round(info.other_fees, 2) if info.other_fees is not None else None,
                '其他费用备注': info.other_text,
                '创建日期': info.f_date.isoformat() if info.f_date else None,
                '创建人员': info.f_staff
            })

        df = pd.DataFrame(data_list)

        export_path = os.path.join(os.getcwd(), 'App', 'analysis', 'export_excel', 'dailyReport_info.xlsx')
        df.to_excel(export_path, index=False)

        return send_file(export_path, as_attachment=True)
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'导出失败 {str(e)}'})


@analysis.route('/analysis/daily_stocksheet', methods=['POST'])  # 查询物料库存资产
def daily_stocksheet():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        # 'basic_id': DHealthDeathinfo.basic_id,
        'date': Analysisdailystocksheet.date
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        print(conditions)
        query = Analysisdailystocksheet.query.filter(and_(*conditions))
    else:
        query = Analysisdailystocksheet.query  # 如果没有条件，查询所有

    # 并且根据id降序排列

    # query = query.filter(Analysisdailystocksheet.belong == 0)
    infos = query.order_by(desc(Analysisdailystocksheet.id)).paginate(page=pageNum, per_page=pageSize,
                                                                      error_out=False)
    total = query.count()

    list = []
    for info in infos:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        data = json.loads(data)
        list.append(data)
    result = {
        "code": 200,
        "data": {
            "list": list,
            "pageNum": pageNum,
            "pageSize": pageSize,
            "total": total
        },
        "msg": '成功'
    }
    return jsonify(result)


@analysis.route('/analysis/daily_stocksheet/update', methods=['POST'])  # 盘算物料库存资产
def update_stocksheet():
    try:
        # 获取当前日期，用于后续插入或更新 Analysisdailystocksheet 表中的记录
        today = date.today()

        # 检查 Analysisdailystocksheet 表中是否已经存在当天日期的记录
        # 如果存在，则将该记录从数据库中删除，以便后续插入最新计算结果
        existing_record = Analysisdailystocksheet.query.filter_by(date=today).first()
        if existing_record:
            db.session.delete(existing_record)
            db.session.commit()

        # 初始化一个字典 result，用于存储各类物品的数量和价值信息
        # 这些信息将用于后续创建或更新 Analysisdailystocksheet 表中的记录
        result = {
            "garlicskin_num": 0,
            "garlicskin_val": 0,
            "peanutseedling_num": 0,
            "peanutseedling_val": 0,
            "ensilage_num": 0,
            "ensilage_val": 0,
            "otherforage_num": 0,
            "otherforage_val": 0,
            "corn_num": 0,
            "corn_val": 0,
            "premix_num": 0,
            "premix_val": 0,
            "bran_num": 0,
            "bran_val": 0,
            "soybeanmeal_num": 0,
            "soybeanmeal_val": 0,
            "salt_num": 0,
            "salt_val": 0,
            "bakingsoda_num": 0,
            "bakingsoda_val": 0,
            "calciumlactate_num": 0,
            "calciumlactate_val": 0,
            "otherfinefodder_num": 0,
            "otherfinefodder_val": 0,
            "smallvaccine_num": 0,
            "smallvaccine_val": 0,
            "threePfourD_num": 0,
            "threePfourD_val": 0,
            "footAmouthdisease_num": 0,
            "footAmouthdisease_val": 0,
            "duolianbiying_num": 0,
            "duolianbiying_val": 0,
            "othervaccine_num": 0,
            "othervaccine_val": 0,
            "gentamicin_num": 0,
            "gentamicin_val": 0,
            "zhongling_num": 0,
            "zhongling_val": 0,
            "tilmicosin_num": 0,
            "tilmicosin_val": 0,
            "othermedicine_num": 0,
            "othermedicine_val": 0
        }

        # 处理草料相关数据
        # 定义需要分别统计的草料名称列表
        forage_goods = ["蒜皮", "花生秧", "青贮"]
        # 用于存储已统计的草料记录的 id，以便后续筛选出“其他草料”
        forage_ids = []
        for good in forage_goods:
            # 从 HStoreInventory 表中查询 type 为 2（代表草料）且 goods 字段包含当前草料名称的所有记录
            records = HStoreInventory.query.filter(
                HStoreInventory.type == 2,
                HStoreInventory.goods.like(f"%{good}%")
            ).all()
            # 计算该草料的总数量，即所有相关记录的 quantity 字段之和
            num = sum([record.quantity for record in records])
            # 计算该草料的总价值，即每条记录的 quantity 乘以 stockPrice 后再求和
            val = sum([record.quantity * record.stockPrice for record in records])
            # 将已统计的记录的 id 加入到 forage_ids 列表中
            for record in records:
                forage_ids.append(record.id)
            # 根据当前草料名称，将计算得到的数量和价值存储到 result 字典的对应键中
            if good == "蒜皮":
                result["garlicskin_num"] = num
                result["garlicskin_val"] = val
            elif good == "花生秧":
                result["peanutseedling_num"] = num
                result["peanutseedling_val"] = val
            elif good == "青贮":
                result["ensilage_num"] = num
                result["ensilage_val"] = val

        # 从 HStoreInventory 表中筛选出 type 为 2 且 id 不在 forage_ids 列表中的记录，即“其他草料”
        other_forage_records = HStoreInventory.query.filter(
            HStoreInventory.type == 2,
            ~HStoreInventory.id.in_(forage_ids)
        ).all()
        # 计算“其他草料”的总数量
        result["otherforage_num"] = sum([record.quantity for record in other_forage_records])
        # 计算“其他草料”的总价值
        result["otherforage_val"] = sum([record.quantity * record.stockPrice for record in other_forage_records])

        # 处理精料相关数据
        # 定义需要分别统计的精料名称列表
        finefodder_goods = ["玉米", "预混料", "麸皮", "豆粕", "盐", "小苏打", "乳酸钙"]
        # 用于存储已统计的精料记录的 id，以便后续筛选出“其他精料”
        finefodder_ids = []
        for good in finefodder_goods:
            # 从 HStoreInventory 表中查询 type 为 3（代表精料）且 goods 字段包含当前精料名称的所有记录
            records = HStoreInventory.query.filter(
                HStoreInventory.type == 3,
                HStoreInventory.goods.like(f"%{good}%")
            ).all()
            # 计算该精料的总数量
            num = sum([record.quantity for record in records])
            # 计算该精料的总价值
            val = sum([record.quantity * record.stockPrice for record in records])
            # 将已统计的记录的 id 加入到 finefodder_ids 列表中
            for record in records:
                finefodder_ids.append(record.id)
            # 根据当前精料名称，将计算得到的数量和价值存储到 result 字典的对应键中
            if good == "玉米":
                result["corn_num"] = num
                result["corn_val"] = val
            elif good == "预混料":
                result["premix_num"] = num
                result["premix_val"] = val
            elif good == "麸皮":
                result["bran_num"] = num
                result["bran_val"] = val
            elif good == "豆粕":
                result["soybeanmeal_num"] = num
                result["soybeanmeal_val"] = val
            elif good == "盐":
                result["salt_num"] = num
                result["salt_val"] = val
            elif good == "小苏打":
                result["bakingsoda_num"] = num
                result["bakingsoda_val"] = val
            elif good == "乳酸钙":
                result["calciumlactate_num"] = num
                result["calciumlactate_val"] = val

        # 从 HStoreInventory 表中筛选出 type 为 3 且 id 不在 finefodder_ids 列表中的记录，即“其他精料”
        other_finefodder_records = HStoreInventory.query.filter(
            HStoreInventory.type == 3,
            ~HStoreInventory.id.in_(finefodder_ids)
        ).all()
        # 计算“其他精料”的总数量
        result["otherfinefodder_num"] = sum([record.quantity for record in other_finefodder_records])
        # 计算“其他精料”的总价值
        result["otherfinefodder_val"] = sum(
            [record.quantity * record.stockPrice for record in other_finefodder_records])

        # 处理疫苗相关数据
        # 定义需要分别统计的疫苗名称列表
        vaccine_goods = ["小反刍山草害二联苗", "三联四防", "口蹄疫", "多联必应"]
        # 用于存储已统计的疫苗记录的 id，以便后续筛选出“其他疫苗”
        vaccine_ids = []
        for good in vaccine_goods:
            # 从 HStoreInventory 表中查询 type 为 0（代表疫苗）且 goods 字段包含当前疫苗名称的所有记录
            records = HStoreInventory.query.filter(
                HStoreInventory.type == 0,
                HStoreInventory.goods.like(f"%{good}%")
            ).all()
            # 计算该疫苗的总数量
            num = sum([record.quantity for record in records])
            # 计算该疫苗的总价值
            val = sum([record.quantity * record.stockPrice for record in records])
            # 将已统计的记录的 id 加入到 vaccine_ids 列表中
            for record in records:
                vaccine_ids.append(record.id)
            # 根据当前疫苗名称，将计算得到的数量和价值存储到 result 字典的对应键中
            if good == "小反刍山草害二联苗":
                result["smallvaccine_num"] = num
                result["smallvaccine_val"] = val
            elif good == "三联四防":
                result["threePfourD_num"] = num
                result["threePfourD_val"] = val
            elif good == "口蹄疫":
                result["footAmouthdisease_num"] = num
                result["footAmouthdisease_val"] = val
            elif good == "多联必应":
                result["duolianbiying_num"] = num
                result["duolianbiying_val"] = val

        # 从 HStoreInventory 表中筛选出 type 为 0 且 id 不在 vaccine_ids 列表中的记录，即“其他疫苗”
        other_vaccine_records = HStoreInventory.query.filter(
            HStoreInventory.type == 0,
            ~HStoreInventory.id.in_(vaccine_ids)
        ).all()
        # 计算“其他疫苗”的总数量
        result["othervaccine_num"] = sum([record.quantity for record in other_vaccine_records])
        # 计算“其他疫苗”的总价值
        result["othervaccine_val"] = sum([record.quantity * record.stockPrice for record in other_vaccine_records])

        # 处理药品相关数据
        # 定义需要分别统计的药品名称列表
        medicine_goods = ["庆大霉素", "中灵", "替米考星"]
        # 用于存储已统计的药品记录的 id，以便后续筛选出“其他药品”
        medicine_ids = []
        for good in medicine_goods:
            # 从 HStoreInventory 表中查询 type 为 1（代表药品）且 goods 字段包含当前药品名称的所有记录
            records = HStoreInventory.query.filter(
                HStoreInventory.type == 1,
                HStoreInventory.goods.like(f"%{good}%")
            ).all()
            # 计算该药品的总数量
            num = sum([record.quantity for record in records])
            # 计算该药品的总价值
            val = sum([record.quantity * record.stockPrice for record in records])
            # 将已统计的记录的 id 加入到 medicine_ids 列表中
            for record in records:
                medicine_ids.append(record.id)
            # 根据当前药品名称，将计算得到的数量和价值存储到 result 字典的对应键中
            if good == "庆大霉素":
                result["gentamicin_num"] = num
                result["gentamicin_val"] = val
            elif good == "中灵":
                result["zhongling_num"] = num
                result["zhongling_val"] = val
            elif good == "替米考星":
                result["tilmicosin_num"] = num
                result["tilmicosin_val"] = val

        # 从 HStoreInventory 表中筛选出 type 为 1 且 id 不在 medicine_ids 列表中的记录，即“其他药品”
        other_medicine_records = HStoreInventory.query.filter(
            HStoreInventory.type == 1,
            ~HStoreInventory.id.in_(medicine_ids)
        ).all()
        # 计算“其他药品”的总数量
        result["othermedicine_num"] = sum([record.quantity for record in other_medicine_records])
        # 计算“其他药品”的总价值
        result["othermedicine_val"] = sum([record.quantity * record.stockPrice for record in other_medicine_records])

        # 将当天日期添加到 result 字典中，用于后续插入到 Analysisdailystocksheet 表中
        result["date"] = today
        # 使用 result 字典创建一个新的 Analysisdailystocksheet 记录对象
        new_record = Analysisdailystocksheet(**result)
        # 将新记录添加到数据库会话中
        db.session.add(new_record)
        # 提交数据库会话，将新记录保存到数据库中
        db.session.commit()
    except Exception as e:
        # 错误处理
        db.session.rollback()
        db.session.flush()
        result = {
            "code": 500,
            "msg": f'更新物资库存信息失败 {str(e)}'
        }
        return jsonify(result)
    result = {
        "code": 200,
        "msg": '更新物资库存信息成功'
    }
    return jsonify(result)


@analysis.route('/analysis/daily_stocksheet/export', methods=['POST'])
def export_stocksheet():
    try:
        selected_ids = request.get_json()

        if selected_ids:
            stocksheet_info = Analysisdailystocksheet.query.filter(Analysisdailystocksheet.id.in_(selected_ids)).all()
        else:
            stocksheet_info = Analysisdailystocksheet.query.all()

        data_list = []
        for info in stocksheet_info:
            data_list.append({
                '日期': info.date.isoformat() if info.date else None,
                '蒜皮数量': round(info.garlicskin_num, 2) if info.garlicskin_num is not None else None,
                '蒜皮价值': round(info.garlicskin_val, 2) if info.garlicskin_val is not None else None,
                '花生秧数量': round(info.peanutseedling_num, 2) if info.peanutseedling_num is not None else None,
                '花生秧价值': round(info.peanutseedling_val, 2) if info.peanutseedling_val is not None else None,
                '青贮数量': round(info.ensilage_num, 2) if info.ensilage_num is not None else None,
                '青贮价值': round(info.ensilage_val, 2) if info.ensilage_val is not None else None,
                '其他草料数量': round(info.otherforage_num, 2) if info.otherforage_num is not None else None,
                '其他草料价值': round(info.otherforage_val, 2) if info.otherforage_val is not None else None,
                '玉米数量': round(info.corn_num, 2) if info.corn_num is not None else None,
                '玉米价值': round(info.corn_val, 2) if info.corn_val is not None else None,
                '预混料数量': round(info.premix_num, 2) if info.premix_num is not None else None,
                '预混料价值': round(info.premix_val, 2) if info.premix_val is not None else None,
                '麸皮数量': round(info.bran_num, 2) if info.bran_num is not None else None,
                '麸皮价值': round(info.bran_val, 2) if info.bran_val is not None else None,
                '豆粕数量': round(info.soybeanmeal_num, 2) if info.soybeanmeal_num is not None else None,
                '豆粕价值': round(info.soybeanmeal_val, 2) if info.soybeanmeal_val is not None else None,
                '盐数量': round(info.salt_num, 2) if info.salt_num is not None else None,
                '盐价值': round(info.salt_val, 2) if info.salt_val is not None else None,
                '小苏打数量': round(info.bakingsoda_num, 2) if info.bakingsoda_num is not None else None,
                '小苏打价值': round(info.bakingsoda_val, 2) if info.bakingsoda_val is not None else None,
                '乳酸钙数量': round(info.calciumlactate_num, 2) if info.calciumlactate_num is not None else None,
                '乳酸钙价值': round(info.calciumlactate_val, 2) if info.calciumlactate_val is not None else None,
                '其他精料数量': round(info.otherfinefodder_num, 2) if info.otherfinefodder_num is not None else None,
                '其他精料价值': round(info.otherfinefodder_val, 2) if info.otherfinefodder_val is not None else None,
                '小反刍山草害二联苗数量': round(info.smallvaccine_num, 2) if info.smallvaccine_num is not None else None,
                '小反刍山草害二联苗价值': round(info.smallvaccine_val, 2) if info.smallvaccine_val is not None else None,
                '三联四防疫苗数量': round(info.threePfourD_num, 2) if info.threePfourD_num is not None else None,
                '三联四防疫苗价值': round(info.threePfourD_val, 2) if info.threePfourD_val is not None else None,
                '口蹄疫疫苗数量': round(info.footAmouthdisease_num, 2) if info.footAmouthdisease_num is not None else None,
                '口蹄疫疫苗价值': round(info.footAmouthdisease_val, 2) if info.footAmouthdisease_val is not None else None,
                '多联必应疫苗数量': round(info.duolianbiying_num, 2) if info.duolianbiying_num is not None else None,
                '多联必应疫苗价值': round(info.duolianbiying_val, 2) if info.duolianbiying_val is not None else None,
                '其他疫苗数量': round(info.othervaccine_num, 2) if info.othervaccine_num is not None else None,
                '其他疫苗价值': round(info.othervaccine_val, 2) if info.othervaccine_val is not None else None,
                '庆大霉素数量': round(info.gentamicin_num, 2) if info.gentamicin_num is not None else None,
                '庆大霉素价值': round(info.gentamicin_val, 2) if info.gentamicin_val is not None else None,
                '中灵数量': round(info.zhongling_num, 2) if info.zhongling_num is not None else None,
                '中灵价值': round(info.zhongling_val, 2) if info.zhongling_val is not None else None,
                '替米考星数量': round(info.tilmicosin_num, 2) if info.tilmicosin_num is not None else None,
                '替米考星价值': round(info.tilmicosin_val, 2) if info.tilmicosin_val is not None else None,
                '其他药品数量': round(info.othermedicine_num, 2) if info.othermedicine_num is not None else None,
                '其他药品价值': round(info.othermedicine_val, 2) if info.othermedicine_val is not None else None
            })

        df = pd.DataFrame(data_list)

        export_path = os.path.join(os.getcwd(), 'App', 'analysis', 'export_excel', 'stocksheet_info.xlsx')
        df.to_excel(export_path, index=False)

        return send_file(export_path, as_attachment=True)
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'导出失败 {str(e)}'})





#这个函数是deepseek写的，留给后面的人参考，-_- 要是有bug,别怪我....
@analysis.route('/analysis/dataVisualize', methods=['POST'])
def get_daily_financial_data():
    """获取每日财务数据接口（增强版）
    返回数据格式：
    [{
        date: "2025-01-01",
        # 收入相关
        income_total: 15000,      # 总收入
        income_sales: {           # 销售明细
            breeding_grass: {number: 10, value: 5000},   # 草种
            fattening_grass: {number: 20, value: 8000},  # 育成草
            lamb: {number: 5, value: 2000},              # 幼苗
            other_grass: {number: 3, value: 1000}        # 其他草
        },
        income_byproducts: {      # 副产品收入
            dung: 300,            # 粪肥
            wool: 500,            # 草叶
            skin: 200,            # 草皮
            manure: 150,          # 堆肥
            feed: 400,            # 饲料
            producted: 600,       # 生产品
            other: 300            # 其他
        },

        # 支出相关
        expense_total: 8000,       # 总支出
        expense_direct: {          # 直接费用
            total: 6000,
            detail: {
                buygrass: 1000,   # 购草费
                forage: 800,      # 草料费
                fine_fodder: 500,  # 精料费
                vaccine: 300,      # 疫苗费
                medicine: 400,     # 药品费
                testing: 200,      # 检测费
                labor: 1500,       # 人工费
                utilities: 600,    # 水电费
                land: 300,         # 土地费
                maintenance: 400   # 维护费
            }
        },
        expense_indirect: {       # 间接费用
            total: 2000,
            detail: {
                transportation: 800,  # 运输费
                management: 600,     # 管理费
                research: 300,       # 研发费
                other: 300           # 其他
            }
        },

        # 资产相关
        grass_asset: 50000,       # 草资产
        stock_asset: 30000,       # 库存资产
        fixed_asset: 80000,       # 固定资产
        profit: 7000              # 当日盈利
    }, ...]
    """
    try:
        # 获取所有有记录的日期（按时间排序）
        dates = (
            db.session.query(Analysisdailysheet.date)
                .union(db.session.query(AnalysisDailyIncome.f_date))
                .order_by(Analysisdailysheet.date)
                .distinct()
                .all()
        )

        result = []
        begin_grass_sheet = 5810147
        for date_item in dates:
            date_str = date_item[0].strftime('%Y-%m-%d')
            current_date = datetime.strptime(date_str, '%Y-%m-%d').date()

            # 1. 收入数据统计 -----------------------------------------------
            # 获取收入明细
            income_data = db.session.query(
                AnalysisDailyIncome.number_0,
                AnalysisDailyIncome.value_0,
                AnalysisDailyIncome.number_1,
                AnalysisDailyIncome.value_1,
                AnalysisDailyIncome.number_2,
                AnalysisDailyIncome.value_2,
                AnalysisDailyIncome.number_3,
                AnalysisDailyIncome.value_3,
                AnalysisDailyIncome.dung_value,
                AnalysisDailyIncome.wool_value,
                AnalysisDailyIncome.skin_value,
                AnalysisDailyIncome.manure_value,
                AnalysisDailyIncome.feed_value,
                AnalysisDailyIncome.producted_value,
                AnalysisDailyIncome.other_value
            ).filter(AnalysisDailyIncome.f_date == current_date).first()
            if not income_data:
                income_data = [0] * 15
            # 处理收入数据
            income_sales = {
                "breeding_grass": {  # 草种
                    "number": float(income_data[0]or 0) if income_data else 0,
                    "value": float(income_data[1]or 0) if income_data else 0
                },
                "fattening_grass": {  # 育成草
                    "number": float(income_data[2]or 0) if income_data else 0,
                    "value": float(income_data[3]or 0) if income_data else 0
                },
                "lamb": {  # 幼苗
                    "number": float(income_data[4]or 0) if income_data else 0,
                    "value": float(income_data[5]or 0) if income_data else 0
                },
                "other_grass": {  # 其他草
                    "number": float(income_data[6]or 0) if income_data else 0,
                    "value": float(income_data[7]or 0) if income_data else 0
                }
            } if income_data else {}

            income_byproducts = {
                "dung": float(income_data[8]or 0) if income_data else 0,
                "wool": float(income_data[9]or 0) if income_data else 0,
                "skin": float(income_data[10]or 0) if income_data else 0,
                "manure": float(income_data[11]or 0) if income_data else 0,
                "feed": float(income_data[12]or 0) if income_data else 0,
                "producted": float(income_data[13]or 0) if income_data else 0,
                "other": float(income_data[14]or 0) if income_data else 0
            } if income_data else {}


            # 计算总收入
            income_total = sum([
                income_sales.get("breeding_grass", {}).get("value", 0),
                income_sales.get("fattening_grass", {}).get("value", 0),
                income_sales.get("lamb", {}).get("value", 0),
                income_sales.get("other_grass", {}).get("value", 0),
                sum(income_byproducts.values()) if income_byproducts else 0
            ])

            # 2. 支出数据统计 -----------------------------------------------
            # 获取支出明细
            expense_data = db.session.query(
                Analysisdailysheet.buygrass_fees,
                Analysisdailysheet.caoliao_fees,
                Analysisdailysheet.jingliao_fees,
                Analysisdailysheet.yimiao_fees,
                Analysisdailysheet.yaopin_fees,
                Analysisdailysheet.test_fees,
                Analysisdailysheet.labor_fees,
                Analysisdailysheet.waterEle_fees,
                Analysisdailysheet.land_fees,
                Analysisdailysheet.maintenance_fees,
                Analysisdailysheet.cheep_fees,
                Analysisdailysheet.manage_fees,
                Analysisdailysheet.research_fees,
                Analysisdailysheet.other_fees
            ).filter(Analysisdailysheet.date == current_date).first()

            if not expense_data:
                expense_data = [0] * 14
            # 处理直接费用
            direct_detail = {
                "buygrass": float(expense_data[0]or 0) if expense_data else 0,
                "forage": float(expense_data[1]or 0) if expense_data else 0,
                "fine_fodder": float(expense_data[2]or 0) if expense_data else 0,
                "vaccine": float(expense_data[3]or 0) if expense_data else 0,
                "medicine": float(expense_data[4]or 0) if expense_data else 0,
                "testing": float(expense_data[5]or 0) if expense_data else 0,
                "labor": float(expense_data[6]or 0) if expense_data else 0,
                "utilities": float(expense_data[7]or 0) if expense_data else 0,
                "land": float(expense_data[8]or 0) if expense_data else 0,
                "maintenance": float(expense_data[9]or 0) if expense_data else 0
            } if expense_data else {}
            direct_total = sum(direct_detail.values())

            # 处理间接费用
            indirect_detail = {
                "transportation": float(expense_data[10]or 0) if expense_data else 0,
                "management": float(expense_data[11]or 0) if expense_data else 0,
                "research": float(expense_data[12]or 0) if expense_data else 0,
                "other": float(expense_data[13]or 0) if expense_data else 0
            } if expense_data else {}
            indirect_total = sum(indirect_detail.values())

            expense_total = direct_total + indirect_total

            # 3. 资产数据统计 -----------------------------------------------
            # 草资产（保持原有逻辑）
            grass_assets = db.session.query(
                *[getattr(AnalysisGrassAsset, c.name) for c in AnalysisGrassAsset.__table__.columns
                  if c.name not in ['id', 'f_date', 'belong']
                  ]).filter(AnalysisGrassAsset.f_date == current_date).first()
            grass_total = sum([float(v or 0) for v in grass_assets]) if grass_assets else 0

            # 库存资产（保持原有逻辑）
            stock_assets = db.session.query(
                *[getattr(Analysisdailystocksheet, c.name) for c in Analysisdailystocksheet.__table__.columns
                  if '_val' in c.name
                  ]).filter(Analysisdailystocksheet.date == current_date).first()
            stock_total = sum([float(v or 0) for v in stock_assets]) if stock_assets else 0

            # 汇总数据
            result.append({
                "date": date_str,
                "income_total": round(income_total, 2),
                "income_sales": income_sales,
                "income_byproducts": income_byproducts,

                "expense_total": round(expense_total, 2),
                "expense_direct": {
                    "total": round(direct_total, 2),
                    "detail": direct_detail
                },
                "expense_indirect": {
                    "total": round(indirect_total, 2),
                    "detail": indirect_detail
                },

                "grass_asset": round(grass_total, 2),
                "stock_asset": round(stock_total, 2),
                "fixed_asset": round(grass_total + stock_total, 2),
                "sub_grass_asset": round(grass_total-begin_grass_sheet, 2),
                "profit": round(income_total - expense_total + grass_total - begin_grass_sheet , 2)
            })
            begin_grass_sheet = grass_total
        return jsonify({"code": 200, "data": result})

    except Exception as e:
        return jsonify({"code": 500, "message": str(e)})




# 按月聚合
@analysis.route('/analysis/monthlyDataVisualize', methods=['POST'])
def get_monthly_financial_data():
    """
    获取整个月度数据：
      - 聚合周期内所有天的收入和支出数据（求和）
      - 资产数据取该月最后一天的数据，如果本月最后一天还未到，则使用今天的数据
      - 盈利：本月收入-支出 +（本周期最后一天草资产 - 上周期最后一天草资产）
    """
    try:
        # 从所有记录中提取日期，然后按"YYYY-MM"去重
        daily_dates = (
            db.session.query(Analysisdailysheet.date)
            .union(db.session.query(AnalysisDailyIncome.f_date))
            .all()
        )
        months_set = set()
        for d in daily_dates:
            if d[0]:
                months_set.add(d[0].strftime('%Y-%m'))
        months = sorted(list(months_set))

        result = []
        # 初始上周期的草资产
        begin_assets = 5810148

        for month in months:
            # 计算本月起始与结束日期
            start_date = datetime.strptime(month + "-01", "%Y-%m-%d").date()
            last_day = calendar.monthrange(start_date.year, start_date.month)[1]
            end_date = date(start_date.year, start_date.month, last_day)

            # 1. 收入数据聚合（按月求和）
            income_data = db.session.query(
                func.sum(AnalysisDailyIncome.number_0),
                func.sum(AnalysisDailyIncome.value_0),
                func.sum(AnalysisDailyIncome.number_1),
                func.sum(AnalysisDailyIncome.value_1),
                func.sum(AnalysisDailyIncome.number_2),
                func.sum(AnalysisDailyIncome.value_2),
                func.sum(AnalysisDailyIncome.number_3),
                func.sum(AnalysisDailyIncome.value_3),
                func.sum(AnalysisDailyIncome.dung_value),
                func.sum(AnalysisDailyIncome.wool_value),
                func.sum(AnalysisDailyIncome.skin_value),
                func.sum(AnalysisDailyIncome.manure_value),
                func.sum(AnalysisDailyIncome.feed_value),
                func.sum(AnalysisDailyIncome.producted_value),
                func.sum(AnalysisDailyIncome.other_value)
            ).filter(AnalysisDailyIncome.f_date.between(start_date, end_date)).first()

            income_sales = {
                "breeding_grass": {
                    "number": float(income_data[0] or 0),
                    "value": float(income_data[1] or 0)
                },
                "fattening_grass": {
                    "number": float(income_data[2] or 0),
                    "value": float(income_data[3] or 0)
                },
                "lamb": {
                    "number": float(income_data[4] or 0),
                    "value": float(income_data[5] or 0)
                },
                "other_grass": {
                    "number": float(income_data[6] or 0),
                    "value": float(income_data[7] or 0)
                }
            }
            income_byproducts = {
                "dung": float(income_data[8] or 0),
                "wool": float(income_data[9] or 0),
                "skin": float(income_data[10] or 0),
                "manure": float(income_data[11] or 0),
                "feed": float(income_data[12] or 0),
                "producted": float(income_data[13] or 0),
                "other": float(income_data[14] or 0)
            }
            income_total = sum([
                income_sales["breeding_grass"]["value"],
                income_sales["fattening_grass"]["value"],
                income_sales["lamb"]["value"],
                income_sales["other_grass"]["value"],
                sum(income_byproducts.values())
            ])

            # 2. 支出数据聚合（按月求和）
            expense_data = db.session.query(
                func.sum(Analysisdailysheet.buygrass_fees),
                func.sum(Analysisdailysheet.caoliao_fees),
                func.sum(Analysisdailysheet.jingliao_fees),
                func.sum(Analysisdailysheet.yimiao_fees),
                func.sum(Analysisdailysheet.yaopin_fees),
                func.sum(Analysisdailysheet.test_fees),
                func.sum(Analysisdailysheet.labor_fees),
                func.sum(Analysisdailysheet.waterEle_fees),
                func.sum(Analysisdailysheet.land_fees),
                func.sum(Analysisdailysheet.maintenance_fees),
                func.sum(Analysisdailysheet.cheep_fees),
                func.sum(Analysisdailysheet.manage_fees),
                func.sum(Analysisdailysheet.research_fees),
                func.sum(Analysisdailysheet.other_fees)
            ).filter(Analysisdailysheet.date.between(start_date, end_date)).first()

            direct_detail = {
                "buygrass": float(expense_data[0] or 0),
                "forage": float(expense_data[1] or 0),
                "fine_fodder": float(expense_data[2] or 0),
                "vaccine": float(expense_data[3] or 0),
                "medicine": float(expense_data[4] or 0),
                "testing": float(expense_data[5] or 0),
                "labor": float(expense_data[6] or 0),
                "utilities": float(expense_data[7] or 0),
                "land": float(expense_data[8] or 0),
                "maintenance": float(expense_data[9] or 0)
            }
            direct_total = sum(direct_detail.values())

            indirect_detail = {
                "transportation": float(expense_data[10] or 0),
                "management": float(expense_data[11] or 0),
                "research": float(expense_data[12] or 0),
                "other": float(expense_data[13] or 0)
            }
            indirect_total = sum(indirect_detail.values())
            expense_total = direct_total + indirect_total

            # 3. 资产数据取本周期最后一天的数据（如果还未到，则使用今天的数据）
            today_date = date.today()
            asset_date = end_date if end_date <= today_date else today_date

            print(asset_date)

            grass_assets = db.session.query(
                *[getattr(AnalysisGrassAsset, c.name)
                  for c in AnalysisGrassAsset.__table__.columns
                  if c.name not in ['id', 'f_date', 'belong']]
            ).filter(AnalysisGrassAsset.f_date == asset_date).first()
            grass_total = sum([float(v) for v in grass_assets]) if grass_assets else 0
            print(grass_total)


            stock_assets = db.session.query(
                *[getattr(Analysisdailystocksheet, c.name)
                  for c in Analysisdailystocksheet.__table__.columns
                  if '_val' in c.name]
            ).filter(Analysisdailystocksheet.date == asset_date).first()
            stock_total = sum([float(v) for v in stock_assets]) if stock_assets else 0

            # 计算本月盈利
            profit = income_total - expense_total + (grass_total - begin_assets)

            result.append({
                "date": month,
                "income_total": round(income_total, 2),
                "income_sales": income_sales,
                "income_byproducts": income_byproducts,
                "expense_total": round(expense_total, 2),
                "expense_direct": {
                    "total": round(direct_total, 2),
                    "detail": direct_detail
                },
                "expense_indirect": {
                    "total": round(indirect_total, 2),
                    "detail": indirect_detail
                },
                "grass_asset": round(grass_total, 2),
                "stock_asset": round(stock_total, 2),
                "grass_total": round(grass_total, 2),
                "sub_grass_asset": round(grass_total - begin_assets, 2),
                "fixed_asset": round(grass_total + stock_total, 2),
                "profit": round(profit, 2)
            })

            begin_assets = grass_total
            print("更新后的资产:", begin_assets)

        return jsonify({"code": 200, "data": result})
    except Exception as e:
        return jsonify({"code": 500, "message": str(e)})


# 按季度聚合
@analysis.route('/analysis/quarterlyDataVisualize', methods=['POST'])
def get_quarterly_financial_data():
    """
    获取整个季度数据：
      - 根据所有记录的日期计算所属季度（格式："YYYY-Qn"）
      - 聚合周期内数据求和，资产数据取该季度最后一天的数据（如果还未到，则取今天的数据）
      - 盈利：本季度收入-支出 +（本季度最后一天草资产 - 上季度最后一天草资产）
    """
    try:
        # 提取所有日期对应的季度标签
        daily_dates = (
            db.session.query(Analysisdailysheet.date)
            .union(db.session.query(AnalysisDailyIncome.f_date))
            .all()
        )
        quarters_set = set()
        for d in daily_dates:
            if d[0]:
                year = d[0].year
                quarter = (d[0].month - 1) // 3 + 1
                quarters_set.add(f"{year}-Q{quarter}")
        quarters = sorted(list(quarters_set))

        result = []
        begin_assets = 5810148

        for q in quarters:
            # q格式：YYYY-Qn
            year, qtr = q.split('-Q')
            year = int(year)
            quarter = int(qtr)
            # 根据季度确定起始与结束日期
            if quarter == 1:
                start_date = date(year, 1, 1)
                end_date = date(year, 3, 31)
            elif quarter == 2:
                start_date = date(year, 4, 1)
                end_date = date(year, 6, 30)
            elif quarter == 3:
                start_date = date(year, 7, 1)
                end_date = date(year, 9, 30)
            else:  # quarter == 4
                start_date = date(year, 10, 1)
                end_date = date(year, 12, 31)

            # 1. 收入数据聚合（按季度求和）
            income_data = db.session.query(
                func.sum(AnalysisDailyIncome.number_0),
                func.sum(AnalysisDailyIncome.value_0),
                func.sum(AnalysisDailyIncome.number_1),
                func.sum(AnalysisDailyIncome.value_1),
                func.sum(AnalysisDailyIncome.number_2),
                func.sum(AnalysisDailyIncome.value_2),
                func.sum(AnalysisDailyIncome.number_3),
                func.sum(AnalysisDailyIncome.value_3),
                func.sum(AnalysisDailyIncome.dung_value),
                func.sum(AnalysisDailyIncome.wool_value),
                func.sum(AnalysisDailyIncome.skin_value),
                func.sum(AnalysisDailyIncome.manure_value),
                func.sum(AnalysisDailyIncome.feed_value),
                func.sum(AnalysisDailyIncome.producted_value),
                func.sum(AnalysisDailyIncome.other_value)
            ).filter(AnalysisDailyIncome.f_date.between(start_date, end_date)).first()

            income_sales = {
                "breeding_grass": {
                    "number": float(income_data[0] or 0),
                    "value": float(income_data[1] or 0)
                },
                "fattening_grass": {
                    "number": float(income_data[2] or 0),
                    "value": float(income_data[3] or 0)
                },
                "lamb": {
                    "number": float(income_data[4] or 0),
                    "value": float(income_data[5] or 0)
                },
                "other_grass": {
                    "number": float(income_data[6] or 0),
                    "value": float(income_data[7] or 0)
                }
            }
            income_byproducts = {
                "dung": float(income_data[8] or 0),
                "wool": float(income_data[9] or 0),
                "skin": float(income_data[10] or 0),
                "manure": float(income_data[11] or 0),
                "feed": float(income_data[12] or 0),
                "producted": float(income_data[13] or 0),
                "other": float(income_data[14] or 0)
            }
            income_total = sum([
                income_sales["breeding_grass"]["value"],
                income_sales["fattening_grass"]["value"],
                income_sales["lamb"]["value"],
                income_sales["other_grass"]["value"],
                sum(income_byproducts.values())
            ])

            # 2. 支出数据聚合（按季度求和）
            expense_data = db.session.query(
                func.sum(Analysisdailysheet.buygrass_fees),
                func.sum(Analysisdailysheet.caoliao_fees),
                func.sum(Analysisdailysheet.jingliao_fees),
                func.sum(Analysisdailysheet.yimiao_fees),
                func.sum(Analysisdailysheet.yaopin_fees),
                func.sum(Analysisdailysheet.test_fees),
                func.sum(Analysisdailysheet.labor_fees),
                func.sum(Analysisdailysheet.waterEle_fees),
                func.sum(Analysisdailysheet.land_fees),
                func.sum(Analysisdailysheet.maintenance_fees),
                func.sum(Analysisdailysheet.cheep_fees),
                func.sum(Analysisdailysheet.manage_fees),
                func.sum(Analysisdailysheet.research_fees),
                func.sum(Analysisdailysheet.other_fees)
            ).filter(Analysisdailysheet.date.between(start_date, end_date)).first()

            direct_detail = {
                "buygrass": float(expense_data[0] or 0),
                "forage": float(expense_data[1] or 0),
                "fine_fodder": float(expense_data[2] or 0),
                "vaccine": float(expense_data[3] or 0),
                "medicine": float(expense_data[4] or 0),
                "testing": float(expense_data[5] or 0),
                "labor": float(expense_data[6] or 0),
                "utilities": float(expense_data[7] or 0),
                "land": float(expense_data[8] or 0),
                "maintenance": float(expense_data[9] or 0)
            }
            direct_total = sum(direct_detail.values())

            indirect_detail = {
                "transportation": float(expense_data[10] or 0),
                "management": float(expense_data[11] or 0),
                "research": float(expense_data[12] or 0),
                "other": float(expense_data[13] or 0)
            }
            indirect_total = sum(indirect_detail.values())
            expense_total = direct_total + indirect_total

            # 3. 资产数据取本周期最后一天的数据（如果还未到，则使用今天的数据）
            today_date = date.today()
            asset_date = end_date if end_date <= today_date else today_date

            grass_assets = db.session.query(
                *[getattr(AnalysisGrassAsset, c.name)
                  for c in AnalysisGrassAsset.__table__.columns
                  if c.name not in ['id', 'f_date', 'belong']]
            ).filter(AnalysisGrassAsset.f_date == asset_date).first()
            grass_total = sum([float(v) for v in grass_assets]) if grass_assets else 0

            stock_assets = db.session.query(
                *[getattr(Analysisdailystocksheet, c.name)
                  for c in Analysisdailystocksheet.__table__.columns
                  if '_val' in c.name]
            ).filter(Analysisdailystocksheet.date == asset_date).first()
            stock_total = sum([float(v) for v in stock_assets]) if stock_assets else 0

            profit = income_total - expense_total + (grass_total - begin_assets)

            result.append({
                "date": q,  # 如 "2025-Q1"
                "income_total": round(income_total, 2),
                "income_sales": income_sales,
                "income_byproducts": income_byproducts,
                "expense_total": round(expense_total, 2),
                "expense_direct": {
                    "total": round(direct_total, 2),
                    "detail": direct_detail
                },
                "expense_indirect": {
                    "total": round(indirect_total, 2),
                    "detail": indirect_detail
                },
                "grass_asset": round(grass_total, 2),
                "stock_asset": round(stock_total, 2),
                "sub_grass_asset": round(grass_total - begin_assets, 2),
                "fixed_asset": round(grass_total + stock_total, 2),
                "profit": round(profit, 2)
            })

            begin_assets = grass_total

        return jsonify({"code": 200, "data": result})
    except Exception as e:
        return jsonify({"code": 500, "message": str(e)})


# 按年度聚合
@analysis.route('/analysis/annualDataVisualize', methods=['POST'])
def get_annual_financial_data():
    """
    获取整年度数据：
      - 根据所有记录日期提取年份（格式："YYYY"）
      - 聚合当年所有数据，资产数据取该年最后一天（12月31日）的数据（如果还未到，则使用今天的数据）
      - 盈利：本年收入-支出 +（本年最后一天草资产 - 上年最后一天草资产）
    """
    try:
        # 提取所有年份
        daily_dates = (
            db.session.query(Analysisdailysheet.date)
            .union(db.session.query(AnalysisDailyIncome.f_date))
            .all()
        )
        years_set = set()
        for d in daily_dates:
            if d[0]:
                years_set.add(d[0].strftime('%Y'))
        years = sorted(list(years_set))

        result = []
        begin_assets = 5810148

        for yr in years:
            year_int = int(yr)
            start_date = date(year_int, 1, 1)
            end_date = date(year_int, 12, 31)

            # 1. 收入数据聚合（按年求和）
            income_data = db.session.query(
                func.sum(AnalysisDailyIncome.number_0),
                func.sum(AnalysisDailyIncome.value_0),
                func.sum(AnalysisDailyIncome.number_1),
                func.sum(AnalysisDailyIncome.value_1),
                func.sum(AnalysisDailyIncome.number_2),
                func.sum(AnalysisDailyIncome.value_2),
                func.sum(AnalysisDailyIncome.number_3),
                func.sum(AnalysisDailyIncome.value_3),
                func.sum(AnalysisDailyIncome.dung_value),
                func.sum(AnalysisDailyIncome.wool_value),
                func.sum(AnalysisDailyIncome.skin_value),
                func.sum(AnalysisDailyIncome.manure_value),
                func.sum(AnalysisDailyIncome.feed_value),
                func.sum(AnalysisDailyIncome.producted_value),
                func.sum(AnalysisDailyIncome.other_value)
            ).filter(AnalysisDailyIncome.f_date.between(start_date, end_date)).first()

            income_sales = {
                "breeding_grass": {
                    "number": float(income_data[0] or 0),
                    "value": float(income_data[1] or 0)
                },
                "fattening_grass": {
                    "number": float(income_data[2] or 0),
                    "value": float(income_data[3] or 0)
                },
                "lamb": {
                    "number": float(income_data[4] or 0),
                    "value": float(income_data[5] or 0)
                },
                "other_grass": {
                    "number": float(income_data[6] or 0),
                    "value": float(income_data[7] or 0)
                }
            }
            income_byproducts = {
                "dung": float(income_data[8] or 0),
                "wool": float(income_data[9] or 0),
                "skin": float(income_data[10] or 0),
                "manure": float(income_data[11] or 0),
                "feed": float(income_data[12] or 0),
                "producted": float(income_data[13] or 0),
                "other": float(income_data[14] or 0)
            }
            income_total = sum([
                income_sales["breeding_grass"]["value"],
                income_sales["fattening_grass"]["value"],
                income_sales["lamb"]["value"],
                income_sales["other_grass"]["value"],
                sum(income_byproducts.values())
            ])

            # 2. 支出数据聚合（按年求和）
            expense_data = db.session.query(
                func.sum(Analysisdailysheet.buygrass_fees),
                func.sum(Analysisdailysheet.caoliao_fees),
                func.sum(Analysisdailysheet.jingliao_fees),
                func.sum(Analysisdailysheet.yimiao_fees),
                func.sum(Analysisdailysheet.yaopin_fees),
                func.sum(Analysisdailysheet.test_fees),
                func.sum(Analysisdailysheet.labor_fees),
                func.sum(Analysisdailysheet.waterEle_fees),
                func.sum(Analysisdailysheet.land_fees),
                func.sum(Analysisdailysheet.maintenance_fees),
                func.sum(Analysisdailysheet.cheep_fees),
                func.sum(Analysisdailysheet.manage_fees),
                func.sum(Analysisdailysheet.research_fees),
                func.sum(Analysisdailysheet.other_fees)
            ).filter(Analysisdailysheet.date.between(start_date, end_date)).first()

            direct_detail = {
                "buygrass": float(expense_data[0] or 0),
                "forage": float(expense_data[1] or 0),
                "fine_fodder": float(expense_data[2] or 0),
                "vaccine": float(expense_data[3] or 0),
                "medicine": float(expense_data[4] or 0),
                "testing": float(expense_data[5] or 0),
                "labor": float(expense_data[6] or 0),
                "utilities": float(expense_data[7] or 0),
                "land": float(expense_data[8] or 0),
                "maintenance": float(expense_data[9] or 0)
            }
            direct_total = sum(direct_detail.values())

            indirect_detail = {
                "transportation": float(expense_data[10] or 0),
                "management": float(expense_data[11] or 0),
                "research": float(expense_data[12] or 0),
                "other": float(expense_data[13] or 0)
            }
            indirect_total = sum(indirect_detail.values())
            expense_total = direct_total + indirect_total

            # 3. 资产数据取该年最后一天（12月31日）的数据，如果还未到，则使用今天的数据
            today_date = date.today()
            asset_date = end_date if end_date <= today_date else today_date

            grass_assets = db.session.query(
                *[getattr(AnalysisGrassAsset, c.name)
                  for c in AnalysisGrassAsset.__table__.columns
                  if c.name not in ['id', 'f_date', 'belong']]
            ).filter(AnalysisGrassAsset.f_date == asset_date).first()
            grass_total = sum([float(v) for v in grass_assets]) if grass_assets else 0

            stock_assets = db.session.query(
                *[getattr(Analysisdailystocksheet, c.name)
                  for c in Analysisdailystocksheet.__table__.columns
                  if '_val' in c.name]
            ).filter(Analysisdailystocksheet.date == asset_date).first()
            stock_total = sum([float(v) for v in stock_assets]) if stock_assets else 0

            profit = income_total - expense_total + (grass_total - begin_assets)

            result.append({
                "date": yr,
                "income_total": round(income_total, 2),
                "income_sales": income_sales,
                "income_byproducts": income_byproducts,
                "expense_total": round(expense_total, 2),
                "expense_direct": {
                    "total": round(direct_total, 2),
                    "detail": direct_detail
                },
                "expense_indirect": {
                    "total": round(indirect_total, 2),
                    "detail": indirect_detail
                },
                "grass_asset": round(grass_total, 2),
                "stock_asset": round(stock_total, 2),
                "sub_grass_asset": round(grass_total - begin_assets, 2),
                "fixed_asset": round(grass_total + stock_total, 2),
                "profit": round(profit, 2)
            })

            begin_assets = grass_total

        return jsonify({"code": 200, "data": result})
    except Exception as e:
        return jsonify({"code": 500, "message": str(e)})


@analysis.route('/analysis/daily_income/edit', methods=['POST'])
def edit_daily_income():
    data = request.get_json()
    id = data['id']
    try:
        AnalysisDailyIncome.query.filter_by(id=id).update(data)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        result = {
            "code": 500,
            "msg": f'修改失败 {str(e)}'
        }
        return jsonify(result)
    result = {
        "code": 200,
        "msg": '修改成功'
    }
    return jsonify(result)


@analysis.route('/analysis/daily_income/del', methods=['POST'])
def del_daily_income():
    ids = request.get_json()
    for i in ids:
        AnalysisDailyIncome.query.filter_by(id=i).delete()
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        result = {
            "code": 500,
            "msg": f'删除失败 {str(e)}'
        }
        return jsonify(result)
    return jsonify({
        "code": 200,
        "msg": '删除成功'
    })


@analysis.route('/analysis/daily_grass_asset/edit', methods=['POST'])
def edit_daily_grass_asset():
    data = request.get_json()
    id = data['id']
    try:
        AnalysisGrassAsset.query.filter_by(id=id).update(data)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        result = {
            "code": 500,
            "msg": f'修改失败 {str(e)}'
        }
        return jsonify(result)
    result = {
        "code": 200,
        "msg": '修改成功'
    }
    return jsonify(result)


@analysis.route('/analysis/daily_grass_asset/del', methods=['POST'])
def del_daily_grass_asset():
    ids = request.get_json()
    for i in ids:
        AnalysisGrassAsset.query.filter_by(id=i).delete()
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        result = {
            "code": 500,
            "msg": f'删除失败 {str(e)}'
        }
        return jsonify(result)
    return jsonify({
        "code": 200,
        "msg": '删除成功'
    })


@analysis.route('/analysis/daily_stocksheet/searchDate', methods=['POST'])
def search_date_stocksheet():
    data = request.get_json()
    sheet = Analysisdailystocksheet.query.filter_by(date=data['date']).all()
    if sheet:
        result = {
            "code": 200,
            "msg": '经查询得知相同日期已经存在一次记录，继续增加则在之前基础上累加！'
        }
        return jsonify(result)
    else:
        result = {
            "code": 200,
            "msg": '未查询到相同日期的记录，请继续添加！'
        }
        return jsonify(result)
