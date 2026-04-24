# views.py: 路由 + 视图函数
import datetime
import random
import os
from flask import Blueprint, render_template, request, make_response, Response, redirect, url_for, session, jsonify, \
    send_file
from sqlalchemy import desc, and_, or_, not_
import pandas as pd

from ..modelsReverse import *
import json
from ..utils.AlchemyEncoder import AlchemyEncoder

d_health = Blueprint('d_health', __name__)


@d_health.route('/d_health/deathinfo', methods=['POST'])  # 绝收信息 后端接口
def get_deathinfo():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        # 'basic_id': DHealthDeathinfo.basic_id,
        'ele_num': DHealthDeathinfo.basic_id,
        'pre_num': DHealthDeathinfo.basic_id,
        'date': DHealthDeathinfo.date,
        'age': DHealthDeathinfo.age,
        'cause': DHealthDeathinfo.cause,
        'harmless_treatment': DHealthDeathinfo.harmless_treatment,
        't_time': DHealthDeathinfo.t_time,
        't_staff': DHealthDeathinfo.t_staff,
        'f_staff': DHealthDeathinfo.f_staff,
        'f_date': DHealthDeathinfo.f_date,
        'notes': DHealthDeathinfo.notes,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'date' or param == 't_time' or param == 'f_date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            elif param == 'ele_num':
                basic_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.ele_num.like(f'%{value}%')).first().id
                conditions.append(column == basic_id)
            elif param == 'pre_num':
                basic_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.pre_num.like(f'%{value}%')).first().id
                conditions.append(column == basic_id)
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = DHealthDeathinfo.query.filter(and_(*conditions))
    else:
        query = DHealthDeathinfo.query  # 如果没有条件，查询所有

    # 并且根据id降序排列

    query = query.filter(DHealthDeathinfo.belong == 0)
    infos = query.order_by(desc(DHealthDeathinfo.id)).paginate(page=pageNum, per_page=pageSize,
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


#卫生管理施药防治
@d_health.route('/d_health/immunizationinfo', methods=['POST'])
def get_immunizationinfo():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        # '': DHealthImmunizationinfo.,
        'basic_id': DHealthImmunizationinfo.basic_id,
        'ele_num': DHealthImmunizationinfo.basic_id,
        'pre_num': DHealthImmunizationinfo.basic_id,
        'imm_date': DHealthImmunizationinfo.imm_date,
        'imm_age': DHealthImmunizationinfo.imm_age,
        'vaccine_id': DHealthImmunizationinfo.vaccine_id,
        'maker_id': DHealthImmunizationinfo.maker_id,

        'cname': DHealthImmunizationinfo.vaccine_id,
        'supplier_name': DHealthImmunizationinfo.maker_id,

        'dose': DHealthImmunizationinfo.dose,
        'anti_level': DHealthImmunizationinfo.anti_level,
        'post_stage': DHealthImmunizationinfo.post_stage,
        'out_time': DHealthImmunizationinfo.out_time,
        'f_date': DHealthImmunizationinfo.f_date,
        'operators': DHealthImmunizationinfo.operators,
        'belong': DHealthImmunizationinfo.belong,
        'f_staff': DHealthImmunizationinfo.f_staff,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'imm_date' or param == 'out_time' or param == 'f_date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            elif param == 'ele_num':
                basic_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.ele_num.like(f'%{value}%')).first().id
                conditions.append(column == basic_id)
            elif param == 'pre_num':
                basic_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.pre_num.like(f'%{value}%')).first().id
                conditions.append(column == basic_id)
            elif param == 'cname':
                vaccine_id = SupplyCommodityinfo.query.filter(
                    SupplyCommodityinfo.cname.like(f'%{value}%')).first().id
                conditions.append(column == vaccine_id)
            elif param == 'supplier_name':
                maker_id = SupplyVSuppliersinfo.query.filter(
                    SupplyVSuppliersinfo.supplier_name.like(f'%{value}%')).first().id
                conditions.append(column == maker_id)
            else:
                conditions.append(column == value)
    # 使用 and_() 组合条件
    if conditions:
        query = DHealthImmunizationinfo.query.filter(and_(*conditions))
    else:
        query = DHealthImmunizationinfo.query  # 如果没有条件，查询所有

    # 并且根据id降序排列

    query = query.filter(DHealthImmunizationinfo.belong == 0)
    infos = query.order_by(desc(DHealthImmunizationinfo.id)).paginate(page=pageNum, per_page=pageSize,
                                                                  error_out=False)
    total = query.count()

    list = []
    for info in infos:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        data = json.loads(data)
        basic_info = BasicBasicinfo.query.filter_by(id=data['basic_id']).first()

        supplycommodityinfo = SupplyCommodityinfo.query.filter_by(id=data['vaccine_id']).first()
        supplyvsuppliersinfo = SupplyVSuppliersinfo.query.filter_by(id=data['maker_id']).first()

        if basic_info:
            data['ele_num'] = basic_info.ele_num
            data['pre_num'] = basic_info.pre_num
        # 有值
        if supplycommodityinfo:
            data['cname'] = supplycommodityinfo.cname
        if supplyvsuppliersinfo:
            data['supplier_name'] = supplyvsuppliersinfo.supplier_name

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


@d_health.route('/d_health/drugbathinfo', methods=['POST'])  # 浸泡施药 后端接口
def get_drugbathinfo():
    print('_______________________________________')
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        # '': DHealthDrugbathinfo.,
        'basic_id': DHealthDrugbathinfo.basic_id,
        'ele_num': DHealthDrugbathinfo.basic_id,
        'pre_num': DHealthDrugbathinfo.basic_id,
        'drug_age': DHealthDrugbathinfo.drug_age,
        'take_time': DHealthDrugbathinfo.take_time,
        'drug_id': DHealthDrugbathinfo.drug_id,
        'vac_maker': DHealthDrugbathinfo.vac_maker,

        'cname': DHealthDrugbathinfo.drug_id,
        'supplier_name': DHealthDrugbathinfo.vac_maker,

        'effect': DHealthDrugbathinfo.effect,
        'timing': DHealthDrugbathinfo.timing,
        'IR_bath': DHealthDrugbathinfo.IR_bath,
        'out_time': DHealthDrugbathinfo.out_time,
        'f_date': DHealthDrugbathinfo.f_date,
        'operators': DHealthDrugbathinfo.operators,
        'belong': DHealthDrugbathinfo.belong,
        'f_staff': DHealthDrugbathinfo.f_staff,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'take_time' or param == 'out_time' or param == 'f_date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            elif param == 'ele_num':
                basic_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.ele_num.like(f'%{value}%')).first().id
                conditions.append(column == basic_id)
            elif param == 'pre_num':
                basic_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.pre_num.like(f'%{value}%')).first().id
                conditions.append(column == basic_id)
            elif param == 'cname':
                drug_id = SupplyCommodityinfo.query.filter(
                    SupplyCommodityinfo.cname.like(f'%{value}%')).first().id
                conditions.append(column == drug_id)
            elif param == 'supplier_name':
                vac_maker = SupplyVSuppliersinfo.query.filter(
                    SupplyVSuppliersinfo.supplier_name.like(f'%{value}%')).first().id
                conditions.append(column == vac_maker)
            else:
                conditions.append(column == value)
    # 使用 and_() 组合条件
    if conditions:
        query = DHealthDrugbathinfo.query.filter(and_(*conditions))
    else:
        query = DHealthDrugbathinfo.query  # 如果没有条件，查询所有

    # 并且根据id降序排列

    query = query.filter(DHealthDrugbathinfo.belong == 0)
    infos = query.order_by(desc(DHealthDrugbathinfo.id)).paginate(page=pageNum, per_page=pageSize,
                                                                  error_out=False)
    total = query.count()

    list = []
    for info in infos:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        data = json.loads(data)
        basic_info = BasicBasicinfo.query.filter_by(id=data['basic_id']).first()

        supplycommodityinfo = SupplyCommodityinfo.query.filter_by(id=data['drug_id']).first()
        supplyvsuppliersinfo = SupplyVSuppliersinfo.query.filter_by(id=data['vac_maker']).first()

        if basic_info:
            data['ele_num'] = basic_info.ele_num
            data['pre_num'] = basic_info.pre_num
        # 有值
        if supplycommodityinfo:
            data['cname'] = supplycommodityinfo.cname
        if supplyvsuppliersinfo:
            data['supplier_name'] = supplyvsuppliersinfo.supplier_name

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


@d_health.route('/d_health/quarantineinfo', methods=['POST'])  # 检疫检验 后端接口
def get_quarantineinfo():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        # 'basic_id': DHealthDeathinfo.basic_id,
        'ele_num': DHealthQuarantineinfo.basic_id,  # 电子耳号
        'pre_num': DHealthQuarantineinfo.basic_id,  # 防疫耳号
        'date': DHealthQuarantineinfo.date,
        'detection_mode': DHealthQuarantineinfo.detection_mode,
        'item': DHealthQuarantineinfo.item,
        'num': DHealthQuarantineinfo.num,
        'antibody': DHealthQuarantineinfo.antibody,
        'institutions': DHealthQuarantineinfo.institutions,
        'third_name': DHealthQuarantineinfo.third_name,
        'inspector': DHealthQuarantineinfo.inspector,
        'result1': DHealthQuarantineinfo.result1,
        'result2': DHealthQuarantineinfo.result2,
        'result3': DHealthQuarantineinfo.result3,
        'situation': DHealthQuarantineinfo.situation,
        'attachment': DHealthQuarantineinfo.attachment,
        'notes': DHealthQuarantineinfo.notes,
        'f_staff': DHealthQuarantineinfo.f_staff
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            elif param == 'ele_num':
                basic_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.ele_num.like(f'%{value}%')).first().id
                conditions.append(column == basic_id)
            elif param == 'pre_num':
                basic_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.pre_num.like(f'%{value}%')).first().id
                conditions.append(column == basic_id)
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = DHealthQuarantineinfo.query.filter(and_(*conditions))
    else:
        query = DHealthQuarantineinfo.query  # 如果没有条件，查询所有

    # 并且根据id降序排列

    query = query.filter(DHealthQuarantineinfo.belong == 0)
    infos = query.order_by(desc(DHealthQuarantineinfo.id)).paginate(page=pageNum, per_page=pageSize,
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


@d_health.route('/d_health/quarantineinfo/edit', methods=['POST'])  # 检验检疫 编辑 后端接口
def edit_quarantineinfo():
    data = request.get_json()
    print("--data-->", data)
    # 这个表更新的话需要1个搜索条件
    id = data['id']
    # 有多余的data信息，pre_num和ele_num
    try:
        if 'ele_num' in data:
            del data['ele_num']
        if 'pre_num' in data:
            del data['pre_num']
    except Exception as e:
        print("--data-->", data)
        print("--Exception-->", str(e))
    print('--------------------------test--------------------------------')
    DHealthQuarantineinfo.query.filter_by(id=id).update(data)

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


@d_health.route('/d_health/nursinginfo', methods=['POST'])  # 护理信息 后端接口
def get_nursinginfo():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        # 'basic_id': DHealthDeathinfo.basic_id,
        'ele_num': DHealthNursinginfo.basic_id,  # 电子耳号
        'pre_num': DHealthNursinginfo.basic_id,  # 防疫耳号
        'age': DHealthNursinginfo.age,
        'nurse': DHealthNursinginfo.nurse,
        'nur_time': DHealthNursinginfo.nur_time,
        'prenatal_paralysi': DHealthNursinginfo.prenatal_paralysi,
        'uterus_fall': DHealthNursinginfo.uterus_fall,
        'swelling': DHealthNursinginfo.swelling,
        'Ab_color': DHealthNursinginfo.Ab_color,
        'Ab_smell': DHealthNursinginfo.Ab_smell,
        'information': DHealthNursinginfo.information,
        'f_date': DHealthNursinginfo.f_date,
        'f_staff': DHealthNursinginfo.f_staff
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'nur_time' or param == 'f_date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            elif param == 'ele_num':
                basic_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.ele_num.like(f'%{value}%')).first().id
                conditions.append(column == basic_id)
            elif param == 'pre_num':
                basic_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.pre_num.like(f'%{value}%')).first().id
                conditions.append(column == basic_id)
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = DHealthNursinginfo.query.filter(and_(*conditions))
    else:
        query = DHealthNursinginfo.query  # 如果没有条件，查询所有

    # 并且根据id降序排列

    query = query.filter(DHealthNursinginfo.belong == 0)
    infos = query.order_by(desc(DHealthNursinginfo.id)).paginate(page=pageNum, per_page=pageSize,
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


@d_health.route('/d_health/nursinginfo/edit', methods=['POST'])  # 护理信息 编辑 后端接口
def edit_nursinginfo():
    data = request.get_json()
    print("--data-->", data)
    # 这个表更新的话需要1个搜索条件
    id = data['id']
    # 有多余的data信息，pre_num和ele_num
    try:
        if 'ele_num' in data:
            del data['ele_num']
        if 'pre_num' in data:
            del data['pre_num']
    except Exception as e:
        print("--data-->", data)
        print("--Exception-->", str(e))
    print('--------------------------test--------------------------------')
    DHealthNursinginfo.query.filter_by(id=id).update(data)

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


@d_health.route('/d_health/diseaseinfo', methods=['POST'])  # 疾病信息 后端接口
def get_diseaseinfo():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        # 'basic_id': DHealthDeathinfo.basic_id,
        'ele_num': DHealthDiseaseinfo.basic_id,  # 电子耳号
        'pre_num': DHealthDiseaseinfo.basic_id,  # 防疫耳号
        'disease_time': DHealthDiseaseinfo.disease_time,
        'age': DHealthDiseaseinfo.age,
        'disease': DHealthDiseaseinfo.disease,
        'treatment_time': DHealthDiseaseinfo.treatment_time,
        'm_staff': DHealthDiseaseinfo.m_staff,
        'drug_id': DHealthDiseaseinfo.drug_id,

        'cname': DHealthDiseaseinfo.drug_id,

        'drug_type': DHealthDiseaseinfo.drug_type,
        'WDT': DHealthDiseaseinfo.WDT,
        'cur_effect': DHealthDiseaseinfo.cur_effect,
        'cur_time': DHealthDiseaseinfo.cur_time,
        'out_time': DHealthDiseaseinfo.out_time,
        'out_no': DHealthDiseaseinfo.out_no,
        'f_staff': DHealthDiseaseinfo.f_staff
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'disease_time' or param == 'treatment_time' or param == 'cur_time' or param == 'out_time':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            elif param == 'ele_num':
                basic_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.ele_num.like(f'%{value}%')).first().id
                conditions.append(column == basic_id)
            elif param == 'pre_num':
                basic_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.pre_num.like(f'%{value}%')).first().id
                conditions.append(column == basic_id)
            elif param == 'cname':
                vaccine_id = SupplyCommodityinfo.query.filter(
                    SupplyCommodityinfo.cname.like(f'%{value}%')).first().id
                conditions.append(column == vaccine_id)
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = DHealthDiseaseinfo.query.filter(and_(*conditions))
    else:
        query = DHealthDiseaseinfo.query  # 如果没有条件，查询所有

    # 并且根据id降序排列

    query = query.filter(DHealthDiseaseinfo.belong == 0)
    infos = query.order_by(desc(DHealthDiseaseinfo.id)).paginate(page=pageNum, per_page=pageSize,
                                                                 error_out=False)
    total = query.count()

    list = []
    for info in infos:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        data = json.loads(data)
        basic_info = BasicBasicinfo.query.filter_by(id=data['basic_id']).first()
        supplycommodityinfo = SupplyCommodityinfo.query.filter_by(id=data['drug_id']).first()

        if basic_info:
            data['ele_num'] = basic_info.ele_num
            data['pre_num'] = basic_info.pre_num
        # 有值
        if supplycommodityinfo:
            data['cname'] = supplycommodityinfo.cname
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


@d_health.route('/d_health/abortioninfo', methods=['POST'])  # 异常脱落信息 后端接口
def get_abortioninfo():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        # 'basic_id': DHealthDeathinfo.basic_id,
        'ele_num': DHealthAbortioninfo.basic_id,  # 电子耳号
        'pre_num': DHealthAbortioninfo.basic_id,  # 防疫耳号
        'notes': DHealthAbortioninfo.notes,
        'method': DHealthAbortioninfo.method,
        'staff': DHealthAbortioninfo.staff,
        'date': DHealthAbortioninfo.date,
        'f_staff': DHealthAbortioninfo.f_staff
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'date' or param == 'f_date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            elif param == 'ele_num':
                basic_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.ele_num.like(f'%{value}%')).first().id
                conditions.append(column == basic_id)
            elif param == 'pre_num':
                basic_id = BasicBasicinfo.query.filter(
                    BasicBasicinfo.pre_num.like(f'%{value}%')).first().id
                conditions.append(column == basic_id)
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = DHealthAbortioninfo.query.filter(and_(*conditions))
    else:
        query = DHealthAbortioninfo.query  # 如果没有条件，查询所有

    # 并且根据id降序排列

    query = query.filter(DHealthAbortioninfo.belong == 0)
    infos = query.order_by(desc(DHealthAbortioninfo.id)).paginate(page=pageNum, per_page=pageSize,
                                                                  error_out=False)
    total = query.count()
    print(total)
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


@d_health.route('/d_health/immunizationinfo/add', methods=['POST'])  # 新增施药信息
def add_immunizationinfo():
    data = request.get_json()
    print(data)
    ctime = datetime.now()
    data['belong'] = 0
    data['f_date'] = ctime
    # 验证电子耳号是否存在在数据库中，如果在就删除掉data中的elenum，若果不在，就返回失败的结果。,
    ele_num = data['ele_num']
    query = BasicBasicinfo.query.filter_by(ele_num=ele_num).first()
    if query:
        del data['ele_num']
        if 'pre_num' in data:
            del data['pre_num']
        basic_info = json.dumps(query, cls=AlchemyEncoder, ensure_ascii=False)
        basic_info = json.loads(basic_info)
        data['basic_id'] = basic_info['id']
    else:
        result = {
            "code": 500,
            "msg": f'添加失败 '
        }
        return jsonify(result)
    # 这里是正常查询到进行的添加
    # 处理其他表中的id和信息
    if 'cname' in data:
        supplycommodityinfo = SupplyCommodityinfo.query.filter_by(cname=data['cname']).first()
    if 'supplier_name' in data:
        supplyvsuppliersinfo = SupplyVSuppliersinfo.query.filter_by(supplier_name=data['supplier_name']).first()
    if supplycommodityinfo and supplyvsuppliersinfo:
        data['vaccine_id'] = supplycommodityinfo.id
        data['maker_id'] = supplyvsuppliersinfo.id
    else:
        result = {
            "code": 500,
            "msg": f'添加失败 '
        }
        return jsonify(result)
    # 在加入list之前要判断是否有数据冗余：同一个basic_id，疫苗类型，接种时间，
    dup_imminfo = DHealthImmunizationinfo.query.filter_by(basic_id=data['basic_id'],
                                                          vaccine_id=data['vaccine_id'],
                                                          imm_date=data['imm_date']).first()
    if dup_imminfo:
        return jsonify({"code": 500, "msg": '存在数据冗余,添加失败'})
    immunizationinfo = DHealthImmunizationinfo()
    for key, value in data.items():
        setattr(immunizationinfo, key, value)
    try:
        db.session.add(immunizationinfo)
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


# 新增浸泡施药信息


@d_health.route('/d_health/drugbathinfo/add', methods=['POST'])  # 新增浸泡施药信息
def add_drugbathinfo():
    data = request.get_json()
    print(data)
    ctime = datetime.now()
    data['belong'] = 0
    data['f_date'] = ctime
    # 验证草地编号是否存在于数据库中，如果在就删除掉data中的elenum，若果不在，就返回失败的结果。,
    ele_num = data['ele_num']
    query = BasicBasicinfo.query.filter_by(ele_num=ele_num).first()
    if query:
        del data['ele_num']
        if 'pre_num' in data:
            del data['pre_num']
        basic_info = json.dumps(query, cls=AlchemyEncoder, ensure_ascii=False)
        basic_info = json.loads(basic_info)
        data['basic_id'] = basic_info['id']
    else:
        result = {
            "code": 500,
            "msg": f'添加失败 '
        }
        return jsonify(result)
        # 处理其他表中的id和信息
    if 'cname' in data:
        supplycommodityinfo = SupplyCommodityinfo.query.filter_by(cname=data['cname']).first()
    if 'supplier_name' in data:
        supplyvsuppliersinfo = SupplyVSuppliersinfo.query.filter_by(supplier_name=data['supplier_name']).first()
    if supplycommodityinfo and supplyvsuppliersinfo:
        data['drug_id'] = supplycommodityinfo.id
        data['vac_maker'] = supplyvsuppliersinfo.id
    else:
        result = {
            "code": 500,
            "msg": f'添加失败 '
        }
        return jsonify(result)
    drugbathinfo = DHealthDrugbathinfo()
    for key, value in data.items():
        setattr(drugbathinfo, key, value)
    try:
        db.session.add(drugbathinfo)
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
    # 新增病虫害检测信息


@d_health.route('/d_health/quarantineinfo/add', methods=['POST'])  # 新增病虫害检测信息
def add_quarantineinfo():
    data = request.get_json()
    # ctime = datetime.now()
    data['belong'] = 0
    # data['f_date'] = ctime
    # 验证草地编号是否存在于数据库中，如果在就删除掉data中的elenum，若果不在，就返回失败的结果。,
    ele_num = data['ele_num']
    query = BasicBasicinfo.query.filter_by(ele_num=ele_num).first()
    if query:
        del data['ele_num']
        if 'pre_num' in data:
            del data['pre_num']
        basic_info = json.dumps(query, cls=AlchemyEncoder, ensure_ascii=False)
        basic_info = json.loads(basic_info)
        data['basic_id'] = basic_info['id']
    else:
        result = {
            "code": 500,
            "msg": f'添加失败 '
        }
        return jsonify(result)
    quarantineinfo = DHealthQuarantineinfo()
    for key, value in data.items():
        setattr(quarantineinfo, key, value)
    try:
        db.session.add(quarantineinfo)
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
    # 新增护理信息


@d_health.route('/d_health/nursinginfo/add', methods=['POST'])  # 新增护理信息
def add_nursinginfo():
    data = request.get_json()
    ctime = datetime.now()
    data['belong'] = 0
    data['f_date'] = ctime
    # 验证电子耳号是否存在在数据库中，如果在就删除掉data中的elenum，若果不在，就返回失败的结果。,
    ele_num = data['ele_num']
    query = BasicBasicinfo.query.filter_by(ele_num=ele_num).first()
    if query:
        del data['ele_num']
        if 'pre_num' in data:
            del data['pre_num']
        basic_info = json.dumps(query, cls=AlchemyEncoder, ensure_ascii=False)
        basic_info = json.loads(basic_info)
        data['basic_id'] = basic_info['id']
    else:
        result = {
            "code": 500,
            "msg": f'添加失败 '
        }
        return jsonify(result)
    nursinginfo = DHealthNursinginfo()
    for key, value in data.items():
        setattr(nursinginfo, key, value)
    try:
        db.session.add(nursinginfo)
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
    # 新增疾病信息


@d_health.route('/d_health/diseaseinfo/add', methods=['POST'])  # 新增疾病信息
def add_diseaseinfo():
    data = request.get_json()
    # ctime = datetime.now()
    data['belong'] = 0
    # data['f_date'] = ctime
    # 验证电子耳号是否存在在数据库中，如果在就删除掉data中的elenum，若果不在，就返回失败的结果。,
    ele_num = data['ele_num']
    query = BasicBasicinfo.query.filter_by(ele_num=ele_num).first()
    if query:
        del data['ele_num']
        if 'pre_num' in data:
            del data['pre_num']
        basic_info = json.dumps(query, cls=AlchemyEncoder, ensure_ascii=False)
        basic_info = json.loads(basic_info)
        data['basic_id'] = basic_info['id']
    else:
        result = {
            "code": 500,
            "msg": f'添加失败 '
        }
        return jsonify(result)
    if 'cname' in data:
        supplycommodityinfo = SupplyCommodityinfo.query.filter_by(cname=data['cname']).first()
    if supplycommodityinfo:
        data['vaccine_id'] = supplycommodityinfo.id
    else:
        result = {
            "code": 500,
            "msg": f'添加失败 '
        }
        return jsonify(result)
    diseaseinfo = DHealthDiseaseinfo()
    for key, value in data.items():
        setattr(diseaseinfo, key, value)
    try:
        db.session.add(diseaseinfo)
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



@d_health.route('/d_health/abortioninfo/add', methods=['POST'])  # 新增异常脱落记录
def add_abortioninfo():
    data = request.get_json()
    ctime = datetime.now()
    data['belong'] = 0
    data['f_date'] = ctime
    # 验证电子耳号是否存在在数据库中，如果在就删除掉data中的elenum，若果不在，就返回失败的结果。,
    ele_num = data['ele_num']
    query = BasicBasicinfo.query.filter_by(ele_num=ele_num).first()
    if query:
        del data['ele_num']
        if 'pre_num' in data:
            del data['pre_num']
        basic_info = json.dumps(query, cls=AlchemyEncoder, ensure_ascii=False)
        basic_info = json.loads(basic_info)
        data['basic_id'] = basic_info['id']
    else:
        result = {
            "code": 500,
            "msg": f'添加失败 '
        }
        return jsonify(result)
    abortioninfo = DHealthAbortioninfo()
    for key, value in data.items():
        setattr(abortioninfo, key, value)
    try:
        # #流产信息必须为母系草地
        # if data['sex']==0:

        db.session.add(abortioninfo)
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


@d_health.route('/d_health/deathinfo/edit', methods=['POST'])  # 绝收信息 编辑 后端接口
def edit_deathinfo():
    data = request.get_json()
    print("--data-->", data)
    # 这个表更新的话需要1个搜索条件
    id = data['id']
    # 有多余的data信息，pre_num和ele_num
    try:
        if 'ele_num' in data:
            del data['ele_num']
        if 'pre_num' in data:
            del data['pre_num']
    except Exception as e:
        print("--data-->", data)
        print("--Exception-->", str(e))
    print('--------------------------test--------------------------------')
    DHealthDeathinfo.query.filter_by(id=id).update(data)

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


@d_health.route('/d_health/immunizationinfo/edit', methods=['POST'])  # 施药记录 编辑 后端接口
def edit_immunizationinfo():
    data = request.get_json()
    print("--data-->", data)
    # 这个表更新的话需要1个搜索条件
    id = data['id']
    # 有多余的data信息，pre_num和ele_num
    try:
        if 'ele_num' in data:
            del data['ele_num']
        if 'pre_num' in data:
            del data['pre_num']
        if 'supplier_name' in data:
            data["maker_id"] = SupplyVSuppliersinfo.query.filter(
                SupplyVSuppliersinfo.supplier_name.like(f'%{data["supplier_name"]}%')).first().id
            del data['supplier_name']
        if 'cname' in data:
            data["vaccine_id"] = SupplyCommodityinfo.query.filter(
                SupplyCommodityinfo.cname.like(f'%{data["cname"]}%')).first().id
            del data['cname']
    except Exception as e:
        print("--data-->", data)
        print("--Exception-->", str(e))
    print('--------------------------test--------------------------------')
    DHealthImmunizationinfo.query.filter_by(id=id).update(data)

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


@d_health.route('/d_health/drugbathinfo/edit', methods=['POST'])  # 药浴免疫 编辑 后端接口
def edit_drugbathinfo():
    data = request.get_json()
    print("--data-->", data)
    # 这个表更新的话需要1个搜索条件
    id = data['id']
    # 有多余的data信息，pre_num和ele_num
    try:
        if 'ele_num' in data:
            del data['ele_num']
        if 'pre_num' in data:
            del data['pre_num']
        if 'supplier_name' in data:
            data["vac_maker"] = SupplyVSuppliersinfo.query.filter(
                SupplyVSuppliersinfo.supplier_name.like(f'%{data["supplier_name"]}%')).first().id
            del data['supplier_name']
        if 'cname' in data:
            data["drug_id"] = SupplyCommodityinfo.query.filter(
                SupplyCommodityinfo.cname.like(f'%{data["cname"]}%')).first().id
            del data['cname']
    except Exception as e:
        print("--data-->", data)
        print("--Exception-->", str(e))
    print('--------------------------test--------------------------------')
    DHealthDrugbathinfo.query.filter_by(id=id).update(data)

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


@d_health.route('/d_health/diseaseinfo/edit', methods=['POST'])  # 疾病信息 编辑 后端接口
def edit_diseaseinfo():
    data = request.get_json()
    print("--data-->", data)
    # 这个表更新的话需要1个搜索条件
    id = data['id']
    # 有多余的data信息，pre_num和ele_num
    try:
        if 'ele_num' in data:
            del data['ele_num']
        if 'pre_num' in data:
            del data['pre_num']
        if 'cname' in data:
            data["drug_id"] = SupplyCommodityinfo.query.filter(
                SupplyCommodityinfo.cname.like(f'%{data["cname"]}%')).first().id
            del data['cname']
    except Exception as e:
        print("--data-->", data)
        print("--Exception-->", str(e))
    print('--------------------------test--------------------------------')
    DHealthDiseaseinfo.query.filter_by(id=id).update(data)

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


@d_health.route('/d_health/abortioninfo/edit', methods=['POST'])  # 流产信息 编辑 后端接口
def edit_abortioninfo():
    data = request.get_json()
    print("--data-->", data)
    # 这个表更新的话需要1个搜索条件
    id = data['id']
    # 有多余的data信息，pre_num和ele_num
    try:
        if 'ele_num' in data:
            del data['ele_num']
        if 'pre_num' in data:
            del data['pre_num']
    except Exception as e:
        print("--data-->", data)
        print("--Exception-->", str(e))
    print('--------------------------test--------------------------------')
    DHealthAbortioninfo.query.filter_by(id=id).update(data)

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


@d_health.route('/d_health/immunizationinfo/del', methods=['POST'])  # 接种免疫 编辑 后端接口
def del_immunizationinfo():
    data = request.get_json()
    print("--data-->", data)
    # 这个表更新的话需要1个搜索条件
    id = data['id']
    print('--------------------------test--------------------------------')
    try:
        DHealthImmunizationinfo.query.filter_by(id=id).delete()
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


# 导出接种免疫
@d_health.route('/d_health/immunizationinfo/export', methods=['POST'])
def export_immunizationinfo():
    try:
        selected_ids = request.get_json()

        if selected_ids:
            immunization_info = DHealthImmunizationBS.query.filter(DHealthImmunizationBS.id.in_(selected_ids)).all()
        else:
            immunization_info = DHealthImmunizationBS.query.all()

        data_list = []
        for info in immunization_info:
            data_list.append({
                '田块记录id': info.basic_id,
                '草地编号': info.ele_num,
                '地块编号': info.pre_num,
                '施药生长月数': info.imm_age,
                '施药日期': info.imm_date.isoformat() if info.imm_date else None,
                '施药剂量': info.dose,
                '农药/防治药物': info.cname,
                '生产厂家': info.supplier_name,
                '创建时间': info.f_date.isoformat() if info.f_date else None,
                '创建人员': info.f_staff
            })

        df = pd.DataFrame(data_list)

        export_path = os.path.join(os.getcwd(), 'App', 'd_health', 'export_excel', 'immunization_info.xlsx')
        df.to_excel(export_path, index=False)

        return send_file(export_path, as_attachment=True)
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'导出失败 {str(e)}'})


# 删除药浴免疫信息
@d_health.route('/d_health/drugbathinfo/del', methods=['POST'])
def del_drugbathinfo():
    ids = request.get_json()
    for i in ids:
        DHealthDrugbathinfo.query.filter_by(id=i).delete()
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


# 导出药浴免疫
@d_health.route('/d_health/drugbathinfo/export', methods=['POST'])
def export_drugbathinfo():
    try:
        selected_ids = request.get_json()

        if selected_ids:
            drugbath_info = (
                db.session.query(DHealthDrugbathinfo, BasicBasicinfo.ele_num, BasicBasicinfo.pre_num,
                                 SupplyCommodityinfo.cname, SupplyVSuppliersinfo.supplier_name)
                    .outerjoin(BasicBasicinfo, BasicBasicinfo.id == DHealthDrugbathinfo.basic_id)
                    .outerjoin(SupplyCommodityinfo, SupplyCommodityinfo.id == DHealthDrugbathinfo.drug_id)
                    .outerjoin(SupplyVSuppliersinfo, SupplyVSuppliersinfo.id == DHealthDrugbathinfo.vac_maker)
                    .filter(DHealthDrugbathinfo.id.in_(selected_ids))
                    .all()
            )
        else:
            drugbath_info = (
                db.session.query(DHealthDrugbathinfo, BasicBasicinfo.ele_num, BasicBasicinfo.pre_num,
                                 SupplyCommodityinfo.cname, SupplyVSuppliersinfo.supplier_name)
                    .outerjoin(BasicBasicinfo, BasicBasicinfo.id == DHealthDrugbathinfo.basic_id)
                    .outerjoin(SupplyCommodityinfo, SupplyCommodityinfo.id == DHealthDrugbathinfo.drug_id)
                    .outerjoin(SupplyVSuppliersinfo, SupplyVSuppliersinfo.id == DHealthDrugbathinfo.vac_maker)
                    .all()
            )

        data_list = []
        for info, ele_num, pre_num, cname, supplier_name in drugbath_info:
            data_list.append({
                '电子耳号': ele_num,
                '防疫耳号': pre_num,
                '药浴月龄': info.drug_age,
                '用药时间': info.take_time.isoformat() if info.take_time else None,
                '药品信息': cname,
                '药品厂家': supplier_name,
                '药效时间': info.timing,
                '创建时间': info.f_date.isoformat() if info.f_date else None,
                '创建人员': info.f_staff
            })
        df = pd.DataFrame(data_list)

        export_path = os.path.join(os.getcwd(), 'App', 'd_health', 'export_excel', 'drugbath_info.xlsx')
        df.to_excel(export_path, index=False)

        return send_file(export_path, as_attachment=True)
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'导出失败 {str(e)}'})


# 删除检疫免疫信息
@d_health.route('/d_health/quarantineinfo/del', methods=['POST'])
def del_quarantineinfo():
    ids = request.get_json()
    for i in ids:
        DHealthQuarantineinfo.query.filter_by(id=i).delete()
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


# 导出检疫免疫
@d_health.route('/d_health/quarantineinfo/export', methods=['POST'])
def export_quarantineinfo():
    try:
        selected_ids = request.get_json()

        if selected_ids:
            quarantine_info = (
                db.session.query(DHealthQuarantineinfo, BasicBasicinfo.ele_num, BasicBasicinfo.pre_num)
                    .outerjoin(BasicBasicinfo, BasicBasicinfo.id == DHealthQuarantineinfo.basic_id)
                    .filter(DHealthQuarantineinfo.id.in_(selected_ids))
                    .all()
            )
        else:
            quarantine_info = (
                db.session.query(DHealthQuarantineinfo, BasicBasicinfo.ele_num, BasicBasicinfo.pre_num)
                    .outerjoin(BasicBasicinfo, BasicBasicinfo.id == DHealthQuarantineinfo.basic_id)
                    .all()
            )

        d_healthDetection_modeType = {
            0: "目视检测",
            1: "实验室检测",
        }
        d_healthResult1Type = {
            0: "害虫未检出",
            1: "害虫已检出",
        }
        d_healthResult2Type = {
            0: "病害阴性",
            1: "病害阳性"
        }
        d_healthResult3Type = {
            0: "预警正常",
            1: "预警触发"
        }
        d_healthSituationType = {
            0: "允许正常生长",
            1: "需要施药",
            2: "隔离观察",
            3: "拔除销毁"
        }

        data_list = []
        for info, ele_num, pre_num in quarantine_info:
            detection_mode = d_healthDetection_modeType.get(info.detection_mode, " ")
            situation = d_healthSituationType.get(info.situation, " ")
            result1 = d_healthResult1Type.get(info.result1, " ")
            result2 = d_healthResult2Type.get(info.result2, " ")
            result3 = d_healthResult3Type.get(info.result3, " ")

            data_list.append({
                '草地编号': ele_num,
                '地块编号': pre_num,
                '采样时间': info.date.isoformat() if info.date else None,
                '检测方式': detection_mode,
                '检测项目': info.item,
                '采样数量': info.num,
                '病虫害抗性': info.antibody,
                '检测机构': info.institutions,
                '第三方机构': info.third_name,
                '检测人员': info.inspector,
                '害虫检出结果': result1,
                '病害检出结果': result2,
                '预警等级': result3,
                '处理情况': situation,
                '创建人员': info.f_staff
            })
        df = pd.DataFrame(data_list)

        export_path = os.path.join(os.getcwd(), 'App', 'd_health', 'export_excel', 'quarantine_info.xlsx')
        df.to_excel(export_path, index=False)

        return send_file(export_path, as_attachment=True)
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'导出失败 {str(e)}'})


# 删除护理信息
@d_health.route('/d_health/nursinginfo/del', methods=['POST'])
def del_nursinginfo():
    ids = request.get_json()
    for i in ids:
        DHealthNursinginfo.query.filter_by(id=i).delete()
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


@d_health.route('/d_health/nursinginfo/export', methods=['POST'])
def export_nursinginfo():
    try:
        selected_ids = request.get_json()

        if selected_ids:
            nursing_info = (
                db.session.query(DHealthNursinginfo, BasicBasicinfo.ele_num, BasicBasicinfo.pre_num)
                    .outerjoin(BasicBasicinfo, BasicBasicinfo.id == DHealthNursinginfo.basic_id)
                    .filter(DHealthNursinginfo.id.in_(selected_ids))
                    .all()
            )
        else:
            nursing_info = (
                db.session.query(DHealthNursinginfo, BasicBasicinfo.ele_num, BasicBasicinfo.pre_num)
                    .outerjoin(BasicBasicinfo, BasicBasicinfo.id == DHealthNursinginfo.basic_id)
                    .all()
            )

        d_healthTestis_shapeType = {
            0: "不正常",
            1: "正常",
        }
        prenatal_paralysi = {
            0: "否",
            1: "是",
        }
        uterus_fall = {
            0: "否",
            1: "是"
        }
        swelling = {
            0: "否",
            1: "是"
        }
        d_healthAb_colorType = {
            0: "黄",
            1: "白",
            2: "红",
            3: "绿"
        }
        d_healthAb_smellType = {
            0: "正常",
            1: "血腥",
            2: "血臭"
        }

        data_list = []
        for info, ele_num, pre_num in nursing_info:
            datatestis_shape = d_healthTestis_shapeType.get(info.testis_shape, " ")
            dataprenatal_paralysi = prenatal_paralysi.get(info.prenatal_paralysi, " ")
            datauterus_fall = uterus_fall.get(info.uterus_fall, " ")
            dataswelling = swelling.get(info.swelling, " ")
            dataAb_color = d_healthAb_colorType.get(info.Ab_color, " ")
            dataAb_smell = d_healthAb_smellType.get(info.Ab_smell, " ")

            data_list.append({
                '草地编号': ele_num,
                '地块编号': pre_num,
                '养护时生长月数': info.age,
                '养护人员': info.nurse,
                '养护时间': info.nur_time.isoformat() if info.nur_time else None,
                '形态是否正常': datatestis_shape,
                '生长前期萎蔫': dataprenatal_paralysi,
                '根系脱落': datauterus_fall,
                '叶片肿胀': dataswelling,
                '分泌物颜色': dataAb_color,
                '分泌物气味': dataAb_smell,
                '情况说明': info.information,
                '创建时间': info.f_date.isoformat() if info.f_date else None,
                '创建人员': info.f_staff
            })
        df = pd.DataFrame(data_list)

        export_path = os.path.join(os.getcwd(), 'App', 'd_health', 'export_excel', 'nursing_info.xlsx')
        df.to_excel(export_path, index=False)

        return send_file(export_path, as_attachment=True)
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'导出失败 {str(e)}'})


@d_health.route('/d_health/diseaseinfo/del', methods=['POST'])
def del_diseaseinfo():
    ids = request.get_json()
    for i in ids:
        DHealthDiseaseinfo.query.filter_by(id=i).delete()
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


@d_health.route('/d_health/diseaseinfo/export', methods=['POST'])
def export_diseaseinfo():
    try:
        selected_ids = request.get_json()

        if selected_ids:
            disease_info = (
                db.session.query(DHealthDiseaseinfo, BasicBasicinfo.ele_num, BasicBasicinfo.pre_num,
                                 SupplyCommodityinfo.cname)
                    .outerjoin(BasicBasicinfo, BasicBasicinfo.id == DHealthDiseaseinfo.basic_id)
                    .outerjoin(SupplyCommodityinfo, SupplyCommodityinfo.id == DHealthDiseaseinfo.drug_id)
                    .filter(DHealthDiseaseinfo.id.in_(selected_ids))
                    .all()
            )
        else:
            disease_info = (
                db.session.query(DHealthDiseaseinfo, BasicBasicinfo.ele_num, BasicBasicinfo.pre_num,
                                 SupplyCommodityinfo.cname)
                    .outerjoin(BasicBasicinfo, BasicBasicinfo.id == DHealthDiseaseinfo.basic_id)
                    .outerjoin(SupplyCommodityinfo, SupplyCommodityinfo.id == DHealthDiseaseinfo.drug_id)
                    .all()
            )

        cur_effect = {
            0: "治愈",
            1: "淘汰",
            2: "死亡"
        }
        data_list = []
        for info, ele_num, pre_num, cname in disease_info:
            datacur_effect = cur_effect.get(info.cur_effect, " ")
            data_list.append({
                '电子耳号': ele_num,
                '防疫耳号': pre_num,
                '发病时间': info.disease_time.isoformat() if info.disease_time else None,
                '年龄': info.age,
                '疾病名称': info.disease,
                '诊疗时间': info.treatment_time.isoformat() if info.treatment_time else None,
                '诊疗人员': info.m_staff,
                '治疗药物': cname,
                '是否国家允许的药物': info.drug_type,
                '休药期': info.WDT,
                '治愈效果': datacur_effect,
                '治愈时间': info.cur_time.isoformat() if info.cur_time else None,
                '出库时间': info.out_time.isoformat() if info.out_time else None,
                '出库编号': info.out_no,
                '创建人员': info.f_staff
            })
        df = pd.DataFrame(data_list)

        export_path = os.path.join(os.getcwd(), 'App', 'd_health', 'export_excel', 'disease_info.xlsx')
        df.to_excel(export_path, index=False)

        return send_file(export_path, as_attachment=True)
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'导出失败 {str(e)}'})


# 删除流产信息
@d_health.route('/d_health/abortioninfo/del', methods=['POST'])
def del_abortioninfo():
    ids = request.get_json()
    for i in ids:
        DHealthAbortioninfo.query.filter_by(id=i).delete()
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


# 删除流产信息
@d_health.route('/d_health/abortioninfo/export', methods=['POST'])
def export_abortioninfo():
    try:
        selected_ids = request.get_json()

        if selected_ids:
            abortion_info = (
                db.session.query(DHealthAbortioninfo, BasicBasicinfo.ele_num, BasicBasicinfo.pre_num)
                    .outerjoin(BasicBasicinfo, BasicBasicinfo.id == DHealthAbortioninfo.basic_id)
                    .filter(DHealthAbortioninfo.id.in_(selected_ids))
                    .all()
            )
        else:
            abortion_info = (
                db.session.query(DHealthAbortioninfo, BasicBasicinfo.ele_num, BasicBasicinfo.pre_num)
                    .outerjoin(BasicBasicinfo, BasicBasicinfo.id == DHealthAbortioninfo.basic_id)
                    .all()
            )

        data_list = []
        for info, ele_num, pre_num in abortion_info:
            data_list.append({
                '草地编号': ele_num,
                '地块编号': pre_num,
                '异常日期': info.date.isoformat() if info.date else None,
                '异常原因': info.notes,
                '处理方式': info.method,
                '处理人员': info.staff,
                '处理时间': info.date.isoformat() if info.date else None,
                '创建人员': info.f_staff,
                '创建时间': info.f_date.isoformat() if info.f_date else None
            })
        df = pd.DataFrame(data_list)

        export_path = os.path.join(os.getcwd(), 'App', 'd_health', 'export_excel', 'abortion_info.xlsx')
        df.to_excel(export_path, index=False)

        return send_file(export_path, as_attachment=True)
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'导出失败 {str(e)}'})
