# views.py: 路由 + 视图函数
import datetime
import random
import json

from flask import Blueprint, render_template, request, make_response, Response, redirect, url_for, session, jsonify, \
    send_file
from sqlalchemy import desc, and_, or_, not_
import pandas as pd

# from .models import *
from ..modelsReverse import *
from ..utils.AlchemyEncoder import AlchemyEncoder

# 蓝图
supply = Blueprint('supply', __name__)


@supply.route('/supply/v_suppliersinfo', methods=['POST'])
def get_v_suppliers_info():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        'supplier_name': SupplyVSuppliersinfo.supplier_name,
        'sale_type': SupplyVSuppliersinfo.sale_type,
        'sup_linkman': SupplyVSuppliersinfo.sup_linkman,
        'sup_contact': SupplyVSuppliersinfo.sup_contact,
        'contact': SupplyVSuppliersinfo.contact,
        'mail': SupplyVSuppliersinfo.mail,
        'address': SupplyVSuppliersinfo.address,
        'operation': SupplyVSuppliersinfo.operation,
        'f_staff': SupplyVSuppliersinfo.f_staff,
        'f_date': SupplyVSuppliersinfo.f_date,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'f_date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = SupplyVSuppliersinfo.query.filter(and_(*conditions))
    else:
        query = SupplyVSuppliersinfo.query  # 如果没有条件，查询所有

    # 并且根据id降序排列

    query = query.filter(SupplyVSuppliersinfo.belong == 0)
    infos = query.order_by(desc(SupplyVSuppliersinfo.id)).paginate(page=pageNum, per_page=pageSize,
                                                                   error_out=False)
    total = query.count()

    list = []
    for info in infos:
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


@supply.route('/supply/v_suppliersinfo/add', methods=['POST'])
def add_v_suppliers_info():
    data = request.get_json()
    ctime = datetime.now()
    # belong为0
    data['belong'] = 0
    data['f_date'] = ctime
    print(data)
    info = SupplyVSuppliersinfo()
    for key, value in data.items():
        setattr(info, key, value)
    try:
        db.session.add(info)
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


# http://127.0.0.1:5000/basic/basicinfo/edit
@supply.route('/supply/v_suppliersinfo/edit', methods=['POST'])
def edit_v_suppliers_info():
    data = request.get_json()
    # print("--data-->", data)
    SupplyVSuppliersinfo.query.filter_by(id=data['id']).update(data)
    try:
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

@supply.route('/supply/v_suppliersinfo/del', methods=['POST'])
def del_v_suppliers_info():
    ids = request.get_json()
    for i in ids:
        SupplyVSuppliersinfo.query.filter_by(id=i).delete()
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

@supply.route('/supply/f_suppliersinfo', methods=['POST'])
def get_f_suppliers_info():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        'supplier_name': SupplyFSuppliersinfo.supplier_name,
        'sale_type': SupplyFSuppliersinfo.sale_type,
        'sup_linkman': SupplyFSuppliersinfo.sup_linkman,
        'sup_contact': SupplyFSuppliersinfo.sup_contact,
        'contact': SupplyFSuppliersinfo.contact,
        'mail': SupplyFSuppliersinfo.mail,
        'address': SupplyFSuppliersinfo.address,
        'operation': SupplyFSuppliersinfo.operation,
        'f_staff': SupplyFSuppliersinfo.f_staff,
        'f_date': SupplyFSuppliersinfo.f_date,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'f_date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = SupplyFSuppliersinfo.query.filter(and_(*conditions))
    else:
        query = SupplyFSuppliersinfo.query  # 如果没有条件，查询所有

    # 并且根据id降序排列

    query = query.filter(SupplyFSuppliersinfo.belong == 0)
    infos = query.order_by(desc(SupplyFSuppliersinfo.id)).paginate(page=pageNum, per_page=pageSize,
                                                                   error_out=False)
    total = query.count()

    list = []
    for info in infos:
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


@supply.route('/supply/f_suppliersinfo/add', methods=['POST'])
def add_f_suppliers_info():
    data = request.get_json()
    ctime = datetime.now()
    # belong为0
    data['belong'] = 0
    data['f_date'] = ctime
    print(data)
    info = SupplyFSuppliersinfo()
    for key, value in data.items():
        setattr(info, key, value)
    try:
        db.session.add(info)
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


# http://127.0.0.1:5000/basic/basicinfo/edit
@supply.route('/supply/f_suppliersinfo/edit', methods=['POST'])
def edit_f_suppliers_info():
    data = request.get_json()
    # print("--data-->", data)
    SupplyFSuppliersinfo.query.filter_by(id=data['id']).update(data)
    try:
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

@supply.route('/supply/f_suppliersinfo/del', methods=['POST'])
def del_f_suppliers_info():
    ids = request.get_json()
    for i in ids:
        SupplyFSuppliersinfo.query.filter_by(id=i).delete()
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



@supply.route('/supply/insuranceinfo', methods=['POST'])
def get_insurance_info():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        'in_name': SupplyInsuranceinfo.in_name,
        'contact': SupplyInsuranceinfo.contact,
        'mail': SupplyInsuranceinfo.mail,
        'handler': SupplyInsuranceinfo.handler,
        'link': SupplyInsuranceinfo.link,
        'f_staff': SupplyInsuranceinfo.f_staff,
        'f_date': SupplyInsuranceinfo.f_date,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'f_date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = SupplyInsuranceinfo.query.filter(and_(*conditions))
    else:
        query = SupplyInsuranceinfo.query  # 如果没有条件，查询所有

    # 并且根据id降序排列

    query = query.filter(SupplyInsuranceinfo.belong == 0)
    infos = query.order_by(desc(SupplyInsuranceinfo.id)).paginate(page=pageNum, per_page=pageSize,
                                                                   error_out=False)
    total = query.count()

    list = []
    for info in infos:
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


@supply.route('/supply/insuranceinfo/add', methods=['POST'])
def add_insurance_info():
    data = request.get_json()
    ctime = datetime.now()
    # belong为0
    data['belong'] = 0
    data['f_date'] = ctime
    print(data)
    info = SupplyInsuranceinfo()
    for key, value in data.items():
        setattr(info, key, value)
    try:
        db.session.add(info)
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


# http://127.0.0.1:5000/basic/basicinfo/edit
@supply.route('/supply/insuranceinfo/edit', methods=['POST'])
def edit_insurance_info():
    data = request.get_json()
    # print("--data-->", data)
    SupplyInsuranceinfo.query.filter_by(id=data['id']).update(data)
    try:
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

@supply.route('/supply/insuranceinfo/del', methods=['POST'])
def del_insurance_info():
    ids = request.get_json()
    for i in ids:
        SupplyInsuranceinfo.query.filter_by(id=i).delete()
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


@supply.route('/supply/commodityinfo', methods=['POST'])
def get_commodity_info():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        'type': SupplyCommodityinfo.type,
        'cname': SupplyCommodityinfo.cname,
        'explain': SupplyCommodityinfo.explain,
        'f_staff': SupplyCommodityinfo.f_staff,
        # 这个表没有f_date
        # 'f_date': SupplyCommodityinfo.f_date,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'f_date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            elif param == 'explain':
                conditions.append(column.like(f'%{value}%'))
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = SupplyCommodityinfo.query.filter(and_(*conditions))
    else:
        query = SupplyCommodityinfo.query  # 如果没有条件，查询所有

    # 并且根据id降序排列

    query = query.filter(SupplyCommodityinfo.belong == 0)
    infos = query.order_by(desc(SupplyCommodityinfo.id)).paginate(page=pageNum, per_page=pageSize,
                                                                   error_out=False)
    total = query.count()

    list = []
    for info in infos:
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


@supply.route('/supply/commodityinfo/add', methods=['POST'])
def add_commodity_info():
    data = request.get_json()
    ctime = datetime.now()
    # belong为0
    data['belong'] = 0
    data['f_date'] = ctime
    print(data)
    info = SupplyCommodityinfo()
    for key, value in data.items():
        setattr(info, key, value)
    try:
        db.session.add(info)
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


# http://127.0.0.1:5000/basic/basicinfo/edit
@supply.route('/supply/commodityinfo/edit', methods=['POST'])
def edit_commodity_info():
    data = request.get_json()
    # print("--data-->", data)
    SupplyCommodityinfo.query.filter_by(id=data['id']).update(data)
    try:
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

@supply.route('/supply/commodityinfo/del', methods=['POST'])
def del_commodity_info():
    ids = request.get_json()
    for i in ids:
        SupplyCommodityinfo.query.filter_by(id=i).delete()
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
