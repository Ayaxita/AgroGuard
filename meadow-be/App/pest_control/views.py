# views.py: 路由 + 视图函数
from datetime import datetime
import random
import os
from flask import Blueprint, render_template, request, make_response, Response, redirect, url_for, session, jsonify, \
    send_file
from sqlalchemy import desc, and_, or_, not_
import pandas as pd

from ..modelsReverse import *
import json
from ..utils.AlchemyEncoder import AlchemyEncoder

pest_control = Blueprint('pest_control', __name__)


@pest_control.route('/pest_control/witherinfo', methods=['POST'])  # 绝收信息 后端接口
def get_witherinfo():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        # 'basic_id': DPlantcareDeathinfo.basic_id,
        'ele_num': DPlantcareDeathinfo.basic_id,
        'pre_num': DPlantcareDeathinfo.basic_id,
        'date': DPlantcareDeathinfo.date,
        'age': DPlantcareDeathinfo.age,
        'cause': DPlantcareDeathinfo.cause,
        'harmless_treatment': DPlantcareDeathinfo.harmless_treatment,
        't_time': DPlantcareDeathinfo.t_time,
        't_staff': DPlantcareDeathinfo.t_staff,
        'f_staff': DPlantcareDeathinfo.f_staff,
        'f_date': DPlantcareDeathinfo.f_date,
        'notes': DPlantcareDeathinfo.notes,
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
        query = DPlantcareDeathinfo.query.filter(and_(*conditions))
    else:
        query = DPlantcareDeathinfo.query  # 如果没有条件，查询所有

    # 并且根据id降序排列

    query = query.filter(DPlantcareDeathinfo.belong == 0)
    infos = query.order_by(desc(DPlantcareDeathinfo.id)).paginate(page=pageNum, per_page=pageSize,
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
@pest_control.route('/pest_control/immunizationinfo', methods=['POST'])
def get_immunizationinfo():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        # '': DPlantcareImmunizationinfo.,
        'basic_id': DPlantcareImmunizationinfo.basic_id,
        'ele_num': DPlantcareImmunizationinfo.basic_id,
        'pre_num': DPlantcareImmunizationinfo.basic_id,
        'imm_date': DPlantcareImmunizationinfo.imm_date,
        'imm_age': DPlantcareImmunizationinfo.imm_age,
        'vaccine_id': DPlantcareImmunizationinfo.vaccine_id,
        'maker_id': DPlantcareImmunizationinfo.maker_id,

        'cname': DPlantcareImmunizationinfo.vaccine_id,
        'supplier_name': DPlantcareImmunizationinfo.maker_id,

        'dose': DPlantcareImmunizationinfo.dose,
        'anti_level': DPlantcareImmunizationinfo.anti_level,
        'post_stage': DPlantcareImmunizationinfo.post_stage,
        'out_time': DPlantcareImmunizationinfo.out_time,
        'f_date': DPlantcareImmunizationinfo.f_date,
        'operators': DPlantcareImmunizationinfo.operators,
        'belong': DPlantcareImmunizationinfo.belong,
        'f_staff': DPlantcareImmunizationinfo.f_staff,
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
        query = DPlantcareImmunizationinfo.query.filter(and_(*conditions))
    else:
        query = DPlantcareImmunizationinfo.query  # 如果没有条件，查询所有

    # 并且根据id降序排列

    query = query.filter(DPlantcareImmunizationinfo.belong == 0)
    infos = query.order_by(desc(DPlantcareImmunizationinfo.id)).paginate(page=pageNum, per_page=pageSize,
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


@pest_control.route('/pest_control/protectioninfo', methods=['POST'])  # 浸泡施药 后端接口
def get_protectioninfo():
    print('_______________________________________')
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        # '': DPlantcareProtectioninfo.,
        'basic_id': DPlantcareProtectioninfo.basic_id,
        'ele_num': DPlantcareProtectioninfo.basic_id,
        'pre_num': DPlantcareProtectioninfo.basic_id,
        'protection_age': DPlantcareProtectioninfo.protection_age,
        'take_time': DPlantcareProtectioninfo.take_time,
        'drug_id': DPlantcareProtectioninfo.drug_id,
        'vac_maker': DPlantcareProtectioninfo.vac_maker,

        'cname': DPlantcareProtectioninfo.drug_id,
        'supplier_name': DPlantcareProtectioninfo.vac_maker,

        'effect': DPlantcareProtectioninfo.effect,
        'timing': DPlantcareProtectioninfo.timing,
        'IR_bath': DPlantcareProtectioninfo.IR_bath,
        'out_time': DPlantcareProtectioninfo.out_time,
        'f_date': DPlantcareProtectioninfo.f_date,
        'operators': DPlantcareProtectioninfo.operators,
        'belong': DPlantcareProtectioninfo.belong,
        'f_staff': DPlantcareProtectioninfo.f_staff,
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
        query = DPlantcareProtectioninfo.query.filter(and_(*conditions))
    else:
        query = DPlantcareProtectioninfo.query  # 如果没有条件，查询所有

    # 并且根据id降序排列

    query = query.filter(DPlantcareProtectioninfo.belong == 0)
    infos = query.order_by(desc(DPlantcareProtectioninfo.id)).paginate(page=pageNum, per_page=pageSize,
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


@pest_control.route('/pest_control/quarantineinfo', methods=['POST'])  # 检疫检验 后端接口
def get_quarantineinfo():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        # 'basic_id': DPlantcareDeathinfo.basic_id,
        'ele_num': DPlantcareQuarantineinfo.basic_id,  # 草地编号
        'pre_num': DPlantcareQuarantineinfo.basic_id,  # 草地类型
        'date': DPlantcareQuarantineinfo.date,
        'detection_mode': DPlantcareQuarantineinfo.detection_mode,
        'item': DPlantcareQuarantineinfo.item,
        'num': DPlantcareQuarantineinfo.num,
        'antibody': DPlantcareQuarantineinfo.antibody,
        'institutions': DPlantcareQuarantineinfo.institutions,
        'third_name': DPlantcareQuarantineinfo.third_name,
        'inspector': DPlantcareQuarantineinfo.inspector,
        'result1': DPlantcareQuarantineinfo.result1,
        'result2': DPlantcareQuarantineinfo.result2,
        'result3': DPlantcareQuarantineinfo.result3,
        'situation': DPlantcareQuarantineinfo.situation,
        'attachment': DPlantcareQuarantineinfo.attachment,
        'notes': DPlantcareQuarantineinfo.notes,
        'f_staff': DPlantcareQuarantineinfo.f_staff
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
        query = DPlantcareQuarantineinfo.query.filter(and_(*conditions))
    else:
        query = DPlantcareQuarantineinfo.query  # 如果没有条件，查询所有

    # 并且根据id降序排列

    query = query.filter(DPlantcareQuarantineinfo.belong == 0)
    infos = query.order_by(desc(DPlantcareQuarantineinfo.id)).paginate(page=pageNum, per_page=pageSize,
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


@pest_control.route('/pest_control/quarantineinfo/edit', methods=['POST'])  # 检验检疫 编辑 后端接口
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
    DPlantcareQuarantineinfo.query.filter_by(id=id).update(data)

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


@pest_control.route('/pest_control/nursinginfo', methods=['POST'])  # 护理信息 后端接口
def get_nursinginfo():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        # 'basic_id': DPlantcareDeathinfo.basic_id,
        'ele_num': DPlantcareNursinginfo.basic_id,  # 草地编号
        'pre_num': DPlantcareNursinginfo.basic_id,  # 草地类型
        'age': DPlantcareNursinginfo.age,
        'nurse': DPlantcareNursinginfo.nurse,
        'nur_time': DPlantcareNursinginfo.nur_time,
        'prenatal_paralysi': DPlantcareNursinginfo.prenatal_paralysi,
        'uterus_fall': DPlantcareNursinginfo.uterus_fall,
        'swelling': DPlantcareNursinginfo.swelling,
        'Ab_color': DPlantcareNursinginfo.Ab_color,
        'Ab_smell': DPlantcareNursinginfo.Ab_smell,
        'information': DPlantcareNursinginfo.information,
        'f_date': DPlantcareNursinginfo.f_date,
        'f_staff': DPlantcareNursinginfo.f_staff
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
        query = DPlantcareNursinginfo.query.filter(and_(*conditions))
    else:
        query = DPlantcareNursinginfo.query  # 如果没有条件，查询所有

    # 并且根据id降序排列

    query = query.filter(DPlantcareNursinginfo.belong == 0)
    infos = query.order_by(desc(DPlantcareNursinginfo.id)).paginate(page=pageNum, per_page=pageSize,
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


@pest_control.route('/pest_control/nursinginfo/edit', methods=['POST'])  # 护理信息 编辑 后端接口
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
    DPlantcareNursinginfo.query.filter_by(id=id).update(data)

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


@pest_control.route('/pest_control/diseaseinfo', methods=['POST'])  # 疾病信息 后端接口
def get_diseaseinfo():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        # 'basic_id': DPlantcareDeathinfo.basic_id,
        'ele_num': DPlantcareDiseaseinfo.basic_id,  # 草地编号
        'pre_num': DPlantcareDiseaseinfo.basic_id,  # 草地类型
        'disease_time': DPlantcareDiseaseinfo.disease_time,
        'age': DPlantcareDiseaseinfo.age,
        'disease': DPlantcareDiseaseinfo.disease,
        'treatment_time': DPlantcareDiseaseinfo.treatment_time,
        'm_staff': DPlantcareDiseaseinfo.m_staff,
        'drug_id': DPlantcareDiseaseinfo.drug_id,

        'cname': DPlantcareDiseaseinfo.drug_id,

        'drug_type': DPlantcareDiseaseinfo.drug_type,
        'WDT': DPlantcareDiseaseinfo.WDT,
        'cur_effect': DPlantcareDiseaseinfo.cur_effect,
        'cur_time': DPlantcareDiseaseinfo.cur_time,
        'out_time': DPlantcareDiseaseinfo.out_time,
        'out_no': DPlantcareDiseaseinfo.out_no,
        'f_staff': DPlantcareDiseaseinfo.f_staff
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
        query = DPlantcareDiseaseinfo.query.filter(and_(*conditions))
    else:
        query = DPlantcareDiseaseinfo.query  # 如果没有条件，查询所有

    # 并且根据id降序排列

    query = query.filter(DPlantcareDiseaseinfo.belong == 0)
    infos = query.order_by(desc(DPlantcareDiseaseinfo.id)).paginate(page=pageNum, per_page=pageSize,
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


@pest_control.route('/pest_control/damageinfo', methods=['POST'])  # 异常脱落信息 后端接口
def get_damageinfo():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        # 'basic_id': DPlantcareDeathinfo.basic_id,
        'ele_num': DPlantcareDamageinfo.basic_id,  # 草地编号
        'pre_num': DPlantcareDamageinfo.basic_id,  # 草地类型
        'notes': DPlantcareDamageinfo.notes,
        'method': DPlantcareDamageinfo.method,
        'staff': DPlantcareDamageinfo.staff,
        'date': DPlantcareDamageinfo.date,
        'f_staff': DPlantcareDamageinfo.f_staff
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
        query = DPlantcareDamageinfo.query.filter(and_(*conditions))
    else:
        query = DPlantcareDamageinfo.query  # 如果没有条件，查询所有

    # 并且根据id降序排列

    query = query.filter(DPlantcareDamageinfo.belong == 0)
    infos = query.order_by(desc(DPlantcareDamageinfo.id)).paginate(page=pageNum, per_page=pageSize,
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


@pest_control.route('/pest_control/immunizationinfo/add', methods=['POST'])  # 新增施药信息
def add_immunizationinfo():
    data = request.get_json()
    print(data)
    ctime = datetime.now()
    data['belong'] = 0
    data['f_date'] = ctime
    # 验证草地编号是否存在在数据库中，如果在就删除掉data中的elenum，若果不在，就返回失败的结果。,
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
    dup_imminfo = DPlantcareImmunizationinfo.query.filter_by(basic_id=data['basic_id'],
                                                          vaccine_id=data['vaccine_id'],
                                                          imm_date=data['imm_date']).first()
    if dup_imminfo:
        return jsonify({"code": 500, "msg": '存在数据冗余,添加失败'})
    immunizationinfo = DPlantcareImmunizationinfo()
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


@pest_control.route('/pest_control/protectioninfo/add', methods=['POST'])  # 新增浸泡施药信息
def add_protectioninfo():
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
    protectioninfo = DPlantcareProtectioninfo()
    for key, value in data.items():
        setattr(protectioninfo, key, value)
    try:
        db.session.add(protectioninfo)
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


@pest_control.route('/pest_control/quarantineinfo/add', methods=['POST'])  # 新增病虫害检测信息
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
    quarantineinfo = DPlantcareQuarantineinfo()
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


@pest_control.route('/pest_control/nursinginfo/add', methods=['POST'])  # 新增护理信息
def add_nursinginfo():
    data = request.get_json()
    ctime = datetime.now()
    data['belong'] = 0
    data['f_date'] = ctime
    # 验证草地编号是否存在在数据库中，如果在就删除掉data中的elenum，若果不在，就返回失败的结果。,
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
    nursinginfo = DPlantcareNursinginfo()
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


@pest_control.route('/pest_control/diseaseinfo/add', methods=['POST'])  # 新增疾病信息
def add_diseaseinfo():
    data = request.get_json()
    # ctime = datetime.now()
    data['belong'] = 0
    # data['f_date'] = ctime
    # 验证草地编号是否存在在数据库中，如果在就删除掉data中的elenum，若果不在，就返回失败的结果。,
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
    diseaseinfo = DPlantcareDiseaseinfo()
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



@pest_control.route('/pest_control/damageinfo/add', methods=['POST'])  # 新增异常脱落记录
def add_damageinfo():
    data = request.get_json()
    ctime = datetime.now()
    data['belong'] = 0
    data['f_date'] = ctime
    # 验证草地编号是否存在在数据库中，如果在就删除掉data中的elenum，若果不在，就返回失败的结果。,
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
    damageinfo = DPlantcareDamageinfo()
    for key, value in data.items():
        setattr(damageinfo, key, value)
    try:
        # #流产信息必须为母系草地
        # if data['sex']==0:

        db.session.add(damageinfo)
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


@pest_control.route('/pest_control/witherinfo/edit', methods=['POST'])  # 绝收信息 编辑 后端接口
def edit_witherinfo():
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
    DPlantcareDeathinfo.query.filter_by(id=id).update(data)

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


@pest_control.route('/pest_control/immunizationinfo/edit', methods=['POST'])  # 施药记录 编辑 后端接口
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
    DPlantcareImmunizationinfo.query.filter_by(id=id).update(data)

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


@pest_control.route('/pest_control/protectioninfo/edit', methods=['POST'])  # 药浴免疫 编辑 后端接口
def edit_protectioninfo():
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
    DPlantcareProtectioninfo.query.filter_by(id=id).update(data)

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


@pest_control.route('/pest_control/diseaseinfo/edit', methods=['POST'])  # 疾病信息 编辑 后端接口
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
    DPlantcareDiseaseinfo.query.filter_by(id=id).update(data)

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


@pest_control.route('/pest_control/damageinfo/edit', methods=['POST'])  # 流产信息 编辑 后端接口
def edit_damageinfo():
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
    DPlantcareDamageinfo.query.filter_by(id=id).update(data)

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


@pest_control.route('/pest_control/immunizationinfo/del', methods=['POST'])  # 接种免疫 编辑 后端接口
def del_immunizationinfo():
    data = request.get_json()
    print("--data-->", data)
    # 这个表更新的话需要1个搜索条件
    id = data['id']
    print('--------------------------test--------------------------------')
    try:
        DPlantcareImmunizationinfo.query.filter_by(id=id).delete()
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
@pest_control.route('/pest_control/immunizationinfo/export', methods=['POST'])
def export_immunizationinfo():
    try:
        selected_ids = request.get_json()

        if selected_ids:
            immunization_info = DPlantcareImmunizationBS.query.filter(DPlantcareImmunizationBS.id.in_(selected_ids)).all()
        else:
            immunization_info = DPlantcareImmunizationBS.query.all()

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

        export_path = os.path.join(os.getcwd(), 'App', 'pest_control', 'export_excel', 'immunization_info.xlsx')
        df.to_excel(export_path, index=False)

        return send_file(export_path, as_attachment=True)
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'导出失败 {str(e)}'})


# 删除药浴免疫信息
@pest_control.route('/pest_control/protectioninfo/del', methods=['POST'])
def del_protectioninfo():
    ids = request.get_json()
    for i in ids:
        DPlantcareProtectioninfo.query.filter_by(id=i).delete()
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
@pest_control.route('/pest_control/protectioninfo/export', methods=['POST'])
def export_protectioninfo():
    try:
        selected_ids = request.get_json()

        if selected_ids:
            protection_info = (
                db.session.query(DPlantcareProtectioninfo, BasicBasicinfo.ele_num, BasicBasicinfo.pre_num,
                                 SupplyCommodityinfo.cname, SupplyVSuppliersinfo.supplier_name)
                    .outerjoin(BasicBasicinfo, BasicBasicinfo.id == DPlantcareProtectioninfo.basic_id)
                    .outerjoin(SupplyCommodityinfo, SupplyCommodityinfo.id == DPlantcareProtectioninfo.drug_id)
                    .outerjoin(SupplyVSuppliersinfo, SupplyVSuppliersinfo.id == DPlantcareProtectioninfo.vac_maker)
                    .filter(DPlantcareProtectioninfo.id.in_(selected_ids))
                    .all()
            )
        else:
            protection_info = (
                db.session.query(DPlantcareProtectioninfo, BasicBasicinfo.ele_num, BasicBasicinfo.pre_num,
                                 SupplyCommodityinfo.cname, SupplyVSuppliersinfo.supplier_name)
                    .outerjoin(BasicBasicinfo, BasicBasicinfo.id == DPlantcareProtectioninfo.basic_id)
                    .outerjoin(SupplyCommodityinfo, SupplyCommodityinfo.id == DPlantcareProtectioninfo.drug_id)
                    .outerjoin(SupplyVSuppliersinfo, SupplyVSuppliersinfo.id == DPlantcareProtectioninfo.vac_maker)
                    .all()
            )

        data_list = []
        for info, ele_num, pre_num, cname, supplier_name in protection_info:
            data_list.append({
                '草地编号': ele_num,
                '草地类型': pre_num,
                '药浴月龄': info.protection_age,
                '用药时间': info.take_time.isoformat() if info.take_time else None,
                '药品信息': cname,
                '药品厂家': supplier_name,
                '药效时间': info.timing,
                '创建时间': info.f_date.isoformat() if info.f_date else None,
                '创建人员': info.f_staff
            })
        df = pd.DataFrame(data_list)

        export_path = os.path.join(os.getcwd(), 'App', 'pest_control', 'export_excel', 'protection_info.xlsx')
        df.to_excel(export_path, index=False)

        return send_file(export_path, as_attachment=True)
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'导出失败 {str(e)}'})


# 删除检疫免疫信息
@pest_control.route('/pest_control/quarantineinfo/del', methods=['POST'])
def del_quarantineinfo():
    ids = request.get_json()
    for i in ids:
        DPlantcareQuarantineinfo.query.filter_by(id=i).delete()
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
@pest_control.route('/pest_control/quarantineinfo/export', methods=['POST'])
def export_quarantineinfo():
    try:
        selected_ids = request.get_json()

        if selected_ids:
            quarantine_info = (
                db.session.query(DPlantcareQuarantineinfo, BasicBasicinfo.ele_num, BasicBasicinfo.pre_num)
                    .outerjoin(BasicBasicinfo, BasicBasicinfo.id == DPlantcareQuarantineinfo.basic_id)
                    .filter(DPlantcareQuarantineinfo.id.in_(selected_ids))
                    .all()
            )
        else:
            quarantine_info = (
                db.session.query(DPlantcareQuarantineinfo, BasicBasicinfo.ele_num, BasicBasicinfo.pre_num)
                    .outerjoin(BasicBasicinfo, BasicBasicinfo.id == DPlantcareQuarantineinfo.basic_id)
                    .all()
            )

        d_plantcareDetection_modeType = {
            0: "目视检测",
            1: "实验室检测",
        }
        d_plantcareResult1Type = {
            0: "害虫未检出",
            1: "害虫已检出",
        }
        d_plantcareResult2Type = {
            0: "病害阴性",
            1: "病害阳性"
        }
        d_plantcareResult3Type = {
            0: "预警正常",
            1: "预警触发"
        }
        d_plantcareSituationType = {
            0: "允许正常生长",
            1: "需要施药",
            2: "隔离观察",
            3: "拔除销毁"
        }

        data_list = []
        for info, ele_num, pre_num in quarantine_info:
            detection_mode = d_plantcareDetection_modeType.get(info.detection_mode, " ")
            situation = d_plantcareSituationType.get(info.situation, " ")
            result1 = d_plantcareResult1Type.get(info.result1, " ")
            result2 = d_plantcareResult2Type.get(info.result2, " ")
            result3 = d_plantcareResult3Type.get(info.result3, " ")

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

        export_path = os.path.join(os.getcwd(), 'App', 'pest_control', 'export_excel', 'quarantine_info.xlsx')
        df.to_excel(export_path, index=False)

        return send_file(export_path, as_attachment=True)
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'导出失败 {str(e)}'})


# 删除护理信息
@pest_control.route('/pest_control/nursinginfo/del', methods=['POST'])
def del_nursinginfo():
    ids = request.get_json()
    for i in ids:
        DPlantcareNursinginfo.query.filter_by(id=i).delete()
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


@pest_control.route('/pest_control/nursinginfo/export', methods=['POST'])
def export_nursinginfo():
    try:
        selected_ids = request.get_json()

        if selected_ids:
            nursing_info = (
                db.session.query(DPlantcareNursinginfo, BasicBasicinfo.ele_num, BasicBasicinfo.pre_num)
                    .outerjoin(BasicBasicinfo, BasicBasicinfo.id == DPlantcareNursinginfo.basic_id)
                    .filter(DPlantcareNursinginfo.id.in_(selected_ids))
                    .all()
            )
        else:
            nursing_info = (
                db.session.query(DPlantcareNursinginfo, BasicBasicinfo.ele_num, BasicBasicinfo.pre_num)
                    .outerjoin(BasicBasicinfo, BasicBasicinfo.id == DPlantcareNursinginfo.basic_id)
                    .all()
            )

        d_plantcareTestis_shapeType = {
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
        d_plantcareAb_colorType = {
            0: "黄",
            1: "白",
            2: "红",
            3: "绿"
        }
        d_plantcareAb_smellType = {
            0: "正常",
            1: "血腥",
            2: "血臭"
        }

        data_list = []
        for info, ele_num, pre_num in nursing_info:
            dataroot_shape = d_plantcareTestis_shapeType.get(info.testis_shape, " ")
            dataprenatal_paralysi = prenatal_paralysi.get(info.prenatal_paralysi, " ")
            datauterus_fall = uterus_fall.get(info.uterus_fall, " ")
            dataswelling = swelling.get(info.swelling, " ")
            dataAb_color = d_plantcareAb_colorType.get(info.Ab_color, " ")
            dataAb_smell = d_plantcareAb_smellType.get(info.Ab_smell, " ")

            data_list.append({
                '草地编号': ele_num,
                '地块编号': pre_num,
                '养护时生长月数': info.age,
                '养护人员': info.nurse,
                '养护时间': info.nur_time.isoformat() if info.nur_time else None,
                '形态是否正常': dataroot_shape,
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

        export_path = os.path.join(os.getcwd(), 'App', 'pest_control', 'export_excel', 'nursing_info.xlsx')
        df.to_excel(export_path, index=False)

        return send_file(export_path, as_attachment=True)
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'导出失败 {str(e)}'})


@pest_control.route('/pest_control/diseaseinfo/del', methods=['POST'])
def del_diseaseinfo():
    ids = request.get_json()
    for i in ids:
        DPlantcareDiseaseinfo.query.filter_by(id=i).delete()
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


@pest_control.route('/pest_control/diseaseinfo/export', methods=['POST'])
def export_diseaseinfo():
    try:
        selected_ids = request.get_json()

        if selected_ids:
            disease_info = (
                db.session.query(DPlantcareDiseaseinfo, BasicBasicinfo.ele_num, BasicBasicinfo.pre_num,
                                 SupplyCommodityinfo.cname)
                    .outerjoin(BasicBasicinfo, BasicBasicinfo.id == DPlantcareDiseaseinfo.basic_id)
                    .outerjoin(SupplyCommodityinfo, SupplyCommodityinfo.id == DPlantcareDiseaseinfo.drug_id)
                    .filter(DPlantcareDiseaseinfo.id.in_(selected_ids))
                    .all()
            )
        else:
            disease_info = (
                db.session.query(DPlantcareDiseaseinfo, BasicBasicinfo.ele_num, BasicBasicinfo.pre_num,
                                 SupplyCommodityinfo.cname)
                    .outerjoin(BasicBasicinfo, BasicBasicinfo.id == DPlantcareDiseaseinfo.basic_id)
                    .outerjoin(SupplyCommodityinfo, SupplyCommodityinfo.id == DPlantcareDiseaseinfo.drug_id)
                    .all()
            )

        cur_effect = {
            0: "治愈",
            1: "淘汰",
            2: "枯萎"
        }
        data_list = []
        for info, ele_num, pre_num, cname in disease_info:
            datacur_effect = cur_effect.get(info.cur_effect, " ")
            data_list.append({
                '草地编号': ele_num,
                '草地类型': pre_num,
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

        export_path = os.path.join(os.getcwd(), 'App', 'pest_control', 'export_excel', 'disease_info.xlsx')
        df.to_excel(export_path, index=False)

        return send_file(export_path, as_attachment=True)
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'导出失败 {str(e)}'})


# 删除流产信息
@pest_control.route('/pest_control/damageinfo/del', methods=['POST'])
def del_damageinfo():
    ids = request.get_json()
    for i in ids:
        DPlantcareDamageinfo.query.filter_by(id=i).delete()
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
@pest_control.route('/pest_control/damageinfo/export', methods=['POST'])
def export_damageinfo():
    try:
        selected_ids = request.get_json()

        if selected_ids:
            damage_info = (
                db.session.query(DPlantcareDamageinfo, BasicBasicinfo.ele_num, BasicBasicinfo.pre_num)
                    .outerjoin(BasicBasicinfo, BasicBasicinfo.id == DPlantcareDamageinfo.basic_id)
                    .filter(DPlantcareDamageinfo.id.in_(selected_ids))
                    .all()
            )
        else:
            damage_info = (
                db.session.query(DPlantcareDamageinfo, BasicBasicinfo.ele_num, BasicBasicinfo.pre_num)
                    .outerjoin(BasicBasicinfo, BasicBasicinfo.id == DPlantcareDamageinfo.basic_id)
                    .all()
            )

        data_list = []
        for info, ele_num, pre_num in damage_info:
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

        export_path = os.path.join(os.getcwd(), 'App', 'pest_control', 'export_excel', 'damage_info.xlsx')
        df.to_excel(export_path, index=False)

        return send_file(export_path, as_attachment=True)
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'导出失败 {str(e)}'})
