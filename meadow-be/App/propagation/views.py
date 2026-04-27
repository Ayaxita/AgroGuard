# views.py: 路由 + 视图函数
import datetime
from datetime import datetime, timedelta  # 导入 timedelta 而不是 datetime.timedelt
import os
import random
import json
import shutil

# import flask_cache
from dateutil.relativedelta import relativedelta
from flask import Blueprint, render_template, request, make_response, Response, redirect, url_for, session, jsonify, \
    send_file
from flask_jwt_extended import jwt_required
from sqlalchemy import desc, and_, or_, not_, text
import pandas as pd

# from .models import *
from sqlalchemy.orm import aliased

from ..modelsReverse import *
from ..utils.AlchemyEncoder import AlchemyEncoder
# 获取数据库数据
propagation = Blueprint('propagation', __name__)


#将死新草地信息回显到list的最后一个,在生长记录编辑和查看的时候用
def move_state_one_to_end(data_list):
    state_one_list = []
    other_list = []
    for data in data_list:
        if data.get('state') == 1:  # 使用 get 方法避免键不存在时引发错误
            state_one_list.append(data)
        else:
            other_list.append(data)
    other_list.extend(state_one_list)  # 将 state 为 1 的列表添加到其他列表的后面
    return other_list

#草地生长监测信息
@propagation.route('/propagation/growth_statusinfo', methods=['POST'])#获取草地生长监测信息
def get_growth_statusinfo():
    pageNum = int(request.json.get('pageNum'))
    # pageNum = int(request.form.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        'ele_num': ECultivationSeedinginfo.basic_id,
        'pre_num': ECultivationSeedinginfo.basic_id,
        'age': ECultivationSeedinginfo.age,
'seeding_status': ECultivationSeedinginfo.seeding_status,
        'belong': ECultivationSeedinginfo.belong,
        'f_staff': ECultivationSeedinginfo.f_staff,
        'f_date': ECultivationSeedinginfo.f_date,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'f_date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            elif param == 'ele_num':
                # 修改为模糊查询
                basic_ids = [basic.id for basic in BasicBasicinfo.query.filter(
                    BasicBasicinfo.ele_num.like(f'%{value}%')).all()]
                if basic_ids:
                    conditions.append(column.in_(basic_ids))
            elif param == 'pre_num':
                basic_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.pre_num.like(f'%{value}%')).first().id
                conditions.append(column == basic_id)
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = ECultivationSeedinginfo.query.filter(and_(*conditions))
    else:
        query = ECultivationSeedinginfo.query  # 如果没有条件，查询所有

    # 筛选出没有被移除的草(状态-1)和没有枯萎的草(状态0)
    # 并且根据id降序排列

    # 并且根据id降序排列

    query = query.filter(ECultivationSeedinginfo.belong == 0)
    infos = query.order_by(desc(ECultivationSeedinginfo.id)).paginate(page=pageNum, per_page=pageSize,
                                                                  error_out=False)
    total = query.count()

    list = []
    for info in infos:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        data = json.loads(data)
        basic_info = BasicBasicinfo.query.filter_by(id=data['basic_id']).first()#从基本表里查耳号添加到里面
        if basic_info:
            data['ele_num'] = basic_info.ele_num
            data['pre_num'] = basic_info.pre_num
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

@propagation.route('/propagation/growth_statusinfo/del', methods=['POST'])#删除草地生长监测信息
def del_growth_statusinfo():
    ids = request.get_json()
    print("______________________________________")
    print(ids)
    for i in ids:
        ECultivationSeedinginfo.query.filter_by(id=i).delete()
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

@propagation.route('/propagation/growth_statusinfo/edit', methods=['POST'])#编辑草地生长监测信息
def edit_growth_statusinfo():
    data = request.get_json()
    print("--data-->", data)
    id = data['id']
    # ele_id = data['ele_num']
    # pre_id = data['pre_num']
    try:
        # 获取字段basic_id并删除无用字段ele_num和pre_num
        if 'ele_num' in data:
            data["basic_id"] = BasicBasicinfo.query.filter(
                BasicBasicinfo.ele_num ==data['ele_num']).first().id
            del data['ele_num']
        if 'pre_num' in data:
            data["basic_id"] = BasicBasicinfo.query.filter(
                BasicBasicinfo.pre_num ==data['pre_num']).first().id
            del data['pre_num']

    except Exception as e:
        print("--data-->", data)
        print("--Exception-->", str(e))
    print('--------------------------test--------------------------------')

    # BasicBasicinfo.query.filter_by(ele_id = ele_id,pre_id = pre_id).update(data)
    try:
        # 更新草地生长监测信息表
        ECultivationSeedinginfo.query.filter_by(id=id).update(data)
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

@propagation.route('/propagation/growth_statusinfo/add', methods=['POST'])#添加草地生长监测信息
def add_growth_statusinfo():
    data = request.get_json()
    #去除剂量两端的空格
    # if 'dose' in data:
    #     data['dose'] = data['dose'].strip()
    #     print(data['dose'])

    ctime = datetime.now()
    data['belong'] = 0
    data['f_date'] = ctime



    # 查询对应的 id
    basic_id = BasicBasicinfo.query.filter_by(ele_num=data['ele_num']).first().id

    data['basic_id'] =basic_id
    print(data)

    rut_info= ECultivationSeedinginfo()

    for key, value in data.items():#将data字典里的数据添加到实例对象中
        setattr(rut_info, key, value)
    try:
        db.session.add(rut_info)
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

#  母草地生长监测
#获取月龄8以上的健康未销售的基础草地记录(在生长记录是12月，在生长监测和培育时8月).。。。。。。。。。。。。。改成6月了
@propagation.route('/propagation/growth_statusinfo/get_femalegrass', methods=['POST'])
def get_femalegrass():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))
    # 当前日期
    current_date = datetime.now().date()

    conditions = []
    search_params = {
        'ele_num': BasicBasicinfo.ele_num,
        'pre_num': BasicBasicinfo.pre_num,
        'purpose': BasicBasicinfo.purpose,
        'variety': BasicBasicinfo.variety,
        'color': BasicBasicinfo.color,
        'sex': BasicBasicinfo.sex,
        'birth': BasicBasicinfo.birth,
        'wea_date': BasicBasicinfo.wea_date,
        'wea_weight': BasicBasicinfo.wea_weight,
        'mon_age': BasicBasicinfo.mon_age,
        'manu_info_name': BasicBasicinfo.manu_info_name,
        'state': BasicBasicinfo.state,
        'house_name': BasicBasicinfo.house_name,
        'hurdle_name': BasicBasicinfo.hurdle_name,
        'gene_a': BasicBasicinfo.gene_a,
        'gene_b': BasicBasicinfo.gene_b,
        'gene_c': BasicBasicinfo.gene_c,
        'f_staff': BasicBasicinfo.f_staff,
        'f_date': BasicBasicinfo.f_date,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'birth' or param == 'f_date' or param == 'wea_date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            elif param == 'ele_num' or param == 'pre_num':
                # 修改为模糊查询
                conditions.append(column.like(f'%{value}%'))
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = BasicBasicinfo.query.filter(and_(
            *conditions,  # 原有的动态条件
            BasicBasicinfo.sex == 1,  # 固定条件：性别为1
            BasicBasicinfo.state == 1, # 固定条件：状态为1
            BasicBasicinfo.mon_age >= 6
        ))
    else:
        query = BasicBasicinfo.query.filter(and_(
            BasicBasicinfo.sex == 1,  # 固定条件：性别为1
            BasicBasicinfo.state == 1 , # 固定条件：状态为1
            BasicBasicinfo.mon_age >= 6
        ))  # 如果没有动态条件，只筛选固定条件

    # 筛选出没有被移除的草(状态-1)和没有枯萎的草(状态0)
    # 并且根据id降序排列

    query = query.filter(and_(BasicBasicinfo.state != -1, BasicBasicinfo.state != 0, BasicBasicinfo.belong == 0))

    # # 获取所有记录（不分页）
    # all_records = query.all()

    basic_infos = query.order_by(desc(BasicBasicinfo.id)).paginate(page=pageNum, per_page=pageSize, error_out=False)
    total = query.count()

    # # 过滤出月龄大于等于12的记录
    # filtered_infos = []
    # for info in basic_infos:
    #     if info.birth:  # 确保出生日期存在
    #         # 计算月龄
    #         print('111111111111111111111')
    #         days_diff = (current_date - info.birth).days
    #         mon_age = round(days_diff / 30, 1)
    #         print(mon_age)
    #         if mon_age >= 12:
    #
    #             info.mon_age = mon_age  # 动态添加月龄属性
    #             filtered_infos.append(info)

    list = []
    # print('___+++++++++++++++++++++++++++')
    # print(filtered_infos)
    for info in basic_infos:
        # list.append({
        #     'id': info.id,
        #     'ele_num': info.ele_num,
        #     'pre_num': info.pre_num,
        #     'purpose': info.purpose,
        #     'variety': info.variety,
        #     'sex': info.sex,
        #     'manu_info_id': info.manu_info_id,
        #     'manu_info_name': info.manu_info_name,
        #     'state': info.state,
        #     'birth': info.birth.isoformat(),
        #     'bir_weight': info.bir_weight,
        #     'wea_weight': info.wea_weight,
        #     'house_id': info.house_id,
        #     'hurdle_id': info.hurdle_id,
        #     'house_name': info.house_name,
        #     'hurdle_name': info.hurdle_name,
        #     'mon_age': info.mon_age,
        #     'color': info.color,
        #     'rank': info.rank,
        #     'father_id': info.father_id,
        #     'mother_id': info.mother_id,
        #     'f_ele_num': info.f_ele_num,
        #     'f_pre_num': info.f_pre_num,
        #     'm_ele_num': info.m_ele_num,
        #     'm_pre_num': info.m_pre_num,
        #     'f_staff': info.f_staff,
        #     'f_date': info.f_date.isoformat(),
        #     'img_positive': info.img_positive,
        #     'img_left': info.img_left,
        #     'img_right': info.img_right,
        #     'note': info.note,
        #     'belong': info.belong,
        #     'gene_a': info.gene_a,
        #     'gene_b': info.gene_b,
        #     'gene_c': info.gene_c,
        #     'score': info.score,
        #     'score_2': info.score_2,
        #     'score_6': info.score_6,
        #     'score_12': info.score_12,
        #     'score_24': info.score_24
        # })
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        list.append(json.loads(data))
    print('-----------------------------')
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

@propagation.route('/propagation/growth_statusinfo/export', methods=['POST'])
def export_growth_statusinfo():
    try:
        selected_ids = request.get_json()
        propagation_dict = {
            1: "是",
            0: "否"
        }

        if selected_ids:
            rut_info = (
                db.session.query(ECultivationSeedinginfo, BasicBasicinfo.ele_num, BasicBasicinfo.pre_num)
                    .outerjoin(BasicBasicinfo, BasicBasicinfo.id == ECultivationSeedinginfo.basic_id)
                    .filter(ECultivationSeedinginfo.id.in_(selected_ids))
                    .all()
            )
        else:
            rut_info = (
                db.session.query(ECultivationSeedinginfo, BasicBasicinfo.ele_num, BasicBasicinfo.pre_num)
                    .outerjoin(BasicBasicinfo, BasicBasicinfo.id == ECultivationSeedinginfo.basic_id)
                    .all()
            )

        data_list = []
        for info, ele_num, pre_num in rut_info:
            propagation_value = propagation_dict.get(info.seeding_status, info.seeding_status)
            data_list.append({
                '草地编号': ele_num,
                '地块编号': pre_num,
                '月龄': info.age,
                '是否培育': propagation_value,
                '创建时间': info.f_date.isoformat() if info.f_date else None,
                '创建人员': info.f_staff
            })
        df = pd.DataFrame(data_list)

        export_path = os.path.join(os.getcwd(), 'App', 'propagation', 'export_excel', 'rut_info.xlsx')
        df.to_excel(export_path, index=False)

        return send_file(export_path, as_attachment=True)
    except Exception as e:
        result = {
            "code": 500,
            "msg": f'导出失败 {str(e)}'
        }
        return jsonify(result)


#草地采样信息
@propagation.route('/propagation/sample_collectinfo', methods=['POST'])
def get_sample_collectinfo():
    pageNum = int(request.json.get('pageNum'))
    # pageNum = int(request.form.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        'ele_num': ECultivationPolleninfo.basic_id,
        'pre_num': ECultivationPolleninfo.basic_id,
        'E_date': ECultivationPolleninfo.E_date,
        'dilution_ratio': ECultivationPolleninfo.dilution_ratio,
        'diluent_type': ECultivationPolleninfo.diluent_type,
        'disused': ECultivationPolleninfo.disused,
        'belong': ECultivationSeedinginfo.belong,
        'f_staff': ECultivationSeedinginfo.f_staff,
        'f_date': ECultivationSeedinginfo.f_date,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'f_date'or param == 'E_date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            elif param == 'ele_num':
                # 修改为模糊查询
                basic_ids = [basic.id for basic in BasicBasicinfo.query.filter(
                    BasicBasicinfo.ele_num.like(f'%{value}%')).all()]
                if basic_ids:
                    conditions.append(column.in_(basic_ids))
            elif param == 'pre_num':
                basic_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.pre_num.like(f'%{value}%')).first().id
                conditions.append(column == basic_id)
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = ECultivationPolleninfo.query.filter(and_(*conditions))
    else:
        query = ECultivationPolleninfo.query  # 如果没有条件，查询所有

    # 筛选出没有被移除的草(状态-1)和没有枯萎的草(状态0)
    # 并且根据id降序排列

    # 并且根据id降序排列

    query = query.filter(ECultivationPolleninfo.belong == 0)
    infos = query.order_by(desc(ECultivationPolleninfo.id)).paginate(page=pageNum, per_page=pageSize,
                                                                  error_out=False)
    total = query.count()

    list = []
    for info in infos:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        data = json.loads(data)
        basic_info = BasicBasicinfo.query.filter_by(id=data['basic_id']).first()
        if basic_info:
            data['ele_num'] = basic_info.ele_num
            data['pre_num'] = basic_info.pre_num
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

@propagation.route('/propagation/sample_collectinfo/del', methods=['POST'])
def del_sample_collectinfo():
    ids = request.get_json()
    print("______________________________________")
    print(ids)
    for i in ids:
        ECultivationPolleninfo.query.filter_by(id=i).delete()
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

@propagation.route('/propagation/sample_collectinfo/edit', methods=['POST'])
def edit_sample_collectinfo():
    data = request.get_json()
    print("--data-->", data)
    id = data['id']
    # ele_id = data['ele_num']
    # pre_id = data['pre_num']
    try:

        if 'ele_num' in data:
            # data["basic_id"] = BasicBasicinfo.query.filter(
            #     BasicBasicinfo.ele_num ==data['ele_num']).first().id
            del data['ele_num']
        if 'pre_num' in data:
            # data["basic_id"] = BasicBasicinfo.query.filter(
            #     BasicBasicinfo.pre_num ==data['pre_num']).first().id
            del data['pre_num']

    except Exception as e:
        print("--data-->", data)
        print("--Exception-->", str(e))
    print('--------------------------test--------------------------------')

    # BasicBasicinfo.query.filter_by(ele_id = ele_id,pre_id = pre_id).update(data)
    try:
        ECultivationPolleninfo.query.filter_by(id=id).update(data)
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

@propagation.route('/propagation/sample_collectinfo/add', methods=['POST'])
def add_sample_collectinfo():
    data = request.get_json()
    #去除剂量两端的空格
    # if 'dose' in data:
    #     data['dose'] = data['dose'].strip()
    #     print(data['dose'])

    ctime = datetime.now()
    data['belong'] = 0
    data['f_date'] = ctime



    # 查询对应的 id
    basic_id = BasicBasicinfo.query.filter_by(ele_num=data['ele_num']).first().id

    data['basic_id'] =basic_id
    print(data)

    sample_collect_info= ECultivationPolleninfo()

    for key, value in data.items():
        setattr(sample_collect_info, key, value)
    try:
        db.session.add(sample_collect_info)
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

@propagation.route('/propagation/sample_collectinfo/export', methods=['POST'])
def export_sample_collectinfo():
    try:
        selected_ids = request.get_json()
        disused_dict = {
            1: "是",
            0: "否"
        }
        diluent_type_dict = {
            0: "优",
            1: "合格",
            2: "差"
        }

        if selected_ids:
            sample_collect_info = (
                db.session.query(ECultivationPolleninfo, BasicBasicinfo.ele_num, BasicBasicinfo.pre_num)
                    .outerjoin(BasicBasicinfo, BasicBasicinfo.id == ECultivationPolleninfo.basic_id)
                    .filter(ECultivationPolleninfo.id.in_(selected_ids))
                    .all()
            )
        else:
            sample_collect_info = (
                db.session.query(ECultivationPolleninfo, BasicBasicinfo.ele_num, BasicBasicinfo.pre_num)
                    .outerjoin(BasicBasicinfo, BasicBasicinfo.id == ECultivationPolleninfo.basic_id)
                    .all()
            )

        data_list = []
        for info, ele_num, pre_num in sample_collect_info:
            disused_value = disused_dict.get(info.disused, info.disused)
            diluent_type_value = diluent_type_dict.get(info.diluent_type, info.diluent_type)
            data_list.append({
                '草地编号': ele_num,
                '地块编号': pre_num,
                '采样日期': info.E_date.isoformat() if info.E_date else None,
                '稀释倍数': info.dilution_ratio,
                '样本活力': diluent_type_value,
                '是否废弃': disused_value,
                '创建时间': info.f_date.isoformat() if info.f_date else None,
                '创建人员': info.f_staff
            })
        df = pd.DataFrame(data_list)

        export_path = os.path.join(os.getcwd(), 'App', 'propagation', 'export_excel', 'sample_collect_info.xlsx')
        df.to_excel(export_path, index=False)

        return send_file(export_path, as_attachment=True)
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'导出失败 {str(e)}'})

# 病虫害繁殖周期采样
#获取月龄8以上的健康未销售的公草地记录(在生长记录是12月，在生长监测和培育时8月)、、、、、、、、、、、、、、、、、、改成6月了
@propagation.route('/propagation/sample_collectinfo/get_malegrass', methods=['POST'])
def get_malegrass():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))
    # 当前日期
    current_date = datetime.now().date()

    conditions = []
    search_params = {
        'ele_num': BasicBasicinfo.ele_num,
        'pre_num': BasicBasicinfo.pre_num,
        'purpose': BasicBasicinfo.purpose,
        'variety': BasicBasicinfo.variety,
        'color': BasicBasicinfo.color,
        'sex': BasicBasicinfo.sex,
        'birth': BasicBasicinfo.birth,
        'wea_date': BasicBasicinfo.wea_date,
        'wea_weight': BasicBasicinfo.wea_weight,
        'mon_age': BasicBasicinfo.mon_age,
        'manu_info_name': BasicBasicinfo.manu_info_name,
        'state': BasicBasicinfo.state,
        'house_name': BasicBasicinfo.house_name,
        'hurdle_name': BasicBasicinfo.hurdle_name,
        'gene_a': BasicBasicinfo.gene_a,
        'gene_b': BasicBasicinfo.gene_b,
        'gene_c': BasicBasicinfo.gene_c,
        'f_staff': BasicBasicinfo.f_staff,
        'f_date': BasicBasicinfo.f_date,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'birth' or param == 'f_date' or param == 'wea_date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            elif param == 'ele_num' or param == 'pre_num':
                # 修改为模糊查询
                conditions.append(column.like(f'%{value}%'))
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = BasicBasicinfo.query.filter(and_(
            *conditions,  # 原有的动态条件
            BasicBasicinfo.sex == 0,  # 固定条件：性别为1
            BasicBasicinfo.state == 1, # 固定条件：状态为1
            BasicBasicinfo.mon_age >= 6
        ))
    else:
        query = BasicBasicinfo.query.filter(and_(
            BasicBasicinfo.sex == 0,  # 固定条件：性别为1
            BasicBasicinfo.state == 1 , # 固定条件：状态为1
            BasicBasicinfo.mon_age >= 6
        ))  # 如果没有动态条件，只筛选固定条件

    # 筛选出没有被移除的草(状态-1)和没有枯萎的草(状态0)
    # 并且根据id降序排列

    query = query.filter(and_(BasicBasicinfo.state != -1, BasicBasicinfo.state != 0, BasicBasicinfo.belong == 0))

    # # 获取所有记录（不分页）
    # all_records = query.all()

    basic_infos = query.order_by(desc(BasicBasicinfo.id)).paginate(page=pageNum, per_page=pageSize, error_out=False)
    total = query.count()

    # # 过滤出月龄大于等于12的记录
    # filtered_infos = []
    # for info in basic_infos:
    #     if info.birth:  # 确保出生日期存在
    #         # 计算月龄
    #         print('111111111111111111111')
    #         days_diff = (current_date - info.birth).days
    #         mon_age = round(days_diff / 30, 1)
    #         print(mon_age)
    #         if mon_age >= 12:
    #
    #             info.mon_age = mon_age  # 动态添加月龄属性
    #             filtered_infos.append(info)

    list = []
    # print('___+++++++++++++++++++++++++++')
    # print(filtered_infos)
    for info in basic_infos:
        # list.append({
        #     'id': info.id,
        #     'ele_num': info.ele_num,
        #     'pre_num': info.pre_num,
        #     'purpose': info.purpose,
        #     'variety': info.variety,
        #     'sex': info.sex,
        #     'manu_info_id': info.manu_info_id,
        #     'manu_info_name': info.manu_info_name,
        #     'state': info.state,
        #     'birth': info.birth.isoformat(),
        #     'bir_weight': info.bir_weight,
        #     'wea_weight': info.wea_weight,
        #     'house_id': info.house_id,
        #     'hurdle_id': info.hurdle_id,
        #     'house_name': info.house_name,
        #     'hurdle_name': info.hurdle_name,
        #     'mon_age': info.mon_age,
        #     'color': info.color,
        #     'rank': info.rank,
        #     'father_id': info.father_id,
        #     'mother_id': info.mother_id,
        #     'f_ele_num': info.f_ele_num,
        #     'f_pre_num': info.f_pre_num,
        #     'm_ele_num': info.m_ele_num,
        #     'm_pre_num': info.m_pre_num,
        #     'f_staff': info.f_staff,
        #     'f_date': info.f_date.isoformat(),
        #     'img_positive': info.img_positive,
        #     'img_left': info.img_left,
        #     'img_right': info.img_right,
        #     'note': info.note,
        #     'belong': info.belong,
        #     'gene_a': info.gene_a,
        #     'gene_b': info.gene_b,
        #     'gene_c': info.gene_c,
        #     'score': info.score,
        #     'score_2': info.score_2,
        #     'score_6': info.score_6,
        #     'score_12': info.score_12,
        #     'score_24': info.score_24
        # })
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        list.append(json.loads(data))
    print('-----------------------------')
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

#培育信息
@propagation.route('/propagation/propagationinfo', methods=['POST'])
def get_propagationinfo():
    pageNum = int(request.json.get('pageNum'))
    # pageNum = int(request.form.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        # '': ECultivationCultivationinfo,
        'cultivation_date': ECultivationCultivationinfo.cultivation_date,
        'pre_harvest_date': ECultivationCultivationinfo.pre_harvest_date,
        'cultivation_way': ECultivationCultivationinfo.cultivation_way,
        'mother_id': ECultivationCultivationinfo.mother_id,
        'male_ele_num': ECultivationCultivationinfo.father_id,
        'male_pre_num': ECultivationCultivationinfo.father_id,
        'female_ele_num': ECultivationCultivationinfo.mother_id,
        'female_pre_num': ECultivationCultivationinfo.mother_id,
        'mother_variety': ECultivationCultivationinfo.mother_variety,
        'father_id': ECultivationCultivationinfo.father_id,
        'father_variety': ECultivationCultivationinfo.father_variety,
        'cultivation_state': ECultivationCultivationinfo.cultivation_state,
        'staff': ECultivationCultivationinfo.staff,
        'f_staff': ECultivationSeedinginfo.f_staff,
        'f_date': ECultivationSeedinginfo.f_date,
        'belong': ECultivationSeedinginfo.belong,
        'growth_period': ECultivationCultivationinfo.growth_period,
        'single_success': ECultivationCultivationinfo.single_success,
        # 'ele_num': ECultivationSeedinginfo.basic_id,
        # 'pre_num': ECultivationSeedinginfo.basic_id,
        # 'age': ECultivationSeedinginfo.age,
        # 'breeding': ECultivationSeedinginfo.seeding_status,


    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'f_date' or param == 'cultivation_date' or param == 'pre_harvest_date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            elif param == 'male_ele_num':
                male_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.ele_num.like(f'%{value}%')).first().id
                print(male_id)
                conditions.append(column == male_id)
            elif param == 'female_ele_num':
                female_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.ele_num.like(f'%{value}%')).first().id
                conditions.append(column == female_id)
            elif param == 'male_pre_num':
                male_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.pre_num.like(f'%{value}%')).first().id
                conditions.append(column == male_id)
            elif param == 'female_pre_num':
                female_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.pre_num.like(f'%{value}%')).first().id
                conditions.append(column == female_id)
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = ECultivationCultivationinfo.query.filter(and_(*conditions))
    else:
        query = ECultivationCultivationinfo.query  # 如果没有条件，查询所有

    # 筛选出没有被移除的草(状态-1)和没有枯萎的草(状态0)
    # 并且根据id降序排列

    # 并且根据id降序排列

    query = query.filter(ECultivationCultivationinfo.belong == 0)
    infos = query.order_by(desc(ECultivationCultivationinfo.id)).paginate(page=pageNum, per_page=pageSize,
                                                                  error_out=False)
    total = query.count()

    list = []
    for info in infos:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        data = json.loads(data)
        ewe_info = BasicBasicinfo.query.filter_by(id=data['mother_id']).first()
        if ewe_info:
            data['female_ele_num'] = ewe_info.ele_num
            data['female_pre_num'] = ewe_info.pre_num
        ram_info = BasicBasicinfo.query.filter_by(id=data['father_id']).first()
        if ram_info:
            data['male_ele_num'] = ram_info.ele_num
            data['male_pre_num'] = ram_info.pre_num
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

@propagation.route('/propagation/propagationinfo/del', methods=['POST'])
def del_propagationinfo():
    ids = request.get_json()
    print("______________________________________")
    print(ids)
    for i in ids:
        ECultivationCultivationinfo.query.filter_by(id=i).delete()
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

@propagation.route('/propagation/propagationinfo/edit', methods=['POST'])
def edit_propagationinfo():
    data = request.get_json()
    # print(data)
    print("--data-->", data)
    id = data['id']
    # ele_id = data['ele_num']
    # pre_id = data['pre_num']
    try:
        print(data)
        if 'male_ele_num' in data:
            # data["basic_id"] = BasicBasicinfo.query.filter(
            #     BasicBasicinfo.ele_num ==data['ele_num']).first().id
            del data['male_ele_num']
        if 'male_pre_num' in data:
            # data["basic_id"] = BasicBasicinfo.query.filter(
            #     BasicBasicinfo.pre_num ==data['pre_num']).first().id
            del data['male_pre_num']
        if 'female_ele_num' in data:
            # data["basic_id"] = BasicBasicinfo.query.filter(
            #     BasicBasicinfo.ele_num ==data['ele_num']).first().id
            del data['female_ele_num']
        if 'female_pre_num' in data:
            # data["basic_id"] = BasicBasicinfo.query.filter(
            #     BasicBasicinfo.pre_num ==data['pre_num']).first().id
            del data['female_pre_num']
        # if 'male_id' in data:
        #     del data['male_id']
        # if 'female_id' in data:
        #     del data['male_id']
        # if 'male_id' in data:
        #     del data['male_id']
        # if 'male_id' in data:
        #     del data['male_id']
        print("----------------------------")
        print(data)
    except Exception as e:
        print("--data-->", data)
        print("--Exception-->", str(e))
    print('--------------------------test--------------------------------')

    # BasicBasicinfo.query.filter_by(ele_id = ele_id,pre_id = pre_id).update(data)
    try:
        ECultivationCultivationinfo.query.filter_by(id=id).update(data)
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

@propagation.route('/propagation/propagationinfo/add', methods=['POST'])
def add_propagationinfo():
    data = request.get_json()
    #去除剂量两端的空格
    # if 'dose' in data:
    #     data['dose'] = data['dose'].strip()
    #     print(data['dose'])

    ctime = datetime.now()
    data['belong'] = 0
    data['f_date'] = ctime



    # 查询对应的 id
    female_id = BasicBasicinfo.query.filter_by(ele_num=data['female_ele_num']).first().id

    data['mother_id'] =female_id

    # 查询对应的 id
    male_id = BasicBasicinfo.query.filter_by(ele_num=data['male_ele_num']).first().id

    data['father_id'] =male_id
    print(data)

    propagationinfo= ECultivationCultivationinfo()

    for key, value in data.items():
        setattr(propagationinfo, key, value)
    try:
        db.session.add(propagationinfo)
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


# 判断是否为近亲
@propagation.route('/propagation/propagationinfo/check_self_pollination', methods=['POST'])
def check_self_pollination():
    """
    通过传入的 male_ele_num 和 female_ele_num 查询相关记录，并检查是否有共同祖先。

    参数:
        male_ele_num (str): 供体草地编号
        female_ele_num (str): 受体田块草地编号

    返回:
        flask.Response: JSON 格式的响应，包含检查结果
    """
    # 获取前端传递的数据
    data = request.get_json()
    male_ele_num = data.get("male_ele_num")
    female_ele_num = data.get("female_ele_num")
    try:
        # 查询公草地记录
        male_record = BasicBasicinfo.query.filter_by(ele_num=male_ele_num).first()
        if not male_record:
            return jsonify({"code": 404, "msg": f"未找到对应的公草地记录：{male_ele_num}"})

        # 查询母草地记录
        female_record = BasicBasicinfo.query.filter_by(ele_num=female_ele_num).first()
        if not female_record:
            return jsonify({"code": 404, "msg": f"未找到对应的母草地记录：{female_ele_num}"})

        # 提取公草地的相关祖先信息
        male_ancestors = [
            male_ele_num,
            male_record.f_ele_num,  # 父亲
            male_record.m_ele_num,  # 母亲
            male_record.paternal_grandfather_ele_num,  # 父方祖父
            male_record.paternal_grandmother_ele_num,  # 父方祖母
            male_record.maternal_grandfather_ele_num,  # 父方外祖父
            male_record.maternal_grandmother_ele_num  # 父方外祖母
        ]

        # 提取母草地的相关祖先信息
        female_ancestors = [
            female_ele_num,
            female_record.f_ele_num,  # 父亲
            female_record.m_ele_num,  # 母亲
            female_record.paternal_grandfather_ele_num,  # 母方祖父
            female_record.paternal_grandmother_ele_num,  # 母方祖母
            female_record.maternal_grandfather_ele_num,  # 母方外祖父
            female_record.maternal_grandmother_ele_num  # 母方外祖母
        ]

        # 去除 None、空字符串和无效值 "0000000000000000"
        male_ancestors = [ancestor for ancestor in male_ancestors if ancestor and ancestor != "0000000000000000"]
        female_ancestors = [ancestor for ancestor in female_ancestors if ancestor and ancestor != "0000000000000000"]

        print(f'{male_ancestors}')
        print('-------------------------------')
        print(f'{female_ancestors}')

        # 计算交集
        common_ancestors = set(male_ancestors) & set(female_ancestors)

        # 构造返回结果
        if common_ancestors:
            result = {
                "code": 200,
                "data": {
                    "list": list(common_ancestors),  # 返回交集内容
                    "boolean": True  # 存在共同祖先
                },
                "msg": "注意：两块草地三代以内有共同祖先，不宜培育"
            }
        else:
            result = {
                "code": 200,
                "data": {
                    "list": [],  # 无交集返回空列表
                    "boolean": False  # 无共同祖先
                },
                "msg": "两块草地三代以内无共同祖先,可以培育"
            }

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "code": 500,
            "msg": f"发生异常: {str(e)}"
        })


@propagation.route('/propagation/propagationinfo/export', methods=['POST'])
def export_propagationinfo():
    try:
        selected_ids = request.get_json()
        varietyType = {
            0: "小麦", 1: "玉米", 2: "水稻",
            3: "大豆", 4: "苜蓿", 5: "黑麦草",
            6: "燕麦", 7: "高粱", 8: "谷子",
            9: "油菜", 10: "其他"
        }

        Breeding_wayType = {
            0: "自然传播",
            1: "气流传播",
            2: "接触传播",
            3: "媒介传播"
        }
        ewe_info = aliased(BasicBasicinfo)
        ram_info = aliased(BasicBasicinfo)

        if selected_ids:
            propagation_info = (
                db.session.query(
                    ECultivationCultivationinfo,
                    ewe_info.ele_num.label("female_ele_num"),
                    ewe_info.pre_num.label("female_pre_num"),
                    ram_info.ele_num.label("male_ele_num"),
                    ram_info.pre_num.label("male_pre_num")
                )
                    .outerjoin(ewe_info, ewe_info.id == ECultivationCultivationinfo.mother_id)
                    .outerjoin(ram_info, ram_info.id == ECultivationCultivationinfo.father_id)
                    .filter(ECultivationCultivationinfo.id.in_(selected_ids))
                    .all()
            )
        else:
            propagation_info = (
                db.session.query(
                    ECultivationCultivationinfo,
                    ewe_info.ele_num.label("female_ele_num"),
                    ewe_info.pre_num.label("female_pre_num"),
                    ram_info.ele_num.label("male_ele_num"),
                    ram_info.pre_num.label("male_pre_num")
                )
                    .outerjoin(ewe_info, ewe_info.id == ECultivationCultivationinfo.mother_id)
                    .outerjoin(ram_info, ram_info.id == ECultivationCultivationinfo.father_id)
                    .all()
            )

        data_list = []
        for info, female_ele_num, female_pre_num, male_ele_num, male_pre_num in propagation_info:
            Breeding_wayType_value = Breeding_wayType.get(info.cultivation_way, info.cultivation_way)
            ewe_varietyType_value = varietyType.get(info.mother_variety, info.mother_variety)
            ram_varietyType_value = varietyType.get(info.father_variety, info.father_variety)
            data_list.append({
                '受体草地编号': female_ele_num,
                '受体地块编号': female_pre_num,
                '受体草地类型': ewe_varietyType_value,
                '供体草地编号': male_ele_num,
                '供体地块编号': male_pre_num,
                '供体草地类型': ram_varietyType_value,
                '传播日期': info.cultivation_date.isoformat() if info.cultivation_date else None,
                '预产日期': info.pre_harvest_date.isoformat() if info.pre_harvest_date else None,
                '传播方式': Breeding_wayType_value,
                '培育状态': info.cultivation_state,
                '培育情期（天）': info.growth_period,
                '单次培育成功率（%）': info.single_success,
                '操作师': info.staff,
                '创建时间': info.f_date.isoformat() if info.f_date else None,
                '创建人员': info.f_staff
            })
        df = pd.DataFrame(data_list)

        export_path = os.path.join(os.getcwd(), 'App', 'propagation', 'export_excel', 'propagationinfo.xlsx')
        df.to_excel(export_path, index=False)

        return send_file(export_path, as_attachment=True)
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'导出失败 {str(e)}'})
#生长记录信息一条龙
@propagation.route('/propagation/post_harvestinfo', methods=['POST'])
def get_post_harvestinfo():
    pageNum = int(request.json.get('pageNum'))
    # pageNum = int(request.form.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        # 'ele_num': ECultivationSeedinginfo.basic_id,
        # 'pre_num': ECultivationSeedinginfo.basic_id,
        'cultivation_date': ECultivationMaturationinfo.cultivation_date,
        'delivery_date': ECultivationMaturationinfo.delivery_date,
        'father_id': ECultivationMaturationinfo.father_id,
        'mother_id': ECultivationMaturationinfo.mother_id,
        'male_ele_num': ECultivationMaturationinfo.father_id,
        'male_pre_num': ECultivationMaturationinfo.father_id,
        'female_ele_num': ECultivationMaturationinfo.mother_id,
        'female_pre_num': ECultivationMaturationinfo.mother_id,
        'Booroola': ECultivationMaturationinfo.Booroola,
        'mother_health': ECultivationMaturationinfo.mother_health,
        'mother_condition': ECultivationMaturationinfo.mother_condition,
        'sprout_ele_num': ECultivationMaturationinfo.sprout_ele_num,
        'sprout_state': ECultivationMaturationinfo.sprout_state,
        'sprout_weight': ECultivationMaturationinfo.sprout_weight,
        'live_seedling_num': ECultivationMaturationinfo.live_seedling_num,
        'planting_attendants': ECultivationMaturationinfo.planting_attendants,
        'notes': ECultivationMaturationinfo.notes,
        'belong': ECultivationSeedinginfo.belong,
        'f_staff': ECultivationSeedinginfo.f_staff,
        'f_date': ECultivationSeedinginfo.f_date,
    }
    for param, column in search_params.items():
        print(param)
        print(column)
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'f_date' or param == 'cultivation_date' or param == 'delivery_date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            elif param == 'father_id':
                id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.id.like(f'%{value}%')).first().id
                conditions.append(column == id)
            elif param == 'mother_id':
                id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.id.like(f'%{value}%')).first().id
                conditions.append(column == id)
            elif param == 'male_ele_num':
                male_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.ele_num.like(f'%{value}%')).first().id
                print(male_id)
                conditions.append(column == male_id)
            elif param == 'female_ele_num':
                female_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.ele_num.like(f'%{value}%')).first().id
                conditions.append(column == female_id)
            elif param == 'male_pre_num':
                male_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.pre_num.like(f'%{value}%')).first().id
                conditions.append(column == male_id)
            elif param == 'female_pre_num':
                female_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.pre_num.like(f'%{value}%')).first().id
                conditions.append(column == female_id)
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = ECultivationMaturationinfo.query.filter(and_(*conditions))
        print(query)
    else:
        query = ECultivationMaturationinfo.query  # 如果没有条件，查询所有

    # 筛选出没有被移除的草(状态-1)和没有枯萎的草(状态0)
    # 并且根据id降序排列

    # 并且根据id降序排列

    query = query.filter(ECultivationMaturationinfo.belong == 0)
    infos = query.order_by(desc(ECultivationMaturationinfo.id)).paginate(page=pageNum, per_page=pageSize,
                                                                  error_out=False)
    total = query.count()

    list = []
    for info in infos:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        data = json.loads(data)
        ram_info = BasicBasicinfo.query.filter_by(id=data['father_id']).first()
        ewe_info = BasicBasicinfo.query.filter_by(id=data['mother_id']).first()
        if ram_info:
            data['male_ele_num'] = ram_info.ele_num
            data['male_pre_num'] = ram_info.pre_num

        if ewe_info:
            data['female_ele_num'] = ewe_info.ele_num
            data['female_pre_num'] = ewe_info.pre_num
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

@propagation.route('/propagation/post_harvestinfo/del', methods=['POST'])
def del_post_harvestinfo():
    ids = request.get_json()
    print("______________________________________")
    print(ids)
    for i in ids:
        ECultivationMaturationinfo.query.filter_by(id=i).delete()
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

@propagation.route('/propagation/post_harvestinfo/edit', methods=['POST'])
def edit_post_harvestinfo():
    data = request.get_json()
    print("--data-->", data)
    id = data['id']
    # ele_id = data['ele_num']
    # pre_id = data['pre_num']

    # 删除list键
    keys_to_remove = []
    for key in data.keys():
        if "list" in key:
            keys_to_remove.append(key)
    print('-----------------------------11')
    print(keys_to_remove)

    for key in keys_to_remove:
        del data[key]
    try:
        if 'female_ele_num' in data:
            del data['female_ele_num']
        if 'female_pre_num' in data:
            del data['female_pre_num']
        if 'male_ele_num' in data:
            del data['male_ele_num']
        if 'male_pre_num' in data:
            del data['male_pre_num']

        print(data)
    except Exception as e:
        print("--data-->", data)
        print("--Exception-->", str(e))
    print('--------------------------test--------------------------------')

    mother_id = data['mother_id']
    # pageNum = int(request.form.get('pageNum'))
    father_id = data['father_id']

    birth = data['delivery_date']

    # 构造查询条件
    conditions = []
    conditions.append(ECultivationSproutinfo.tobasic != 1)
    if mother_id:
        conditions.append(ECultivationSproutinfo.mother_id == mother_id)
    if father_id:
        conditions.append(ECultivationSproutinfo.father_id == father_id)
    if birth:
        conditions.append(ECultivationSproutinfo.sprout_date == birth)

    # 查询数据库，获取符合条件的记录
    deleted_seedlings = ECultivationSproutinfo.query.filter(and_(*conditions)).delete()

    print(f'删除了{deleted_seedlings}条记录')

    # 插入新的草籽数据
    seedling_data = []
    delivery_date = datetime.strptime(data['delivery_date'], '%Y-%m-%d')
    delivery_date_str = delivery_date.strftime('%Y%m%d')
    ewe = db.session.query(BasicBasicinfo).filter_by(id=mother_id).first()
    ram = db.session.query(BasicBasicinfo).filter_by(id=father_id).first()

    # 获取父母耳号及品种信息
    m_pre_num = ewe.pre_num if ewe else None
    m_ele_num = ewe.ele_num if ewe else None
    variety = ewe.variety if ewe else None

    f_pre_num = ram.pre_num if ram else None
    f_ele_num = ram.ele_num if ram else None

    for i in range(1, int(data['live_seedling_num']) + 1):
        logo = f"{m_ele_num}_{delivery_date_str}_{i}"
        lamb = {
            'cultivation_id': data['cultivation_id'],
            'tobasic': 0,
            'logo': logo,
            'pre_num': data.get(f'pre_num_{i}'),
            'variety': variety,
            'sex': data.get(f'sex_{i}'),
            'belong': 0,
            'manu_info_id': 0,
            'manu_info_name': '本场扩繁',
            'state': data.get(f'state_{i}'),
            'sprout_date': delivery_date,
            'sprout_weight': data.get(f'bir_weight_{i}'),
'mother_id': mother_id,
             'father_id': father_id,
            'f_ele_num': f_ele_num,
            'f_pre_num': f_pre_num,
            'm_ele_num': m_ele_num,
            'm_pre_num': m_pre_num,
            'color': data.get(f'color_{i}'),
            'rank': data.get(f'rank_{i}'),
            'f_staff': data.get('f_staff'),
            'f_date': data.get('f_date'),
        }
        seedling_data.append(lamb)

    if seedling_data:
        try:
            for lamb in seedling_data:
                seedlinginfo = ECultivationSproutinfo()
                for key, value in lamb.items():
                    setattr(seedlinginfo, key, value)
                db.session.add(seedlinginfo)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            result = {
                "code": 500,
                "msg": f'添加草籽信息失败 {str(e)}'
            }
            return jsonify(result)

    # 删除多余的数据
    live_seedling_num = int(data['live_seedling_num'])
    for i in range(1, live_seedling_num + 1):
        for key in [f'pre_num_{i}', f'sex_{i}', f'state_{i}', f'bir_weight_{i}', f'color_{i}', f'rank_{i}']:
            data.pop(key, None)

    print(data)
    # 更新主表数据
    try:
        ECultivationMaturationinfo.query.filter_by(id=id).update(data)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
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

    # try:
    #     ECultivationMaturationinfo.query.filter_by(id=id).update(data)
    #     db.session.commit()
    # except Exception as e:
    #     db.session.rollback()
    #     db.session.flush()
    #     result = {
    #         "code": 500,
    #         "msg": f'修改失败 {str(e)}'
    #     }
    #     return jsonify(result)
    # result = {
    #     "code": 200,
    #     "msg": '修改成功'
    # }
    # return jsonify(result)


@propagation.route('/propagation/post_harvestinfo/export', methods=['POST'])
def export_post_harvestinfo():
    try:
        selected_ids = request.get_json()
        Ewe_healthType = {
            1: "正常",
            0: "不正常"
        }
        Ewe_conditionType = {
            0: "好",
            1: "一般",
            2: "差"
        }
        ewe_info = aliased(BasicBasicinfo)
        ram_info = aliased(BasicBasicinfo)

        if selected_ids:
            post_harvest_info = (
                db.session.query(
                    ECultivationMaturationinfo,
                    ewe_info.ele_num.label("female_ele_num"),
                    ewe_info.pre_num.label("female_pre_num"),
                    ram_info.ele_num.label("male_ele_num"),
                    ram_info.pre_num.label("male_pre_num")
                )
                    .outerjoin(ECultivationCultivationinfo, ECultivationCultivationinfo.id == ECultivationMaturationinfo.cultivation_id)
                    .outerjoin(ewe_info, ewe_info.id == ECultivationCultivationinfo.mother_id)
                    .outerjoin(ram_info, ram_info.id == ECultivationCultivationinfo.father_id)
                    .filter(ECultivationMaturationinfo.id.in_(selected_ids))
                    .all()
            )
        else:
            post_harvest_info = (
                db.session.query(
                    ECultivationMaturationinfo,
                    ewe_info.ele_num.label("female_ele_num"),
                    ewe_info.pre_num.label("female_pre_num"),
                    ram_info.ele_num.label("male_ele_num"),
                    ram_info.pre_num.label("male_pre_num")
                )
                    .outerjoin(ECultivationCultivationinfo, ECultivationCultivationinfo.id == ECultivationMaturationinfo.cultivation_id)
                    .outerjoin(ewe_info, ewe_info.id == ECultivationCultivationinfo.mother_id)
                    .outerjoin(ram_info, ram_info.id == ECultivationCultivationinfo.father_id)
                    .all()
            )

        data_list = []
        for info, female_ele_num, female_pre_num, male_ele_num, male_pre_num in post_harvest_info:
            Ewe_healthType_value = Ewe_healthType.get(info.mother_health, info.mother_health)
            Ewe_conditionType_value = Ewe_conditionType.get(info.mother_condition, info.mother_condition)
            data_list.append({
                '受体草地编号': female_ele_num,
                '受体地块编号': female_pre_num,
                '供体草地编号': male_ele_num,
                '供体地块编号': male_pre_num,
                '传播日期': info.cultivation_date.isoformat() if info.cultivation_date else None,
                '发病日期': info.delivery_date.isoformat() if info.delivery_date else None,
                '受体感染率': info.Booroola,
                '受体健康情况': Ewe_healthType_value,
                '受体状态': Ewe_conditionType_value,
                '感染数量': info.live_seedling_num,
                '记录人员': info.planting_attendants,
                '创建时间': info.f_date.isoformat() if info.f_date else None,
                '创建人员': info.f_staff
            })
        df = pd.DataFrame(data_list)

        export_path = os.path.join(os.getcwd(), 'App', 'propagation', 'export_excel', 'post_harvest_info.xlsx')
        df.to_excel(export_path, index=False)

        return send_file(export_path, as_attachment=True)
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'导出失败 {str(e)}'})

#获取月龄12以上的健康未销售的基础草地记录(在生长记录是12月，在生长监测和培育时8月)，，，，，，，，，改成6月和11月了
@propagation.route('/propagation/post_harvestinfo/get_ewe', methods=['POST'])
def get_ewe():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))
    # 当前日期
    current_date = datetime.now().date()

    conditions = []
    search_params = {
        'ele_num': BasicBasicinfo.ele_num,
        'pre_num': BasicBasicinfo.pre_num,
        'purpose': BasicBasicinfo.purpose,
        'variety': BasicBasicinfo.variety,
        'color': BasicBasicinfo.color,
        'sex': BasicBasicinfo.sex,
        'birth': BasicBasicinfo.birth,
        'wea_date': BasicBasicinfo.wea_date,
        'wea_weight': BasicBasicinfo.wea_weight,
        'mon_age': BasicBasicinfo.mon_age,
        'manu_info_name': BasicBasicinfo.manu_info_name,
        'state': BasicBasicinfo.state,
        'house_name': BasicBasicinfo.house_name,
        'hurdle_name': BasicBasicinfo.hurdle_name,
        'gene_a': BasicBasicinfo.gene_a,
        'gene_b': BasicBasicinfo.gene_b,
        'gene_c': BasicBasicinfo.gene_c,
        'f_staff': BasicBasicinfo.f_staff,
        'f_date': BasicBasicinfo.f_date,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'birth' or param == 'f_date' or param == 'wea_date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            elif param == 'ele_num' or param == 'pre_num':
                # 修改为模糊查询
                conditions.append(column.like(f'%{value}%'))
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = BasicBasicinfo.query.filter(and_(
            *conditions,  # 原有的动态条件
            BasicBasicinfo.sex == 1,  # 固定条件：性别为1
            BasicBasicinfo.state == 1, # 固定条件：状态为1
            BasicBasicinfo.mon_age >= 11
        ))
    else:
        query = BasicBasicinfo.query.filter(and_(
            BasicBasicinfo.sex == 1,  # 固定条件：性别为1
            BasicBasicinfo.state == 1 , # 固定条件：状态为1
            BasicBasicinfo.mon_age >= 11
        ))  # 如果没有动态条件，只筛选固定条件

    # 筛选出没有被移除的草(状态-1)和没有枯萎的草(状态0)
    # 并且根据id降序排列

    query = query.filter(and_(BasicBasicinfo.state != -1, BasicBasicinfo.state != 0, BasicBasicinfo.belong == 0))

    # # 获取所有记录（不分页）
    # all_records = query.all()

    basic_infos = query.order_by(desc(BasicBasicinfo.id)).paginate(page=pageNum, per_page=pageSize, error_out=False)
    total = query.count()

    # # 过滤出月龄大于等于12的记录
    # filtered_infos = []
    # for info in basic_infos:
    #     if info.birth:  # 确保出生日期存在
    #         # 计算月龄
    #         print('111111111111111111111')
    #         days_diff = (current_date - info.birth).days
    #         mon_age = round(days_diff / 30, 1)
    #         print(mon_age)
    #         if mon_age >= 12:
    #
    #             info.mon_age = mon_age  # 动态添加月龄属性
    #             filtered_infos.append(info)

    list = []
    # print('___+++++++++++++++++++++++++++')
    # print(filtered_infos)
    for info in basic_infos:
        # list.append({
        #     'id': info.id,
        #     'ele_num': info.ele_num,
        #     'pre_num': info.pre_num,
        #     'purpose': info.purpose,
        #     'variety': info.variety,
        #     'sex': info.sex,
        #     'manu_info_id': info.manu_info_id,
        #     'manu_info_name': info.manu_info_name,
        #     'state': info.state,
        #     'birth': info.birth.isoformat(),
        #     'bir_weight': info.bir_weight,
        #     'wea_weight': info.wea_weight,
        #     'house_id': info.house_id,
        #     'hurdle_id': info.hurdle_id,
        #     'house_name': info.house_name,
        #     'hurdle_name': info.hurdle_name,
        #     'mon_age': info.mon_age,
        #     'color': info.color,
        #     'rank': info.rank,
        #     'father_id': info.father_id,
        #     'mother_id': info.mother_id,
        #     'f_ele_num': info.f_ele_num,
        #     'f_pre_num': info.f_pre_num,
        #     'm_ele_num': info.m_ele_num,
        #     'm_pre_num': info.m_pre_num,
        #     'f_staff': info.f_staff,
        #     'f_date': info.f_date.isoformat(),
        #     'img_positive': info.img_positive,
        #     'img_left': info.img_left,
        #     'img_right': info.img_right,
        #     'note': info.note,
        #     'belong': info.belong,
        #     'gene_a': info.gene_a,
        #     'gene_b': info.gene_b,
        #     'gene_c': info.gene_c,
        #     'score': info.score,
        #     'score_2': info.score_2,
        #     'score_6': info.score_6,
        #     'score_12': info.score_12,
        #     'score_24': info.score_24
        # })
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        list.append(json.loads(data))
    print('-----------------------------')
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

#获取月龄12以上的健康未销售的公草地记录(在生长记录是12月，在生长监测和培育时8月)，，，，改成6月和11月了
@propagation.route('/propagation/post_harvestinfo/get_ram', methods=['POST'])
def get_ram():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))
    # 当前日期
    current_date = datetime.now().date()

    conditions = []
    search_params = {
        'ele_num': BasicBasicinfo.ele_num,
        'pre_num': BasicBasicinfo.pre_num,
        'purpose': BasicBasicinfo.purpose,
        'variety': BasicBasicinfo.variety,
        'color': BasicBasicinfo.color,
        'sex': BasicBasicinfo.sex,
        'birth': BasicBasicinfo.birth,
        'wea_date': BasicBasicinfo.wea_date,
        'wea_weight': BasicBasicinfo.wea_weight,
        'mon_age': BasicBasicinfo.mon_age,
        'manu_info_name': BasicBasicinfo.manu_info_name,
        'state': BasicBasicinfo.state,
        'house_name': BasicBasicinfo.house_name,
        'hurdle_name': BasicBasicinfo.hurdle_name,
        'gene_a': BasicBasicinfo.gene_a,
        'gene_b': BasicBasicinfo.gene_b,
        'gene_c': BasicBasicinfo.gene_c,
        'f_staff': BasicBasicinfo.f_staff,
        'f_date': BasicBasicinfo.f_date,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'birth' or param == 'f_date' or param == 'wea_date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            elif param == 'ele_num' or param == 'pre_num':
                # 修改为模糊查询
                conditions.append(column.like(f'%{value}%'))
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = BasicBasicinfo.query.filter(and_(
            *conditions,  # 原有的动态条件
            BasicBasicinfo.sex == 0,  # 固定条件：性别为1
            BasicBasicinfo.state == 1, # 固定条件：状态为1
            BasicBasicinfo.mon_age >= 11#12个月查找不到有的草，不能过于理想化
        ))
    else:
        query = BasicBasicinfo.query.filter(and_(
            BasicBasicinfo.sex == 0,  # 固定条件：性别为1
            BasicBasicinfo.state == 1 , # 固定条件：状态为1
            BasicBasicinfo.mon_age >= 12
        ))  # 如果没有动态条件，只筛选固定条件

    # 筛选出没有被移除的草(状态-1)和没有枯萎的草(状态0)
    # 并且根据id降序排列

    query = query.filter(and_(BasicBasicinfo.state != -1, BasicBasicinfo.state != 0, BasicBasicinfo.belong == 0))

    # # 获取所有记录（不分页）
    # all_records = query.all()

    basic_infos = query.order_by(desc(BasicBasicinfo.id)).paginate(page=pageNum, per_page=pageSize, error_out=False)
    total = query.count()

    # # 过滤出月龄大于等于12的记录
    # filtered_infos = []
    # for info in basic_infos:
    #     if info.birth:  # 确保出生日期存在
    #         # 计算月龄
    #         print('111111111111111111111')
    #         days_diff = (current_date - info.birth).days
    #         mon_age = round(days_diff / 30, 1)
    #         print(mon_age)
    #         if mon_age >= 12:
    #
    #             info.mon_age = mon_age  # 动态添加月龄属性
    #             filtered_infos.append(info)

    list = []
    # print('___+++++++++++++++++++++++++++')
    # print(filtered_infos)
    for info in basic_infos:
        # list.append({
        #     'id': info.id,
        #     'ele_num': info.ele_num,
        #     'pre_num': info.pre_num,
        #     'purpose': info.purpose,
        #     'variety': info.variety,
        #     'sex': info.sex,
        #     'manu_info_id': info.manu_info_id,
        #     'manu_info_name': info.manu_info_name,
        #     'state': info.state,
        #     'birth': info.birth.isoformat(),
        #     'bir_weight': info.bir_weight,
        #     'wea_weight': info.wea_weight,
        #     'house_id': info.house_id,
        #     'hurdle_id': info.hurdle_id,
        #     'house_name': info.house_name,
        #     'hurdle_name': info.hurdle_name,
        #     'mon_age': info.mon_age,
        #     'color': info.color,
        #     'rank': info.rank,
        #     'father_id': info.father_id,
        #     'mother_id': info.mother_id,
        #     'f_ele_num': info.f_ele_num,
        #     'f_pre_num': info.f_pre_num,
        #     'm_ele_num': info.m_ele_num,
        #     'm_pre_num': info.m_pre_num,
        #     'f_staff': info.f_staff,
        #     'f_date': info.f_date.isoformat(),
        #     'img_positive': info.img_positive,
        #     'img_left': info.img_left,
        #     'img_right': info.img_right,
        #     'note': info.note,
        #     'belong': info.belong,
        #     'gene_a': info.gene_a,
        #     'gene_b': info.gene_b,
        #     'gene_c': info.gene_c,
        #     'score': info.score,
        #     'score_2': info.score_2,
        #     'score_6': info.score_6,
        #     'score_12': info.score_12,
        #     'score_24': info.score_24
        # })
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        list.append(json.loads(data))
    print('-----------------------------')
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


@propagation.route('/propagation/post_harvestinfo/getseedling', methods=['POST'])#回显生长记录中新草地
def get_seedling():
    mother_id = request.json.get('mother_id')
    # pageNum = int(request.form.get('pageNum'))
    father_id = request.json.get('father_id')

    birth = request.json.get('delivery_date')

    # 构造查询条件
    conditions = []
    if mother_id:
        conditions.append(ECultivationSproutinfo.mother_id == mother_id)
    if father_id:
        conditions.append(ECultivationSproutinfo.father_id == father_id)
    if birth:
        conditions.append(ECultivationSproutinfo.sprout_date == birth)

    # 查询数据库，获取符合条件的记录
    infos = ECultivationSproutinfo.query.filter(and_(*conditions)).all()

    # 将查询结果转换为字典格式，并添加到列表
    list = []
    for info in infos:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        data = json.loads(data)
        list.append(data)

    # 返回查询结果
    list = move_state_one_to_end(list)#将死羔信息回显到list的最后一个
    result = {
        "code": 200,
        "data": {
            "list": list,
        },
        "msg": '成功'
    }
    return jsonify(result)


# 查询母草地信息记录是否已经在培育信息表中有记录（选择完分娩日期后进入）。。。。。。。。改成查7个月之内得了
@propagation.route('/propagation/post_harvestinfo/search_ewe_grass', methods=['POST'])
def search_ewe_grass():
    parms = request.get_json()
    d_date = parms['deliveryDate']  # 获取前端传递过来的字典数据
    ele_num = parms['eweEleNum']
    print("----------------------------")
    print(d_date)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(ele_num)
    print(parms)

    # 查询 BasicBasicinfo 表，找到与 ele_num 对应的 id
    basic_info = BasicBasicinfo.query.filter_by(ele_num=ele_num).first()

    if not basic_info:
        return jsonify({"code": 400, "msg": "未找到对应的草地编号信息"})

    # 获取对应的 female_id
    female_id = basic_info.id

    # 将分娩日期 d_date 转换为 datetime 对象
    delivery_date = datetime.strptime(d_date, "%Y-%m-%d")

    # 将分娩日期往前推六个月
    pre_date = delivery_date - timedelta(days=7 * 30)  # 近似六个月，30天为一个月，后面改成七个月了

    # 查询 ECultivationCultivationinfo 表，查找对应 female_id 并且 propagation_date 大于等于 pre_date（分娩往前推六个月，一株作物从培育到收获大约150天） 的记录
    propagation_info = ECultivationCultivationinfo.query.filter(
        ECultivationCultivationinfo.mother_id == female_id,
        ECultivationCultivationinfo.cultivation_date >= pre_date
    ).order_by(ECultivationCultivationinfo.cultivation_date.desc()).first()  # 排序后取最近的一条记录

    # 新增的条件查询，在ECultivationMaturationinfo里面，在pre_date日期之后没有female_id的记录
    # 保证一条生长记录对应一条培育记录
    postnatal_check = ECultivationMaturationinfo.query.filter(
        ECultivationMaturationinfo.mother_id == female_id,
        ECultivationMaturationinfo.f_date >= pre_date
    ).first()
    if postnatal_check:
        return jsonify({"code": 400, "msg": "在对应培育记录之后已有生长记录，请勿重复添加生长信息"})

    if propagation_info:
        # 找到与 female_id 相关的 male_id
        male_id = propagation_info.father_id

        # 获取 male_id 对应的 ele_num（male_id 是 BasicBasicinfo 表中的 id）
        ram_info = BasicBasicinfo.query.filter_by(id=male_id).first()

        if ram_info:
            male_ele_num = ram_info.ele_num
        else:
            male_ele_num = None
        print(male_ele_num)
        # 如果有符合条件的记录，返回成功的响应
        result = {
            "code": 200,
            "msg": '成功',
            "data": {
                "male_ele_num": male_ele_num   # 返回供体（公草地）的 ele_num
            },
            # 如果需要分页或其他数据，可以在这里添加
        }
    else:
        # 如果没有符合条件的记录，返回错误信息
        result = {
            "code": 200,
            "msg": '培育信息表中无此草地记录，请添加培育信息'
        }

    return jsonify(result)
    # result = {
    #     "code": 200,
    #     # "data": {
    #     #     "list": list,
    #     #     "pageNum": pageNum,
    #     #     "pageSize": pageSize,
    #     #     "total": total
    #     # },
    #     "msg": '成功'
    # }
    # return jsonify(result)

# 添加传播记录：将供体和受体信息写入传播记录表（由发病日期往前推150天推算传播日期）
@propagation.route('/propagation/post_harvestinfo/add_propagation', methods=['POST'])
def add_propagation():
    data = request.get_json()
    variety_type = [
        {"label": "湖草", "value": 0},
        {"label": "小尾寒草", "value": 1},
        {"label": "无角道赛特", "value": 2},
        {"label": "道寒杂交F1", "value": 3},
        {"label": "白杜泊", "value": 4},
        {"label": "白萨福克", "value": 5},
        {"label": "杜湖杂交", "value": 6},
        {"label": "萨湖杂交", "value": 7},
        {"label": "杜寒杂交", "value": 8},
        {"label": "萨寒杂交", "value": 9},
        {"label": "道湖", "value": 10}
    ]
    # 获取前端传递的数据
    male_ele_num = data.get('male_ele_num')
    male_pre_num = data.get('male_pre_num')
    # variety = data.get('variety')
    variety_label = data.get('variety')  # 前端传递的文字品种
    delivery_date = data.get('delivery_date')
    female_ele_num = data.get('female_ele_num')

    # 将品种文字转换为对应的数字
    variety = next((item['value'] for item in variety_type if item['label'] == variety_label), None)

    # 校验数据
    if not all([male_ele_num, male_pre_num, variety_label, delivery_date, female_ele_num]):
        result = {
            "code": 400,
            "msg": "输入参数缺失"}
        return jsonify(result)


    # 查找供体和受体田块信息
    ram_info = BasicBasicinfo.query.filter_by(ele_num=male_ele_num).first()
    ewe_info = BasicBasicinfo.query.filter_by(ele_num=female_ele_num).first()

    if not ram_info or not ewe_info:
        result = {
            "code": 400,
            "msg": "未找到对应的供体或受体田块信息"}
        return jsonify(result)

    # 计算所需字段
    male_id = ram_info.id
    female_id = ewe_info.id
    ewe_variety = ewe_info.variety
    ram_variety = variety
    pre_production_date = delivery_date
    propagation_date = (datetime.strptime(delivery_date, "%Y-%m-%d") - timedelta(days=150)).strftime("%Y-%m-%d")#往前推180改成150
    f_date = delivery_date

    # 创建培育信息对象
    breeding_data = {
        "cultivation_date": propagation_date,
        "pre_harvest_date": pre_production_date,
        "cultivation_way": 0,  # 默认值
        "father_id": male_id,
        "father_variety": ram_variety,
        "mother_id": female_id,
        "mother_variety": ewe_variety,
        "cultivation_state": 1,  # 默认值
        "staff": None,
        "f_staff": None,
        "f_date": f_date,
        "belong": 0,  # 默认值
        "growth_period": 12,
        "single_success": None
    }

    # 创建新的培育记录
    propagationinfo = ECultivationCultivationinfo()

    # 将数据填充到培育记录
    for key, value in breeding_data.items():
        setattr(propagationinfo, key, value)

    # 保存到数据库
    try:
        db.session.add(propagationinfo)
        db.session.commit()
        result = {
            "code": 200,
            "msg": "添加成功"
        }
        return jsonify(result)
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        result = {
            "code": 500,
            "msg": f"添加失败 {str(e)}"
        }
        return jsonify(result)


#添加生长记录（同时添加一条监测信息记录），，，，改成分娩日期往前推150天了
@propagation.route('/propagation/post_harvestinfo/add', methods=['POST'])
def add_post_harvestinfo():
    data = request.get_json()
    print("+++++++++++")
    print(data)
    ctime = datetime.now()
    data['belong'] = 0
    data['f_date'] = ctime



    # 根据 female_ele_num 和 male_ele_num 查找对应的 BasicBasicinfo 表中的 id
    female_ele_num = data.get('female_ele_num')
    male_ele_num = data.get('male_ele_num')

    # 在填写生长记录时添加一条监测记录
    pre_data = {}
    live_seedling_num = data.get('live_seedling_num')  # 要添加到备注信息里面的胎数
    pre_data['check_type'] = 'B超'
    pre_data['flowering_status'] = '怀孕'
    pre_data['f_staff'] = data.get('f_staff')
    pre_data['notes'] = f'共有{live_seedling_num}胎'
    pre_data['belong'] = 0

    growth_cycle_info = ECultivationFloweringinfo()

    ewe = db.session.query(BasicBasicinfo).filter_by(ele_num=female_ele_num).first()
    if ewe:
        data['mother_id'] = ewe.id  # 将 female_id 设置为查找到的 id
    else:
        return jsonify({"code": 404, "msg": "未找到对应的 female_ele_num"}), 404

    # 查找 male_ele_num 对应的 id
    ram = db.session.query(BasicBasicinfo).filter_by(ele_num=male_ele_num).first()
    if ram:
        data['father_id'] = ram.id  # 将 male_id 设置为查找到的 id
    else:
        return jsonify({"code": 404, "msg": "未找到对应的 male_ele_num"}), 404

    # 删除 female_ele_num 和 male_ele_num 不需要存入数据库
    data.pop('female_ele_num', None)
    data.pop('male_ele_num', None)

    # 假设 delivery_date 是从前端传来的字符串，比如 '2024-12-01'
    delivery_date_str = data.get('delivery_date')  # 取前端传过来的分娩日期
    delivery_date = datetime.strptime(delivery_date_str, '%Y-%m-%d')  # 转换为 datetime 对象


    # 将交配日期往前推六个月
    pre_date = delivery_date - timedelta(days=7 * 30)  # 近似六个月，30天为一个月，改成五个月
    propagation_info = db.session.query(ECultivationCultivationinfo).filter(
        ECultivationCultivationinfo.mother_id == data['mother_id'],  # 查找符合 female_id 的记录
        ECultivationCultivationinfo.cultivation_date >= pre_date  # 查找 propagation_date 大于等于 pre_date（这个日期是分娩日期往前推六个月的日期） 的记录
    ).order_by(ECultivationCultivationinfo.cultivation_date.desc()).first()  # 按照 propagation_date 降序排序，取最新的一条记录

    # 判断是否找到了符合条件的记录
    if propagation_info:
        # 找到对应的培育记录后返回 id
        data['cultivation_id'] = propagation_info.id
        # 在生长记录里面添加培育信息id的同时在监测记录里面也添加
        pre_data['cultivation_id'] = propagation_info.id
        # 获取propagation_info中的propagation_date
        propagation_date = propagation_info.cultivation_date
        # 使用timedelta来表示时间间隔，这里是两个星期，也就是14天
        two_weeks_later = propagation_date + timedelta(days=14)
        # 将计算后的日期赋值给pre_data['f_date']
        pre_data['f_date'] = two_weeks_later  # 至此，孕检信息的字段全部获取完成

    else:
        return jsonify({"code": 404, "msg": "未找到符合条件的培育记录"}), 404


    # 其实下面这些propagation_date好像都不用写，直接拿就行，因为在上面添加培育信息步骤里已经弄了，但是我忘了这块是不是这么写的逻辑了，所以不删了
    # 使用 timedelta 将日期往前推180天（假设6个月为180天）。。。。。。。。。。。。。。。。。。。。改成推150天
    propagation_date = delivery_date - timedelta(days=150)

    # 将 propagation_date 转回字符串格式，如果需要的话
    propagation_date_str = propagation_date.strftime('%Y-%m-%d')

    # 将计算出来的 propagation_date 填入数据字典
    data['cultivation_date'] = propagation_date_str

    # 插入数据到 ECultivationMaturationinfo 表
    post_harvestinfo = ECultivationMaturationinfo()

    #  插入数据到ECultivationFloweringinfo中
    growth_cycle_info = ECultivationFloweringinfo()

    for key, value in data.items():
        setattr(post_harvestinfo, key, value)

    for key, value in pre_data.items():
        setattr(growth_cycle_info, key, value)

    try:
        db.session.add(growth_cycle_info)
        db.session.add(post_harvestinfo)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        result = {
            "code": 500,
            "msg": f'添加母系草地信息失败 {str(e)}'
        }
        return jsonify(result)

    # 提取草籽数据，包含耳号、状态、性别、颜色、出生重、等级
    seedling_data = []
    for i in range(1, int(data['live_seedling_num']) + 1):  # 根据 live_seedling_num 确定需要处理的草籽数量
        # 生成 logo 字段
        logo = f"{female_ele_num}_{delivery_date_str}_{i}"

        # 从 BasicBasicinfo 中查找父母的草地类型
        ewe = db.session.query(BasicBasicinfo).filter_by(id=data['mother_id']).first()
        ram = db.session.query(BasicBasicinfo).filter_by(id=data['father_id']).first()
        print("++++++++++++++_________________________+++++++++++++++")
        print(ewe)
        print(ewe.variety)

        # 获取父母耳号
        if ewe:
            m_pre_num = ewe.pre_num  # 母草地的地块编号
            m_ele_num = ewe.ele_num  # 母草地的草地编号
            variety = ewe.variety
        else:
            m_pre_num = None
            m_ele_num = None
            variety = None
            # 可以添加异常处理或返回错误
            print(f"未找到母草地（mother_id: {data['mother_id']}）的地块编号")

        if ram:
            f_pre_num = ram.pre_num  # 父草的地块编号
            f_ele_num = ram.ele_num
        else:
            f_pre_num = None
            f_ele_num = None
            # 可以添加异常处理或返回错误
            print(f"未找到父草（father_id: {data['father_id']}）的地块编号")
        lamb = {
            'cultivation_id': data['cultivation_id'],
            'tobasic': 0,
            'logo': logo,
            'pre_num': data.get(f'pre_num_{i}'),
            'variety': variety,
            'sex': data.get(f'sex_{i}'),
            'belong': 0,
            'manu_info_id': 0,
            'manu_info_name': '本场扩繁',
            'state': data.get(f'state_{i}'),
            'sprout_date':delivery_date,
            'sprout_weight': data.get(f'bir_weight_{i}'),
            'mother_id': data['mother_id'],  # 关联母草地的 mother_id
            'father_id':data['father_id'],
            'f_ele_num': f_ele_num,
            'f_pre_num': f_pre_num,
            'm_ele_num': m_ele_num,
            'm_pre_num': m_pre_num,
            'color': data.get(f'color_{i}'),
            'rank': data.get(f'rank_{i}'),

            'f_staff': data.get('f_staff'),  # 如果有其他通用字段，也可以在此添加
            'f_date': data.get('f_date'),
            # 'planting_attendants': data.get('planting_attendants')  # 可以继续添加其他字段
        }
        seedling_data.append(lamb)

    # 插入草籽数据到 ECultivationSproutinfo 表
    if seedling_data:
        try:
            for lamb in seedling_data:
                seedlinginfo = ECultivationSproutinfo()
                for key, value in lamb.items():
                    setattr(seedlinginfo, key, value)
                db.session.add(seedlinginfo)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            result = {
                "code": 500,
                "msg": f'添加草籽信息失败 {str(e)}'
            }
            return jsonify(result)

    result = {
        "code": 200,
        "msg": '添加成功'
    }
    return jsonify(result)


#孕期监测信息
@propagation.route('/propagation/growth_cycleinfo', methods=['POST'])
def get_growth_cycleinfo():
    pageNum = int(request.json.get('pageNum'))
    # pageNum = int(request.form.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        # 'ele_num': ECultivationFloweringinfo.cultivation_id,
        # 'pre_num': ECultivationFloweringinfo.cultivation_id,
        'cultivation_id': ECultivationFloweringinfo.cultivation_id,#这个是查询条件要和你传递的值对比的
        'female_ele_num': ECultivationFloweringinfo.cultivation_id,
        'female_pre_num': ECultivationFloweringinfo.cultivation_id,
        'check_type': ECultivationFloweringinfo.check_type,
        'flowering_status': ECultivationFloweringinfo.flowering_status,
        'notes': ECultivationFloweringinfo.notes,
        'belong': ECultivationFloweringinfo.belong,
        'f_staff': ECultivationFloweringinfo.f_staff,
        'f_date': ECultivationFloweringinfo.f_date,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'f_date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))

            elif param == 'female_ele_num':#如果是查草地编号，首先要查基本信息表里面，获取这个草地编号的id
                basic_id = BasicBasicinfo.query.filter(
                        BasicBasicinfo.ele_num.like(f'%{value}%')).first().id
                print(basic_id)
                propagation_info = ECultivationCultivationinfo.query.filter_by(mother_id=basic_id).first()#然后再从培育信息表里找到这条培育记录
                print('------------------------')
                print(propagation_info)
                if propagation_info:
                    propagation_id = propagation_info.id
                    print(propagation_id)
                    growth_cycle_info = ECultivationFloweringinfo.query.filter_by(cultivation_id=propagation_id).first()#通过培育信息表里的id获取监测表的id，然后对比孕检表中有没有这条propagation_id，把这个作为搜索条件
                    print(growth_cycle_info)                                                                  #这么写好像逻辑上写复杂了，算了，小脑萎缩了，不想了，反正能跑出来
                    conditions.append(column == growth_cycle_info.cultivation_id)
            elif param == 'female_pre_num':
                basic_id = BasicBasicinfo.query.filter(
                        BasicBasicinfo.pre_num.like(f'%{value}%')).first().id
                print(basic_id)
                # 通过propagation_id查找female_id
                propagation_info = ECultivationCultivationinfo.query.filter_by(mother_id=basic_id).first()
                print('------------------------')
                print(propagation_info)
                if propagation_info:
                    propagation_id = propagation_info.id
                    print(propagation_id)
                    # 查找BasicBasicinfo中的ele_num或pre_num
                    growth_cycle_info = ECultivationFloweringinfo.query.filter_by(cultivation_id=propagation_id).first()
                    print(growth_cycle_info)
                    conditions.append(column == growth_cycle_info.cultivation_id)
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = ECultivationFloweringinfo.query.filter(and_(*conditions))
    else:
        query = ECultivationFloweringinfo.query  # 如果没有条件，查询所有

    # 筛选出没有被移除的草(状态-1)和没有枯萎的草(状态0)
    # 并且根据id降序排列

    # 并且根据id降序排列

    query = query.filter(ECultivationFloweringinfo.belong == 0)
    infos = query.order_by(desc(ECultivationFloweringinfo.id)).paginate(page=pageNum, per_page=pageSize,
                                                                  error_out=False)
    total = query.count()

    list = []
    for info in infos:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        data = json.loads(data)
        propagation_info = ECultivationCultivationinfo.query.filter_by(id=data['cultivation_id']).first()
        if propagation_info:
            female_id = propagation_info.mother_id
            # 查找BasicBasicinfo中的ele_num或pre_num
            basic_info = BasicBasicinfo.query.filter_by(id=female_id).first()
            if basic_info:
                data['female_ele_num'] = basic_info.ele_num
                data['female_pre_num'] = basic_info.pre_num
        # basic_info = BasicBasicinfo.query.filter_by(id=data['basic_id']).first()
        # if basic_info:
        #     data['ele_num'] = basic_info.ele_num
        #     data['pre_num'] = basic_info.pre_num
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

@propagation.route('/propagation/growth_cycleinfo/del', methods=['POST'])
def del_growth_cycleinfo():
    ids = request.get_json()
    print("______________________________________")
    print(ids)
    for i in ids:
        ECultivationFloweringinfo.query.filter_by(id=i).delete()
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

@propagation.route('/propagation/growth_cycleinfo/edit', methods=['POST'])
def edit_growth_cycleinfo():
    data = request.get_json()
    print("--data-->", data)
    id = data['id']
    # ele_id = data['ele_num']
    # pre_id = data['pre_num']
    try:
        if 'female_ele_num' in data:

            del data['female_ele_num']
        if 'female_pre_num' in data:

            del data['female_pre_num']


    except Exception as e:
        print("--data-->", data)
        print("--Exception-->", str(e))
    print('--------------------------test--------------------------------')

    # BasicBasicinfo.query.filter_by(ele_id = ele_id,pre_id = pre_id).update(data)
    try:
        ECultivationFloweringinfo.query.filter_by(id=id).update(data)
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

@propagation.route('/propagation/growth_cycleinfo/add', methods=['POST'])
def add_growth_cycleinfo():
    data = request.get_json()
    #去除剂量两端的空格
    # if 'dose' in data:
    #     data['dose'] = data['dose'].strip()
    #     print(data['dose'])

    ctime = datetime.now()
    data['belong'] = 0
    data['f_date'] = ctime

    print(data)

    # # 查询对应的 id
    # female_id = BasicBasicinfo.query.filter_by(ele_num=data['female_ele_num']).first().id
    # propagation_id = ECultivationCultivationinfo.filter_by(female_id=female_id).first().id
    #
    # data['basic_id'] =basic_id
    # print(data)

    growth_cycleinfo= ECultivationFloweringinfo()

    for key, value in data.items():
        setattr(growth_cycleinfo, key, value)
    try:
        db.session.add(growth_cycleinfo)
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

@propagation.route('/propagation/growth_cycleinfo/export', methods=['POST'])
def export_growth_cycleinfo():
    try:
        selected_ids = request.get_json()

        if selected_ids:
            growth_cycle_info = (
                db.session.query(ECultivationFloweringinfo, BasicBasicinfo.ele_num, BasicBasicinfo.pre_num)
                    .outerjoin(ECultivationCultivationinfo, ECultivationCultivationinfo.id == ECultivationFloweringinfo.cultivation_id)
                    .outerjoin(BasicBasicinfo, BasicBasicinfo.id == ECultivationCultivationinfo.mother_id)
                    .filter(ECultivationFloweringinfo.id.in_(selected_ids))
                    .all()
            )
        else:
            growth_cycle_info = (
                db.session.query(ECultivationFloweringinfo, BasicBasicinfo.ele_num, BasicBasicinfo.pre_num)
                    .outerjoin(ECultivationCultivationinfo, ECultivationCultivationinfo.id == ECultivationFloweringinfo.cultivation_id)
                    .outerjoin(BasicBasicinfo, BasicBasicinfo.id == ECultivationCultivationinfo.mother_id)
                    .all()
            )

        data_list = []
        for info, ele_num, pre_num in growth_cycle_info:
            data_list.append({
                '受体草地编号': ele_num,
                '受体地块编号': pre_num,
                '检查类别': info.check_type,
                '孕检信息': info.flowering_status,
                '创建时间': info.f_date.isoformat() if info.f_date else None,
                '创建人员': info.f_staff,
                '备注': info.notes,
            })
        df = pd.DataFrame(data_list)

        export_path = os.path.join(os.getcwd(), 'App', 'propagation', 'export_excel', 'growth_cycle_info.xlsx')
        df.to_excel(export_path, index=False)

        return send_file(export_path, as_attachment=True)
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'导出失败 {str(e)}'})

#养护记录信息
@propagation.route('/propagation/artificial_careinfo', methods=['POST'])
def get_artificial_careinfo():
    pageNum = int(request.json.get('pageNum'))
    # pageNum = int(request.form.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        'sprout_id': ECultivationIrrigationinfo.sprout_id,
        'ele_num':ECultivationIrrigationinfo.sprout_id,
        'pre_num': ECultivationIrrigationinfo.sprout_id,
        'delivery_date':ECultivationIrrigationinfo.delivery_date,
        'BW': ECultivationIrrigationinfo.BW,
        'reason': ECultivationIrrigationinfo.reason,
        'feeding_material': ECultivationIrrigationinfo.feeding_material,
        'mcal': ECultivationIrrigationinfo.mcal,
        'health': ECultivationIrrigationinfo.health,
        'help': ECultivationIrrigationinfo.help,
        'dose': ECultivationIrrigationinfo.dose,
        'feeding_staff': ECultivationIrrigationinfo.feeding_staff,
        'belong': ECultivationSeedinginfo.belong,
        'f_staff': ECultivationSeedinginfo.f_staff,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'f_date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            elif param == 'ele_num':
                lamb_id = ECultivationSproutinfo.query.filter(
                    ECultivationSproutinfo.ele_num.like(f'%{value}%')).first().id
                conditions.append(column == lamb_id)
            elif param == 'pre_num':
                lamb_id = ECultivationSproutinfo.query.filter(
                    ECultivationSproutinfo.pre_num.like(f'%{value}%')).first().id
                conditions.append(column == lamb_id)
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = ECultivationIrrigationinfo.query.filter(and_(*conditions))
    else:
        query = ECultivationIrrigationinfo.query  # 如果没有条件，查询所有

    # 筛选出没有被移除的草(状态-1)和没有枯萎的草(状态0)
    # 并且根据id降序排列

    # 并且根据id降序排列

    query = query.filter(ECultivationIrrigationinfo.belong == 0)
    infos = query.order_by(desc(ECultivationIrrigationinfo.id)).paginate(page=pageNum, per_page=pageSize,
                                                                  error_out=False)
    total = query.count()

    list = []
    for info in infos:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        data = json.loads(data)
        seedling_info = ECultivationSproutinfo.query.filter_by(id=data['sprout_id']).first()
        print(seedling_info)
        print(seedling_info.ele_num)
        print(seedling_info.pre_num)
        if seedling_info:
            data['ele_num'] = seedling_info.ele_num
            data['pre_num'] = seedling_info.pre_num
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

@propagation.route('/propagation/artificial_careinfo/del', methods=['POST'])
def del_artificial_careinfo():
    ids = request.get_json()
    print("______________________________________")
    print(ids)
    for i in ids:
        ECultivationIrrigationinfo.query.filter_by(id=i).delete()
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

@propagation.route('/propagation/artificial_careinfo/edit', methods=['POST'])
def edit_artificial_careinfo():
    data = request.get_json()
    print("--data-->", data)
    id = data['id']
    # ele_id = data['ele_num']
    # pre_id = data['pre_num']
    try:
        if 'ele_num' in data:

            del data['ele_num']
        if 'pre_num' in data:

            del data['pre_num']


    except Exception as e:
        print("--data-->", data)
        print("--Exception-->", str(e))
    print('--------------------------test--------------------------------')

    # BasicBasicinfo.query.filter_by(ele_id = ele_id,pre_id = pre_id).update(data)
    try:
        ECultivationIrrigationinfo.query.filter_by(id=id).update(data)
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

@propagation.route('/propagation/artificial_careinfo/add', methods=['POST'])
def add_artificial_careinfo():
    data = request.get_json()
    #去除剂量两端的空格
    # if 'dose' in data:
    #     data['dose'] = data['dose'].strip()
    #     print(data['dose'])

    ctime = datetime.now()
    data['belong'] = 0
    data['f_date'] = ctime



    # 查询对应的 id
    lamb_id = ECultivationSproutinfo.query.filter_by(ele_num=data['ele_num']).first().id

    data['sprout_id'] =lamb_id
    print(data)

    artificial_careinfo= ECultivationIrrigationinfo()

    for key, value in data.items():
        setattr(artificial_careinfo, key, value)
    try:
        db.session.add(artificial_careinfo)
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

@propagation.route('/propagation/artificial_careinfo/export', methods=['POST'])
def export_artificial_careinfo():
    try:
        selected_ids = request.get_json()

        if selected_ids:
            artificial_care_info = (
                db.session.query(ECultivationIrrigationinfo, ECultivationSproutinfo.ele_num, ECultivationSproutinfo.pre_num)
                    .outerjoin(ECultivationSproutinfo, ECultivationSproutinfo.id == ECultivationIrrigationinfo.sprout_id)
                    .filter(ECultivationIrrigationinfo.id.in_(selected_ids))
                    .all()
            )
        else:
            artificial_care_info = (
                db.session.query(ECultivationIrrigationinfo, ECultivationSproutinfo.ele_num, ECultivationSproutinfo.pre_num)
                    .outerjoin(ECultivationSproutinfo, ECultivationSproutinfo.id == ECultivationIrrigationinfo.sprout_id)
                    .all()
            )

        data_list = []
        for info, ele_num, pre_num in artificial_care_info:
            data_list.append({
                '地块草地编号': ele_num,
                '地块防疫编号': pre_num,
                '繁殖日期': info.delivery_date.isoformat() if info.delivery_date else None,
                '体重监测': info.BW,
                '养护原因': info.reason,
                '养护物': info.feeding_material,
                '食量': info.mcal,
                '健康情况': info.health,
                '求助情况': info.help,
                '用量': info.dose,
                '养护人员': info.feeding_staff,
                '创建人员': info.f_staff
            })
        df = pd.DataFrame(data_list)

        export_path = os.path.join(os.getcwd(), 'App', 'propagation', 'export_excel', 'artificial_care_info.xlsx')
        df.to_excel(export_path, index=False)

        return send_file(export_path, as_attachment=True)
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'导出失败 {str(e)}'})


#成坪记录信息
@propagation.route('/propagation/hardeninginfo', methods=['POST'])
def get_hardeninginfo():
    pageNum = int(request.json.get('pageNum'))
    # pageNum = int(request.form.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        'sprout_id': ECultivationGerminationinfo.sprout_id,
        'sprout_ele_num':ECultivationGerminationinfo.sprout_id,
        'lamb_pre_num':ECultivationGerminationinfo.sprout_id,
        'logo': ECultivationGerminationinfo.sprout_id,
        'Delivery_date':ECultivationGerminationinfo.Delivery_date,
        'cultivation_way': ECultivationGerminationinfo.cultivation_way,
        'Seedling_weight': ECultivationGerminationinfo.Seedling_weight,
        'wea_weight': ECultivationGerminationinfo.wea_weight,
        'rank': ECultivationGerminationinfo.rank,
        # '': ECultivationGerminationinfo,
        'belong': ECultivationSeedinginfo.belong,
        'f_staff': ECultivationSeedinginfo.f_staff,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'Delivery_date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            elif param == 'sprout_ele_num':
                lamb_id = ECultivationSproutinfo.query.filter(
                    ECultivationSproutinfo.ele_num.like(f'%{value}%')).first().id
                conditions.append(column == lamb_id)
            elif param == 'lamb_pre_num':
                lamb_id = ECultivationSproutinfo.query.filter(
                    ECultivationSproutinfo.pre_num.like(f'%{value}%')).first().id
                conditions.append(column == lamb_id)
            elif param == 'logo':
                lamb_id = ECultivationSproutinfo.query.filter(
                    ECultivationSproutinfo.logo.like(f'%{value}%')).first().id
                conditions.append(column == lamb_id)
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = ECultivationGerminationinfo.query.filter(and_(*conditions))
    else:
        query = ECultivationGerminationinfo.query  # 如果没有条件，查询所有

    # 筛选出没有被移除的草(状态-1)和没有枯萎的草(状态0)
    # 并且根据id降序排列

    # 并且根据id降序排列

    query = query.filter(ECultivationGerminationinfo.belong == 0)
    infos = query.order_by(desc(ECultivationGerminationinfo.id)).paginate(page=pageNum, per_page=pageSize,
                                                                  error_out=False)
    total = query.count()

    list = []
    for info in infos:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        data = json.loads(data)
        seedling_info = ECultivationSproutinfo.query.filter_by(id=data['sprout_id']).first()
        if seedling_info:
            data['sprout_ele_num'] = seedling_info.ele_num
            data['lamb_pre_num'] = seedling_info.pre_num
            data['logo'] = seedling_info.logo
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

@propagation.route('/propagation/hardeninginfo/del', methods=['POST'])
def del_hardeninginfo():
    ids = request.get_json()
    print("______________________________________")
    print(ids)
    for i in ids:
        ECultivationGerminationinfo.query.filter_by(id=i).delete()
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

@propagation.route('/propagation/hardeninginfo/edit', methods=['POST'])
def edit_hardeninginfo():
    data = request.get_json()
    print("--data-->", data)
    id = data['id']
    # ele_id = data['ele_num']
    # pre_id = data['pre_num']

    seedling_info = ECultivationSproutinfo.query.filter_by(pre_num=data['lamb_pre_num']).first()
    lamb_pre_num = seedling_info.pre_num
    # lamb_id = ECultivationSproutinfo.query.filter_by(pre_num=data['lamb_pre_num']).first().id

    # data['sprout_id'] =lamb_id
    try:
        if 'sprout_ele_num' in data:

            del data['sprout_ele_num']
        if 'lamb_pre_num' in data:

            del data['lamb_pre_num']
        if 'logo' in data:

            del data['logo']


    except Exception as e:
        print("--data-->", data)
        print("--Exception-->", str(e))
    print('--------------------------test--------------------------------')

    # BasicBasicinfo.query.filter_by(ele_id = ele_id,pre_id = pre_id).update(data)
    try:
        # 更新EbreedLambinfo的wea_weight等字段
        seedling_info.wea_weight = data.get('wea_weight')
        seedling_info.wea_date = data.get('Delivery_date')
        seedling_info.sprout_weight = data.get('Seedling_weight')
        # 更新BasicBasicinfo的wea_weight和wea_date等字段
        basic_info = BasicBasicinfo.query.filter_by(pre_num=lamb_pre_num).first()

        print(basic_info)
        if basic_info:
            basic_info.wea_weight = data.get('wea_weight')
            basic_info.wea_date = data.get('Delivery_date')
            basic_info.bir_weight = data.get('Seedling_weight')
        ECultivationGerminationinfo.query.filter_by(id=id).update(data)
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

@propagation.route('/propagation/hardeninginfo/add', methods=['POST'])
def add_hardeninginfo():
    data = request.get_json()
    #去除剂量两端的空格
    # if 'dose' in data:
    #     data['dose'] = data['dose'].strip()
    #     print(data['dose'])

    ctime = datetime.now()
    data['belong'] = 0
    data['f_date'] = ctime

    print(data)

    # 查询对应的 id
    # 查询对应的id
    seedling_info = ECultivationSproutinfo.query.filter_by(pre_num=data['lamb_pre_num']).first()
    lamb_id = ECultivationSproutinfo.query.filter_by(pre_num=data['lamb_pre_num']).first().id

    data['sprout_id'] =lamb_id
    print(data)

    hardeninginfo= ECultivationGerminationinfo()

    for key, value in data.items():
        setattr(hardeninginfo, key, value)
    try:
        # 更新EbreedLambinfo的wea_weight、wea_date字段
        seedling_info.wea_weight = data.get('wea_weight')
        seedling_info.wea_date = data.get('Delivery_date')
        seedling_info.sprout_weight = data.get('Seedling_weight')
        # 更新BasicBasicinfo的wea_weight和wea_date字段
        basic_info = BasicBasicinfo.query.filter_by(pre_num=data['lamb_pre_num']).first()
        if basic_info:
            basic_info.wea_weight = data.get('wea_weight')
            basic_info.wea_date = data.get('Delivery_date')
            basic_info.bir_weight = data.get('Seedling_weight')
        db.session.add(hardeninginfo)
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

@propagation.route('/propagation/hardeninginfo/export', methods=['POST'])
def export_hardeninginfo():
    try:
        selected_ids = request.get_json()
        Feeding_wayType = {
            0: "自然养护",
            1: "人工养护"
        }
        HardeningRankType = {
            0: "特级",
            1: "一级",
            2: "二级",
            3: "三级",
            9: "未评级"
        }

        if selected_ids:
            hardening_info = (
                db.session.query(ECultivationGerminationinfo, ECultivationSproutinfo.ele_num, ECultivationSproutinfo.pre_num)
                    .outerjoin(ECultivationSproutinfo, ECultivationSproutinfo.id == ECultivationGerminationinfo.sprout_id)
                    .filter(ECultivationGerminationinfo.id.in_(selected_ids))
                    .all()
            )
        else:
            hardening_info = (
                db.session.query(ECultivationGerminationinfo, ECultivationSproutinfo.ele_num, ECultivationSproutinfo.pre_num)
                    .outerjoin(ECultivationSproutinfo, ECultivationSproutinfo.id == ECultivationGerminationinfo.sprout_id)
                    .all()
            )

        data_list = []
        for info, ele_num, pre_num in hardening_info:
            Feeding_wayType_value = Feeding_wayType.get(info.cultivation_way, info.cultivation_way)
            HardeningRankType_value = HardeningRankType.get(info.rank, info.rank)
            data_list.append({
                '草地编号': ele_num,
                '地块编号': pre_num,
                '成坪日期': info.Delivery_date.isoformat() if info.Delivery_date else None,
                '养护方式': Feeding_wayType_value,
                '出生重': info.Seedling_weight,
                '成坪重（出栏体重）': info.wea_weight,
                '成坪评级': HardeningRankType_value,
                '创建人员': info.f_staff
            })
        df = pd.DataFrame(data_list)

        export_path = os.path.join(os.getcwd(), 'App', 'propagation', 'export_excel', 'hardening_info.xlsx')
        df.to_excel(export_path, index=False)

        return send_file(export_path, as_attachment=True)
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'导出失败 {str(e)}'})

@propagation.route('/propagation/hardeninginfo/add', methods=['POST'])
def add_hardeninginfo_upbasiclamb():
    data = request.get_json()
    # ctime = datetime.now()
    data['belong'] = 0
    # data['f_date'] = ctime
    print(data)
    # 查找 BasicBasicinfo 中的 id，通过 lamb_pre_num
    basic_info = BasicBasicinfo.query.filter_by(pre_num=data['lamb_pre_num']).first()

    if not basic_info:
        result = {
            "code": 400,
            "msg": '未找到对应的 BasicBasicinfo 数据'
        }
        return jsonify(result)

    hardeninginfo = ECultivationGerminationinfo()
    for key, value in data.items():
        setattr(hardeninginfo, key, value)
    # 将找到的 basic_id 添加到 ECultivationGerminationinfo
    hardeninginfo.sprout_id = basic_info.id

    try:
        db.session.add(hardeninginfo)
        db.session.commit()
        # 根据 lamb_pre_num 查找 ECultivationSproutinfo
        seedling_info = ECultivationSproutinfo.query.filter_by(pre_num=data['lamb_pre_num']).first()
        if not basic_info:
            result = {
                "code": 400,
                "msg": '未找到对应的 BasicBasicinfo 数据'
            }
            return jsonify(result)

        if seedling_info:
            # 更新 ECultivationSproutinfo 中的 wea_weight
            seedling_info.wea_weight = data['wea_weight']
            db.session.commit()

            # 更新 BasicBasicinfo 中的 Delivery_date 和 wea_weight
            basic_info.wea_date = data['Delivery_date']
            basic_info.wea_weight = data['wea_weight']
            db.session.commit()
        else:
            raise Exception('ECultivationSproutinfo not found for lamb_pre_num')

        result = {
            "code": 200,
            "msg": '添加成功'
        }
        return jsonify(result)

    except Exception as e:
        db.session.rollback()
        db.session.flush()
        result = {
            "code": 500,
            "msg": f'添加失败 {str(e)}'
        }
        return jsonify(result)

#获取新草地信息
@propagation.route('/propagation/seedlinginfo', methods=['POST'])
def get_seedlinginfo():
    pageNum = int(request.json.get('pageNum'))
    # pageNum = int(request.form.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        # 'propagation_id': ECultivationSproutinfo.cultivation_id,
        # 'basic_id': ECultivationSproutinfo.basic_id,
        'tobasic': ECultivationSproutinfo.tobasic,
        'logo': ECultivationSproutinfo.logo,
        'ele_num': ECultivationSproutinfo.ele_num,
        'pre_num': ECultivationSproutinfo.pre_num,
        'purpose': ECultivationSproutinfo.purpose,
        'variety': ECultivationSproutinfo.variety,
        'sex': ECultivationSproutinfo.sex,
        'manu_info_id': ECultivationSproutinfo.manu_info_id,
        'manu_info_name': ECultivationSproutinfo.manu_info_name,
        'state': ECultivationSproutinfo.state,
        'sprout_date': ECultivationSproutinfo.sprout_date,
        'sprout_weight': ECultivationSproutinfo.sprout_weight,
        'wea_date': ECultivationSproutinfo.wea_date,
        'wea_weight': ECultivationSproutinfo.wea_weight,
        'house_name': ECultivationSproutinfo.house_name,
        'hurdle_name': ECultivationSproutinfo.hurdle_name,
        'f_staff': ECultivationSproutinfo.f_staff,
        'f_date': ECultivationSproutinfo.f_date,
        'f_ele_num': ECultivationSproutinfo.father_id,
        'f_pre_num': ECultivationSproutinfo.father_id,
        'm_ele_num': ECultivationSproutinfo.mother_id,
        'm_pre_num': ECultivationSproutinfo.mother_id,
        'gene_a': ECultivationSproutinfo.gene_a,
        'rank': ECultivationSproutinfo.rank,
        'color': ECultivationSproutinfo.color,



        # 'lamb_id': ECultivationGerminationinfo.sprout_id,
        # 'Delivery_date':ECultivationGerminationinfo.Delivery_date,
        # 'feeding_way': ECultivationGerminationinfo.cultivation_way,
        # 'Seedling_weight': ECultivationGerminationinfo.Seedling_weight,
        # 'rank': ECultivationGerminationinfo.rank,
        # # '': ECultivationGerminationinfo,
        # 'belong': ECultivationSeedinginfo.belong,

    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'f_date' or param == 'sprout_date' or param == 'wea_date' :  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            elif param == 'logo':
                # 修改为模糊查询
                conditions.append(column.like(f'%{value}%'))
            elif param == 'ele_num' or param == 'pre_num':
                # 修改为模糊查询
                conditions.append(column.like(f'%{value}%'))
            elif param == 'f_ele_num':
                father_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.ele_num.like(f'%{value}%')).first().id
                print(father_id)
                conditions.append(column == father_id)
            elif param == 'm_ele_num':
                mother_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.ele_num.like(f'%{value}%')).first().id
                conditions.append(column == mother_id)
            elif param == 'f_pre_num':
                father_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.pre_num.like(f'%{value}%')).first().id
                conditions.append(column == father_id)
            elif param == 'm_pre_num':
                mother_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.pre_num.like(f'%{value}%')).first().id
                conditions.append(column == mother_id)
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = ECultivationSproutinfo.query.filter(and_(*conditions))
    else:
        query = ECultivationSproutinfo.query  # 如果没有条件，查询所有

    # 筛选出没有被移除的草(状态-1)和没有枯萎的草(状态0)
    # 并且根据id降序排列

    # 并且根据id降序排列

    query = query.filter(ECultivationSproutinfo.belong == 0)
    infos = query.order_by(desc(ECultivationSproutinfo.id)).paginate(page=pageNum, per_page=pageSize,
                                                                  error_out=False)
    total = query.count()

    list = []
    for info in infos:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        data = json.loads(data)
        # basic_info = BasicBasicinfo.query.filter_by(id=data['basic_id']).first()
        # if basic_info:
        #     data['ele_num'] = basic_info.ele_num
        #     data['pre_num'] = basic_info.pre_num
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

# 成坪信息添加时，筛选出没有添加过成坪信息的草地
@propagation.route('/propagation/seedlinginfo/NoneHardening', methods=['POST'])
def get_None_weaning_seedlinginfo():
    pageNum = int(request.json.get('pageNum'))
    # pageNum = int(request.form.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        # 'propagation_id': ECultivationSproutinfo.cultivation_id,
        # 'basic_id': ECultivationSproutinfo.basic_id,
        'tobasic': ECultivationSproutinfo.tobasic,
        'logo': ECultivationSproutinfo.logo,
        'ele_num': ECultivationSproutinfo.ele_num,
        'pre_num': ECultivationSproutinfo.pre_num,
        'purpose': ECultivationSproutinfo.purpose,
        'variety': ECultivationSproutinfo.variety,
        'sex': ECultivationSproutinfo.sex,
        'manu_info_id': ECultivationSproutinfo.manu_info_id,
        'manu_info_name': ECultivationSproutinfo.manu_info_name,
        'state': ECultivationSproutinfo.state,
        'sprout_date': ECultivationSproutinfo.sprout_date,
        'sprout_weight': ECultivationSproutinfo.sprout_weight,
        'wea_date': ECultivationSproutinfo.wea_date,
        'wea_weight': ECultivationSproutinfo.wea_weight,
        'house_name': ECultivationSproutinfo.house_name,
        'hurdle_name': ECultivationSproutinfo.hurdle_name,
        'f_staff': ECultivationSproutinfo.f_staff,
        'f_date': ECultivationSproutinfo.f_date,
        'f_ele_num': ECultivationSproutinfo.father_id,
        'f_pre_num': ECultivationSproutinfo.father_id,
        'm_ele_num': ECultivationSproutinfo.mother_id,
        'm_pre_num': ECultivationSproutinfo.mother_id,
        'gene_a': ECultivationSproutinfo.gene_a,
        'rank': ECultivationSproutinfo.rank,
        'color': ECultivationSproutinfo.color,



        # 'lamb_id': ECultivationGerminationinfo.sprout_id,
        # 'Delivery_date':ECultivationGerminationinfo.Delivery_date,
        # 'feeding_way': ECultivationGerminationinfo.cultivation_way,
        # 'Seedling_weight': ECultivationGerminationinfo.Seedling_weight,
        # 'rank': ECultivationGerminationinfo.rank,
        # # '': ECultivationGerminationinfo,
        # 'belong': ECultivationSeedinginfo.belong,

    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'f_date' or param == 'sprout_date' or param == 'wea_date' :  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            elif param == 'logo':
                # 修改为模糊查询
                conditions.append(column.like(f'%{value}%'))
            elif param == 'ele_num' or param == 'pre_num':
                # 修改为模糊查询
                conditions.append(column.like(f'%{value}%'))
            elif param == 'f_ele_num':
                father_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.ele_num.like(f'%{value}%')).first().id
                print(father_id)
                conditions.append(column == father_id)
            elif param == 'm_ele_num':
                mother_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.ele_num.like(f'%{value}%')).first().id
                conditions.append(column == mother_id)
            elif param == 'f_pre_num':
                father_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.pre_num.like(f'%{value}%')).first().id
                conditions.append(column == father_id)
            elif param == 'm_pre_num':
                mother_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.pre_num.like(f'%{value}%')).first().id
                conditions.append(column == mother_id)
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = ECultivationSproutinfo.query.filter(and_(*conditions))
    else:
        query = ECultivationSproutinfo.query  # 如果没有条件，查询所有


    # 筛选出没有被移除的草(状态-1)和没有枯萎的草(状态0)
    # 并且根据id降序排列

    # 并且根据id降序排列

    query = query.filter(ECultivationSproutinfo.belong == 0)
        # 增加筛选条件：排除在 ECultivationGerminationinfo 中有记录的草
    weaned_lamb_ids = ECultivationGerminationinfo.query.with_entities(ECultivationGerminationinfo.sprout_id).subquery()
    query = query.filter(~ECultivationSproutinfo.id.in_(weaned_lamb_ids))

    infos = query.order_by(desc(ECultivationSproutinfo.id)).paginate(page=pageNum, per_page=pageSize,
                                                                  error_out=False)
    total = query.count()

    list = []
    for info in infos:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        data = json.loads(data)
        # basic_info = BasicBasicinfo.query.filter_by(id=data['basic_id']).first()
        # if basic_info:
        #     data['ele_num'] = basic_info.ele_num
        #     data['pre_num'] = basic_info.pre_num
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

@propagation.route('/propagation/seedlinginfo/del', methods=['POST'])
def del_seedlinginfo():
    ids = request.get_json()
    print("______________________________________")
    print(ids)
    for i in ids:
        ECultivationSproutinfo.query.filter_by(id=i).delete()
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

@propagation.route('/propagation/seedlinginfo/export', methods=['POST'])
def export_seedlinginfo():
    try:
        selected_ids = request.get_json()
        tobasic_dict = {
            1: "是",
            0: "否"
        }
        purposeType = {
            0: "草地(待分类)",
            1: "育肥田",
            2: "试验田",
            5: "繁殖父系草地",
            6: "繁殖母系草地",
            8: "成坪草地"
        }
        sexType = {
            1: "种植区",
            0: "生产区"
        }
        Lamb_statType = {
            0: "健康",
            1: "死亡",
            2: "瘦弱",
            3: "残疾"
        }
        colorType = {
            0: "白",
            1: "黑",
            2: "咖",
            3: "混合色"
        }
        rankType = {
            0: "特级",
            1: "一级",
            2: "二级",
            3: "三级",
            9: "未评级"
        }
        gene_aType = {
            0: "BB",
            1: "B+",
            2: "++",
            3: "暂空"
        }
        varietyType = {
            0: "小麦",
            1: "玉米",
            2: "水稻",
            3: "大豆",
            4: "苜蓿",
            5: "黑麦草",
            6: "燕麦",
            7: "高粱",
            8: "谷子",
            9: "油菜",
            10: "其他"
        }

        if selected_ids:
            seedling_info = (
                db.session.query(ECultivationSproutinfo)
                    .filter(ECultivationSproutinfo.id.in_(selected_ids))
                    .all()
            )
        else:
            seedling_info = (
                db.session.query(ECultivationSproutinfo)
                    .all()
            )

        data_list = []
        for info in seedling_info:
            tobasic_dict_value = tobasic_dict.get(info.tobasic, info.tobasic)
            purposeType_value = purposeType.get(info.purpose, info.purpose)
            varietyType_value = varietyType.get(info.variety, info.variety)
            sexTypee_value = sexType.get(info.sex, info.sex)
            Lamb_statTypee_value = Lamb_statType.get(info.state, info.state)
            colorType_value = colorType.get(info.color, info.color)
            rankType_value = rankType.get(info.rank, info.rank)
            gene_aType_value = gene_aType.get(info.gene_a, info.gene_a)
            data_list.append({
                '草地编号': info.ele_num,
                '地块编号': info.pre_num,
                '是否入库': tobasic_dict_value,
                '批次标识': info.logo,
                '用途': purposeType_value,
                '草地类型': varietyType_value,
                '作物类型': sexTypee_value,
                '原产地': info.manu_info_name,
                '状态': Lamb_statTypee_value,
                '出生体重(Kg)': info.sprout_weight,
                '成坪重(Kg)': info.wea_weight,
                '所属监测区域': info.house_name,
                '监测地块': info.hurdle_name,
                '生长月数': info.mon_age,
                '草地颜色': colorType_value,
                '受灾等级': rankType_value,
                '母草地编号': info.m_ele_num,
                '母地块编号': info.m_pre_num,
                '父草地编号': info.f_ele_num,
                '父地块编号': info.f_pre_num,
                '抗虫基因型': gene_aType_value,
                '综合评分': info.score,
                '创建时间': info.f_date.isoformat() if info.f_date else None,
                '创建人员': info.f_staff,
                '备注': info.note
            })
        df = pd.DataFrame(data_list)

        export_path = os.path.join(os.getcwd(), 'App', 'propagation', 'export_excel', 'seedling_info.xlsx')
        df.to_excel(export_path, index=False)

        return send_file(export_path, as_attachment=True)
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'导出失败 {str(e)}'})

#添加入库信息tobasic添加记录到基本信息表并修改新草地信息表
@propagation.route('/propagation/seedlinginfo/edit_and_tobasic', methods=['POST'])
def edit_and_tobasic():
    # 入棚自动添加草地编号
    def generate_ele_num(pre_num, birth_date, variety):
        # 固定的前6位
        prefix = "131102"

        # 获取出生日期的后两位年份和月日
        year = str(birth_date.year)[2:]  # 获取年份的后两位
        month_day = birth_date.strftime("%m%d")  # 获取月日部分

        # # 获取variety的对应value
        # variety_value = None
        # for variety in variety_type:
        #     if variety['label'] == variety_label:
        #         variety_value = variety['value']
        #         break
        #
        # if variety_value is None:
        #     raise ValueError(f"未找到匹配的品种: {variety_label}")

        # 拼接生成ele_num，直接将pre_num拼接
        ele_num = prefix + year + month_day + str(variety) + str(pre_num)

        return ele_num

    try:
        # 获取前端传递的数据
        data = request.get_json()
        print("_____________________________")
        print(data)

        seedling_info = db.session.query(ECultivationSproutinfo).filter_by(id=data['id']).first()
        print(seedling_info)
        if not seedling_info:
            return jsonify({"code": 404, "msg": "新草地信息未找到"})
        # # 如果没有ele_num，根据pre_num生成ele_num
        # if  seedling_info.ele_num is None:  # 如果ele_num为空
        #     birth_date = seedling_info.birth  # 获取出生日期
        #     variety = data.get('variety') # 获取品种标签
        #     pre_num = seedling_info.pre_num  # 获取草地类型
        #     seedling_info.ele_num = generate_ele_num(pre_num, birth_date, variety)  # 根据pre_num、birth和variety生成ele_num
        #     print(seedling_info.ele_num)


        # 更新成坪信息到成坪信息表

        # 检查前端是否传递了 ele_num
        if 'ele_num' in data and data['ele_num']:
            seedling_info.ele_num = data['ele_num']
        else:
            # 如果没有传递 ele_num，根据 pre_num 生成 ele_num
            birth_date = seedling_info.sprout_date  # 获取出生日期
            variety = data.get('variety')  # 获取品种标签
            pre_num = seedling_info.pre_num  # 获取草地类型
            seedling_info.ele_num = generate_ele_num(pre_num, birth_date, variety)  # 根据 pre_num、birth 和 variety 生成 ele_num
        print(seedling_info.ele_num)

        wearing_info = db.session.query(ECultivationGerminationinfo).filter_by(sprout_id=data['id']).first()

        if wearing_info:
            wearing_info.wea_weight = data.get('wea_weight')
            wearing_info.Delivery_date = data.get('wea_date')
            wearing_info.Seedling_weight = data.get('bir_weight')
            db.session.commit()
        # else:
        #     # 创建新的成坪信息记录
        #     new_wearing_info = ECultivationGerminationinfo(
        #         lamb_id=data['id'],
        #         wea_weight=data.get('wea_weight'),
        #         Delivery_date=data.get('wea_date'),
        #         Seedling_weight=data.get('bir_weight'),
        #         rank=9,
        #         f_staff=data.get('f_staff'),
        #         belong=0,
        #         feeding_way=0
        #     )
        #     db.session.add(new_wearing_info)
        #     db.session.commit()




        # 添加到 Basicbasicinfo 表

        birth_str = data.get('birth')
        birth_date = datetime.strptime(birth_str, '%Y-%m-%d').date()
        today = datetime.now().date()
        print(birth_date)
        print(today)

        basic_info = BasicBasicinfo(
            ele_num=seedling_info.ele_num,
            pre_num=data.get('pre_num'),
            purpose=data.get('purpose'),
            variety=data.get('variety'),
            sex=data.get('sex'),
            manu_info_id=data.get('manu_info_id'),
            manu_info_name=data.get('manu_info_name'),
            state=1,
            birth=data.get('birth'),
            mon_age = round((today - birth_date).days / 30, 1),
            bir_weight=data.get('bir_weight'),
            wea_date = data.get('wea_date'),
            wea_weight=data.get('wea_weight'),
            house_id=data.get('house_id'),
            house_name=data.get('house_name'),
            hurdle_id=data.get('hurdle_id'),
            hurdle_name=data.get('hurdle_name'),
            f_ele_num = data.get('f_ele_num'),
            f_pre_num = data.get('f_pre_num'),
            m_ele_num = data.get('m_ele_num'),
            m_pre_num = data.get('m_pre_num'),
            father_id = data.get('father_id'),
            mother_id=data.get('mother_id'),
            f_staff=data.get('f_staff'),
            f_date=data.get('f_date'),
            belong=0,
            color=data.get('color'),
            rank=data.get('rank'),
            gene_a = data.get('gene_a'),

        )
        db.session.add(basic_info)

        # 提交事务
        db.session.commit()


        # 获取新插入的 BasicBasicinfo 表的 id
        basic_id = basic_info.id

        # 更新 Ebreedseedlinginfo 表


        # 更新字段
        seedling_info.basic_id = basic_id  # 更新 basic_id
        seedling_info.belong = data.get('belong')
        seedling_info.tobasic = data.get('tobasic')
        seedling_info.sprout_weight = data.get('bir_weight')
        seedling_info.wea_weight = data.get('wea_weight')
        seedling_info.sprout_date = data.get('birth')
        seedling_info.mon_age = round((today - birth_date).days / 30, 1)
        seedling_info.wea_date = data.get('wea_date')
        seedling_info.color = data.get('color')
        seedling_info.ele_num = seedling_info.ele_num
        seedling_info.f_date = data.get('f_date')
        seedling_info.f_ele_num = data.get('f_ele_num')
        seedling_info.f_pre_num = data.get('f_pre_num')
        seedling_info.f_staff = data.get('f_staff')
        seedling_info.father_id = data.get('father_id')
        seedling_info.gene_a = data.get('gene_a')
        seedling_info.house_id = data.get('house_id')
        seedling_info.house_name = data.get('house_name')  # 这里也更新
        seedling_info.hurdle_id = data.get('hurdle_id')
        seedling_info.hurdle_name = data.get('hurdle_name')  # 这里也更新
        seedling_info.logo = data.get('logo')
        seedling_info.m_ele_num = data.get('m_ele_num')
        seedling_info.m_pre_num = data.get('m_pre_num')
        seedling_info.mother_id = data.get('mother_id')
        seedling_info.manu_info_id = data.get('manu_info_id')
        seedling_info.purpose = data.get('purpose')
        seedling_info.rank = data.get('rank')
        seedling_info.sex = data.get('sex')
        seedling_info.state = data.get('state')
        seedling_info.variety = data.get('variety')
        seedling_info.note = data.get('note')  # 如果传递了 note，也可以更新

        # 如果需要可以更新其他字段...

        # 提交更新事务
        db.session.commit()

        # 返回成功响应
        return jsonify({"code": 200, "msg": "信息更新并添加成功"})

    except Exception as e:
        # 如果出现异常，回滚事务并返回错误信息
        db.session.rollback()
        return jsonify({"code": 500, "msg": f"操作失败: {str(e)}"})
