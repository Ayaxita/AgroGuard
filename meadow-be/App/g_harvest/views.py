# views.py: 路由 + 视图函数
from datetime import datetime
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

@g_harvest.route('/g_harvest/binformationinfo', methods=['POST'])
def get_g_harvest_binformationinfo_list():
    pageNum = int(request.json.get('pageNum', 1))
    pageSize = int(request.json.get('pageSize', 10))
    conditions = []
    search_params = {
        'belong': GHarvestBinformationinfo.belong,
        'date': GHarvestBinformationinfo.date,
        'month': GHarvestBinformationinfo.month,
        'basic_id': GHarvestBinformationinfo.basic_id,
        'variety': GHarvestBinformationinfo.variety,
        'source': GHarvestBinformationinfo.source,
        'back_fat_thickness': GHarvestBinformationinfo.back_fat_thickness,
        'net_meat_ratio': GHarvestBinformationinfo.net_meat_ratio,
        'CWT': GHarvestBinformationinfo.CWT,
        'emuscle_area': GHarvestBinformationinfo.emuscle_area,
        'back_thickness': GHarvestBinformationinfo.back_thickness,
        'level': GHarvestBinformationinfo.level,
        'recorder': GHarvestBinformationinfo.recorder,
        'notes': GHarvestBinformationinfo.notes,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:
            conditions.append(column == value)
    if conditions:
        query = GHarvestBinformationinfo.query.filter(and_(*conditions))
    else:
        query = GHarvestBinformationinfo.query
    infos = query.filter(GHarvestBinformationinfo.belong == 0).paginate(page=pageNum, per_page=pageSize, error_out=False)
    total = query.count()
    list = []
    for info in infos:
        list.append({
            'id': info.id,
            'belong': info.belong,
            'date': info.date,
            'month': info.month,
            'basic_id': info.basic_id,
            'variety': info.variety,
            'source': info.source,
            'back_fat_thickness': info.back_fat_thickness,
            'net_meat_ratio': info.net_meat_ratio,
            'CWT': info.CWT,
            'emuscle_area': info.emuscle_area,
            'back_thickness': info.back_thickness,
            'level': info.level,
            'recorder': info.recorder,
            'notes': info.notes,
        })
    result = {"code": 200, "data": {"list": list, "pageNum": pageNum, "pageSize": pageSize, "total": total}, "msg": '成功'}
    return jsonify(result)


@g_harvest.route('/g_harvest/binformationinfo/add', methods=['POST'])
def add_g_harvest_binformationinfo():
    data = request.get_json()
    data['belong'] = 0
    obj = GHarvestBinformationinfo()
    for key, value in data.items():
        if hasattr(obj, key):
            setattr(obj, key, value)
    try:
        db.session.add(obj)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        return jsonify({"code": 500, "msg": f'添加失败 {str(e)}'})
    return jsonify({"code": 200, "msg": '添加成功'})


@g_harvest.route('/g_harvest/binformationinfo/edit', methods=['POST'])
def edit_g_harvest_binformationinfo():
    data = request.get_json()
    id = data.get('id')
    if not id:
        return jsonify({"code": 400, "msg": '缺少id'})
    GHarvestBinformationinfo.query.filter_by(id=id).update(data)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        return jsonify({"code": 500, "msg": f'修改失败 {str(e)}'})
    return jsonify({"code": 200, "msg": '修改成功'})


@g_harvest.route('/g_harvest/binformationinfo/del', methods=['POST'])
def del_g_harvest_binformationinfo():
    data = request.get_json()
    id = data.get('id')
    if not id:
        return jsonify({"code": 400, "msg": '缺少id'})
    obj = GHarvestBinformationinfo.query.get(id)
    if not obj:
        return jsonify({"code": 404, "msg": '记录不存在'})
    try:
        db.session.delete(obj)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        return jsonify({"code": 500, "msg": f'删除失败 {str(e)}'})
    return jsonify({"code": 200, "msg": '删除成功'})


@g_harvest.route('/g_harvest/economicinfo', methods=['POST'])
def get_g_harvest_economicinfo_list():
    pageNum = int(request.json.get('pageNum', 1))
    pageSize = int(request.json.get('pageSize', 10))
    conditions = []
    search_params = {
        'belong': GHarvestEconomicinfo.belong,
        'basic_id': GHarvestEconomicinfo.basic_id,
        'age': GHarvestEconomicinfo.age,
        'house_id': GHarvestEconomicinfo.house_id,
        'in_weight': GHarvestEconomicinfo.in_weight,
        'in_1_5': GHarvestEconomicinfo.in_1_5,
        'in_3': GHarvestEconomicinfo.in_3,
        'in_4_5': GHarvestEconomicinfo.in_4_5,
        'out_weight': GHarvestEconomicinfo.out_weight,
        'put_volume': GHarvestEconomicinfo.put_volume,
        'intake': GHarvestEconomicinfo.intake,
        'menu': GHarvestEconomicinfo.menu,
        'cost': GHarvestEconomicinfo.cost,
        'FCR': GHarvestEconomicinfo.FCR,
        'ADG': GHarvestEconomicinfo.ADG,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:
            conditions.append(column == value)
    if conditions:
        query = GHarvestEconomicinfo.query.filter(and_(*conditions))
    else:
        query = GHarvestEconomicinfo.query
    infos = query.filter(GHarvestEconomicinfo.belong == 0).paginate(page=pageNum, per_page=pageSize, error_out=False)
    total = query.count()
    list = []
    for info in infos:
        list.append({
            'id': info.id,
            'belong': info.belong,
            'basic_id': info.basic_id,
            'age': info.age,
            'house_id': info.house_id,
            'in_weight': info.in_weight,
            'in_1_5': info.in_1_5,
            'in_3': info.in_3,
            'in_4_5': info.in_4_5,
            'out_weight': info.out_weight,
            'put_volume': info.put_volume,
            'intake': info.intake,
            'menu': info.menu,
            'cost': info.cost,
            'FCR': info.FCR,
            'ADG': info.ADG,
        })
    result = {"code": 200, "data": {"list": list, "pageNum": pageNum, "pageSize": pageSize, "total": total}, "msg": '成功'}
    return jsonify(result)


@g_harvest.route('/g_harvest/economicinfo/add', methods=['POST'])
def add_g_harvest_economicinfo():
    data = request.get_json()
    data['belong'] = 0
    obj = GHarvestEconomicinfo()
    for key, value in data.items():
        if hasattr(obj, key):
            setattr(obj, key, value)
    try:
        db.session.add(obj)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        return jsonify({"code": 500, "msg": f'添加失败 {str(e)}'})
    return jsonify({"code": 200, "msg": '添加成功'})


@g_harvest.route('/g_harvest/economicinfo/edit', methods=['POST'])
def edit_g_harvest_economicinfo():
    data = request.get_json()
    id = data.get('id')
    if not id:
        return jsonify({"code": 400, "msg": '缺少id'})
    GHarvestEconomicinfo.query.filter_by(id=id).update(data)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        return jsonify({"code": 500, "msg": f'修改失败 {str(e)}'})
    return jsonify({"code": 200, "msg": '修改成功'})


@g_harvest.route('/g_harvest/economicinfo/del', methods=['POST'])
def del_g_harvest_economicinfo():
    data = request.get_json()
    id = data.get('id')
    if not id:
        return jsonify({"code": 400, "msg": '缺少id'})
    obj = GHarvestEconomicinfo.query.get(id)
    if not obj:
        return jsonify({"code": 404, "msg": '记录不存在'})
    try:
        db.session.delete(obj)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        return jsonify({"code": 500, "msg": f'删除失败 {str(e)}'})
    return jsonify({"code": 200, "msg": '删除成功'})


@g_harvest.route('/g_harvest/segmentinfo', methods=['POST'])
def get_g_harvest_segmentinfo_list():
    pageNum = int(request.json.get('pageNum', 1))
    pageSize = int(request.json.get('pageSize', 10))
    conditions = []
    search_params = {
        'belong': GHarvestSegmentinfo.belong,
        'basic_id': GHarvestSegmentinfo.basic_id,
        'age': GHarvestSegmentinfo.age,
        'source': GHarvestSegmentinfo.source,
        'in_weight': GHarvestSegmentinfo.in_weight,
        'CWT': GHarvestSegmentinfo.CWT,
        'net_meat_weight': GHarvestSegmentinfo.net_meat_weight,
        'spine': GHarvestSegmentinfo.spine,
        'chops_weight': GHarvestSegmentinfo.chops_weight,
        'stick_bone_weight': GHarvestSegmentinfo.stick_bone_weight,
        'others_weight': GHarvestSegmentinfo.others_weight,
        'head_weight': GHarvestSegmentinfo.head_weight,
        'blood_weight': GHarvestSegmentinfo.blood_weight,
        'skin_weight': GHarvestSegmentinfo.skin_weight,
        'heart_weight': GHarvestSegmentinfo.heart_weight,
        'liver_weight': GHarvestSegmentinfo.liver_weight,
        'lungs_weight': GHarvestSegmentinfo.lungs_weight,
        'tripe_weight': GHarvestSegmentinfo.tripe_weight,
        'hoof_weight': GHarvestSegmentinfo.hoof_weight,
        'L_intestine_weight': GHarvestSegmentinfo.L_intestine_weight,
        'S_intestine_weight': GHarvestSegmentinfo.S_intestine_weight,
        'kidney_weight': GHarvestSegmentinfo.kidney_weight,
        'white_weight': GHarvestSegmentinfo.white_weight,
        'date': GHarvestSegmentinfo.date,
        'f_staff': GHarvestSegmentinfo.f_staff,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:
            conditions.append(column == value)
    if conditions:
        query = GHarvestSegmentinfo.query.filter(and_(*conditions))
    else:
        query = GHarvestSegmentinfo.query
    infos = query.filter(GHarvestSegmentinfo.belong == 0).paginate(page=pageNum, per_page=pageSize, error_out=False)
    total = query.count()
    list = []
    for info in infos:
        list.append({
            'id': info.id,
            'belong': info.belong,
            'basic_id': info.basic_id,
            'age': info.age,
            'source': info.source,
            'in_weight': info.in_weight,
            'CWT': info.CWT,
            'net_meat_weight': info.net_meat_weight,
            'spine': info.spine,
            'chops_weight': info.chops_weight,
            'stick_bone_weight': info.stick_bone_weight,
            'others_weight': info.others_weight,
            'head_weight': info.head_weight,
            'blood_weight': info.blood_weight,
            'skin_weight': info.skin_weight,
            'heart_weight': info.heart_weight,
            'liver_weight': info.liver_weight,
            'lungs_weight': info.lungs_weight,
            'tripe_weight': info.tripe_weight,
            'hoof_weight': info.hoof_weight,
            'L_intestine_weight': info.L_intestine_weight,
            'S_intestine_weight': info.S_intestine_weight,
            'kidney_weight': info.kidney_weight,
            'white_weight': info.white_weight,
            'date': info.date,
            'f_staff': info.f_staff,
        })
    result = {"code": 200, "data": {"list": list, "pageNum": pageNum, "pageSize": pageSize, "total": total}, "msg": '成功'}
    return jsonify(result)


@g_harvest.route('/g_harvest/segmentinfo/add', methods=['POST'])
def add_g_harvest_segmentinfo():
    data = request.get_json()
    data['belong'] = 0
    obj = GHarvestSegmentinfo()
    for key, value in data.items():
        if hasattr(obj, key):
            setattr(obj, key, value)
    try:
        db.session.add(obj)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        return jsonify({"code": 500, "msg": f'添加失败 {str(e)}'})
    return jsonify({"code": 200, "msg": '添加成功'})


@g_harvest.route('/g_harvest/segmentinfo/edit', methods=['POST'])
def edit_g_harvest_segmentinfo():
    data = request.get_json()
    id = data.get('id')
    if not id:
        return jsonify({"code": 400, "msg": '缺少id'})
    GHarvestSegmentinfo.query.filter_by(id=id).update(data)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        return jsonify({"code": 500, "msg": f'修改失败 {str(e)}'})
    return jsonify({"code": 200, "msg": '修改成功'})


@g_harvest.route('/g_harvest/segmentinfo/del', methods=['POST'])
def del_g_harvest_segmentinfo():
    data = request.get_json()
    id = data.get('id')
    if not id:
        return jsonify({"code": 400, "msg": '缺少id'})
    obj = GHarvestSegmentinfo.query.get(id)
    if not obj:
        return jsonify({"code": 404, "msg": '记录不存在'})
    try:
        db.session.delete(obj)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        return jsonify({"code": 500, "msg": f'删除失败 {str(e)}'})
    return jsonify({"code": 200, "msg": '删除成功'})
