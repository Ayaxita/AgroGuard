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

g_slaughter = Blueprint('g_slaughter', __name__)


@g_slaughter.route('/g_slaughter/s_salesinfo', methods=['POST'])#草只销售
def get_s_salesinfo():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        'sales_date': GSlaughterSSalesinfo.sales_date,
        'sales_order': GSlaughterSSalesinfo.sales_order,
        'type': GSlaughterSSalesinfo.type,
        'quarantine_coding': GSlaughterSSalesinfo.quarantine_coding,
        'ele_num': GSlaughterSSalesinfo.ele_num,
        'age': GSlaughterSSalesinfo.age,
        'medical_leave': GSlaughterSSalesinfo.medical_leave,
        'billing_unit': GSlaughterSSalesinfo.billing_unit,
        'unit_price': GSlaughterSSalesinfo.unit_price,
        'weight':GSlaughterSSalesinfo.weight,
        'total_price': GSlaughterSSalesinfo.total_price,
        'transportation': GSlaughterSSalesinfo.transportation,
        'sales_site': GSlaughterSSalesinfo.sales_site,
        'name': GSlaughterSSalesinfo.name,
        'buyer': GSlaughterSSalesinfo.buyer,
        'buyer_phone': GSlaughterSSalesinfo.buyer_phone,
        'selling_type': GSlaughterSSalesinfo.selling_type,
        'notes': GSlaughterSSalesinfo.notes,
        'f_staff': GSlaughterSSalesinfo.f_staff,
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
        query = GSlaughterSSalesinfo.query.filter(and_(*conditions))
    else:
        query = GSlaughterSSalesinfo.query  # 如果没有条件，查询所有

    # 根据id降序排列

    query = query.filter(GSlaughterSSalesinfo.belong == 0)
    data_infos = query.order_by(desc(GSlaughterSSalesinfo.id)).paginate(page=pageNum, per_page=pageSize,
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

# @g_slaughter.route('/g_slaughter/s_salesinfo/add', methods=['POST'])#  新增
# def add_s_salesinfo():
#     data = request.get_json()
#
#     ctime = datetime.now()
#     data['belong'] = 0
#     data['f_date'] = ctime
#
#
#     data_info= GSlaughterSSalesinfo()
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

@g_slaughter.route('/g_slaughter/s_salesinfo/edit', methods=['POST'])#  编辑
def edit_s_salesinfo():
    data = request.get_json()
    print("--data-->", data)
    id = data['id']

    # BasicBasicinfo.query.filter_by(ele_id = ele_id,pre_id = pre_id).update(data)
    try:
        # 更新
        GSlaughterSSalesinfo.query.filter_by(id=id).update(data)
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


@g_slaughter.route('/g_slaughter/g_salesinfo', methods=['POST'])#草副产品销售
def get_g_salesinfo():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        'sales_date': GSlaughterGSalesinfo.sales_date,
        'sales_order': GSlaughterGSalesinfo.sales_order,
        'type': GSlaughterGSalesinfo.type,
        # 'quarantine_coding': GSlaughterGSalesinfo.quarantine_coding,
        # 'ele_num': GSlaughterGSalesinfo.ele_num,
        # 'age': GSlaughterGSalesinfo.age,
        # 'medical_leave': GSlaughterGSalesinfo.medical_leave,
        'billing_unit': GSlaughterGSalesinfo.billing_unit,
        'unit_price': GSlaughterGSalesinfo.unit_price,
        'weight':GSlaughterGSalesinfo.weight,
        'total_price': GSlaughterGSalesinfo.total_price,
        'transportation': GSlaughterGSalesinfo.transportation,
        'sales_site': GSlaughterGSalesinfo.sales_site,
        'name': GSlaughterGSalesinfo.name,
        'buyer': GSlaughterGSalesinfo.buyer,
        'buyer_phone': GSlaughterGSalesinfo.buyer_phone,
        'selling_type': GSlaughterGSalesinfo.selling_type,
        'notes': GSlaughterGSalesinfo.notes,
        'f_staff': GSlaughterGSalesinfo.f_staff,
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
        query = GSlaughterGSalesinfo.query.filter(and_(*conditions))
    else:
        query = GSlaughterGSalesinfo.query  # 如果没有条件，查询所有

    # 根据id降序排列

    query = query.filter(GSlaughterGSalesinfo.belong == 0)
    print(query)
    data_infos = query.order_by(desc(GSlaughterGSalesinfo.id)).paginate(page=pageNum, per_page=pageSize,
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


@g_slaughter.route('/g_slaughter/g_salesinfo/add', methods=['POST'])#  新增
def add_g_salesinfo():
    data = request.get_json()

    ctime = datetime.now()
    data['belong'] = 0
    data['f_date'] = ctime


    data_info= GSlaughterGSalesinfo()

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

@g_slaughter.route('/g_slaughter/g_salesinfo/edit', methods=['POST'])#  编辑
def edit_g_salesinfo():
    data = request.get_json()
    print("--data-->", data)
    id = data['id']

    # BasicBasicinfo.query.filter_by(ele_id = ele_id,pre_id = pre_id).update(data)
    try:
        # 更新
        GSlaughterGSalesinfo.query.filter_by(id=id).update(data)
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

@g_slaughter.route('/g_slaughter/g_salesinfo/del', methods=['POST'])#  删除
def del_g_saleinfo():
    ids = request.get_json()
    print("______________________________________")
    print(ids)
    for i in ids:
        GSlaughterGSalesinfo.query.filter_by(id=i).delete()
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