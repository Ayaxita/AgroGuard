# views.py: 路由 + 视图函数
import datetime
import random

from flask import Blueprint, render_template, request, make_response, Response, redirect, url_for, session, jsonify, \
    send_file
from sqlalchemy import desc, and_, or_, not_
import pandas as pd

from ..modelsReverse import *
import json
from ..utils.AlchemyEncoder import AlchemyEncoder

g_harvest = Blueprint('g_harvest', __name__)


@g_harvest.route('/g_harvest/s_salesinfo', methods=['POST'])#草只销售
def get_s_salesinfo():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        'sales_date': GHarvestSSalesinfo.sales_date,
        'sales_order': GHarvestSSalesinfo.sales_order,
        'type': GHarvestSSalesinfo.type,
        'quarantine_coding': GHarvestSSalesinfo.quarantine_coding,
        'ele_num': GHarvestSSalesinfo.ele_num,
        'age': GHarvestSSalesinfo.age,
        'medical_leave': GHarvestSSalesinfo.medical_leave,
        'billing_unit': GHarvestSSalesinfo.billing_unit,
        'unit_price': GHarvestSSalesinfo.unit_price,
        'weight':GHarvestSSalesinfo.weight,
        'total_price': GHarvestSSalesinfo.total_price,
        'transportation': GHarvestSSalesinfo.transportation,
        'sales_site': GHarvestSSalesinfo.sales_site,
        'name': GHarvestSSalesinfo.name,
        'buyer': GHarvestSSalesinfo.buyer,
        'buyer_phone': GHarvestSSalesinfo.buyer_phone,
        'selling_type': GHarvestSSalesinfo.selling_type,
        'notes': GHarvestSSalesinfo.notes,
        'f_staff': GHarvestSSalesinfo.f_staff,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'sales_date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = GHarvestSSalesinfo.query.filter(and_(*conditions))
    else:
        query = GHarvestSSalesinfo.query  # 如果没有条件，查询所有

    # 根据id降序排列

    query = query.filter(GHarvestSSalesinfo.belong == 0)
    data_infos = query.order_by(desc(GHarvestSSalesinfo.id)).paginate(page=pageNum, per_page=pageSize,
                                                                          error_out=False)
    total = query.count()

    list = []
    for info in data_infos:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        list.append(json.loads(data))
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

# @g_harvest.route('/g_harvest/s_salesinfo/add', methods=['POST'])#  新增
# def add_s_salesinfo():
#     data = request.get_json()
#
#     ctime = datetime.now()
#     data['belong'] = 0
#     data['f_date'] = ctime
#
#
#     data_info= GHarvestSSalesinfo()
#
#     for key, value in data.items():#将data字典里的数据添加到实例对象中
#         setattr(data_info, key, value)
#     try:
#         db.session.add(data_info)
#         db.session.commit()
#     except Exception as e:
#         db.session.rollback()
#         db.session.flush()
#         result = {
#             "code": 500,
#             "msg": f'添加失败 {str(e)}'
#         }
#         return jsonify(result)
#     result = {
#         "code": 200,
#         "msg": '添加成功'
#     }
#     return jsonify(result)

@g_harvest.route('/g_harvest/s_salesinfo/edit', methods=['POST'])#  编辑
def edit_s_salesinfo():
    data = request.get_json()
    print("--data-->", data)
    id = data['id']

    # BasicBasicinfo.query.filter_by(ele_id = ele_id,pre_id = pre_id).update(data)
    try:
        # 更新
        GHarvestSSalesinfo.query.filter_by(id=id).update(data)
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


@g_harvest.route('/g_harvest/g_salesinfo', methods=['POST'])#草副产品销售
def get_g_salesinfo():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        'sales_date': GHarvestGSalesinfo.sales_date,
        'sales_order': GHarvestGSalesinfo.sales_order,
        'type': GHarvestGSalesinfo.type,
        # 'quarantine_coding': GHarvestGSalesinfo.quarantine_coding,
        # 'ele_num': GHarvestGSalesinfo.ele_num,
        # 'age': GHarvestGSalesinfo.age,
        # 'medical_leave': GHarvestGSalesinfo.medical_leave,
        'billing_unit': GHarvestGSalesinfo.billing_unit,
        'unit_price': GHarvestGSalesinfo.unit_price,
        'weight':GHarvestGSalesinfo.weight,
        'total_price': GHarvestGSalesinfo.total_price,
        'transportation': GHarvestGSalesinfo.transportation,
        'sales_site': GHarvestGSalesinfo.sales_site,
        'name': GHarvestGSalesinfo.name,
        'buyer': GHarvestGSalesinfo.buyer,
        'buyer_phone': GHarvestGSalesinfo.buyer_phone,
        'selling_type': GHarvestGSalesinfo.selling_type,
        'notes': GHarvestGSalesinfo.notes,
        'f_staff': GHarvestGSalesinfo.f_staff,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'sales_date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = GHarvestGSalesinfo.query.filter(and_(*conditions))
    else:
        query = GHarvestGSalesinfo.query  # 如果没有条件，查询所有

    # 根据id降序排列

    query = query.filter(GHarvestGSalesinfo.belong == 0)
    print(query)
    data_infos = query.order_by(desc(GHarvestGSalesinfo.id)).paginate(page=pageNum, per_page=pageSize,
                                                                          error_out=False)
    print(data_infos)
    total = query.count()
    print(total)

    list = []
    for info in data_infos:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        list.append(json.loads(data))
        print(f'data{data}')
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


@g_harvest.route('/g_harvest/g_salesinfo/add', methods=['POST'])#  新增
def add_g_salesinfo():
    data = request.get_json()

    ctime = datetime.now()
    data['belong'] = 0
    data['f_date'] = ctime


    data_info= GHarvestGSalesinfo()

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

@g_harvest.route('/g_harvest/g_salesinfo/edit', methods=['POST'])#  编辑
def edit_g_salesinfo():
    data = request.get_json()
    print("--data-->", data)
    id = data['id']

    # BasicBasicinfo.query.filter_by(ele_id = ele_id,pre_id = pre_id).update(data)
    try:
        # 更新
        GHarvestGSalesinfo.query.filter_by(id=id).update(data)
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

@g_harvest.route('/g_harvest/g_salesinfo/del', methods=['POST'])#  删除
def del_g_saleinfo():
    ids = request.get_json()
    print("______________________________________")
    print(ids)
    for i in ids:
        GHarvestGSalesinfo.query.filter_by(id=i).delete()
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