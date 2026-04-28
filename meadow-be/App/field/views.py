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

field = Blueprint('field', __name__)


@field.route('/field/houseinfo', methods=['POST'])
def get_houseinfo():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        'id': FieldHouseinfo.id,
        'name': FieldHouseinfo.name,
        'function': FieldHouseinfo.function,
        'area': FieldHouseinfo.area,
        'h_type': FieldHouseinfo.h_type,
        'h_lwh': FieldHouseinfo.h_lwh,
        'sports_lwh': FieldHouseinfo.sports_lwh,
        'grass_type': FieldHouseinfo.grass_type,
        'area_pro': FieldHouseinfo.area_pro,
        'grass_quantity': FieldHouseinfo.grass_quantity,
        'build_time': FieldHouseinfo.build_time,
        'staff': FieldHouseinfo.staff,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'build_time':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = FieldHouseinfo.query.filter(and_(*conditions))
    else:
        query = FieldHouseinfo.query  # 如果没有条件，查询所有

    # 筛选出棚(pid==0)
    # 并且根据id降序排列

    query = query.filter(FieldHouseinfo.belong == 0, FieldHouseinfo.pid == 0)
    data_infos = query.order_by(desc(FieldHouseinfo.id)).paginate(page=pageNum, per_page=pageSize, error_out=False)
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


@field.route('/field/houseinfo/add', methods=['POST'])
def add_houseinfo():
    data = request.get_json()
    # 校验必填字段
    if not data.get('name') or str(data.get('name')).strip() == '':
        return jsonify({"code": 400, "msg": '监测站点名称不能为空'})
    # belong为0
    data['belong'] = 0
    # 作物密度比例不能为空
    data['area_pro'] = 0
    data['pid'] = 0
    data['grass_quantity'] = 0
    # print(data)
    data_info = FieldHouseinfo()
    for key, value in data.items():
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


@field.route('/field/houseinfo/edit', methods=['POST'])
def edit_houseinfo():
    data = request.get_json()
    # print("--data-->", data)
    id = data['id']
    FieldHouseinfo.query.filter_by(id=id).update(data)
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


@field.route('/field/houseinfo/del', methods=['POST'])
def del_houseinfo():
    ids = request.get_json()
    for i in ids:
        sons = FieldHouseinfo.query.filter_by(pid=i).all()
        if len(sons) > 0:
            # return jsonify(status=200, data=None, msg='棚栏下存在栏舍，删除失败，请先删除其下的数据再来操作')
            return jsonify({
                "code": 500,
                "msg": '监测区域下存在监测地块，删除失败，请先删除其下的数据再来操作'
            })

        for i in sons:
            if i.grass_quantity > 0:
                return jsonify({
                    "code": 500,
                    "msg": '监测地块下存在田块记录，删除失败，请先迁移数据再操作'
                })


    for i in ids:
        FieldHouseinfo.query.filter_by(id=i).delete()
    db.session.commit()
    return jsonify({
        "code": 200,
        "msg": '删除成功'
    })

# 初始化棚舍
@field.route('/field/hurdleinfo/initHouse', methods=['POST'])
def init_house():
    data = FieldHouseinfo.query.filter_by(belong=0, pid=0).all()
    list = []
    for info in data:
        list.append({"value": info.id, "label": info.name})
    result = {
        "code": 200,
        "data": {
            "list": list,
        },
        "msg": '监测区域列表获取成功'
    }
    return jsonify(result)


# hurdleinfo 监测地块信息
@field.route('/field/hurdleinfo', methods=['POST'])
def get_hurdleinfo():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))
    house_id = request.json.get('house_id')

    conditions = []
    search_params = {
        'id': FieldHouseinfo.id,
        'name': FieldHouseinfo.name,
        'function': FieldHouseinfo.function,
        'area': FieldHouseinfo.area,
        'h_type': FieldHouseinfo.h_type,
        'h_lwh': FieldHouseinfo.h_lwh,
        'sports_lwh': FieldHouseinfo.sports_lwh,
        'grass_type': FieldHouseinfo.grass_type,
        'area_pro': FieldHouseinfo.area_pro,
        'grass_quantity': FieldHouseinfo.grass_quantity,
        'build_time': FieldHouseinfo.build_time,
        'staff': FieldHouseinfo.staff,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'build_time':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = FieldHouseinfo.query.filter(and_(*conditions))
    else:
        query = FieldHouseinfo.query  # 如果没有条件，查询所有

    # 筛选出监测地块(pid!=0)
    # 并且根据id降序排列

    query = query.filter(FieldHouseinfo.belong == 0, FieldHouseinfo.pid != 0)
    if house_id is not None and str(house_id).strip() != '':
        query = query.filter(FieldHouseinfo.pid == int(house_id))
    data_infos = query.order_by(desc(FieldHouseinfo.id)).paginate(page=pageNum, per_page=pageSize, error_out=False)
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


@field.route('/field/hurdleinfo/add', methods=['POST'])
def add_hurdleinfo():
    data = request.get_json()
    # 校验必填字段
    if not data.get('name') or str(data.get('name')).strip() == '':
        return jsonify({"code": 400, "msg": '监测地块名称不能为空'})
    # belong为0
    data['belong'] = 0
    # 作物密度比例不能为空
    data['area_pro'] = 0
    house_id = request.json.get('house_id')
    if not house_id or str(house_id).strip() == '':
        return jsonify({"code": 400, "msg": '请先选择所属监测站点'})
    data['pid'] = int(house_id)
    data['grass_quantity'] = 0
    # print(data)
    data_info = FieldHouseinfo()
    for key, value in data.items():
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


@field.route('/field/hurdleinfo/edit', methods=['POST'])
def edit_hurdleinfo():
    data = request.get_json()
    # print("--data-->", data)
    id = data['id']

    # 空值保护：pid 和 house_id 不能为空字符串
    if 'pid' in data and (data['pid'] == '' or data['pid'] is None):
        data['pid'] = 0
    house_id = data.get('house_id')
    if house_id is not None and str(house_id).strip() == '':
        data['pid'] = 0

    FieldHouseinfo.query.filter_by(id=id).update(data)
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


# 合并监测地块
@field.route('/field/hurdleinfo/set', methods=['POST'])
def set_hurdle():
    # 获取监测地块编号
    ids = request.get_json()

    # 获取要合并的监测地块信息
    houses_to_merge = FieldHouseinfo.query.filter(FieldHouseinfo.id.in_(ids)).all()

    if not houses_to_merge:
        return jsonify({
            "code": 500,
            "msg": '没有找到需要合并的监测地块'
        })

    # 检查每个监测地块是否有记录，如果有记录则无法删除
    for house in houses_to_merge:
        if house.grass_quantity > 0:
            return jsonify({
                "code": 500,
                "msg": '监测地块下存在田块记录，合并失败，请先将记录转移再来操作'
            })

    # 获取要保留的字段（第一个监测地块的值）
    pid = houses_to_merge[0].pid  # 监测区域按照合并前归属
    build_time = houses_to_merge[0].build_time  # 建立时间
    function = houses_to_merge[0].function  # 功能
    h_type = houses_to_merge[0].h_type  # 区域类型
    staff = houses_to_merge[0].staff  # 责任人员
    f_staff = houses_to_merge[0].f_staff  # 创建人员
    difinfect_time = houses_to_merge[0].difinfect_time  # 消杀时间
    grass_type = houses_to_merge[0].grass_type  # 作物类型
    belong = 0  # 默认值
    grass_quantity = 0  # 默认值

    # 拼接需要拼接的字段
    name_str = ','.join(house.name for house in houses_to_merge)  # 分区名称
    h_lwh_str = ','.join(house.h_lwh for house in houses_to_merge)  # 分区长宽高
    sports_lwh_str = ','.join(house.sports_lwh for house in houses_to_merge)  # 缓冲区长宽高
    area_pro_str = ','.join(house.area_pro for house in houses_to_merge)  # 作物密度比例

    # 获取每个监测地块的 area 字段（假设是浮动类型）
    areas = [house.area for house in houses_to_merge]

    # 拼接 area 字段并保存到 add_area（字符串类型字段）
    add_area_str = ','.join(map(str, areas))  # 将浮动类型的 area 转换为字符串并拼接

    # 计算 area 字段的总和
    total_area = sum(areas)  # 对浮动类型列表求和

    # 创建新的监测地块记录（合并后的监测地块）
    new_house = FieldHouseinfo(
        pid=pid,
        build_time=build_time,
        function=function,
        h_type=h_type,
        staff=staff,
        f_staff=f_staff,
        difinfect_time=difinfect_time,
        belong=belong,  # 默认值
        grass_quantity=grass_quantity,  # 默认值
        grass_type=grass_type,  # 默认值
        name=name_str,  # 拼接后的 name 字段
        h_lwh=h_lwh_str,  # 拼接后的 h_lwh 字段
        sports_lwh=sports_lwh_str,  # 拼接后的 sports_lwh 字段
        area_pro=area_pro_str,  # 拼接后的 area_pro 字段
        add_area=add_area_str,  # 拼接后的 area 字段
        area=total_area  # 保存总和到 area 字段
    )

    # 将合并的监测地块记录保存到数据库
    db.session.add(new_house)

    # 删除原有的监测地块记录
    for house in houses_to_merge:
        db.session.delete(house)

    # 提交事务
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        result = {
            "code": 500,
            "msg": f'合并失败 {str(e)}'
        }
        return jsonify(result)

    return jsonify({
        "code": 200,
        "msg": '合并成功'
    })


# 拆分监测地块
@field.route('/field/hurdleinfo/unseal', methods=['POST'])
def unseal_hurdle():
    # 获取监测地块编号
    ids = request.get_json()

    # 获取要拆分的监测地块信息
    houses_to_unseal = FieldHouseinfo.query.filter(FieldHouseinfo.id.in_(ids)).all()

    if not houses_to_unseal:
        return jsonify({
            "code": 500,
            "msg": '没有找到要拆分的监测地块'
        })

    # 检查每个监测地块是否可以拆分
    for house in houses_to_unseal:
        if not house.add_area:
            return jsonify({
                "code": 500,
                "msg": '拆分失败，该监测地块已为最小单位'
            })
    # 开始拆分监测地块
    new_houses = []  # 用来保存拆分后的新监测地块

    for house in houses_to_unseal:
        # 获取合并时拼接的字段并按逗号拆分
        name_list = house.name.split(',')
        h_lwh_list = house.h_lwh.split(',')
        sports_lwh_list = house.sports_lwh.split(',')
        area_pro_list = house.area_pro.split(',')
        add_area_list = house.add_area.split(',')

        # 拆分后的数量应该是拼接字段的数量（假设所有字段拆分后数量相同）
        num_splits = len(name_list)

        # 生成拆分后的监测地块记录
        for i in range(num_splits):
            # 创建拆分后的新监测地块
            new_house = FieldHouseinfo(
                pid=house.pid,
                build_time=house.build_time,
                function=house.function,
                h_type=house.h_type,
                staff=house.staff,
                f_staff=house.f_staff,
                difinfect_time=house.difinfect_time,
                belong=house.belong,  # 保持不变
                grass_quantity=house.grass_quantity,  # 田块数量，保持不变
                grass_type=house.grass_type,  # 作物类型，保持不变
                name=name_list[i],  # 拆分后的分区名称
                h_lwh=h_lwh_list[i],  # 拆分后的分区长宽高
                sports_lwh=sports_lwh_list[i],  # 拆分后的缓冲区长宽高
                area_pro=area_pro_list[i],  # 拆分后的作物密度比例
                add_area=None,  # 拆分后无附加区域
                area=float(add_area_list[i])  # 计算拆分后的面积
            )

            new_houses.append(new_house)

        # 删除原来的合并监测地块
        db.session.delete(house)

    # 将拆分后的监测地块记录保存到数据库
    try:
        db.session.add_all(new_houses)  # 批量添加新记录
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        return jsonify({
            "code": 500,
            "msg": f'拆分失败: {str(e)}'
        })

    return jsonify({
        "code": 200,
        "msg": '拆分成功'
    })


@field.route('/field/hurdleinfo/del', methods=['POST'])
def del_hurdleinfo():
    # 获取监测地块编号
    ids = request.get_json()
    # 可以一次删除多个监测地块，遍历每个地块，判断是否有田块记录，有则不能删除
    for i in ids:
        # 获取该监测地块信息
        item = FieldHouseinfo.query.filter_by(id=i).first()
        # 判断该监测地块是否有田块记录
        if item.grass_quantity > 0:
            return jsonify({
                "code": 500,
                "msg": '监测地块下存在田块记录，删除失败，请先将记录转移再来操作'
            })

        FieldHouseinfo.query.filter_by(id=i).delete()

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


@field.route('/field/houseinfo/updateHouseNumber', methods=['POST'])
def update_house_number():
    colony_infos = FieldHouseinfo.query.filter_by(belong=0, pid=0).all()
    for info in colony_infos:
        info.grass_quantity = BasicBasicinfo.query.filter_by(house_id=info.id).count()
        if info.grass_quantity != 0:
            info.area_pro = info.area / info.grass_quantity
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        result = {
            "code": 500,
            "msg": f'更新地块信息失败 {str(e)}'
        }
        return jsonify(result)
    result = {
        "code": 200,
        "msg": '更新地块信息成功'
    }
    return jsonify(result)
    result = {
        "code": 200,
        "msg": '更新地块信息成功'
    }
    return jsonify(result)


@field.route('/field/hurdleinfo/updateHurdleNumber', methods=['POST'])
def update_hurdle_number():
    colony_infos = FieldHouseinfo.query.filter(FieldHouseinfo.belong == 0, FieldHouseinfo.pid != 0).all()
    for info in colony_infos:
        info.grass_quantity = BasicBasicinfo.query.filter_by(hurdle_id=info.id).count()
        if info.grass_quantity != 0:
            info.area_pro = info.area / info.grass_quantity
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        result = {
            "code": 500,
            "msg": f'更新地块信息失败 {str(e)}'
        }
        return jsonify(result)
    result = {
        "code": 200,
        "msg": '更新地块信息成功'
    }
    return jsonify(result)


@field.route('/field/hurdleinfo/disinfectHurdle', methods=['POST'])
def disinfect_hurdle():
    data = request.get_json()
    ids = data['hurdle_ids']
    data.pop('hurdle_ids')
    list = []
    for id in ids:
        disinfect_info = FieldDisinfectioninfo()
        disinfect_info.house_id = id
        disinfect_info.belong = 0
        for key, value in data.items():
            setattr(disinfect_info, key, value)
        list.append(disinfect_info)
        hurdle_info = FieldHouseinfo.query.filter_by(id=id).first()
        hurdle_info.difinfect_time = data['date']
    try:
        db.session.add_all(list)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        result = {
            "code": 500,
            "msg": f'消毒失败 {str(e)}'
        }
        return jsonify(result)
    result = {
        "code": 200,
        "msg": '消毒成功'
    }
    return jsonify(result)


@field.route('/field/disinfectioninfo', methods=['POST'])
def get_disinfectioninfo():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        'house_id': FieldDisinfectioninfo.house_id,
        'date': FieldDisinfectioninfo.date,
        'staff': FieldDisinfectioninfo.staff,
        'drug': FieldDisinfectioninfo.drug,
        'dose': FieldDisinfectioninfo.dose,
        'method': FieldDisinfectioninfo.method,
        'notes': FieldDisinfectioninfo.notes,
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
        query = FieldDisinfectioninfo.query.filter(and_(*conditions))
    else:
        query = FieldDisinfectioninfo.query  # 如果没有条件，查询所有

    # 根据id降序排列

    query = query.filter(FieldDisinfectioninfo.belong == 0)
    data_infos = query.order_by(desc(FieldDisinfectioninfo.id)).paginate(page=pageNum, per_page=pageSize,
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


@field.route('/field/test', methods=['POST'])
def get_test():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        'id': FieldHouseinfo.id,
        'name': FieldHouseinfo.name,
        'function': FieldHouseinfo.function,
        'area': FieldHouseinfo.area,
        'h_type': FieldHouseinfo.h_type,
        'h_lwh': FieldHouseinfo.h_lwh,
        'sports_lwh': FieldHouseinfo.sports_lwh,
        'grass_type': FieldHouseinfo.grass_type,
        'area_pro': FieldHouseinfo.area_pro,
        'grass_quantity': FieldHouseinfo.grass_quantity,
        'build_time': FieldHouseinfo.build_time,
        'staff': FieldHouseinfo.staff,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'build_time':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = FieldHouseinfo.query.filter(and_(*conditions))
    else:
        query = FieldHouseinfo.query  # 如果没有条件，查询所有

    # 筛选出棚(pid==0)
    # 并且根据id降序排列

    query = query.filter(FieldHouseinfo.belong == 0, FieldHouseinfo.pid == 0)
    data_infos = query.order_by(desc(FieldHouseinfo.id)).paginate(page=pageNum, per_page=pageSize, error_out=False)
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


@field.route('/field/test/add', methods=['POST'])
def add_test():
    data = request.get_json()
    # belong为0
    data['belong'] = 0
    # 草只面积比例不能为空
    data['area_pro'] = 0
    data['pid'] = 0
    # print(data)
    data_info = FieldHouseinfo()
    for key, value in data.items():
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


@field.route('/field/test/edit', methods=['POST'])
def edit_test():
    data = request.get_json()
    # print("--data-->", data)
    id = data['id']
    FieldHouseinfo.query.filter_by(id=id).update(data)
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


@field.route('/field/test/del', methods=['POST'])
def del_test():
    ids = request.get_json()
    for i in ids:
        sons = FieldHouseinfo.query.filter_by(pid=i).all()
        if len(sons) > 0:
            return jsonify({
                "code": 500,
                "msg": '监测区域下存在监测地块，删除失败，请先删除其下的数据再来操作'
            })

        for i in sons:
            if i.grass_quantity > 0:
                return jsonify({
                    "code": 500,
                    "msg": '监测区域下存在田块记录，删除失败，请先将记录转移再来操作'
                })

    for i in ids:
        FieldHouseinfo.query.filter_by(id=i).delete()
    db.session.commit()
    return jsonify({
        "code": 200,
        "msg": '删除成功'
    })


@field.route('/field/maintenanceinfo', methods=['POST'])
def get_field_maintenanceinfo_list():
    pageNum = int(request.json.get('pageNum', 1))
    pageSize = int(request.json.get('pageSize', 10))
    conditions = []
    search_params = {
        'house_id': FieldMaintenanceinfo.house_id,
        'M_condition': FieldMaintenanceinfo.M_condition,
        'M_details': FieldMaintenanceinfo.M_details,
        'M_time': FieldMaintenanceinfo.M_time,
        'M_cost': FieldMaintenanceinfo.M_cost,
        'f_date': FieldMaintenanceinfo.f_date,
        'f_staff': FieldMaintenanceinfo.f_staff,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:
            conditions.append(column == value)
    if conditions:
        query = FieldMaintenanceinfo.query.filter(and_(*conditions))
    else:
        query = FieldMaintenanceinfo.query
    infos = query.filter(FieldMaintenanceinfo.belong == 0).paginate(page=pageNum, per_page=pageSize, error_out=False)
    total = query.count()
    list = []
    for info in infos:
        list.append({
            'id': info.id,
            'house_id': info.house_id,
            'M_condition': info.M_condition,
            'M_details': info.M_details,
            'M_time': info.M_time,
            'M_cost': info.M_cost,
            'f_date': info.f_date,
            'f_staff': info.f_staff,
        })
    result = {"code": 200, "data": {"list": list, "pageNum": pageNum, "pageSize": pageSize, "total": total}, "msg": '成功'}
    return jsonify(result)


@field.route('/field/maintenanceinfo/add', methods=['POST'])
def add_field_maintenanceinfo():
    data = request.get_json()
    data['belong'] = 0
    obj = FieldMaintenanceinfo()
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


@field.route('/field/maintenanceinfo/edit', methods=['POST'])
def edit_field_maintenanceinfo():
    data = request.get_json()
    id = data.get('id')
    if not id:
        return jsonify({"code": 400, "msg": '缺少id'})
    FieldMaintenanceinfo.query.filter_by(id=id).update(data)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        return jsonify({"code": 500, "msg": f'修改失败 {str(e)}'})
    return jsonify({"code": 200, "msg": '修改成功'})


@field.route('/field/maintenanceinfo/del', methods=['POST'])
def del_field_maintenanceinfo():
    data = request.get_json()
    id = data.get('id')
    if not id:
        return jsonify({"code": 400, "msg": '缺少id'})
    obj = FieldMaintenanceinfo.query.get(id)
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


@field.route('/field/transferinfo', methods=['POST'])
def get_field_transferinfo_list():
    pageNum = int(request.json.get('pageNum', 1))
    pageSize = int(request.json.get('pageSize', 10))
    conditions = []
    search_params = {
        'basic_id': FieldTransferinfo.basic_id,
        'new_house_id': FieldTransferinfo.new_house_id,
        'old_house_id': FieldTransferinfo.old_house_id,
        'reason': FieldTransferinfo.reason,
        'trans_time': FieldTransferinfo.trans_time,
        'grass_type': FieldTransferinfo.grass_type,
        'f_date': FieldTransferinfo.f_date,
        'f_staff': FieldTransferinfo.f_staff,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:
            conditions.append(column == value)
    if conditions:
        query = FieldTransferinfo.query.filter(and_(*conditions))
    else:
        query = FieldTransferinfo.query
    infos = query.filter(FieldTransferinfo.belong == 0).paginate(page=pageNum, per_page=pageSize, error_out=False)
    total = query.count()
    list = []
    for info in infos:
        list.append({
            'id': info.id,
            'basic_id': info.basic_id,
            'new_house_id': info.new_house_id,
            'old_house_id': info.old_house_id,
            'reason': info.reason,
            'trans_time': info.trans_time,
            'grass_type': info.grass_type,
            'f_date': info.f_date,
            'f_staff': info.f_staff,
        })
    result = {"code": 200, "data": {"list": list, "pageNum": pageNum, "pageSize": pageSize, "total": total}, "msg": '成功'}
    return jsonify(result)


@field.route('/field/transferinfo/add', methods=['POST'])
def add_field_transferinfo():
    data = request.get_json()
    data['belong'] = 0
    obj = FieldTransferinfo()
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


@field.route('/field/transferinfo/edit', methods=['POST'])
def edit_field_transferinfo():
    data = request.get_json()
    id = data.get('id')
    if not id:
        return jsonify({"code": 400, "msg": '缺少id'})
    FieldTransferinfo.query.filter_by(id=id).update(data)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        return jsonify({"code": 500, "msg": f'修改失败 {str(e)}'})
    return jsonify({"code": 200, "msg": '修改成功'})


@field.route('/field/transferinfo/del', methods=['POST'])
def del_field_transferinfo():
    data = request.get_json()
    id = data.get('id')
    if not id:
        return jsonify({"code": 400, "msg": '缺少id'})
    obj = FieldTransferinfo.query.get(id)
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
