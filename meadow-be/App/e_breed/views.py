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
e_breed = Blueprint('e_breed', __name__)


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
@e_breed.route('/e_breed/rutinfo', methods=['POST'])#获取草地生长监测信息
def get_rutinfo():
    pageNum = int(request.json.get('pageNum'))
    # pageNum = int(request.form.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        'ele_num': EBreedRutinfo.basic_id,
        'pre_num': EBreedRutinfo.basic_id,
        'age': EBreedRutinfo.age,
        'breeding': EBreedRutinfo.breeding,
        'belong': EBreedRutinfo.belong,
        'f_staff': EBreedRutinfo.f_staff,
        'f_date': EBreedRutinfo.f_date,
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
        query = EBreedRutinfo.query.filter(and_(*conditions))
    else:
        query = EBreedRutinfo.query  # 如果没有条件，查询所有

    # 筛选出没有被移除的草(状态-1)和没有枯萎的草(状态0)
    # 并且根据id降序排列

    # 并且根据id降序排列

    query = query.filter(EBreedRutinfo.belong == 0)
    infos = query.order_by(desc(EBreedRutinfo.id)).paginate(page=pageNum, per_page=pageSize,
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

@e_breed.route('/e_breed/rutinfo/del', methods=['POST'])#删除草地生长监测信息
def del_rutinfo():
    ids = request.get_json()
    print("______________________________________")
    print(ids)
    for i in ids:
        EBreedRutinfo.query.filter_by(id=i).delete()
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

@e_breed.route('/e_breed/rutinfo/edit', methods=['POST'])#编辑草地生长监测信息
def edit_rutinfo():
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
        EBreedRutinfo.query.filter_by(id=id).update(data)
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

@e_breed.route('/e_breed/rutinfo/add', methods=['POST'])#添加草地生长监测信息
def add_rutinfo():
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

    rut_info= EBreedRutinfo()

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
@e_breed.route('/e_breed/rutinfo/get_ewesheep', methods=['POST'])
def get_ewesheep():
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

@e_breed.route('/e_breed/rutinfo/export', methods=['POST'])
def export_rutinfo():
    try:
        selected_ids = request.get_json()
        breeding_dict = {
            1: "是",
            0: "否"
        }

        if selected_ids:
            rut_info = (
                db.session.query(EBreedRutinfo, BasicBasicinfo.ele_num, BasicBasicinfo.pre_num)
                    .outerjoin(BasicBasicinfo, BasicBasicinfo.id == EBreedRutinfo.basic_id)
                    .filter(EBreedRutinfo.id.in_(selected_ids))
                    .all()
            )
        else:
            rut_info = (
                db.session.query(EBreedRutinfo, BasicBasicinfo.ele_num, BasicBasicinfo.pre_num)
                    .outerjoin(BasicBasicinfo, BasicBasicinfo.id == EBreedRutinfo.basic_id)
                    .all()
            )

        data_list = []
        for info, ele_num, pre_num in rut_info:
            breeding_value = breeding_dict.get(info.breeding, info.breeding)
            data_list.append({
                '草地编号': ele_num,
                '地块编号': pre_num,
                '月龄': info.age,
                '是否培育': breeding_value,
                '创建时间': info.f_date.isoformat() if info.f_date else None,
                '创建人员': info.f_staff
            })
        df = pd.DataFrame(data_list)

        export_path = os.path.join(os.getcwd(), 'App', 'e_breed', 'export_excel', 'rut_info.xlsx')
        df.to_excel(export_path, index=False)

        return send_file(export_path, as_attachment=True)
    except Exception as e:
        result = {
            "code": 500,
            "msg": f'导出失败 {str(e)}'
        }
        return jsonify(result)


#草地采样信息
@e_breed.route('/e_breed/semencollectinfo', methods=['POST'])
def get_semencollectinfo():
    pageNum = int(request.json.get('pageNum'))
    # pageNum = int(request.form.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        'ele_num': EBreedSemencollectinfo.basic_id,
        'pre_num': EBreedSemencollectinfo.basic_id,
        'E_date': EBreedSemencollectinfo.E_date,
        'dilution_ratio': EBreedSemencollectinfo.dilution_ratio,
        'diluent_type': EBreedSemencollectinfo.diluent_type,
        'disused': EBreedSemencollectinfo.disused,
        'belong': EBreedRutinfo.belong,
        'f_staff': EBreedRutinfo.f_staff,
        'f_date': EBreedRutinfo.f_date,
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
        query = EBreedSemencollectinfo.query.filter(and_(*conditions))
    else:
        query = EBreedSemencollectinfo.query  # 如果没有条件，查询所有

    # 筛选出没有被移除的草(状态-1)和没有枯萎的草(状态0)
    # 并且根据id降序排列

    # 并且根据id降序排列

    query = query.filter(EBreedSemencollectinfo.belong == 0)
    infos = query.order_by(desc(EBreedSemencollectinfo.id)).paginate(page=pageNum, per_page=pageSize,
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

@e_breed.route('/e_breed/semencollectinfo/del', methods=['POST'])
def del_semencollectinfo():
    ids = request.get_json()
    print("______________________________________")
    print(ids)
    for i in ids:
        EBreedSemencollectinfo.query.filter_by(id=i).delete()
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

@e_breed.route('/e_breed/semencollectinfo/edit', methods=['POST'])
def edit_semencollectinfo():
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
        EBreedSemencollectinfo.query.filter_by(id=id).update(data)
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

@e_breed.route('/e_breed/semencollectinfo/add', methods=['POST'])
def add_semencollectinfo():
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

    semencollect_info= EBreedSemencollectinfo()

    for key, value in data.items():
        setattr(semencollect_info, key, value)
    try:
        db.session.add(semencollect_info)
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

@e_breed.route('/e_breed/semencollectinfo/export', methods=['POST'])
def export_semencollectinfo():
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
            semencollect_info = (
                db.session.query(EBreedSemencollectinfo, BasicBasicinfo.ele_num, BasicBasicinfo.pre_num)
                    .outerjoin(BasicBasicinfo, BasicBasicinfo.id == EBreedSemencollectinfo.basic_id)
                    .filter(EBreedSemencollectinfo.id.in_(selected_ids))
                    .all()
            )
        else:
            semencollect_info = (
                db.session.query(EBreedSemencollectinfo, BasicBasicinfo.ele_num, BasicBasicinfo.pre_num)
                    .outerjoin(BasicBasicinfo, BasicBasicinfo.id == EBreedSemencollectinfo.basic_id)
                    .all()
            )

        data_list = []
        for info, ele_num, pre_num in semencollect_info:
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

        export_path = os.path.join(os.getcwd(), 'App', 'e_breed', 'export_excel', 'semencollect_info.xlsx')
        df.to_excel(export_path, index=False)

        return send_file(export_path, as_attachment=True)
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'导出失败 {str(e)}'})

# 病虫害繁殖周期采样
#获取月龄8以上的健康未销售的公草地记录(在生长记录是12月，在生长监测和培育时8月)、、、、、、、、、、、、、、、、、、改成6月了
@e_breed.route('/e_breed/semencollectinfo/get_ramsheep', methods=['POST'])
def get_ramsheep():
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
@e_breed.route('/e_breed/breedinginfo', methods=['POST'])
def get_breedinginfo():
    pageNum = int(request.json.get('pageNum'))
    # pageNum = int(request.form.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        # '': EBreedBreedinginfo,
        'breeding_date': EBreedBreedinginfo.breeding_date,
        'pre_production_date': EBreedBreedinginfo.pre_production_date,
        'breeding_way': EBreedBreedinginfo.breeding_way,
        'ewe_id': EBreedBreedinginfo.ewe_id,
        'ram_ele_num': EBreedBreedinginfo.ram_id,
        'ram_pre_num': EBreedBreedinginfo.ram_id,
        'ewe_ele_num': EBreedBreedinginfo.ewe_id,
        'ewe_pre_num': EBreedBreedinginfo.ewe_id,
        'ewe_variety': EBreedBreedinginfo.ewe_variety,
        'ram_id': EBreedBreedinginfo.ram_id,
        'ram_variety': EBreedBreedinginfo.ram_variety,
        'breeding_state': EBreedBreedinginfo.breeding_state,
        'staff': EBreedBreedinginfo.staff,
        'f_staff': EBreedRutinfo.f_staff,
        'f_date': EBreedRutinfo.f_date,
        'belong': EBreedRutinfo.belong,
        'mat_period': EBreedBreedinginfo.mat_period,
        'single_ok': EBreedBreedinginfo.single_ok,
        # 'ele_num': EBreedRutinfo.basic_id,
        # 'pre_num': EBreedRutinfo.basic_id,
        # 'age': EBreedRutinfo.age,
        # 'breeding': EBreedRutinfo.breeding,


    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'f_date' or param == 'breeding_date' or param == 'pre_production_date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            elif param == 'ram_ele_num':
                ram_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.ele_num.like(f'%{value}%')).first().id
                print(ram_id)
                conditions.append(column == ram_id)
            elif param == 'ewe_ele_num':
                ewe_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.ele_num.like(f'%{value}%')).first().id
                conditions.append(column == ewe_id)
            elif param == 'ram_pre_num':
                ram_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.pre_num.like(f'%{value}%')).first().id
                conditions.append(column == ram_id)
            elif param == 'ewe_pre_num':
                ewe_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.pre_num.like(f'%{value}%')).first().id
                conditions.append(column == ewe_id)
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = EBreedBreedinginfo.query.filter(and_(*conditions))
    else:
        query = EBreedBreedinginfo.query  # 如果没有条件，查询所有

    # 筛选出没有被移除的草(状态-1)和没有枯萎的草(状态0)
    # 并且根据id降序排列

    # 并且根据id降序排列

    query = query.filter(EBreedBreedinginfo.belong == 0)
    infos = query.order_by(desc(EBreedBreedinginfo.id)).paginate(page=pageNum, per_page=pageSize,
                                                                  error_out=False)
    total = query.count()

    list = []
    for info in infos:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        data = json.loads(data)
        ewe_info = BasicBasicinfo.query.filter_by(id=data['ewe_id']).first()
        if ewe_info:
            data['ewe_ele_num'] = ewe_info.ele_num
            data['ewe_pre_num'] = ewe_info.pre_num
        ram_info = BasicBasicinfo.query.filter_by(id=data['ram_id']).first()
        if ram_info:
            data['ram_ele_num'] = ram_info.ele_num
            data['ram_pre_num'] = ram_info.pre_num
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

@e_breed.route('/e_breed/breedinginfo/del', methods=['POST'])
def del_breedinginfo():
    ids = request.get_json()
    print("______________________________________")
    print(ids)
    for i in ids:
        EBreedBreedinginfo.query.filter_by(id=i).delete()
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

@e_breed.route('/e_breed/breedinginfo/edit', methods=['POST'])
def edit_breedinginfo():
    data = request.get_json()
    # print(data)
    print("--data-->", data)
    id = data['id']
    # ele_id = data['ele_num']
    # pre_id = data['pre_num']
    try:
        print(data)
        if 'ram_ele_num' in data:
            # data["basic_id"] = BasicBasicinfo.query.filter(
            #     BasicBasicinfo.ele_num ==data['ele_num']).first().id
            del data['ram_ele_num']
        if 'ram_pre_num' in data:
            # data["basic_id"] = BasicBasicinfo.query.filter(
            #     BasicBasicinfo.pre_num ==data['pre_num']).first().id
            del data['ram_pre_num']
        if 'ewe_ele_num' in data:
            # data["basic_id"] = BasicBasicinfo.query.filter(
            #     BasicBasicinfo.ele_num ==data['ele_num']).first().id
            del data['ewe_ele_num']
        if 'ewe_pre_num' in data:
            # data["basic_id"] = BasicBasicinfo.query.filter(
            #     BasicBasicinfo.pre_num ==data['pre_num']).first().id
            del data['ewe_pre_num']
        # if 'ram_id' in data:
        #     del data['ram_id']
        # if 'ewe_id' in data:
        #     del data['ram_id']
        # if 'ram_id' in data:
        #     del data['ram_id']
        # if 'ram_id' in data:
        #     del data['ram_id']
        print("----------------------------")
        print(data)
    except Exception as e:
        print("--data-->", data)
        print("--Exception-->", str(e))
    print('--------------------------test--------------------------------')

    # BasicBasicinfo.query.filter_by(ele_id = ele_id,pre_id = pre_id).update(data)
    try:
        EBreedBreedinginfo.query.filter_by(id=id).update(data)
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

@e_breed.route('/e_breed/breedinginfo/add', methods=['POST'])
def add_breedinginfo():
    data = request.get_json()
    #去除剂量两端的空格
    # if 'dose' in data:
    #     data['dose'] = data['dose'].strip()
    #     print(data['dose'])

    ctime = datetime.now()
    data['belong'] = 0
    data['f_date'] = ctime



    # 查询对应的 id
    ewe_id = BasicBasicinfo.query.filter_by(ele_num=data['ewe_ele_num']).first().id

    data['ewe_id'] =ewe_id

    # 查询对应的 id
    ram_id = BasicBasicinfo.query.filter_by(ele_num=data['ram_ele_num']).first().id

    data['ram_id'] =ram_id
    print(data)

    breedinginfo= EBreedBreedinginfo()

    for key, value in data.items():
        setattr(breedinginfo, key, value)
    try:
        db.session.add(breedinginfo)
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
@e_breed.route('/e_breed/breedinginfo/judge_inbreed', methods=['POST'])
def judge_inbreed():
    """
    通过传入的 ram_ele_num 和 ewe_ele_num 查询相关记录，并检查是否有共同祖先。

    参数:
        ram_ele_num (str): 供体草地编号
        ewe_ele_num (str): 受体田块草地编号

    返回:
        flask.Response: JSON 格式的响应，包含检查结果
    """
    # 获取前端传递的数据
    data = request.get_json()
    ram_ele_num = data.get("ram_ele_num")
    ewe_ele_num = data.get("ewe_ele_num")
    try:
        # 查询公草地记录
        ram_record = BasicBasicinfo.query.filter_by(ele_num=ram_ele_num).first()
        if not ram_record:
            return jsonify({"code": 404, "msg": f"未找到对应的公草地记录：{ram_ele_num}"})

        # 查询母草地记录
        ewe_record = BasicBasicinfo.query.filter_by(ele_num=ewe_ele_num).first()
        if not ewe_record:
            return jsonify({"code": 404, "msg": f"未找到对应的母草地记录：{ewe_ele_num}"})

        # 提取公草地的相关祖先信息
        ram_ancestors = [
            ram_ele_num,
            ram_record.f_ele_num,  # 父亲
            ram_record.m_ele_num,  # 母亲
            ram_record.ram_grandfather_ele_num,  # 父方祖父
            ram_record.ram_grandmother_ele_num,  # 父方祖母
            ram_record.ewe_grandfather_ele_num,  # 父方外祖父
            ram_record.ewe_grandmother_ele_num  # 父方外祖母
        ]

        # 提取母草地的相关祖先信息
        ewe_ancestors = [
            ewe_ele_num,
            ewe_record.f_ele_num,  # 父亲
            ewe_record.m_ele_num,  # 母亲
            ewe_record.ram_grandfather_ele_num,  # 母方祖父
            ewe_record.ram_grandmother_ele_num,  # 母方祖母
            ewe_record.ewe_grandfather_ele_num,  # 母方外祖父
            ewe_record.ewe_grandmother_ele_num  # 母方外祖母
        ]

        # 去除 None、空字符串和无效值 "0000000000000000"
        ram_ancestors = [ancestor for ancestor in ram_ancestors if ancestor and ancestor != "0000000000000000"]
        ewe_ancestors = [ancestor for ancestor in ewe_ancestors if ancestor and ancestor != "0000000000000000"]

        print(f'{ram_ancestors}')
        print('-------------------------------')
        print(f'{ewe_ancestors}')

        # 计算交集
        common_ancestors = set(ram_ancestors) & set(ewe_ancestors)

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


@e_breed.route('/e_breed/breedinginfo/export', methods=['POST'])
def export_breedinginfo():
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
            breeding_info = (
                db.session.query(
                    EBreedBreedinginfo,
                    ewe_info.ele_num.label("ewe_ele_num"),
                    ewe_info.pre_num.label("ewe_pre_num"),
                    ram_info.ele_num.label("ram_ele_num"),
                    ram_info.pre_num.label("ram_pre_num")
                )
                    .outerjoin(ewe_info, ewe_info.id == EBreedBreedinginfo.ewe_id)
                    .outerjoin(ram_info, ram_info.id == EBreedBreedinginfo.ram_id)
                    .filter(EBreedBreedinginfo.id.in_(selected_ids))
                    .all()
            )
        else:
            breeding_info = (
                db.session.query(
                    EBreedBreedinginfo,
                    ewe_info.ele_num.label("ewe_ele_num"),
                    ewe_info.pre_num.label("ewe_pre_num"),
                    ram_info.ele_num.label("ram_ele_num"),
                    ram_info.pre_num.label("ram_pre_num")
                )
                    .outerjoin(ewe_info, ewe_info.id == EBreedBreedinginfo.ewe_id)
                    .outerjoin(ram_info, ram_info.id == EBreedBreedinginfo.ram_id)
                    .all()
            )

        data_list = []
        for info, ewe_ele_num, ewe_pre_num, ram_ele_num, ram_pre_num in breeding_info:
            Breeding_wayType_value = Breeding_wayType.get(info.breeding_way, info.breeding_way)
            ewe_varietyType_value = varietyType.get(info.ewe_variety, info.ewe_variety)
            ram_varietyType_value = varietyType.get(info.ram_variety, info.ram_variety)
            data_list.append({
                '受体草地编号': ewe_ele_num,
                '受体地块编号': ewe_pre_num,
                '受体草地类型': ewe_varietyType_value,
                '供体草地编号': ram_ele_num,
                '供体地块编号': ram_pre_num,
                '供体草地类型': ram_varietyType_value,
                '传播日期': info.breeding_date.isoformat() if info.breeding_date else None,
                '预产日期': info.pre_production_date.isoformat() if info.pre_production_date else None,
                '传播方式': Breeding_wayType_value,
                '培育状态': info.breeding_state,
                '培育情期（天）': info.mat_period,
                '单次培育成功率（%）': info.single_ok,
                '操作师': info.staff,
                '创建时间': info.f_date.isoformat() if info.f_date else None,
                '创建人员': info.f_staff
            })
        df = pd.DataFrame(data_list)

        export_path = os.path.join(os.getcwd(), 'App', 'e_breed', 'export_excel', 'breedinginfo.xlsx')
        df.to_excel(export_path, index=False)

        return send_file(export_path, as_attachment=True)
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'导出失败 {str(e)}'})
#生长记录信息一条龙
@e_breed.route('/e_breed/postnatalinfo', methods=['POST'])
def get_postnatalinfo():
    pageNum = int(request.json.get('pageNum'))
    # pageNum = int(request.form.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        # 'ele_num': EBreedRutinfo.basic_id,
        # 'pre_num': EBreedRutinfo.basic_id,
        'breeding_date': EBreedPostnatalinfo.breeding_date,
        'delivery_date': EBreedPostnatalinfo.delivery_date,
        'ram_id': EBreedPostnatalinfo.ram_id,
        'ewe_id': EBreedPostnatalinfo.ewe_id,
        'ram_ele_num': EBreedPostnatalinfo.ram_id,
        'ram_pre_num': EBreedPostnatalinfo.ram_id,
        'ewe_ele_num': EBreedPostnatalinfo.ewe_id,
        'ewe_pre_num': EBreedPostnatalinfo.ewe_id,
        'Booroola': EBreedPostnatalinfo.Booroola,
        'ewe_health': EBreedPostnatalinfo.ewe_health,
        'ewe_condition': EBreedPostnatalinfo.ewe_condition,
        'lamb_ele_num': EBreedPostnatalinfo.lamb_ele_num,
        'lamb_state': EBreedPostnatalinfo.lamb_state,
        'bir_weight': EBreedPostnatalinfo.bir_weight,
        'live_num': EBreedPostnatalinfo.live_num,
        'birth_attendants': EBreedPostnatalinfo.birth_attendants,
        'notes': EBreedPostnatalinfo.notes,
        'belong': EBreedRutinfo.belong,
        'f_staff': EBreedRutinfo.f_staff,
        'f_date': EBreedRutinfo.f_date,
    }
    for param, column in search_params.items():
        print(param)
        print(column)
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'f_date' or param == 'breeding_date' or param == 'delivery_date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            elif param == 'ram_id':
                id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.id.like(f'%{value}%')).first().id
                conditions.append(column == id)
            elif param == 'ewe_id':
                id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.id.like(f'%{value}%')).first().id
                conditions.append(column == id)
            elif param == 'ram_ele_num':
                ram_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.ele_num.like(f'%{value}%')).first().id
                print(ram_id)
                conditions.append(column == ram_id)
            elif param == 'ewe_ele_num':
                ewe_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.ele_num.like(f'%{value}%')).first().id
                conditions.append(column == ewe_id)
            elif param == 'ram_pre_num':
                ram_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.pre_num.like(f'%{value}%')).first().id
                conditions.append(column == ram_id)
            elif param == 'ewe_pre_num':
                ewe_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.pre_num.like(f'%{value}%')).first().id
                conditions.append(column == ewe_id)
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = EBreedPostnatalinfo.query.filter(and_(*conditions))
        print(query)
    else:
        query = EBreedPostnatalinfo.query  # 如果没有条件，查询所有

    # 筛选出没有被移除的草(状态-1)和没有枯萎的草(状态0)
    # 并且根据id降序排列

    # 并且根据id降序排列

    query = query.filter(EBreedPostnatalinfo.belong == 0)
    infos = query.order_by(desc(EBreedPostnatalinfo.id)).paginate(page=pageNum, per_page=pageSize,
                                                                  error_out=False)
    total = query.count()

    list = []
    for info in infos:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        data = json.loads(data)
        ram_info = BasicBasicinfo.query.filter_by(id=data['ram_id']).first()
        ewe_info = BasicBasicinfo.query.filter_by(id=data['ewe_id']).first()
        if ram_info:
            data['ram_ele_num'] = ram_info.ele_num
            data['ram_pre_num'] = ram_info.pre_num

        if ewe_info:
            data['ewe_ele_num'] = ewe_info.ele_num
            data['ewe_pre_num'] = ewe_info.pre_num
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

@e_breed.route('/e_breed/postnatalinfo/del', methods=['POST'])
def del_postnatalinfo():
    ids = request.get_json()
    print("______________________________________")
    print(ids)
    for i in ids:
        EBreedPostnatalinfo.query.filter_by(id=i).delete()
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

@e_breed.route('/e_breed/postnatalinfo/edit', methods=['POST'])
def edit_postnatalinfo():
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
        if 'ewe_ele_num' in data:
            del data['ewe_ele_num']
        if 'ewe_pre_num' in data:
            del data['ewe_pre_num']
        if 'ram_ele_num' in data:
            del data['ram_ele_num']
        if 'ram_pre_num' in data:
            del data['ram_pre_num']

        print(data)
    except Exception as e:
        print("--data-->", data)
        print("--Exception-->", str(e))
    print('--------------------------test--------------------------------')

    ewe_id = data['ewe_id']
    # pageNum = int(request.form.get('pageNum'))
    ram_id = data['ram_id']

    birth = data['delivery_date']

    # 构造查询条件
    conditions = []
    conditions.append(EBreedLambinfo.tobasic != 1)
    if ewe_id:
        conditions.append(EBreedLambinfo.mother_id == ewe_id)
    if ram_id:
        conditions.append(EBreedLambinfo.father_id == ram_id)
    if birth:
        conditions.append(EBreedLambinfo.birth == birth)

    # 查询数据库，获取符合条件的记录
    deleted_lambs = EBreedLambinfo.query.filter(and_(*conditions)).delete()

    print(f'删除了{deleted_lambs}条记录')

    # 插入新的草籽数据
    lamb_data = []
    delivery_date = datetime.strptime(data['delivery_date'], '%Y-%m-%d')
    delivery_date_str = delivery_date.strftime('%Y%m%d')
    ewe = db.session.query(BasicBasicinfo).filter_by(id=ewe_id).first()
    ram = db.session.query(BasicBasicinfo).filter_by(id=ram_id).first()

    # 获取父母耳号及品种信息
    m_pre_num = ewe.pre_num if ewe else None
    m_ele_num = ewe.ele_num if ewe else None
    variety = ewe.variety if ewe else None

    f_pre_num = ram.pre_num if ram else None
    f_ele_num = ram.ele_num if ram else None

    for i in range(1, int(data['live_num']) + 1):
        logo = f"{m_ele_num}_{delivery_date_str}_{i}"
        lamb = {
            'breeding_id': data['breeding_id'],
            'tobasic': 0,
            'logo': logo,
            'pre_num': data.get(f'pre_num_{i}'),
            'variety': variety,
            'sex': data.get(f'sex_{i}'),
            'belong': 0,
            'manu_info_id': 0,
            'manu_info_name': '本场扩繁',
            'state': data.get(f'state_{i}'),
            'birth': delivery_date,
            'bir_weight': data.get(f'bir_weight_{i}'),
            'mother_id': ewe_id,
            'father_id': ram_id,
            'f_ele_num': f_ele_num,
            'f_pre_num': f_pre_num,
            'm_ele_num': m_ele_num,
            'm_pre_num': m_pre_num,
            'color': data.get(f'color_{i}'),
            'rank': data.get(f'rank_{i}'),
            'f_staff': data.get('f_staff'),
            'f_date': data.get('f_date'),
        }
        lamb_data.append(lamb)

    if lamb_data:
        try:
            for lamb in lamb_data:
                lambinfo = EBreedLambinfo()
                for key, value in lamb.items():
                    setattr(lambinfo, key, value)
                db.session.add(lambinfo)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            result = {
                "code": 500,
                "msg": f'添加草籽信息失败 {str(e)}'
            }
            return jsonify(result)

    # 删除多余的数据
    live_num = int(data['live_num'])
    for i in range(1, live_num + 1):
        for key in [f'pre_num_{i}', f'sex_{i}', f'state_{i}', f'bir_weight_{i}', f'color_{i}', f'rank_{i}']:
            data.pop(key, None)

    print(data)
    # 更新主表数据
    try:
        EBreedPostnatalinfo.query.filter_by(id=id).update(data)
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
    #     EBreedPostnatalinfo.query.filter_by(id=id).update(data)
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


@e_breed.route('/e_breed/postnatalinfo/export', methods=['POST'])
def export_postnatalinfo():
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
            postnatal_info = (
                db.session.query(
                    EBreedPostnatalinfo,
                    ewe_info.ele_num.label("ewe_ele_num"),
                    ewe_info.pre_num.label("ewe_pre_num"),
                    ram_info.ele_num.label("ram_ele_num"),
                    ram_info.pre_num.label("ram_pre_num")
                )
                    .outerjoin(EBreedBreedinginfo, EBreedBreedinginfo.id == EBreedPostnatalinfo.breeding_id)
                    .outerjoin(ewe_info, ewe_info.id == EBreedBreedinginfo.ewe_id)
                    .outerjoin(ram_info, ram_info.id == EBreedBreedinginfo.ram_id)
                    .filter(EBreedPostnatalinfo.id.in_(selected_ids))
                    .all()
            )
        else:
            postnatal_info = (
                db.session.query(
                    EBreedPostnatalinfo,
                    ewe_info.ele_num.label("ewe_ele_num"),
                    ewe_info.pre_num.label("ewe_pre_num"),
                    ram_info.ele_num.label("ram_ele_num"),
                    ram_info.pre_num.label("ram_pre_num")
                )
                    .outerjoin(EBreedBreedinginfo, EBreedBreedinginfo.id == EBreedPostnatalinfo.breeding_id)
                    .outerjoin(ewe_info, ewe_info.id == EBreedBreedinginfo.ewe_id)
                    .outerjoin(ram_info, ram_info.id == EBreedBreedinginfo.ram_id)
                    .all()
            )

        data_list = []
        for info, ewe_ele_num, ewe_pre_num, ram_ele_num, ram_pre_num in postnatal_info:
            Ewe_healthType_value = Ewe_healthType.get(info.ewe_health, info.ewe_health)
            Ewe_conditionType_value = Ewe_conditionType.get(info.ewe_condition, info.ewe_condition)
            data_list.append({
                '受体草地编号': ewe_ele_num,
                '受体地块编号': ewe_pre_num,
                '供体草地编号': ram_ele_num,
                '供体地块编号': ram_pre_num,
                '传播日期': info.breeding_date.isoformat() if info.breeding_date else None,
                '发病日期': info.delivery_date.isoformat() if info.delivery_date else None,
                '受体感染率': info.Booroola,
                '受体健康情况': Ewe_healthType_value,
                '受体状态': Ewe_conditionType_value,
                '感染数量': info.live_num,
                '记录人员': info.birth_attendants,
                '创建时间': info.f_date.isoformat() if info.f_date else None,
                '创建人员': info.f_staff
            })
        df = pd.DataFrame(data_list)

        export_path = os.path.join(os.getcwd(), 'App', 'e_breed', 'export_excel', 'postnatal_info.xlsx')
        df.to_excel(export_path, index=False)

        return send_file(export_path, as_attachment=True)
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'导出失败 {str(e)}'})

#获取月龄12以上的健康未销售的基础草地记录(在生长记录是12月，在生长监测和培育时8月)，，，，，，，，，改成6月和11月了
@e_breed.route('/e_breed/postnatalinfo/get_ewe', methods=['POST'])
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
@e_breed.route('/e_breed/postnatalinfo/get_ram', methods=['POST'])
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


@e_breed.route('/e_breed/postnatalinfo/getlamb', methods=['POST'])#回显生长记录中新草地
def get_lamb():
    ewe_id = request.json.get('ewe_id')
    # pageNum = int(request.form.get('pageNum'))
    ram_id = request.json.get('ram_id')

    birth = request.json.get('delivery_date')

    # 构造查询条件
    conditions = []
    if ewe_id:
        conditions.append(EBreedLambinfo.mother_id == ewe_id)
    if ram_id:
        conditions.append(EBreedLambinfo.father_id == ram_id)
    if birth:
        conditions.append(EBreedLambinfo.birth == birth)

    # 查询数据库，获取符合条件的记录
    infos = EBreedLambinfo.query.filter(and_(*conditions)).all()

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
@e_breed.route('/e_breed/postnatalinfo/search_ewe_sheep', methods=['POST'])
def search_ewe_sheep():
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
        return jsonify({"code": 400, "msg": "未找到对应的电子耳号信息"})

    # 获取对应的 ewe_id
    ewe_id = basic_info.id

    # 将分娩日期 d_date 转换为 datetime 对象
    delivery_date = datetime.strptime(d_date, "%Y-%m-%d")

    # 将分娩日期往前推六个月
    pre_date = delivery_date - timedelta(days=7 * 30)  # 近似六个月，30天为一个月，后面改成七个月了

    # 查询 EBreedBreedinginfo 表，查找对应 ewe_id 并且 breeding_date 大于等于 pre_date（分娩往前推六个月，一株作物从培育到收获大约150天） 的记录
    breeding_info = EBreedBreedinginfo.query.filter(
        EBreedBreedinginfo.ewe_id == ewe_id,
        EBreedBreedinginfo.breeding_date >= pre_date
    ).order_by(EBreedBreedinginfo.breeding_date.desc()).first()  # 排序后取最近的一条记录

    # 新增的条件查询，在EBreedPostnatalinfo里面，在pre_date日期之后没有ewe_id的记录
    # 保证一条生长记录对应一条培育记录
    postnatal_check = EBreedPostnatalinfo.query.filter(
        EBreedPostnatalinfo.ewe_id == ewe_id,
        EBreedPostnatalinfo.f_date >= pre_date
    ).first()
    if postnatal_check:
        return jsonify({"code": 400, "msg": "在对应培育记录之后已有生长记录，请勿重复添加生长信息"})

    if breeding_info:
        # 找到与 ewe_id 相关的 ram_id
        ram_id = breeding_info.ram_id

        # 获取 ram_id 对应的 ele_num（ram_id 是 BasicBasicinfo 表中的 id）
        ram_info = BasicBasicinfo.query.filter_by(id=ram_id).first()

        if ram_info:
            ram_ele_num = ram_info.ele_num
        else:
            ram_ele_num = None
        print(ram_ele_num)
        # 如果有符合条件的记录，返回成功的响应
        result = {
            "code": 200,
            "msg": '成功',
            "data": {
                "ram_ele_num": ram_ele_num   # 返回供体（公草地）的 ele_num
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
@e_breed.route('/e_breed/postnatalinfo/add_breeding', methods=['POST'])
def add_breeding():
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
    ram_ele_num = data.get('ram_ele_num')
    ram_pre_num = data.get('ram_pre_num')
    # variety = data.get('variety')
    variety_label = data.get('variety')  # 前端传递的文字品种
    delivery_date = data.get('delivery_date')
    ewe_ele_num = data.get('ewe_ele_num')

    # 将品种文字转换为对应的数字
    variety = next((item['value'] for item in variety_type if item['label'] == variety_label), None)

    # 校验数据
    if not all([ram_ele_num, ram_pre_num, variety_label, delivery_date, ewe_ele_num]):
        result = {
            "code": 400,
            "msg": "输入参数缺失"}
        return jsonify(result)


    # 查找供体和受体田块信息
    ram_info = BasicBasicinfo.query.filter_by(ele_num=ram_ele_num).first()
    ewe_info = BasicBasicinfo.query.filter_by(ele_num=ewe_ele_num).first()

    if not ram_info or not ewe_info:
        result = {
            "code": 400,
            "msg": "未找到对应的供体或受体田块信息"}
        return jsonify(result)

    # 计算所需字段
    ram_id = ram_info.id
    ewe_id = ewe_info.id
    ewe_variety = ewe_info.variety
    ram_variety = variety
    pre_production_date = delivery_date
    breeding_date = (datetime.strptime(delivery_date, "%Y-%m-%d") - timedelta(days=150)).strftime("%Y-%m-%d")#往前推180改成150
    f_date = delivery_date

    # 创建培育信息对象
    breeding_data = {
        "breeding_date": breeding_date,
        "pre_production_date": pre_production_date,
        "breeding_way": 0,  # 默认值
        "ram_id": ram_id,
        "ram_variety": ram_variety,
        "ewe_id": ewe_id,
        "ewe_variety": ewe_variety,
        "breeding_state": 1,  # 默认值
        "staff": None,
        "f_staff": None,
        "f_date": f_date,
        "belong": 0,  # 默认值
        "mat_period": 12,
        "single_ok": None
    }

    # 创建新的培育记录
    breedinginfo = EBreedBreedinginfo()

    # 将数据填充到培育记录
    for key, value in breeding_data.items():
        setattr(breedinginfo, key, value)

    # 保存到数据库
    try:
        db.session.add(breedinginfo)
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
@e_breed.route('/e_breed/postnatalinfo/add', methods=['POST'])
def add_postnatalinfo():
    data = request.get_json()
    print("+++++++++++")
    print(data)
    ctime = datetime.now()
    data['belong'] = 0
    data['f_date'] = ctime



    # 根据 ewe_ele_num 和 ram_ele_num 查找对应的 BasicBasicinfo 表中的 id
    ewe_ele_num = data.get('ewe_ele_num')
    ram_ele_num = data.get('ram_ele_num')

    # 在填写生长记录时添加一条监测记录
    pre_data = {}
    live_num = data.get('live_num')  # 要添加到备注信息里面的胎数
    pre_data['check_type'] = 'B超'
    pre_data['In_pregnancy'] = '怀孕'
    pre_data['f_staff'] = data.get('f_staff')
    pre_data['notes'] = f'共有{live_num}胎'
    pre_data['belong'] = 0

    pregnant_info = EBreedPregnantinfo()

    ewe = db.session.query(BasicBasicinfo).filter_by(ele_num=ewe_ele_num).first()
    if ewe:
        data['ewe_id'] = ewe.id  # 将 ewe_id 设置为查找到的 id
    else:
        return jsonify({"code": 404, "msg": "未找到对应的 ewe_ele_num"}), 404

    # 查找 ram_ele_num 对应的 id
    ram = db.session.query(BasicBasicinfo).filter_by(ele_num=ram_ele_num).first()
    if ram:
        data['ram_id'] = ram.id  # 将 ram_id 设置为查找到的 id
    else:
        return jsonify({"code": 404, "msg": "未找到对应的 ram_ele_num"}), 404

    # 删除 ewe_ele_num 和 ram_ele_num 不需要存入数据库
    data.pop('ewe_ele_num', None)
    data.pop('ram_ele_num', None)

    # 假设 delivery_date 是从前端传来的字符串，比如 '2024-12-01'
    delivery_date_str = data.get('delivery_date')  # 取前端传过来的分娩日期
    delivery_date = datetime.strptime(delivery_date_str, '%Y-%m-%d')  # 转换为 datetime 对象


    # 将交配日期往前推六个月
    pre_date = delivery_date - timedelta(days=7 * 30)  # 近似六个月，30天为一个月，改成五个月
    breeding_info = db.session.query(EBreedBreedinginfo).filter(
        EBreedBreedinginfo.ewe_id == data['ewe_id'],  # 查找符合 ewe_id 的记录
        EBreedBreedinginfo.breeding_date >= pre_date  # 查找 breeding_date 大于等于 pre_date（这个日期是分娩日期往前推六个月的日期） 的记录
    ).order_by(EBreedBreedinginfo.breeding_date.desc()).first()  # 按照 breeding_date 降序排序，取最新的一条记录

    # 判断是否找到了符合条件的记录
    if breeding_info:
        # 找到对应的培育记录后返回 id
        data['breeding_id'] = breeding_info.id
        # 在生长记录里面添加培育信息id的同时在监测记录里面也添加
        pre_data['breeding_id'] = breeding_info.id
        # 获取breeding_info中的breeding_date
        breeding_date = breeding_info.breeding_date
        # 使用timedelta来表示时间间隔，这里是两个星期，也就是14天
        two_weeks_later = breeding_date + timedelta(days=14)
        # 将计算后的日期赋值给pre_data['f_date']
        pre_data['f_date'] = two_weeks_later  # 至此，孕检信息的字段全部获取完成

    else:
        return jsonify({"code": 404, "msg": "未找到符合条件的培育记录"}), 404


    # 其实下面这些breeding_date好像都不用写，直接拿就行，因为在上面添加培育信息步骤里已经弄了，但是我忘了这块是不是这么写的逻辑了，所以不删了
    # 使用 timedelta 将日期往前推180天（假设6个月为180天）。。。。。。。。。。。。。。。。。。。。改成推150天
    breeding_date = delivery_date - timedelta(days=150)

    # 将 breeding_date 转回字符串格式，如果需要的话
    breeding_date_str = breeding_date.strftime('%Y-%m-%d')

    # 将计算出来的 breeding_date 填入数据字典
    data['breeding_date'] = breeding_date_str

    # 插入数据到 EBreedPostnatalinfo 表
    postnatalinfo = EBreedPostnatalinfo()

    #  插入数据到EBreedPregnantinfo中
    pregnant_info = EBreedPregnantinfo()

    for key, value in data.items():
        setattr(postnatalinfo, key, value)

    for key, value in pre_data.items():
        setattr(pregnant_info, key, value)

    try:
        db.session.add(pregnant_info)
        db.session.add(postnatalinfo)
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
    lamb_data = []
    for i in range(1, int(data['live_num']) + 1):  # 根据 live_num 确定需要处理的草籽数量
        # 生成 logo 字段
        logo = f"{ewe_ele_num}_{delivery_date_str}_{i}"

        # 从 BasicBasicinfo 中查找父母的防疫耳号
        ewe = db.session.query(BasicBasicinfo).filter_by(id=data['ewe_id']).first()
        ram = db.session.query(BasicBasicinfo).filter_by(id=data['ram_id']).first()
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
            print(f"未找到母草地（ewe_id: {data['ewe_id']}）的地块编号")

        if ram:
            f_pre_num = ram.pre_num  # 父草的地块编号
            f_ele_num = ram.ele_num
        else:
            f_pre_num = None
            f_ele_num = None
            # 可以添加异常处理或返回错误
            print(f"未找到父草（ram_id: {data['ram_id']}）的地块编号")
        lamb = {
            'breeding_id': data['breeding_id'],
            'tobasic': 0,
            'logo': logo,
            'pre_num': data.get(f'pre_num_{i}'),
            'variety': variety,
            'sex': data.get(f'sex_{i}'),
            'belong': 0,
            'manu_info_id': 0,
            'manu_info_name': '本场扩繁',
            'state': data.get(f'state_{i}'),
            'birth':delivery_date,
            'bir_weight': data.get(f'bir_weight_{i}'),
            'mother_id': data['ewe_id'],  # 关联母草地的 ewe_id
            'father_id':data['ram_id'],
            'f_ele_num': f_ele_num,
            'f_pre_num': f_pre_num,
            'm_ele_num': m_ele_num,
            'm_pre_num': m_pre_num,
            'color': data.get(f'color_{i}'),
            'rank': data.get(f'rank_{i}'),

            'f_staff': data.get('f_staff'),  # 如果有其他通用字段，也可以在此添加
            'f_date': data.get('f_date'),
            # 'birth_attendants': data.get('birth_attendants')  # 可以继续添加其他字段
        }
        lamb_data.append(lamb)

    # 插入草籽数据到 EBreedLambinfo 表
    if lamb_data:
        try:
            for lamb in lamb_data:
                lambinfo = EBreedLambinfo()
                for key, value in lamb.items():
                    setattr(lambinfo, key, value)
                db.session.add(lambinfo)
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
@e_breed.route('/e_breed/pregnantinfo', methods=['POST'])
def get_pregnantinfo():
    pageNum = int(request.json.get('pageNum'))
    # pageNum = int(request.form.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        # 'ele_num': EBreedPregnantinfo.breeding_id,
        # 'pre_num': EBreedPregnantinfo.breeding_id,
        'breeding_id': EBreedPregnantinfo.breeding_id,#这个是查询条件要和你传递的值对比的
        'ewe_ele_num': EBreedPregnantinfo.breeding_id,
        'ewe_pre_num': EBreedPregnantinfo.breeding_id,
        'check_type': EBreedPregnantinfo.check_type,
        'In_pregnancy': EBreedPregnantinfo.In_pregnancy,
        'notes': EBreedPregnantinfo.notes,
        'belong': EBreedPregnantinfo.belong,
        'f_staff': EBreedPregnantinfo.f_staff,
        'f_date': EBreedPregnantinfo.f_date,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'f_date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))

            elif param == 'ewe_ele_num':#如果是查电子耳号，首先要查基本信息表里面，获取这个电子耳号的id
                basic_id = BasicBasicinfo.query.filter(
                        BasicBasicinfo.ele_num.like(f'%{value}%')).first().id
                print(basic_id)
                breeding_info = EBreedBreedinginfo.query.filter_by(ewe_id=basic_id).first()#然后再从培育信息表里找到这条培育记录
                print('------------------------')
                print(breeding_info)
                if breeding_info:
                    breeding_id = breeding_info.id
                    print(breeding_id)
                    pregnant_info = EBreedPregnantinfo.query.filter_by(breeding_id=breeding_id).first()#通过培育信息表里的id获取监测表的id，然后对比孕检表中有没有这条breeding_id，把这个作为搜索条件
                    print(pregnant_info)                                                                  #这么写好像逻辑上写复杂了，算了，小脑萎缩了，不想了，反正能跑出来
                    conditions.append(column == pregnant_info.breeding_id)
            elif param == 'ewe_pre_num':
                basic_id = BasicBasicinfo.query.filter(
                        BasicBasicinfo.pre_num.like(f'%{value}%')).first().id
                print(basic_id)
                # 通过breeding_id查找ewe_id
                breeding_info = EBreedBreedinginfo.query.filter_by(ewe_id=basic_id).first()
                print('------------------------')
                print(breeding_info)
                if breeding_info:
                    breeding_id = breeding_info.id
                    print(breeding_id)
                    # 查找BasicBasicinfo中的ele_num或pre_num
                    pregnant_info = EBreedPregnantinfo.query.filter_by(breeding_id=breeding_id).first()
                    print(pregnant_info)
                    conditions.append(column == pregnant_info.breeding_id)
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = EBreedPregnantinfo.query.filter(and_(*conditions))
    else:
        query = EBreedPregnantinfo.query  # 如果没有条件，查询所有

    # 筛选出没有被移除的草(状态-1)和没有枯萎的草(状态0)
    # 并且根据id降序排列

    # 并且根据id降序排列

    query = query.filter(EBreedPregnantinfo.belong == 0)
    infos = query.order_by(desc(EBreedPregnantinfo.id)).paginate(page=pageNum, per_page=pageSize,
                                                                  error_out=False)
    total = query.count()

    list = []
    for info in infos:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        data = json.loads(data)
        breeding_info = EBreedBreedinginfo.query.filter_by(id=data['breeding_id']).first()
        if breeding_info:
            ewe_id = breeding_info.ewe_id
            # 查找BasicBasicinfo中的ele_num或pre_num
            basic_info = BasicBasicinfo.query.filter_by(id=ewe_id).first()
            if basic_info:
                data['ewe_ele_num'] = basic_info.ele_num
                data['ewe_pre_num'] = basic_info.pre_num
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

@e_breed.route('/e_breed/pregnantinfo/del', methods=['POST'])
def del_pregnantinfo():
    ids = request.get_json()
    print("______________________________________")
    print(ids)
    for i in ids:
        EBreedPregnantinfo.query.filter_by(id=i).delete()
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

@e_breed.route('/e_breed/pregnantinfo/edit', methods=['POST'])
def edit_pregnantinfo():
    data = request.get_json()
    print("--data-->", data)
    id = data['id']
    # ele_id = data['ele_num']
    # pre_id = data['pre_num']
    try:
        if 'ewe_ele_num' in data:

            del data['ewe_ele_num']
        if 'ewe_pre_num' in data:

            del data['ewe_pre_num']


    except Exception as e:
        print("--data-->", data)
        print("--Exception-->", str(e))
    print('--------------------------test--------------------------------')

    # BasicBasicinfo.query.filter_by(ele_id = ele_id,pre_id = pre_id).update(data)
    try:
        EBreedPregnantinfo.query.filter_by(id=id).update(data)
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

@e_breed.route('/e_breed/pregnantinfo/add', methods=['POST'])
def add_pregnantinfo():
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
    # ewe_id = BasicBasicinfo.query.filter_by(ele_num=data['ewe_ele_num']).first().id
    # breeding_id = EBreedBreedinginfo.filter_by(ewe_id=ewe_id).first().id
    #
    # data['basic_id'] =basic_id
    # print(data)

    pregnantinfo= EBreedPregnantinfo()

    for key, value in data.items():
        setattr(pregnantinfo, key, value)
    try:
        db.session.add(pregnantinfo)
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

@e_breed.route('/e_breed/pregnantinfo/export', methods=['POST'])
def export_pregnantinfo():
    try:
        selected_ids = request.get_json()

        if selected_ids:
            pregnant_info = (
                db.session.query(EBreedPregnantinfo, BasicBasicinfo.ele_num, BasicBasicinfo.pre_num)
                    .outerjoin(EBreedBreedinginfo, EBreedBreedinginfo.id == EBreedPregnantinfo.breeding_id)
                    .outerjoin(BasicBasicinfo, BasicBasicinfo.id == EBreedBreedinginfo.ewe_id)
                    .filter(EBreedPregnantinfo.id.in_(selected_ids))
                    .all()
            )
        else:
            pregnant_info = (
                db.session.query(EBreedPregnantinfo, BasicBasicinfo.ele_num, BasicBasicinfo.pre_num)
                    .outerjoin(EBreedBreedinginfo, EBreedBreedinginfo.id == EBreedPregnantinfo.breeding_id)
                    .outerjoin(BasicBasicinfo, BasicBasicinfo.id == EBreedBreedinginfo.ewe_id)
                    .all()
            )

        data_list = []
        for info, ele_num, pre_num in pregnant_info:
            data_list.append({
                '受体草地编号': ele_num,
                '受体地块编号': pre_num,
                '检查类别': info.check_type,
                '孕检信息': info.In_pregnancy,
                '创建时间': info.f_date.isoformat() if info.f_date else None,
                '创建人员': info.f_staff,
                '备注': info.notes,
            })
        df = pd.DataFrame(data_list)

        export_path = os.path.join(os.getcwd(), 'App', 'e_breed', 'export_excel', 'pregnant_info.xlsx')
        df.to_excel(export_path, index=False)

        return send_file(export_path, as_attachment=True)
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'导出失败 {str(e)}'})

#养护记录信息
@e_breed.route('/e_breed/artificialfeedinginfo', methods=['POST'])
def get_artificialfeedinginfo():
    pageNum = int(request.json.get('pageNum'))
    # pageNum = int(request.form.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        'lamb_id': EBreedArtificialfeedinginfo.lamb_id,
        'ele_num':EBreedArtificialfeedinginfo.lamb_id,
        'pre_num': EBreedArtificialfeedinginfo.lamb_id,
        'delivery_date':EBreedArtificialfeedinginfo.delivery_date,
        'BW': EBreedArtificialfeedinginfo.BW,
        'reason': EBreedArtificialfeedinginfo.reason,
        'feeding_material': EBreedArtificialfeedinginfo.feeding_material,
        'mcal': EBreedArtificialfeedinginfo.mcal,
        'health': EBreedArtificialfeedinginfo.health,
        'help': EBreedArtificialfeedinginfo.help,
        'dose': EBreedArtificialfeedinginfo.dose,
        'feeding_staff': EBreedArtificialfeedinginfo.feeding_staff,
        'belong': EBreedRutinfo.belong,
        'f_staff': EBreedRutinfo.f_staff,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'f_date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            elif param == 'ele_num':
                lamb_id = EBreedLambinfo.query.filter(
                    EBreedLambinfo.ele_num.like(f'%{value}%')).first().id
                conditions.append(column == lamb_id)
            elif param == 'pre_num':
                lamb_id = EBreedLambinfo.query.filter(
                    EBreedLambinfo.pre_num.like(f'%{value}%')).first().id
                conditions.append(column == lamb_id)
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = EBreedArtificialfeedinginfo.query.filter(and_(*conditions))
    else:
        query = EBreedArtificialfeedinginfo.query  # 如果没有条件，查询所有

    # 筛选出没有被移除的草(状态-1)和没有枯萎的草(状态0)
    # 并且根据id降序排列

    # 并且根据id降序排列

    query = query.filter(EBreedArtificialfeedinginfo.belong == 0)
    infos = query.order_by(desc(EBreedArtificialfeedinginfo.id)).paginate(page=pageNum, per_page=pageSize,
                                                                  error_out=False)
    total = query.count()

    list = []
    for info in infos:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        data = json.loads(data)
        lamb_info = EBreedLambinfo.query.filter_by(id=data['lamb_id']).first()
        print(lamb_info)
        print(lamb_info.ele_num)
        print(lamb_info.pre_num)
        if lamb_info:
            data['ele_num'] = lamb_info.ele_num
            data['pre_num'] = lamb_info.pre_num
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

@e_breed.route('/e_breed/artificialfeedinginfo/del', methods=['POST'])
def del_artificialfeedinginfo():
    ids = request.get_json()
    print("______________________________________")
    print(ids)
    for i in ids:
        EBreedArtificialfeedinginfo.query.filter_by(id=i).delete()
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

@e_breed.route('/e_breed/artificialfeedinginfo/edit', methods=['POST'])
def edit_artificialfeedinginfo():
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
        EBreedArtificialfeedinginfo.query.filter_by(id=id).update(data)
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

@e_breed.route('/e_breed/artificialfeedinginfo/add', methods=['POST'])
def add_artificialfeedinginfo():
    data = request.get_json()
    #去除剂量两端的空格
    # if 'dose' in data:
    #     data['dose'] = data['dose'].strip()
    #     print(data['dose'])

    ctime = datetime.now()
    data['belong'] = 0
    data['f_date'] = ctime



    # 查询对应的 id
    lamb_id = EBreedLambinfo.query.filter_by(ele_num=data['ele_num']).first().id

    data['lamb_id'] =lamb_id
    print(data)

    artificialfeedinginfo= EBreedArtificialfeedinginfo()

    for key, value in data.items():
        setattr(artificialfeedinginfo, key, value)
    try:
        db.session.add(artificialfeedinginfo)
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

@e_breed.route('/e_breed/artificialfeedinginfo/export', methods=['POST'])
def export_artificialfeedinginfo():
    try:
        selected_ids = request.get_json()

        if selected_ids:
            artificialfeeding_info = (
                db.session.query(EBreedArtificialfeedinginfo, EBreedLambinfo.ele_num, EBreedLambinfo.pre_num)
                    .outerjoin(EBreedLambinfo, EBreedLambinfo.id == EBreedArtificialfeedinginfo.lamb_id)
                    .filter(EBreedArtificialfeedinginfo.id.in_(selected_ids))
                    .all()
            )
        else:
            artificialfeeding_info = (
                db.session.query(EBreedArtificialfeedinginfo, EBreedLambinfo.ele_num, EBreedLambinfo.pre_num)
                    .outerjoin(EBreedLambinfo, EBreedLambinfo.id == EBreedArtificialfeedinginfo.lamb_id)
                    .all()
            )

        data_list = []
        for info, ele_num, pre_num in artificialfeeding_info:
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

        export_path = os.path.join(os.getcwd(), 'App', 'e_breed', 'export_excel', 'artificialfeeding_info.xlsx')
        df.to_excel(export_path, index=False)

        return send_file(export_path, as_attachment=True)
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'导出失败 {str(e)}'})


#成坪记录信息
@e_breed.route('/e_breed/weaninginfo', methods=['POST'])
def get_weaninginfo():
    pageNum = int(request.json.get('pageNum'))
    # pageNum = int(request.form.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        'lamb_id': EBreedWeaninginfo.lamb_id,
        'lamb_ele_num':EBreedWeaninginfo.lamb_id,
        'lamb_pre_num':EBreedWeaninginfo.lamb_id,
        'logo': EBreedWeaninginfo.lamb_id,
        'Delivery_date':EBreedWeaninginfo.Delivery_date,
        'feeding_way': EBreedWeaninginfo.feeding_way,
        'Bir_weight': EBreedWeaninginfo.Bir_weight,
        'wea_weight': EBreedWeaninginfo.wea_weight,
        'rank': EBreedWeaninginfo.rank,
        # '': EBreedWeaninginfo,
        'belong': EBreedRutinfo.belong,
        'f_staff': EBreedRutinfo.f_staff,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'Delivery_date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            elif param == 'lamb_ele_num':
                lamb_id = EBreedLambinfo.query.filter(
                    EBreedLambinfo.ele_num.like(f'%{value}%')).first().id
                conditions.append(column == lamb_id)
            elif param == 'lamb_pre_num':
                lamb_id = EBreedLambinfo.query.filter(
                    EBreedLambinfo.pre_num.like(f'%{value}%')).first().id
                conditions.append(column == lamb_id)
            elif param == 'logo':
                lamb_id = EBreedLambinfo.query.filter(
                    EBreedLambinfo.logo.like(f'%{value}%')).first().id
                conditions.append(column == lamb_id)
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = EBreedWeaninginfo.query.filter(and_(*conditions))
    else:
        query = EBreedWeaninginfo.query  # 如果没有条件，查询所有

    # 筛选出没有被移除的草(状态-1)和没有枯萎的草(状态0)
    # 并且根据id降序排列

    # 并且根据id降序排列

    query = query.filter(EBreedWeaninginfo.belong == 0)
    infos = query.order_by(desc(EBreedWeaninginfo.id)).paginate(page=pageNum, per_page=pageSize,
                                                                  error_out=False)
    total = query.count()

    list = []
    for info in infos:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        data = json.loads(data)
        lamb_info = EBreedLambinfo.query.filter_by(id=data['lamb_id']).first()
        if lamb_info:
            data['lamb_ele_num'] = lamb_info.ele_num
            data['lamb_pre_num'] = lamb_info.pre_num
            data['logo'] = lamb_info.logo
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

@e_breed.route('/e_breed/weaninginfo/del', methods=['POST'])
def del_weaninginfo():
    ids = request.get_json()
    print("______________________________________")
    print(ids)
    for i in ids:
        EBreedWeaninginfo.query.filter_by(id=i).delete()
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

@e_breed.route('/e_breed/weaninginfo/edit', methods=['POST'])
def edit_weaninginfo():
    data = request.get_json()
    print("--data-->", data)
    id = data['id']
    # ele_id = data['ele_num']
    # pre_id = data['pre_num']

    lamb_info = EBreedLambinfo.query.filter_by(pre_num=data['lamb_pre_num']).first()
    lamb_pre_num = lamb_info.pre_num
    # lamb_id = EBreedLambinfo.query.filter_by(pre_num=data['lamb_pre_num']).first().id

    # data['lamb_id'] =lamb_id
    try:
        if 'lamb_ele_num' in data:

            del data['lamb_ele_num']
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
        lamb_info.wea_weight = data.get('wea_weight')
        lamb_info.wea_date = data.get('Delivery_date')
        lamb_info.bir_weight = data.get('Bir_weight')
        # 更新BasicBasicinfo的wea_weight和wea_date等字段
        basic_info = BasicBasicinfo.query.filter_by(pre_num=lamb_pre_num).first()

        print(basic_info)
        if basic_info:
            basic_info.wea_weight = data.get('wea_weight')
            basic_info.wea_date = data.get('Delivery_date')
            basic_info.bir_weight = data.get('Bir_weight')
        EBreedWeaninginfo.query.filter_by(id=id).update(data)
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

@e_breed.route('/e_breed/weaninginfo/add', methods=['POST'])
def add_weaninginfo():
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
    lamb_info = EBreedLambinfo.query.filter_by(pre_num=data['lamb_pre_num']).first()
    lamb_id = EBreedLambinfo.query.filter_by(pre_num=data['lamb_pre_num']).first().id

    data['lamb_id'] =lamb_id
    print(data)

    weaninginfo= EBreedWeaninginfo()

    for key, value in data.items():
        setattr(weaninginfo, key, value)
    try:
        # 更新EbreedLambinfo的wea_weight、wea_date字段
        lamb_info.wea_weight = data.get('wea_weight')
        lamb_info.wea_date = data.get('Delivery_date')
        lamb_info.bir_weight = data.get('Bir_weight')
        # 更新BasicBasicinfo的wea_weight和wea_date字段
        basic_info = BasicBasicinfo.query.filter_by(pre_num=data['lamb_pre_num']).first()
        if basic_info:
            basic_info.wea_weight = data.get('wea_weight')
            basic_info.wea_date = data.get('Delivery_date')
            basic_info.bir_weight = data.get('Bir_weight')
        db.session.add(weaninginfo)
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

@e_breed.route('/e_breed/weaninginfo/export', methods=['POST'])
def export_weaninginfo():
    try:
        selected_ids = request.get_json()
        Feeding_wayType = {
            0: "自然养护",
            1: "人工养护"
        }
        WeaningRankType = {
            0: "特级",
            1: "一级",
            2: "二级",
            3: "三级",
            9: "未评级"
        }

        if selected_ids:
            weaning_info = (
                db.session.query(EBreedWeaninginfo, EBreedLambinfo.ele_num, EBreedLambinfo.pre_num)
                    .outerjoin(EBreedLambinfo, EBreedLambinfo.id == EBreedWeaninginfo.lamb_id)
                    .filter(EBreedWeaninginfo.id.in_(selected_ids))
                    .all()
            )
        else:
            weaning_info = (
                db.session.query(EBreedWeaninginfo, EBreedLambinfo.ele_num, EBreedLambinfo.pre_num)
                    .outerjoin(EBreedLambinfo, EBreedLambinfo.id == EBreedWeaninginfo.lamb_id)
                    .all()
            )

        data_list = []
        for info, ele_num, pre_num in weaning_info:
            Feeding_wayType_value = Feeding_wayType.get(info.feeding_way, info.feeding_way)
            WeaningRankType_value = WeaningRankType.get(info.rank, info.rank)
            data_list.append({
                '草地编号': ele_num,
                '地块编号': pre_num,
                '成坪日期': info.Delivery_date.isoformat() if info.Delivery_date else None,
                '养护方式': Feeding_wayType_value,
                '出生重': info.Bir_weight,
                '成坪重（出栏体重）': info.wea_weight,
                '成坪评级': WeaningRankType_value,
                '创建人员': info.f_staff
            })
        df = pd.DataFrame(data_list)

        export_path = os.path.join(os.getcwd(), 'App', 'e_breed', 'export_excel', 'weaning_info.xlsx')
        df.to_excel(export_path, index=False)

        return send_file(export_path, as_attachment=True)
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'导出失败 {str(e)}'})

@e_breed.route('/e_breed/weaninginfo/add', methods=['POST'])
def add_weaninginfo_upbasiclamb():
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

    weaninginfo = EBreedWeaninginfo()
    for key, value in data.items():
        setattr(weaninginfo, key, value)
    # 将找到的 basic_id 添加到 EBreedWeaninginfo
    weaninginfo.lamb_id = basic_info.id

    try:
        db.session.add(weaninginfo)
        db.session.commit()
        # 根据 lamb_pre_num 查找 EBreedLambinfo
        lamb_info = EBreedLambinfo.query.filter_by(pre_num=data['lamb_pre_num']).first()
        if not basic_info:
            result = {
                "code": 400,
                "msg": '未找到对应的 BasicBasicinfo 数据'
            }
            return jsonify(result)

        if lamb_info:
            # 更新 EBreedLambinfo 中的 wea_weight
            lamb_info.wea_weight = data['wea_weight']
            db.session.commit()

            # 更新 BasicBasicinfo 中的 Delivery_date 和 wea_weight
            basic_info.wea_date = data['Delivery_date']
            basic_info.wea_weight = data['wea_weight']
            db.session.commit()
        else:
            raise Exception('EBreedLambinfo not found for lamb_pre_num')

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
@e_breed.route('/e_breed/lambinfo', methods=['POST'])
def get_lambinfo():
    pageNum = int(request.json.get('pageNum'))
    # pageNum = int(request.form.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        # 'breeding_id': EBreedLambinfo.breeding_id,
        # 'basic_id': EBreedLambinfo.basic_id,
        'tobasic': EBreedLambinfo.tobasic,
        'logo': EBreedLambinfo.logo,
        'ele_num': EBreedLambinfo.ele_num,
        'pre_num': EBreedLambinfo.pre_num,
        'purpose': EBreedLambinfo.purpose,
        'variety': EBreedLambinfo.variety,
        'sex': EBreedLambinfo.sex,
        'manu_info_id': EBreedLambinfo.manu_info_id,
        'manu_info_name': EBreedLambinfo.manu_info_name,
        'state': EBreedLambinfo.state,
        'birth': EBreedLambinfo.birth,
        'bir_weight': EBreedLambinfo.bir_weight,
        'wea_date': EBreedLambinfo.wea_date,
        'wea_weight': EBreedLambinfo.wea_weight,
        'house_name': EBreedLambinfo.house_name,
        'hurdle_name': EBreedLambinfo.hurdle_name,
        'f_staff': EBreedLambinfo.f_staff,
        'f_date': EBreedLambinfo.f_date,
        'f_ele_num': EBreedLambinfo.father_id,
        'f_pre_num': EBreedLambinfo.father_id,
        'm_ele_num': EBreedLambinfo.mother_id,
        'm_pre_num': EBreedLambinfo.mother_id,
        'gene_a': EBreedLambinfo.gene_a,
        'rank': EBreedLambinfo.rank,
        'color': EBreedLambinfo.color,



        # 'lamb_id': EBreedWeaninginfo.lamb_id,
        # 'Delivery_date':EBreedWeaninginfo.Delivery_date,
        # 'feeding_way': EBreedWeaninginfo.feeding_way,
        # 'Bir_weight': EBreedWeaninginfo.Bir_weight,
        # 'rank': EBreedWeaninginfo.rank,
        # # '': EBreedWeaninginfo,
        # 'belong': EBreedRutinfo.belong,

    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'f_date' or param == 'birth' or param == 'wea_date' :  # 日期需要转换
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
        query = EBreedLambinfo.query.filter(and_(*conditions))
    else:
        query = EBreedLambinfo.query  # 如果没有条件，查询所有

    # 筛选出没有被移除的草(状态-1)和没有枯萎的草(状态0)
    # 并且根据id降序排列

    # 并且根据id降序排列

    query = query.filter(EBreedLambinfo.belong == 0)
    infos = query.order_by(desc(EBreedLambinfo.id)).paginate(page=pageNum, per_page=pageSize,
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
@e_breed.route('/e_breed/lambinfo/NoneWeaning', methods=['POST'])
def get_None_weaning_lambinfo():
    pageNum = int(request.json.get('pageNum'))
    # pageNum = int(request.form.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        # 'breeding_id': EBreedLambinfo.breeding_id,
        # 'basic_id': EBreedLambinfo.basic_id,
        'tobasic': EBreedLambinfo.tobasic,
        'logo': EBreedLambinfo.logo,
        'ele_num': EBreedLambinfo.ele_num,
        'pre_num': EBreedLambinfo.pre_num,
        'purpose': EBreedLambinfo.purpose,
        'variety': EBreedLambinfo.variety,
        'sex': EBreedLambinfo.sex,
        'manu_info_id': EBreedLambinfo.manu_info_id,
        'manu_info_name': EBreedLambinfo.manu_info_name,
        'state': EBreedLambinfo.state,
        'birth': EBreedLambinfo.birth,
        'bir_weight': EBreedLambinfo.bir_weight,
        'wea_date': EBreedLambinfo.wea_date,
        'wea_weight': EBreedLambinfo.wea_weight,
        'house_name': EBreedLambinfo.house_name,
        'hurdle_name': EBreedLambinfo.hurdle_name,
        'f_staff': EBreedLambinfo.f_staff,
        'f_date': EBreedLambinfo.f_date,
        'f_ele_num': EBreedLambinfo.father_id,
        'f_pre_num': EBreedLambinfo.father_id,
        'm_ele_num': EBreedLambinfo.mother_id,
        'm_pre_num': EBreedLambinfo.mother_id,
        'gene_a': EBreedLambinfo.gene_a,
        'rank': EBreedLambinfo.rank,
        'color': EBreedLambinfo.color,



        # 'lamb_id': EBreedWeaninginfo.lamb_id,
        # 'Delivery_date':EBreedWeaninginfo.Delivery_date,
        # 'feeding_way': EBreedWeaninginfo.feeding_way,
        # 'Bir_weight': EBreedWeaninginfo.Bir_weight,
        # 'rank': EBreedWeaninginfo.rank,
        # # '': EBreedWeaninginfo,
        # 'belong': EBreedRutinfo.belong,

    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'f_date' or param == 'birth' or param == 'wea_date' :  # 日期需要转换
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
        query = EBreedLambinfo.query.filter(and_(*conditions))
    else:
        query = EBreedLambinfo.query  # 如果没有条件，查询所有


    # 筛选出没有被移除的草(状态-1)和没有枯萎的草(状态0)
    # 并且根据id降序排列

    # 并且根据id降序排列

    query = query.filter(EBreedLambinfo.belong == 0)
        # 增加筛选条件：排除在 EBreedWeaninginfo 中有记录的草
    weaned_lamb_ids = EBreedWeaninginfo.query.with_entities(EBreedWeaninginfo.lamb_id).subquery()
    query = query.filter(~EBreedLambinfo.id.in_(weaned_lamb_ids))

    infos = query.order_by(desc(EBreedLambinfo.id)).paginate(page=pageNum, per_page=pageSize,
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

@e_breed.route('/e_breed/lambinfo/del', methods=['POST'])
def del_lambinfo():
    ids = request.get_json()
    print("______________________________________")
    print(ids)
    for i in ids:
        EBreedLambinfo.query.filter_by(id=i).delete()
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

@e_breed.route('/e_breed/lambinfo/export', methods=['POST'])
def export_lambinfo():
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
            lamb_info = (
                db.session.query(EBreedLambinfo)
                    .filter(EBreedLambinfo.id.in_(selected_ids))
                    .all()
            )
        else:
            lamb_info = (
                db.session.query(EBreedLambinfo)
                    .all()
            )

        data_list = []
        for info in lamb_info:
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
                '出生体重(Kg)': info.bir_weight,
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

        export_path = os.path.join(os.getcwd(), 'App', 'e_breed', 'export_excel', 'lamb_info.xlsx')
        df.to_excel(export_path, index=False)

        return send_file(export_path, as_attachment=True)
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'导出失败 {str(e)}'})

#添加入库信息tobasic添加记录到基本信息表并修改新草地信息表
@e_breed.route('/e_breed/lambinfo/edit_and_tobasic', methods=['POST'])
def edit_and_tobasic():
    # 入棚自动添加电子耳号
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

        lamb_info = db.session.query(EBreedLambinfo).filter_by(id=data['id']).first()
        print(lamb_info)
        if not lamb_info:
            return jsonify({"code": 404, "msg": "新草地信息未找到"})
        # # 如果没有ele_num，根据pre_num生成ele_num
        # if  lamb_info.ele_num is None:  # 如果ele_num为空
        #     birth_date = lamb_info.birth  # 获取出生日期
        #     variety = data.get('variety') # 获取品种标签
        #     pre_num = lamb_info.pre_num  # 获取防疫耳号
        #     lamb_info.ele_num = generate_ele_num(pre_num, birth_date, variety)  # 根据pre_num、birth和variety生成ele_num
        #     print(lamb_info.ele_num)


        # 更新成坪信息到成坪信息表

        # 检查前端是否传递了 ele_num
        if 'ele_num' in data and data['ele_num']:
            lamb_info.ele_num = data['ele_num']
        else:
            # 如果没有传递 ele_num，根据 pre_num 生成 ele_num
            birth_date = lamb_info.birth  # 获取出生日期
            variety = data.get('variety')  # 获取品种标签
            pre_num = lamb_info.pre_num  # 获取防疫耳号
            lamb_info.ele_num = generate_ele_num(pre_num, birth_date, variety)  # 根据 pre_num、birth 和 variety 生成 ele_num
        print(lamb_info.ele_num)

        wearing_info = db.session.query(EBreedWeaninginfo).filter_by(lamb_id=data['id']).first()

        if wearing_info:
            wearing_info.wea_weight = data.get('wea_weight')
            wearing_info.Delivery_date = data.get('wea_date')
            wearing_info.Bir_weight = data.get('bir_weight')
            db.session.commit()
        # else:
        #     # 创建新的成坪信息记录
        #     new_wearing_info = EBreedWeaninginfo(
        #         lamb_id=data['id'],
        #         wea_weight=data.get('wea_weight'),
        #         Delivery_date=data.get('wea_date'),
        #         Bir_weight=data.get('bir_weight'),
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
            ele_num=lamb_info.ele_num,
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

        # 更新 Ebreedlambinfo 表


        # 更新字段
        lamb_info.basic_id = basic_id  # 更新 basic_id
        lamb_info.belong = data.get('belong')
        lamb_info.tobasic = data.get('tobasic')
        lamb_info.bir_weight = data.get('bir_weight')
        lamb_info.wea_weight = data.get('wea_weight')
        lamb_info.birth = data.get('birth')
        lamb_info.mon_age = round((today - birth_date).days / 30, 1)
        lamb_info.wea_date = data.get('wea_date')
        lamb_info.color = data.get('color')
        lamb_info.ele_num = lamb_info.ele_num
        lamb_info.f_date = data.get('f_date')
        lamb_info.f_ele_num = data.get('f_ele_num')
        lamb_info.f_pre_num = data.get('f_pre_num')
        lamb_info.f_staff = data.get('f_staff')
        lamb_info.father_id = data.get('father_id')
        lamb_info.gene_a = data.get('gene_a')
        lamb_info.house_id = data.get('house_id')
        lamb_info.house_name = data.get('house_name')  # 这里也更新
        lamb_info.hurdle_id = data.get('hurdle_id')
        lamb_info.hurdle_name = data.get('hurdle_name')  # 这里也更新
        lamb_info.logo = data.get('logo')
        lamb_info.m_ele_num = data.get('m_ele_num')
        lamb_info.m_pre_num = data.get('m_pre_num')
        lamb_info.mother_id = data.get('mother_id')
        lamb_info.manu_info_id = data.get('manu_info_id')
        lamb_info.purpose = data.get('purpose')
        lamb_info.rank = data.get('rank')
        lamb_info.sex = data.get('sex')
        lamb_info.state = data.get('state')
        lamb_info.variety = data.get('variety')
        lamb_info.note = data.get('note')  # 如果传递了 note，也可以更新

        # 如果需要可以更新其他字段...

        # 提交更新事务
        db.session.commit()

        # 返回成功响应
        return jsonify({"code": 200, "msg": "信息更新并添加成功"})

    except Exception as e:
        # 如果出现异常，回滚事务并返回错误信息
        db.session.rollback()
        return jsonify({"code": 500, "msg": f"操作失败: {str(e)}"})
