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

colony = Blueprint('colony', __name__)


@colony.route('/colony/houseinfo', methods=['POST'])
def get_houseinfo():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        'id': ColonyHouseinfo.id,
        'name': ColonyHouseinfo.name,
        'function': ColonyHouseinfo.function,
        'area': ColonyHouseinfo.area,
        'h_type': ColonyHouseinfo.h_type,
        'h_lwh': ColonyHouseinfo.h_lwh,
        'sports_lwh': ColonyHouseinfo.sports_lwh,
        'sheep_type': ColonyHouseinfo.sheep_type,
        'area_pro': ColonyHouseinfo.area_pro,
        'sheep_quantity': ColonyHouseinfo.sheep_quantity,
        'build_time': ColonyHouseinfo.build_time,
        'staff': ColonyHouseinfo.staff,
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
        query = ColonyHouseinfo.query.filter(and_(*conditions))
    else:
        query = ColonyHouseinfo.query  # 如果没有条件，查询所有

    # 筛选出棚(pid==0)
    # 并且根据id降序排列

    query = query.filter(ColonyHouseinfo.belong == 0, ColonyHouseinfo.pid == 0)
    data_infos = query.order_by(desc(ColonyHouseinfo.id)).paginate(page=pageNum, per_page=pageSize, error_out=False)
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


@colony.route('/colony/houseinfo/add', methods=['POST'])
def add_houseinfo():
    data = request.get_json()
    # belong为0
    data['belong'] = 0
    # 作物密度比例不能为空
    data['area_pro'] = 0
    data['pid'] = 0
    data['sheep_quantity'] = 0
    # print(data)
    data_info = ColonyHouseinfo()
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


@colony.route('/colony/houseinfo/edit', methods=['POST'])
def edit_houseinfo():
    data = request.get_json()
    # print("--data-->", data)
    id = data['id']
    ColonyHouseinfo.query.filter_by(id=id).update(data)
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


@colony.route('/colony/houseinfo/del', methods=['POST'])
def del_houseinfo():
    ids = request.get_json()
    for i in ids:
        sons = ColonyHouseinfo.query.filter_by(pid=i).all()
        if len(sons) > 0:
            # return jsonify(status=200, data=None, msg='棚栏下存在栏舍，删除失败，请先删除其下的数据再来操作')
            return jsonify({
                "code": 500,
                "msg": '监测区域下存在监测地块，删除失败，请先删除其下的数据再来操作'
            })

        for i in sons:
            if i.sheep_quantity > 0:
                return jsonify({
                    "code": 500,
                    "msg": '监测地块下存在田块记录，删除失败，请先迁移数据再操作'
                })


    for i in ids:
        ColonyHouseinfo.query.filter_by(id=i).delete()
    db.session.commit()
    return jsonify({
        "code": 200,
        "msg": '删除成功'
    })

# 初始化棚舍
@colony.route('/colony/hurdleinfo/initHouse', methods=['POST'])
def init_house():
    data = ColonyHouseinfo.query.filter_by(belong=0, pid=0).all()
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
@colony.route('/colony/hurdleinfo', methods=['POST'])
def get_hurdleinfo():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))
    house_id = request.json.get('house_id')

    conditions = []
    search_params = {
        'id': ColonyHouseinfo.id,
        'name': ColonyHouseinfo.name,
        'function': ColonyHouseinfo.function,
        'area': ColonyHouseinfo.area,
        'h_type': ColonyHouseinfo.h_type,
        'h_lwh': ColonyHouseinfo.h_lwh,
        'sports_lwh': ColonyHouseinfo.sports_lwh,
        'sheep_type': ColonyHouseinfo.sheep_type,
        'area_pro': ColonyHouseinfo.area_pro,
        'sheep_quantity': ColonyHouseinfo.sheep_quantity,
        'build_time': ColonyHouseinfo.build_time,
        'staff': ColonyHouseinfo.staff,
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
        query = ColonyHouseinfo.query.filter(and_(*conditions))
    else:
        query = ColonyHouseinfo.query  # 如果没有条件，查询所有

    # 筛选出监测地块(pid!=0)
    # 并且根据id降序排列

    query = query.filter(ColonyHouseinfo.belong == 0, ColonyHouseinfo.pid != 0,
                         ColonyHouseinfo.pid == house_id)
    data_infos = query.order_by(desc(ColonyHouseinfo.id)).paginate(page=pageNum, per_page=pageSize, error_out=False)
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


@colony.route('/colony/hurdleinfo/add', methods=['POST'])
def add_hurdleinfo():
    data = request.get_json()
    # belong为0
    data['belong'] = 0
    # 作物密度比例不能为空
    data['area_pro'] = 0
    data['pid'] = request.json.get('house_id')
    data['sheep_quantity'] = 0
    # print(data)
    data_info = ColonyHouseinfo()
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


@colony.route('/colony/hurdleinfo/edit', methods=['POST'])
def edit_hurdleinfo():
    data = request.get_json()
    # print("--data-->", data)
    id = data['id']

    ColonyHouseinfo.query.filter_by(id=id).update(data)
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
@colony.route('/colony/hurdleinfo/set', methods=['POST'])
def set_hurdle():
    # 获取监测地块编号
    ids = request.get_json()

    # 获取要合并的监测地块信息
    houses_to_merge = ColonyHouseinfo.query.filter(ColonyHouseinfo.id.in_(ids)).all()

    if not houses_to_merge:
        return jsonify({
            "code": 500,
            "msg": '没有找到需要合并的监测地块'
        })

    # 检查每个监测地块是否有记录，如果有记录则无法删除
    for house in houses_to_merge:
        if house.sheep_quantity > 0:
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
    sheep_type = houses_to_merge[0].sheep_type  # 作物类型
    belong = 0  # 默认值
    sheep_quantity = 0  # 默认值

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
    new_house = ColonyHouseinfo(
        pid=pid,
        build_time=build_time,
        function=function,
        h_type=h_type,
        staff=staff,
        f_staff=f_staff,
        difinfect_time=difinfect_time,
        belong=belong,  # 默认值
        sheep_quantity=sheep_quantity,  # 默认值
        sheep_type=sheep_type,  # 默认值
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
@colony.route('/colony/hurdleinfo/unseal', methods=['POST'])
def unseal_hurdle():
    # 获取监测地块编号
    ids = request.get_json()

    # 获取要拆分的监测地块信息
    houses_to_unseal = ColonyHouseinfo.query.filter(ColonyHouseinfo.id.in_(ids)).all()

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
            new_house = ColonyHouseinfo(
                pid=house.pid,
                build_time=house.build_time,
                function=house.function,
                h_type=house.h_type,
                staff=house.staff,
                f_staff=house.f_staff,
                difinfect_time=house.difinfect_time,
                belong=house.belong,  # 保持不变
                sheep_quantity=house.sheep_quantity,  # 田块数量，保持不变
                sheep_type=house.sheep_type,  # 作物类型，保持不变
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


@colony.route('/colony/hurdleinfo/del', methods=['POST'])
def del_hurdleinfo():
    # 获取监测地块编号
    ids = request.get_json()
    # 可以一次删除多个监测地块，遍历每个地块，判断是否有田块记录，有则不能删除
    for i in ids:
        # 获取该监测地块信息
        item = ColonyHouseinfo.query.filter_by(id=i).first()
        # 判断该监测地块是否有田块记录
        if item.sheep_quantity > 0:
            return jsonify({
                "code": 500,
                "msg": '监测地块下存在田块记录，删除失败，请先将记录转移再来操作'
            })

        ColonyHouseinfo.query.filter_by(id=i).delete()

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


@colony.route('/colony/houseinfo/updateHouseNumber', methods=['POST'])
def update_house_number():
    colony_infos = ColonyHouseinfo.query.filter_by(belong=0, pid=0).all()
    for info in colony_infos:
        info.sheep_quantity = BasicBasicinfo.query.filter_by(house_id=info.id).count()
        if info.sheep_quantity != 0:
            info.area_pro = info.area / info.sheep_quantity
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


@colony.route('/colony/hurdleinfo/updateHurdleNumber', methods=['POST'])
def update_hurdle_number():
    colony_infos = ColonyHouseinfo.query.filter(ColonyHouseinfo.belong == 0, ColonyHouseinfo.pid != 0).all()
    for info in colony_infos:
        info.sheep_quantity = BasicBasicinfo.query.filter_by(hurdle_id=info.id).count()
        if info.sheep_quantity != 0:
            info.area_pro = info.area / info.sheep_quantity
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


@colony.route('/colony/hurdleinfo/disinfectHurdle', methods=['POST'])
def disinfect_hurdle():
    data = request.get_json()
    ids = data['hurdle_ids']
    data.pop('hurdle_ids')
    list = []
    for id in ids:
        disinfect_info = ColonyDisinfectioninfo()
        disinfect_info.house_id = id
        disinfect_info.belong = 0
        for key, value in data.items():
            setattr(disinfect_info, key, value)
        list.append(disinfect_info)
        hurdle_info = ColonyHouseinfo.query.filter_by(id=id).first()
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


@colony.route('/colony/disinfectioninfo', methods=['POST'])
def get_disinfectioninfo():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        'house_id': ColonyDisinfectioninfo.house_id,
        'date': ColonyDisinfectioninfo.date,
        'staff': ColonyDisinfectioninfo.staff,
        'drug': ColonyDisinfectioninfo.drug,
        'dose': ColonyDisinfectioninfo.dose,
        'method': ColonyDisinfectioninfo.method,
        'notes': ColonyDisinfectioninfo.notes,
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
        query = ColonyDisinfectioninfo.query.filter(and_(*conditions))
    else:
        query = ColonyDisinfectioninfo.query  # 如果没有条件，查询所有

    # 根据id降序排列

    query = query.filter(ColonyDisinfectioninfo.belong == 0)
    data_infos = query.order_by(desc(ColonyDisinfectioninfo.id)).paginate(page=pageNum, per_page=pageSize,
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


@colony.route('/colony/test', methods=['POST'])
def get_test():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        'id': ColonyHouseinfo.id,
        'name': ColonyHouseinfo.name,
        'function': ColonyHouseinfo.function,
        'area': ColonyHouseinfo.area,
        'h_type': ColonyHouseinfo.h_type,
        'h_lwh': ColonyHouseinfo.h_lwh,
        'sports_lwh': ColonyHouseinfo.sports_lwh,
        'sheep_type': ColonyHouseinfo.sheep_type,
        'area_pro': ColonyHouseinfo.area_pro,
        'sheep_quantity': ColonyHouseinfo.sheep_quantity,
        'build_time': ColonyHouseinfo.build_time,
        'staff': ColonyHouseinfo.staff,
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
        query = ColonyHouseinfo.query.filter(and_(*conditions))
    else:
        query = ColonyHouseinfo.query  # 如果没有条件，查询所有

    # 筛选出棚(pid==0)
    # 并且根据id降序排列

    query = query.filter(ColonyHouseinfo.belong == 0, ColonyHouseinfo.pid == 0)
    data_infos = query.order_by(desc(ColonyHouseinfo.id)).paginate(page=pageNum, per_page=pageSize, error_out=False)
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


@colony.route('/colony/test/add', methods=['POST'])
def add_test():
    data = request.get_json()
    # belong为0
    data['belong'] = 0
    # 羊只面积比例不能为空
    data['area_pro'] = 0
    data['pid'] = 0
    # print(data)
    data_info = ColonyHouseinfo()
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


@colony.route('/colony/test/edit', methods=['POST'])
def edit_test():
    data = request.get_json()
    # print("--data-->", data)
    id = data['id']
    ColonyHouseinfo.query.filter_by(id=id).update(data)
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


@colony.route('/colony/test/del', methods=['POST'])
def del_test():
    ids = request.get_json()
    for i in ids:
        sons = ColonyHouseinfo.query.filter_by(pid=i).all()
        if len(sons) > 0:
            return jsonify({
                "code": 500,
                "msg": '监测区域下存在监测地块，删除失败，请先删除其下的数据再来操作'
            })

        for i in sons:
            if i.sheep_quantity > 0:
                return jsonify({
                    "code": 500,
                    "msg": '监测区域下存在田块记录，删除失败，请先将记录转移再来操作'
                })

    for i in ids:
        ColonyHouseinfo.query.filter_by(id=i).delete()
    db.session.commit()
    return jsonify({
        "code": 200,
        "msg": '删除成功'
    })
