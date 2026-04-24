# views.py: 路由 + 视图函数
from datetime import datetime, timedelta
import random
import json
from decimal import Decimal

from flask import Blueprint, render_template, request, make_response, Response, redirect, url_for, session, jsonify, \
    send_file
from sqlalchemy import desc, and_, or_, not_
import pandas as pd

# from .models import *
from ..modelsReverse import *
from ..utils.AlchemyEncoder import AlchemyEncoder

# 蓝图
h_store = Blueprint('h_store', __name__)


@h_store.route('/h_store/generate_outbound_no', methods=['POST'])
def generate_outbound_no():
    try:
        params = request.get_json()
        print(params)
        source = params.get('type')

        if params.get('param') is None:
            # 获取当前日期
            today = datetime.now().strftime('%Y%m%d')
        else:
            # 将字符串转换为 datetime 对象
            date_obj = datetime.strptime(params.get('param'), "%Y-%m-%d")
            # 按照指定格式输出日期字符串
            today = date_obj.strftime("%Y%m%d")
        # 查找今天的所有出库单号
        # 如果是饲料那边走这个订单号
        if source == "疫苗":
            today_records = HStoreVaccineOut.query.filter(HStoreVaccineOut.outbound_no.startswith(today)).all()
        elif source == "饲料":
            today_records = HStoreFeedingOut.query.filter(HStoreFeedingOut.outbound_no.startswith(today)).all()
        else:
            result = {
                "code": 500,
                "msg": "不清楚来源，无法自动生成订单编号"
            }
            return jsonify(result)
        # 如果是疫苗药品那边走另一个订单号
        # 下午把这个函数改一下，先确定前端传过来的值，然后在把之前的疫苗出库记录给完成了。
        # today_records = HStoreFeedingOut.query.filter(HStoreFeedingOut.outbound_no.startswith(today)).all()

        if not today_records:
            # 如果没有今天的记录，生成第一个单号
            new_outbound_no = today + '01'
        else:
            # 找出最大的序号
            max_sequence = 0
            for record in today_records:
                sequence = int(record.outbound_no[-2:])
                if sequence > max_sequence:
                    max_sequence = sequence
            # 生成新的单号
            new_outbound_no = today + str(max_sequence + 1).zfill(2)
        result = {
            "code": 200,
            "data": new_outbound_no,
            "msg": "成功"
        }
        return jsonify(result)
    except Exception as e:
        result = {
            "code": 500,
            "msg": f"出现了一点问题 {str(e)}"
        }
        return jsonify(result)


@h_store.route('/h_store/validate_outNum', methods=['POST'])
def validate_outNum():
    out_num = request.json.get('value')
    maker_name = request.json.get('maker_name')
    maker_id = request.json.get('maker_id')
    name = request.json.get('name')
    type = request.json.get('type')

    # 如果是手动输入的生产者名称，则根据名称查询id
    if maker_name and not maker_id and type in [2, 3]:
        maker_id = SupplyFSuppliersinfo.query.filter_by(supplier_name=maker_name).first().id
    elif maker_name and not maker_id and type in [0, 1]:
        maker_id = SupplyVSuppliersinfo.query.filter_by(supplier_name=maker_name).first().id
    info = HStoreInventory.query.filter_by(maker_id=maker_id, goods=name, type=type).first()
    if info is None:
        result = {
            "code": 200,
            'realcode': 500,
            "msg": '该生产产家没有此类物品名称'
        }
        return jsonify(result)
    status = (float(info.quantity) - float(out_num)) - float(info.alert)
    if status == 0 and float(info.alert) == 0:
        result = {
            "code": 200,
            "realcode": 501,
            "msg": "注意，这次出库之后库存数量为0，库存系统会自动把记录删除！"
        }
    elif status > 0:
        result = {
            "code": 200,
            'realcode': 200,
            "msg": '可以出库'
        }

    else:
        result = {
            "code": 200,
            'realcode': 500,
            'data': float(info.quantity) - float(info.alert),
            "msg": '超出库存警戒线，不能出库,已经为您调整出库数量。'
        }
    return jsonify(result)


@h_store.route('/h_store/inventory', methods=['POST'])
def get_inventory():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        'type': HStoreInventory.type,
        'goods': HStoreInventory.goods,
        'maker_name': HStoreInventory.id,
        'maker_id': HStoreInventory.maker_id,
        'quantity': HStoreInventory.quantity,
        'alert': HStoreInventory.alert,
        'f_date': HStoreInventory.f_date,
        'f_staff': HStoreInventory.f_staff,
        'out_time': HStoreInventory.out_time,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'f_date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            elif param == 'maker_name':
                v_suppliers_info = SupplyVSuppliersinfo.query.filter(
                    SupplyVSuppliersinfo.supplier_name.like(f'%{value}%')).all()
                f_suppliers_info = SupplyFSuppliersinfo.query.filter(
                    SupplyFSuppliersinfo.supplier_name.like(f'%{value}%')).all()
                v_maker_ids = [v.id for v in v_suppliers_info]
                f_maker_ids = [f.id for f in f_suppliers_info]
                v_ids = HStoreInventory.query.filter(
                    and_(HStoreInventory.maker_id.in_(v_maker_ids), or_(HStoreInventory.type == 0,
                                                                        HStoreInventory.type == 1))).all()
                f_ids = HStoreInventory.query.filter(
                    and_(HStoreInventory.maker_id.in_(f_maker_ids), or_(HStoreInventory.type == 2,
                                                                        HStoreInventory.type == 3))).all()
                ids = [v.id for v in v_ids] + [f.id for f in f_ids]
                conditions.append(column.in_(ids))
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = HStoreInventory.query.filter(and_(*conditions))
    else:
        query = HStoreInventory.query  # 如果没有条件，查询所有

    # 并且根据id降序排列

    query = query.filter(and_(HStoreInventory.belong == 0, HStoreInventory.type.in_([0, 1])))
    infos = query.order_by(desc(HStoreInventory.id)).paginate(page=pageNum, per_page=pageSize,
                                                              error_out=False)
    total = query.count()

    list = []
    for info in infos:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        data = json.loads(data)
        # print(data)
        if data['type'] == 0 or data['type'] == 1:
            data['maker_name'] = SupplyVSuppliersinfo.query.filter_by(id=data['maker_id']).first().supplier_name
        # else:
        #     data['maker_name'] = SupplyFSuppliersinfo.query.filter_by(id=data['maker_id']).first().supplier_name
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


@h_store.route('/h_store/inventoryForage', methods=['POST'])
def get_inventoryForage():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        'type': HStoreInventory.type,
        'goods': HStoreInventory.goods,
        'maker_name': HStoreInventory.id,
        'maker_id': HStoreInventory.maker_id,
        'quantity': HStoreInventory.quantity,
        'alert': HStoreInventory.alert,
        'f_date': HStoreInventory.f_date,
        'f_staff': HStoreInventory.f_staff,
        'out_time': HStoreInventory.out_time,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'f_date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            elif param == 'maker_name':
                v_suppliers_info = SupplyVSuppliersinfo.query.filter(
                    SupplyVSuppliersinfo.supplier_name.like(f'%{value}%')).all()
                f_suppliers_info = SupplyFSuppliersinfo.query.filter(
                    SupplyFSuppliersinfo.supplier_name.like(f'%{value}%')).all()
                v_maker_ids = [v.id for v in v_suppliers_info]
                f_maker_ids = [f.id for f in f_suppliers_info]
                v_ids = HStoreInventory.query.filter(
                    and_(HStoreInventory.maker_id.in_(v_maker_ids), or_(HStoreInventory.type == 0,
                                                                        HStoreInventory.type == 1))).all()
                f_ids = HStoreInventory.query.filter(
                    and_(HStoreInventory.maker_id.in_(f_maker_ids), or_(HStoreInventory.type == 2,
                                                                        HStoreInventory.type == 3))).all()
                ids = [v.id for v in v_ids] + [f.id for f in f_ids]
                conditions.append(column.in_(ids))
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = HStoreInventory.query.filter(and_(*conditions))
    else:
        query = HStoreInventory.query  # 如果没有条件，查询所有

    # 并且根据id降序排列

    query = query.filter(and_(HStoreInventory.belong == 0, HStoreInventory.type.in_([2, 3])))
    infos = query.order_by(desc(HStoreInventory.id)).paginate(page=pageNum, per_page=pageSize,
                                                              error_out=False)
    total = query.count()

    list = []
    for info in infos:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        data = json.loads(data)
        # print(data)
        # if data['type'] == 0 or data['type'] == 1:
        #     data['maker_name'] = SupplyVSuppliersinfo.query.filter_by(id=data['maker_id']).first().supplier_name
        if data['type'] == 2 or data['type'] == 3:
            data['maker_name'] = SupplyFSuppliersinfo.query.filter_by(id=data['maker_id']).first().supplier_name
        list.append(data)
        print(list)
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

@h_store.route('/h_store/inventory/add', methods=['POST'])
def add_inventory():
    data = request.get_json()
    ctime = datetime.now()
    # belong为0
    data['belong'] = 0
    data['f_date'] = ctime
    print(data)
    info = HStoreInventory()
    for key, value in data.items():
        setattr(info, key, value)

    # 更新inventory表的相应的"更新时间"
    # HStoreInventory.query.filter_by(id=data['id']).update({'out_time': ctime})

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
@h_store.route('/h_store/inventory/edit', methods=['POST'])
def edit_inventory():
    data = request.get_json()
    ctime = datetime.now()
    # print("--data-->", data)
    data.pop('maker_name')
    HStoreInventory.query.filter_by(id=data['id']).update(data)

    # 更新inventory表的相应的"更新时间"
    HStoreInventory.query.filter_by(id=data['id']).update({'out_time': ctime})

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


# 这一部分代码是想要做，自动补全下拉菜单的，由于时间问题没有成功实现这个目标，主要问题在于前端显示不正常，可以留下供之后选择使用。
# @h_store.route('/h_store/inventory/search', methods=['GET'])
# def search_inventory():
#     # 获取前端传递的关键字
#     keyword = request.args.get('keyword')
#     # 获取货物名称
#     names = HStoreInventory.query.filter(HStoreInventory.goods.like(f'%{keyword}%')).all()
#     # 打印名称，检查是否出错
#     list = []
#     for name in names:
#         list.append(name.goods)
#     print(list)
#     return jsonify(list)

@h_store.route('/h_store/inventory/del', methods=['POST'])
def del_inventory():
    ids = request.get_json()
    for i in ids:
        HStoreInventory.query.filter_by(id=i).delete()
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


@h_store.route('/h_store/vaccine_in', methods=['POST'])
def get_vaccine_in():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        'maker_name': HStoreVaccineIn.maker_id,
        'v_name': HStoreVaccineIn.v_name,
        'type': HStoreVaccineIn.type,
        'purpose': HStoreVaccineIn.purpose,
        'produce_date': HStoreVaccineIn.produce_date,
        'expiration_date': HStoreVaccineIn.expiration_date,
        'produce_num': HStoreVaccineIn.produce_num,
        'billing_unit': HStoreVaccineIn.billing_unit,
        'in_amount': HStoreVaccineIn.in_amount,
        'unit_price': HStoreVaccineIn.unit_price,
        'total_price': HStoreVaccineIn.total_price,
        'fare': HStoreVaccineIn.fare,
        'avg_price': HStoreVaccineIn.avg_price,
        'in_time': HStoreVaccineIn.in_time,
        'keep_amount': HStoreVaccineIn.keep_amount,
        'f_date': HStoreVaccineIn.f_date,
        'f_staff': HStoreVaccineIn.f_staff,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'f_date' or param == 'produce_date' or param == 'expiration_date' or param == 'in_time':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            elif param == 'maker_name':
                v_suppliers_info = SupplyVSuppliersinfo.query.filter(
                    SupplyVSuppliersinfo.supplier_name.like(f'%{value}%')).all()
                v_maker_ids = [v.id for v in v_suppliers_info]
                conditions.append(column.in_(v_maker_ids))
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = HStoreVaccineIn.query.filter(and_(*conditions))
    else:
        query = HStoreVaccineIn.query  # 如果没有条件，查询所有

    # 并且根据id降序排列

    query = query.filter(HStoreVaccineIn.belong == 0)
    infos = query.order_by(desc(HStoreVaccineIn.id)).paginate(page=pageNum, per_page=pageSize,
                                                              error_out=False)
    total = query.count()

    list = []
    for info in infos:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        data = json.loads(data)
        data['maker_name'] = SupplyVSuppliersinfo.query.filter_by(id=data['maker_id']).first().supplier_name
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


@h_store.route('/h_store/vaccine_in/add', methods=['POST'])
def add_vaccine_in():
    data = request.get_json()
    ctime = datetime.now()
    # belong为0
    try:
        data['maker_id'] = SupplyVSuppliersinfo.query.filter_by(
            supplier_name=data['maker_name']).first().id
    except Exception as e:
        result = {
            "code": 500,
            "msg": "获取厂商失败，请确认厂商名称在厂商库中存在！"
        }
        return jsonify(result)
    data['belong'] = 0
    data['f_date'] = ctime
    # 去掉maker_name
    # data.pop('maker_name')
    print(data)
    info = HStoreVaccineIn()
    for key, value in data.items():
        setattr(info, key, value)
    # 会有重名的厂家
    # print(data['maker_id'])
    inv_info = HStoreInventory.query.filter_by(maker_id=data['maker_id'], goods=data['v_name'], type=data['type'])
    inv_info_ins = inv_info.first()
    if inv_info_ins:
        # 同样需要更新库存价格和总花费 25-2-10新加的字段, 需要注意这里的inv_info_ins和inv_info表示对象的不一样
        inv_info_ins.stockPrice = ((inv_info_ins.stockPrice * inv_info_ins.quantity) + Decimal(str(
                data['avg_price'] * data['in_amount']))) / (inv_info_ins.quantity + Decimal(str(data['in_amount'])))
        inv_info_ins.totalCost += Decimal(str(data['avg_price'] * data['in_amount']))
        inv_info_ins.quantity += Decimal(str(data['in_amount']))
        # 更新inventory表的相应的"更新时间"
        inv_info.update({'out_time': ctime})
    else:
        new_inv_info = HStoreInventory()
        new_inv_info.maker_id = data['maker_id']
        new_inv_info.goods = data['v_name']
        new_inv_info.type = data['type']
        new_inv_info.quantity = data['in_amount']
        new_inv_info.ingredientsType = data['ingredientsType']
        # 库存价格
        new_inv_info.stockPrice = data['avg_price']
        # 总花费
        new_inv_info.totalCost = data['avg_price'] * data['in_amount']
        new_inv_info.alert = 0
        new_inv_info.f_date = ctime
        new_inv_info.belong = 0
        new_inv_info.out_time = ctime
        try:
            db.session.add(new_inv_info)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            result = {
                "code": 500,
                "msg": f'添加失败 {str(e)}'
            }
            return jsonify(result)

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
@h_store.route('/h_store/vaccine_in/edit', methods=['POST'])
def edit_vaccine_in():
    data = request.get_json()
    # print("--data-->", data)
    # 去掉maker_name
    ctime = datetime.now()
    data.pop('maker_name')

    # 数量更新逻辑
    maker = HStoreVaccineIn.query.filter_by(id=data['id'])
    old_quantity = maker.first().in_amount
    old_avgPrice = maker.first().avgPrice
    result_quantity = data['in_amount'] - old_quantity
    result_cost = data['in_amount'] * data['avg_price'] - old_quantity * old_avgPrice
    # 更新Inventory表的的数量
    inv_maker = HStoreInventory.query.filter_by(maker_id=data['maker_id'], goods=data['v_name'], type=data['type'])
    inv_maker.first().stockPrice = (inv_maker.first().stockPrice * inv_maker.first().quantity + result_cost) / (
            inv_maker.first().quantity + result_quantity)
    inv_maker.first().totalCost += result_cost  # 总花费
    inv_maker.first().quantity += result_quantity
    maker.update(data)
    # 更新inventory表的相应的"更新时间"
    inv_maker.update({'out_time': ctime})

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


@h_store.route('/h_store/vaccine_in/del', methods=['POST'])
def del_vaccine_in():
    ids = request.get_json()
    for i in ids:
        HStoreVaccineIn.query.filter_by(id=i).delete()

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


@h_store.route('/h_store/vaccine_out', methods=['POST'])
def get_vaccine_out():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        'maker_name': HStoreVaccineOut.maker_id,
        'outbound_no': HStoreVaccineOut.outbound_no,
        'v_name': HStoreVaccineOut.v_name,
        'type': HStoreVaccineOut.type,
        'delivery_time': HStoreVaccineOut.delivery_time,
        'out_purposes': HStoreVaccineOut.out_purposes,
        'out_staff': HStoreVaccineOut.out_staff,
        'contact_phone': HStoreVaccineOut.contact_phone,
        'notes': HStoreVaccineOut.notes,
        'f_staff': HStoreVaccineOut.f_staff,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'f_date' or param == 'delivery_time':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            elif param == 'maker_name':
                v_suppliers_info = SupplyVSuppliersinfo.query.filter(
                    SupplyVSuppliersinfo.supplier_name.like(f'%{value}%')).all()
                v_maker_ids = [v.id for v in v_suppliers_info]
                conditions.append(column.in_(v_maker_ids))
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = HStoreVaccineOut.query.filter(and_(*conditions))
    else:
        query = HStoreVaccineOut.query  # 如果没有条件，查询所有

    # 并且根据id降序排列

    query = query.filter(HStoreVaccineOut.belong == 0)
    infos = query.order_by(desc(HStoreVaccineOut.id)).paginate(page=pageNum, per_page=pageSize,
                                                               error_out=False)
    total = query.count()

    list = []
    for info in infos:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        data = json.loads(data)
        data['maker_name'] = SupplyVSuppliersinfo.query.filter_by(id=data['maker_id']).first().supplier_name
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


@h_store.route('/h_store/vaccine_out/add', methods=['POST'])
def add_vaccine_out():
    # 目前最新的逻辑是，
    # 1. 记录出库的记录并且保留出库价格，按理来讲第一次出库的时候，这条记录在出库表中的出库价格就永远不能变化了
    # 2. 更改库存信息中的数量
    # 3. 将出库费用分为药品或者疫苗，记录在对应日期的日支出报表中
    # 4. 判断出库单号是否有重复，如果有重复就直接返回就可以了
    data = request.get_json()
    if HStoreVaccineOut.query.filter_by(outbound_no=data['outbound_no']).first():
        result = {
            "code": 500,
            "msg": f'库存单号重复，不允许添加'
        }
        return jsonify(result)
    # ctime = datetime.now()
    # belong为0
    data['maker_id'] = SupplyVSuppliersinfo.query.filter_by(supplier_name=data['maker_name']).first().id
    data['belong'] = 0
    # 这个表没有f_date
    # data['f_date'] = ctime
    ctime = datetime.now()
    print(data)
    # 将日期字符串转换为 datetime 对象
    date_obj = datetime.strptime(data['delivery_time'], '%Y-%m-%d')  # date_obj 出库日期
    if date_obj > ctime:
        result = {
            "code": 500,
            "msg": '出库日期不可以大于当天日期'
        }
        return jsonify(result)
    info = HStoreVaccineOut()  # 构建疫苗药品出库记录数据对象
    for key, value in data.items():  # 将前端的信息赋值给info
        setattr(info, key, value)
    # 取出库存信息中对应的记录，方便更改
    maker = HStoreInventory.query.filter_by(maker_id=data['maker_id'], goods=data['v_name'], type=data['type'])
    '''
    在赋值数量之前需要计算今天得花费并且加入到日支出报表里面，并且要考虑日期是提交上来的日期
    ，并不是固定，唯一可以确定的就是日期不可能超过当下最新的日期。
    '''
    # 首先，我觉得要把对应日期的记录提取出来
    ADsheet = Analysisdailysheet.query.filter_by(date=info.delivery_time).first()
    if not ADsheet:  # 如果不存在的话就需要新创建一个
        sheet = Analysisdailysheet()
        #
        # # 计算上一天的日期
        # previous_day = date_obj - timedelta(days=1)
        # # 将上一天的日期转换为字符串
        # previous_day_str = previous_day.strftime('%Y-%m-%d')
        # # 实际上并不是 日期是连续记录的，但是为了方便我必须要弄成每天一条
        # last_daysheet = Analysisdailysheet.query.filter_by(date=previous_day_str).first()
        if data['type'] == 0:
            sheet.yimiao_fees = Decimal(data['num']) * maker.first().stockPrice
        elif data['type'] == 1:
            sheet.yaopin_fees = Decimal(data['num']) * maker.first().stockPrice
        else:
            result = {
                "code": 500,
                "msg": '不确定data["type"]的类型！'
            }
            return jsonify(result)
        sheet.date = info.delivery_time
        sheet.belong = 0
        # db.session.add(sheet)  # 添加新的日报表记录到会话
    else:  # 这样就是对应的出库日期已经存在日报表记录
        sheet = ADsheet
        if sheet.yimiao_fees is None:
            sheet.yimiao_fees = 0
        if sheet.yaopin_fees is None:
            sheet.yaopin_fees = 0
        if data['type'] == 0:
            sheet.yimiao_fees += Decimal(data['num']) * maker.first().stockPrice
        elif data['type'] == 1:
            sheet.yaopin_fees += Decimal(data['num']) * maker.first().stockPrice

    # 出库影响的一般只有数量，所以处理数量就可以了
    maker.first().quantity = float(maker.first().quantity) - float(data['num'])
    # 在这里将出库价格 赋值给新增的这个 info
    setattr(info, 'out_price', maker.first().stockPrice)
    # 更新inventory表的相应的"更新时间"
    maker.update({'out_time': ctime})
    if maker.first().quantity == 0:
        maker.update({"belong": 1, "stockPrice": 0})

    try:
        db.session.add(sheet)
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
@h_store.route('/h_store/vaccine_out/edit', methods=['POST'])
def edit_vaccine_out():
    data = request.get_json()
    # print("--data-->", data)
    ctime = datetime.now()
    data.pop('maker_name')

    # 数量更新逻辑
    maker = HStoreVaccineOut.query.filter_by(id=data['id'])  # 这里取的是疫苗和药品出库记录，但是取名字叫做maker
    old_quantity = maker.first().num  # 拿旧的数量
    result_quantity = int(data['num']) - old_quantity  # 将新的数量和旧的数量做差
    # 更新Inventory表的的数量
    inv_maker = HStoreInventory.query.filter_by(maker_id=data['maker_id'], goods=data['v_name'], type=data['type'])
    inv_maker.first().quantity -= result_quantity
    # 我认为在这里可以 做一个 日支出报表 那个表的的更新：主要更新的字段是 药品支出费用或者疫苗支出费用
    # 费用等于 直接 -= result_quantity * 出库价格 为什么不是 += 因为对于入库是+=，出库应该是-=
    # 还有一件事情就是考虑 出库时间是否会有变化 如果出库时间有变化的话就得更改两个日期的 日支出报表。
    if maker.first().delivery_time == data["delivery_time"]:  # 如果两个日期相同那就更改一个 日支出报表
        dailySheet = Analysisdailysheet.query.filter_by(date=data["delivery_time"]).first()
        if data["type"] == 0:  # 说明是药品，更改的是药品支出费用
            dailySheet.yimiao_fees -= result_quantity * maker.first().out_price
        else:
            dailySheet.yaoping_fees -= result_quantity * maker.first().out_price
    else:  # 两个日期不相等 , 还需要考虑新的日期是否再数据库中存在：暂时避免这种情况可以按照自动化程序每天自动生成一条当天的日支出报表信息，全部为0

        old_dailySheet = Analysisdailysheet.query.filter_by(date=maker.first().delivery_time).first()
        new_dailySheet = Analysisdailysheet.query.filter_by(date=data["delivery_time"]).first()
        # 如果需要考虑两个日期必须都得存在，未来可以在这个地方判断，在这里做一个标记
        if data["type"] == 0:  # 说明是药品，更改的是药品支出费用
            # 应该先在新日期上直接赋予新的值 ，然后在旧的日期上减去原来的费用
            new_dailySheet.yimiao_fees += int(data["num"]) * maker.first().out_price
            old_dailySheet.yimiao_fees -= old_quantity * maker.first().out_price
        else:
            new_dailySheet.yaopin_fees += int(data["num"]) * maker.first().out_price
            old_dailySheet.yaopin_fees -= old_quantity * maker.first().out_price
    # 同样地对于饲料出库也是相同的逻辑。

    maker.update(data)
    # 更新inventory表的相应的"更新时间"
    inv_maker.update({'out_time': ctime})

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


@h_store.route('/h_store/vaccine_out/del', methods=['POST'])
def del_vaccine_out():
    ids = request.get_json()
    for i in ids:
        HStoreVaccineOut.query.filter_by(id=i).delete()
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


@h_store.route('/h_store/feedingin', methods=['POST'])
def get_feedingin():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        'maker_name': HStoreFeedingin.maker_id,
        'type': HStoreFeedingin.type,
        'f_name': HStoreFeedingin.f_name,
        'warehouse_num': HStoreFeedingin.warehouse_num,
        'nutrients': HStoreFeedingin.nutrients,
        'buy_time': HStoreFeedingin.buy_time,
        'billing_unit': HStoreFeedingin.billing_unit,
        'quantity': HStoreFeedingin.quantity,
        'unit_price': HStoreFeedingin.unit_price,
        'total_price': HStoreFeedingin.total_price,
        'fare': HStoreFeedingin.fare,
        'avg_price': HStoreFeedingin.avg_price,
        'specifications': HStoreFeedingin.specifications,
        'purpose': HStoreFeedingin.purpose,
        'water_content': HStoreFeedingin.water_content,
        'mildew': HStoreFeedingin.mildew,
        'impurity_content': HStoreFeedingin.impurity_content,
        'notes': HStoreFeedingin.notes,
        'keep_amount': HStoreFeedingin.keep_amount,
        'f_date': HStoreFeedingin.f_date,
        'f_staff': HStoreFeedingin.f_staff,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'f_date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            elif param == 'maker_name':
                f_suppliers_info = SupplyFSuppliersinfo.query.filter(
                    SupplyFSuppliersinfo.supplier_name.like(f'%{value}%')).all()
                f_maker_ids = [f.id for f in f_suppliers_info]
                conditions.append(column.in_(f_maker_ids))
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = HStoreFeedingin.query.filter(and_(*conditions))
    else:
        query = HStoreFeedingin.query  # 如果没有条件，查询所有

    # 并且根据id降序排列

    query = query.filter(HStoreFeedingin.belong == 0)
    infos = query.order_by(desc(HStoreFeedingin.id)).paginate(page=pageNum, per_page=pageSize,
                                                              error_out=False)
    total = query.count()

    list = []
    for info in infos:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        data = json.loads(data)
        data['maker_name'] = SupplyFSuppliersinfo.query.filter_by(id=data['maker_id']).first().supplier_name
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


@h_store.route('/h_store/feedingin/add', methods=['POST'])
def add_feedingin():
    data = request.get_json()
    ctime = datetime.now()
    print(data)
    # belong为0
    try:
        data['maker_id'] = SupplyFSuppliersinfo.query.filter_by(
            supplier_name=data['maker_name']).first().id  # 获取原本正确厂家的id用于入库的记录
    except Exception as e:
        result = {
            "code": 500,
            "msg": "获取厂商失败，请确认厂商名称在厂商库中存在！"
        }
        return jsonify(result)
    hebau_id = SupplyFSuppliersinfo.query.filter_by(supplier_name="统一厂商").first().id  # 关于饲料统一记录为同一个厂家
    data['belong'] = 0
    data['f_date'] = ctime  # 初始化前端没有传过来的信息
    print(data)  # 打印构建的数据
    info = HStoreFeedingin()  # 实例化饲料入库记录对象
    for key, value in data.items():
        setattr(info, key, value)

        # 会有重名的厂家
        # print(data['maker_id'])
    inv_info = HStoreInventory.query.filter_by(maker_id=hebau_id, goods=data['f_name'],
                                               type=data['type'])  # 对于饲料，查找库存中相同种类和货物名称的记录
    inv_info_ins = inv_info.first()  # 取查出来的第一条记录，这里其实就应该只有一条记录
    if inv_info_ins:  # 如果之前存在这样的记录
        # 同样需要更新库存价格和总花费 25-2-10新加的字段, 需要注意这里的inv_info_ins和inv_info表示对象的不一样
        # 在计算的时候出现TypeError: unsupported operand type(s) for +: 'decimal.Decimal' and 'float'报错
        # 需要统一处理一下上面的报错。
        inv_info_ins.stockPrice = ((inv_info_ins.stockPrice * inv_info_ins.quantity) + Decimal(str(
                data['avg_price'] * data['quantity']))) / (inv_info_ins.quantity + Decimal(str(data['quantity'])))
        inv_info_ins.totalCost += Decimal(str(data['avg_price'] * data['quantity']))
        # 更新库存数量,计算库存数量一定要在计算库存价格和总花费之后，因为前者需要原来的库存数量进行计算
        inv_info_ins.quantity += Decimal(str(data['quantity']))

        # 更新inventory表的相应的"更新时间"
        inv_info.update({'out_time': ctime})

    else:  # 如果不存在这样的记录
        new_inv_info = HStoreInventory()
        # 赋值所有的属性
        new_inv_info.maker_id = data['maker_id']
        new_inv_info.goods = data['f_name']
        new_inv_info.type = data['type']
        new_inv_info.ingredientsType = data['ingredientsType']
        # 数量
        new_inv_info.quantity = data['quantity']
        # 库存价格
        new_inv_info.stockPrice = data['avg_price']
        # 总花费
        new_inv_info.totalCost = data['avg_price'] * data['quantity']
        new_inv_info.alert = 0
        new_inv_info.f_date = ctime
        new_inv_info.belong = 0
        new_inv_info.out_time = ctime
        try:
            db.session.add(new_inv_info)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            result = {
                "code": 500,
                "msg": f'添加失败 {str(e)}'
            }
            return jsonify(result)

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
@h_store.route('/h_store/feedingin/edit', methods=['POST'])
def edit_feedingin():
    data = request.get_json()
    # print("--data-->", data)
    ctime = datetime.now()
    data.pop('maker_name')
    # 数量更新，价格更新，总花费更新，库存价格更新逻辑
    maker = HStoreFeedingin.query.filter_by(id=data['id'])  # 根据前端传过来的id来找到当下的记录，命名maker
    old_quantity = maker.first().quantity  # 获取同一条记录上次记录的时候写的数量
    old_avgPrice = maker.first().avgPrice  # 获取同一条记录上次记录的时候写的折合单价
    result_quantity = data['quantity'] - old_quantity  # 将这次的数量和上次的数量做差值，作为这次处理的值
    result_cost = data['quantity'] * data['avg_price'] - old_quantity * old_avgPrice
    # 更新Inventory表的的数量
    hebau_id = SupplyFSuppliersinfo.query.filter_by(supplier_name="统一厂商").first().id  # 关于饲料统一记录为同一个厂家
    inv_maker = HStoreInventory.query.filter_by(maker_id=hebau_id, goods=data['f_name'], type=data['type'])
    # 库存价格
    inv_maker.first().stockPrice = (inv_maker.first().stockPrice * inv_maker.first().quantity + result_cost) / (
            inv_maker.first().quantity + result_quantity)
    inv_maker.first().totalCost += result_cost  # 总花费
    inv_maker.first().quantity += result_quantity  # 同样的，在更新数量之前先更新库存价格和总花费

    maker.update(data)  # 更新入库的记录
    # 更新inventory表的相应的"更新时间"
    inv_maker.update({'out_time': ctime})
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


@h_store.route('/h_store/feedingin/del', methods=['POST'])
def del_feedingin():
    ids = request.get_json()
    for i in ids:
        HStoreFeedingin.query.filter_by(id=i).delete()
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


@h_store.route('/h_store/feeding_out', methods=['POST'])
def get_feeding_out():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        'maker_name': HStoreFeedingOut.maker_id,
        'outbound_no': HStoreFeedingOut.outbound_no,
        'type': HStoreFeedingOut.type,
        'f_name': HStoreFeedingOut.f_name,
        'warehouse_num': HStoreFeedingOut.warehouse_num,
        'delivery_time': HStoreFeedingOut.delivery_time,
        'out_purposes': HStoreFeedingOut.out_purposes,
        'num': HStoreFeedingOut.num,
        'out_staff': HStoreFeedingOut.out_staff,
        'contact_phone': HStoreFeedingOut.contact_phone,
        'notes': HStoreFeedingOut.notes,
        'f_staff': HStoreFeedingOut.f_staff,
        # 这个表没有f_date
        # 'f_date': SupplyCommodityinfo.f_date,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'f_date' or param =='delivery_time':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            elif param == 'maker_name':
                f_suppliers_info = SupplyFSuppliersinfo.query.filter(
                    SupplyFSuppliersinfo.supplier_name.like(f'%{value}%')).all()
                f_maker_ids = [f.id for f in f_suppliers_info]
                conditions.append(column.in_(f_maker_ids))
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = HStoreFeedingOut.query.filter(and_(*conditions))
    else:
        query = HStoreFeedingOut.query  # 如果没有条件，查询所有

    # 并且根据id降序排列

    query = query.filter(HStoreFeedingOut.belong == 0)
    infos = query.order_by(desc(HStoreFeedingOut.id)).paginate(page=pageNum, per_page=pageSize,
                                                               error_out=False)
    total = query.count()

    list = []
    for info in infos:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        data = json.loads(data)
        data['maker_name'] = SupplyFSuppliersinfo.query.filter_by(id=data['maker_id']).first().supplier_name
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


@h_store.route('/h_store/feeding_out/add', methods=['POST'])
def add_feeding_out():
    data = request.get_json()
    if HStoreFeedingOut.query.filter_by(outbound_no=data['outbound_no']).first():
        result = {
            "code": 500,
            "msg": f'库存单号重复，不允许添加'
        }
        return jsonify(result)
    # ctime = datetime.now()
    # belong为0
    data['maker_id'] = SupplyFSuppliersinfo.query.filter_by(supplier_name=data['maker_name']).first().id
    hebau_id = SupplyFSuppliersinfo.query.filter_by(supplier_name="统一厂商").first().id
    data['belong'] = 0
    # data['f_date'] = ctime
    ctime = datetime.now()
    print(data)
    # 将日期字符串转换为 datetime 对象
    date_obj = datetime.strptime(data['delivery_time'], '%Y-%m-%d')
    if date_obj > ctime:
        result = {
            "code": 500,
            "msg": '出库日期不可以大于当天日期'
        }
        return jsonify(result)
    info = HStoreFeedingOut()
    for key, value in data.items():
        setattr(info, key, value)

    maker = HStoreInventory.query.filter_by(maker_id=hebau_id, goods=data['f_name'], type=data['type'])
    maker_ins = maker.first()

    # 首先，我觉得要把对应日期的记录提取出来
    ADsheet = Analysisdailysheet.query.filter_by(date=info.delivery_time).first()
    if not ADsheet:  # 如果不存在的话就需要新创建一个
        sheet = Analysisdailysheet()

        # # 计算上一天的日期
        # previous_day = date_obj - timedelta(days=1)
        # # 将上一天的日期转换为字符串
        # previous_day_str = previous_day.strftime('%Y-%m-%d')
        # # 实际上并不是 日期是连续记录的，但是为了方便我必须要弄成每天一条
        # last_daysheet = Analysisdailysheet.query.filter_by(date=previous_day_str).first()
        if data['type'] == 2:
            sheet.caoliao_fees = Decimal(data['num']) * maker_ins.stockPrice
        elif data['type'] == 3:
            sheet.jingliao_fees = Decimal(data['num']) * maker_ins.stockPrice
        else:
            result = {
                "code": 500,
                "msg": '不确定data["type"]的类型！'
            }
            return jsonify(result)
        sheet.date = info.delivery_time
        sheet.belong = 0

    else:  # 这样就是对应的出库日期已经存在日报表记录
        sheet = ADsheet
        if sheet.caoliao_fees is None:
            sheet.caoliao_fees = 0
        if sheet.jingliao_fees is None:
            sheet.jingliao_fees = 0
        if data['type'] == 2:
            sheet.caoliao_fees += Decimal(data['num']) * maker_ins.stockPrice
        elif data['type'] == 3:
            sheet.jingliao_fees += Decimal(data['num']) * maker_ins.stockPrice

    maker_ins.quantity = float(maker_ins.quantity) - float(data['num'])
    # 在这里将出库价格 赋值给新增的这个 info
    setattr(info, 'out_price', maker.first().stockPrice)
    # 更新inventory表的相应的"更新时间"
    maker.update({'out_time': ctime})
    if maker.first().quantity == 0:
        maker.update({"belong": 1, "out_price": 0})

    try:
        db.session.add(sheet)  # 添加新的日报表记录到会话
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
@h_store.route('/h_store/feeding_out/edit', methods=['POST'])
def edit_feeding_out():
    data = request.get_json()
    # print("--data-->", data)
    ctime = datetime.now()
    data.pop('maker_name')

    # 数量更新逻辑
    maker = HStoreFeedingOut.query.filter_by(id=data['id'])
    old_quantity = maker.first().num
    # num存的是int
    result_quantity = int(data['num']) - old_quantity
    # 更新Inventory表的的数量
    inv_maker = HStoreInventory.query.filter_by(maker_id=data['maker_id'], goods=data['f_name'], type=data['type'])
    inv_maker.first().quantity -= result_quantity
    # 我认为在这里可以 做一个 日支出报表 那个表的的更新：主要更新的字段是 草料支出费用或者精料支出费用
    # 费用等于 直接 -= result_quantity * 出库价格 为什么不是 += 因为对于入库是+=，出库应该是-=
    # 还有一件事情就是考虑 出库时间是否会有变化 如果出库时间有变化的话就得更改两个日期的 日支出报表。
    if maker.first().delivery_time == data["delivery_time"]:  # 如果两个日期相同那就更改一个 日支出报表
        dailySheet = Analysisdailysheet.query.filter_by(date=data["delivery_time"]).first()
        if data["type"] == 2:  # 说明是草料，更改的是草料支出费用
            dailySheet.caoliao_fees -= result_quantity * maker.first().out_price
        else:
            dailySheet.jingliao_fees -= result_quantity * maker.first().out_price
    else:  # 两个日期不相等 , 还需要考虑新的日期是否再数据库中存在：暂时避免这种情况可以按照自动化程序每天自动生成一条当天的日支出报表信息，全部为0

        old_dailySheet = Analysisdailysheet.query.filter_by(date=maker.first().delivery_time).first()
        new_dailySheet = Analysisdailysheet.query.filter_by(date=data["delivery_time"]).first()
        # 如果需要考虑两个日期必须都得存在，未来可以在这个地方判断，在这里做一个标记
        if data["type"] == 2:  # 说明是药品，更改的是药品支出费用
            # 应该先在新日期上直接赋予新的值 ，然后在旧的日期上减去原来的费用
            new_dailySheet.caoliao_fees += int(data["num"]) * maker.first().out_price
            old_dailySheet.caoliao_fees -= old_quantity * maker.first().out_price
        else:
            new_dailySheet.jingliao_fees += int(data["num"]) * maker.first().out_price
            old_dailySheet.jingliao_fees -= old_quantity * maker.first().out_price
    # 同样地对于饲料出库也是相同的逻辑。
    maker.update(data)
    # 更新inventory表的相应的"更新时间"
    inv_maker.update({'out_time': ctime})
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


@h_store.route('/h_store/feeding_out/del', methods=['POST'])
def del_feeding_out():
    ids = request.get_json()
    for i in ids:
        HStoreFeedingOut.query.filter_by(id=i).delete()
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
