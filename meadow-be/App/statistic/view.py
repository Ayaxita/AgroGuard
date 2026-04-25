# views.py: 路由 + 视图函数
import datetime
import random
import os
from flask import Blueprint, render_template, request, make_response, Response, redirect, url_for, session, jsonify, \
    send_file
from sqlalchemy import desc, and_, or_, not_, text, func
import pandas as pd

from ..basic.views import load_data_from_yaml
from ..modelsReverse import *
import json
from ..utils.AlchemyEncoder import AlchemyEncoder
from flask import Blueprint, request, jsonify
from sqlalchemy import and_, desc, or_
from datetime import datetime
import datetime as dt
import json
from docxtpl import DocxTemplate

import datetime
import os
import random
import json
import shutil
import yaml
from flask import Blueprint, render_template, request, make_response, Response, redirect, url_for, session, jsonify, \
    send_file
from flask_jwt_extended import jwt_required
from sqlalchemy import desc, and_, or_, not_, text
import pandas as pd

# from .models import *
from ..modelsReverse import *
from ..utils.AlchemyEncoder import AlchemyEncoder


Statistic = Blueprint('statistic', __name__)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

color_type = [
    {"label": "浅绿", "value": 0},
    {"label": "深绿", "value": 1},
    {"label": "黄绿", "value": 2},
    {"label": "混合色", "value": 3}
]

gene_a_type = [
    {"label": "抗虫型(RR)", "value": 0},
    {"label": "杂合型(Rr)", "value": 1},
    {"label": "感虫型(rr)", "value": 2},
    {"label": "未检测", "value": 3}
]

gene_b_type = [
    {"label": "抗病型A", "value": 0},
    {"label": "抗病型B", "value": 1},
    {"label": "感病型", "value": 2},
    {"label": "未检测", "value": 3}
]

gene_c_type = [
    {"label": "耐旱型A", "value": 0},
    {"label": "耐旱型B", "value": 1},
    {"label": "普通型", "value": 2},
    {"label": "未检测", "value": 3}
]

purpose_type = [
    {"label": "粮食作物", "value": 0},
    {"label": "经济作物", "value": 1},
    {"label": "饲草作物", "value": 2},
    {"label": "蔬菜作物", "value": 5},
    {"label": "牧草", "value": 6},
    {"label": "幼苗期作物", "value": 8}
]

rank_type = [
    {"label": "重度受灾", "value": 0},
    {"label": "中度受灾", "value": 1},
    {"label": "轻度受灾", "value": 2},
    {"label": "疑似受灾", "value": 3},
    {"label": "未评级", "value": 9}
]

sex_type = [
    {"label": "草本", "value": 1},
    {"label": "木本", "value": 0}
]

state_type = [
    {"label": "已淘汰", "value": -1},
    {"label": "绝收", "value": 0},
    {"label": "正常", "value": 1},
    {"label": "已处理", "value": 2}
]

variety_type = [
    {"label": "小麦", "value": 0},
    {"label": "玉米", "value": 1},
    {"label": "水稻", "value": 2},
    {"label": "大豆", "value": 3},
    {"label": "苜蓿", "value": 4},
    {"label": "黑麦草", "value": 5},
    {"label": "燕麦", "value": 6},
    {"label": "高粱", "value": 7},
    {"label": "谷子", "value": 8},
    {"label": "油菜", "value": 9},
    {"label": "其他", "value": 10}
]

result2_chocie=[
    {"label": "布病(阴性)", "value": 0},
    {"label": "布病(阳性)", "value": 1},
]
detection_mode_choice = [
    {"label": "尿检", "value": 0},
    {"label": "血检", "value": 1},
]
breeding_way_choices = [
    {"label": "自然交配", "value": 0},
    {"label": "人工辅助交配", "value": 1},
    {"label": "人工授精", "value": 2},
    {"label": "胚胎移植", "value": 3}
]

def generate_ele_num(pre_num, birth_date, variety_label):
    # 固定的前6位
    prefix = "131102"

    # 获取出生日期的后两位年份和月日
    year = str(birth_date.year)[2:]  # 获取年份的后两位
    month_day = birth_date.strftime("%m%d")  # 获取月日部分

    # 检查variety_label类型，如果是数字，直接使用
    if isinstance(variety_label, int):
        variety_value = variety_label
    elif isinstance(variety_label, str):
        # 如果是字符串，匹配字典
        variety_value = None
        for variety in variety_type:
            if variety['label'] == variety_label:
                variety_value = variety['value']
                break

        if variety_value is None:
            raise ValueError(f"未找到匹配的品种: {variety_label}")
    else:
        raise ValueError(f"variety_label 的类型不正确，应该是数字或字符串，当前类型为 {type(variety_label)}")

    # 拼接生成ele_num，直接将pre_num拼接
    ele_num = prefix + year + month_day + str(variety_value) + str(pre_num)  # 直接拼接pre_num

    return ele_num


@Statistic.route('/statistic/basicinfo', methods=['POST'])    #统计数据源
# 获取数据库数据
def get_basic_info():
    pageNum = int(request.json.get('pageNum'))
    # pageNum = int(request.form.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

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
        query = BasicBasicinfo.query.filter(and_(*conditions))
    else:
        query = BasicBasicinfo.query  # 如果没有条件，查询所有

    # 筛选出没有被移除的草(状态-1)和没有枯萎的草(状态0)
    # 并且根据id降序排列

    query = query.filter(and_(BasicBasicinfo.belong == 0))
    basic_infos = query.order_by(desc(BasicBasicinfo.id)).paginate(page=pageNum, per_page=pageSize, error_out=False)
    total = query.count()

    list = []
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
    # return jsonify({
    #     "method": 'GET'
    # })

@Statistic.route('/statistic/basicinfo/initHouseAndHurdle', methods=['POST'])
def initHouseAndHurdle():
    house_data = ColonyHouseinfo.query.filter_by(belong=0, pid=0).all()

    list = []
    for house in house_data:
        hurdle_data = ColonyHouseinfo.query.filter_by(pid=house.id)
        list.append({"house_id": house.id, "house_name": house.name,
                     "hurdle_list": [{"hurdle_id": hurdle.id, "hurdle_name": hurdle.name} for hurdle in hurdle_data]})
    result = {
        "code": 200,
        "data": {
            "list": list,
        },
        "msg": '棚舍列表获取成功'
    }
    return jsonify(result)


@Statistic.route('/statistic/basicinfo/initManu', methods=['POST'])
def initManu():
    manu_data = BasicManuinfo.query.filter_by(belong=0).all()

    list = []
    for manu in manu_data:
        list.append({"manu_info_id": manu.id, "manu_info_name": manu.manu_name})
    result = {
        "code": 200,
        "data": {
            "list": list,
        },
        "msg": '原产地列表获取成功'
    }
    return jsonify(result)

@Statistic.route('/statistic/basicinfo/grassTransfer', methods=['POST'])
def grassTransfer():
    datas = request.get_json()
    for data in datas:
        basic_info = BasicBasicinfo.query.filter_by(id=data['id']).first()
        basic_info.house_id = data['new_house_id']
        basic_info.house_name = data['new_house_name']
        basic_info.hurdle_id = data['new_hurdle_id']
        basic_info.hurdle_name = data['new_hurdle_name']
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        result = {
            "code": 500,
            "msg": f'转圈失败 {str(e)}'
        }
        return jsonify(result)
    result = {
        "code": 200,
        "msg": '转圈成功'
    }
    return jsonify(result)


@Statistic.route('/statistic/file/upload/img', methods=['POST'])
# 供新增和编辑时上传图片时调用
def upload_img():
    # 三个图片的标签
    files_to_check = ['img_positive', 'img_left', 'img_right']
    # file存储什么？
    file = None
    # 图片类型
    type = None
    # 遍历三个标签，找到第一个有值的标签
    for field_name in files_to_check:
        # print(f'field_name: {field_name}')
        file = request.files.get(field_name)
        # print(f'file: {file}')
        if file:
            type = field_name
            break

    file.filename = type + '-' + file.filename

    file_path = os.path.join(os.getcwd(), 'App', 'basic', 'img', file.filename)
    # print(f'file_path: {file_path}')
    file.save(file_path)
    result = {
        "code": 200,
        "data": {
            "fileUrl": file.filename,
        },
        "msg": '上传成功'
    }
    return jsonify(result)


@Statistic.route('/statistic/file/download/img', methods=['GET'])
def download_img():
    # print('download---------------------------------------')
    filename = request.args.get('filename')
    file_path = os.path.join(os.getcwd(), 'App', 'basic', 'img', filename)
    return send_file(file_path, as_attachment=True)


@Statistic.route('/statistic/basicinfo/detail', methods=['POST'])
def get_basic_info_detail():
    basic_info = BasicBasicinfo.query.filter_by(ele_num=request.json.get('ele_num')).first()
    # print(basic_info,request.json.get('ele_num'))
    # house_name
    data = json.dumps(basic_info, cls=AlchemyEncoder, ensure_ascii=False)
    data = json.loads(data)
    result = {
        "code": 200,
        "data": {
            "list": data
        },
        "msg": '成功'
    }
    return jsonify(result)


@Statistic.route('/statistic/basicinfo/addImmunization', methods=['POST'])
def add_Immunization():
    obj_list = []
    data = request.get_json()
    ctime = datetime.now()
    # data[0]["basic_id"] = 17646
    # print(data[0]["basic_id"])
    # print(data[0]["basic_info"]["id"])
    # 重新构建一下数据
    try:
        for i in range(len(data)):  # 循环遍历，需要增加的免疫信息
            immunizationinfo = DHealthImmunizationinfo()
            data[i]['f_date'] = ctime
            data[i]["basic_id"] = data[i]["basic_info"]["id"]
            data[i]["belong"] = data[i]["basic_info"]["belong"]
            data[i]["imm_age"] = round((
                                               datetime.now().date() - datetime.fromisoformat(
                                           data[i]["basic_info"]["birth"]).date()
                                       ).days / 30, 1)  # 更新月龄
            # 依次删除  title  basic_info
            if "title" in data[i]:
                del data[i]["title"]
            if "basic_info" in data[i]:
                del data[i]["basic_info"]
            if 'cname' in data[i]:
                supplycommodityinfo = SupplyCommodityinfo.query.filter_by(cname=data[i]['cname']).first()
            if 'supplier_name' in data[i]:
                supplyvsuppliersinfo = SupplyVSuppliersinfo.query.filter_by(
                    supplier_name=data[i]['supplier_name']).first()
            if supplycommodityinfo and supplyvsuppliersinfo:
                data[i]['vaccine_id'] = supplycommodityinfo.id
                data[i]['maker_id'] = supplyvsuppliersinfo.id
            else:
                return jsonify({"code": 500, "msg": f'没找到合适的疫苗信息和厂家信息'})
            # 在加入list之前要判断是否有数据冗余：同一个basic_id，疫苗类型，接种时间，
            dup_imminfo = DHealthImmunizationinfo.query.filter_by(basic_id=data[i]['basic_id'],
                                                                  vaccine_id=data[i]['vaccine_id'],
                                                                  imm_date=data[i]['imm_date']).first()
            if dup_imminfo:
                return jsonify({"code": 500, "msg": '存在数据冗余,添加失败'})
            for key, value in data[i].items():
                setattr(immunizationinfo, key, value)
            obj_list.append(immunizationinfo)
        # 将多个对象构建成数组   【 ， ， ， 】

    except Exception as e:
        result = {
            "code": 500,
            "msg": f'构建数据失败 {str(e)}'
        }
        return jsonify(result)

    # 这里是正常查询到进行的添加

    try:
        db.session.add_all(obj_list)
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
# http://127.0.0.1:5000/basic/basicinfo/add
@Statistic.route('/statistic/basicinfo/add', methods=['POST'])
def add_basic_info():
    data = request.get_json()
    print("--data-->", data)
    ctime = datetime.now()
    # belong为0
    data['belong'] = 0
    data['f_date'] = ctime
    data['state'] = 1
    # print(data)

    # 处理出生日期为 datetime 对象
    if isinstance(data.get('birth'), str):  # 检查是否为字符串
        data['birth'] = datetime.strptime(data['birth'], "%Y-%m-%d")  # 将字符串转为 datetime

    # 其他代码保持不变
    pre_num = data.get('pre_num')
    birth = data.get('birth')  # 现在是 datetime 对象
    variety = data.get('variety')

    if 'ele_num' not in data or not data['ele_num']:
        data['ele_num'] = generate_ele_num(pre_num, birth, variety)

    if 'img_positive' in data and data['img_positive'] != '':
        old_name = os.path.join(os.getcwd(), 'App', 'basic', 'img', data['img_positive'].split('=')[-1])
        new_name = os.path.join(os.getcwd(), 'App', 'basic', 'img',
                                data['ele_num'] + '-' + 'img_positive.' + data['img_positive'].split('.')[-1])
        os.rename(old_name, new_name)
        data['img_positive'] = data['ele_num'] + '-' + 'img_positive.' + data['img_positive'].split('.')[-1]

    if 'img_left' in data and data['img_left'] != '':
        old_name = os.path.join(os.getcwd(), 'App', 'basic', 'img', data['img_left'].split('=')[-1])
        new_name = os.path.join(os.getcwd(), 'App', 'basic', 'img',
                                data['ele_num'] + '-' + 'img_left.' + data['img_left'].split('.')[-1])
        os.rename(old_name, new_name)
        data['img_left'] = data['ele_num'] + '-' + 'img_left.' + data['img_left'].split('.')[-1]

    if 'img_right' in data and data['img_right'] != '':
        old_name = os.path.join(os.getcwd(), 'App', 'basic', 'img', data['img_right'].split('=')[-1])
        new_name = os.path.join(os.getcwd(), 'App', 'basic', 'img',
                                data['ele_num'] + '-' + 'img_right.' + data['img_right'].split('.')[-1])
        os.rename(old_name, new_name)
        data['img_right'] = data['ele_num'] + '-' + 'img_right.' + data['img_right'].split('.')[-1]

    # 在圈舍表中添加草地数量
    if request.json.get('house_id') is not None:
        house_info = ColonyHouseinfo.query.filter_by(id=request.json.get('house_id')).first()
        hurdle_info = ColonyHouseinfo.query.filter_by(id=request.json.get('hurdle_id')).first()
        if house_info.grass_quantity is None:
            house_info.grass_quantity = 1
            hurdle_info.grass_quantity = 1
        else:
            house_info.grass_quantity += 1
            hurdle_info.grass_quantity += 1
    basic_info = BasicBasicinfo()
    if data['f_ele_num'] == '000000000000000':
        basic_info.father_id = 0
        basic_info.mother_id = BasicBasicinfo.query.filter_by(ele_num=data['m_ele_num']).first().id
    elif data['m_ele_num'] == '000000000000000':
        basic_info.mother_id = 0
        basic_info.father_id = BasicBasicinfo.query.filter_by(ele_num=data['f_ele_num']).first().id
    else:
        basic_info.father_id = BasicBasicinfo.query.filter_by(ele_num=data['f_ele_num']).first().id
        basic_info.mother_id = BasicBasicinfo.query.filter_by(ele_num=data['m_ele_num']).first().id
    for key, value in data.items():
        setattr(basic_info, key, value)
    try:
        db.session.add(basic_info)
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


@Statistic.route('/statistic/basicinfo/validateGrassNum', methods=['POST'])
def validate_grass_num():
    prop = request.json.get('prop')
    value = request.json.get('value')
    if prop == 'ele_num':
        if BasicBasicinfo.query.filter_by(ele_num=value).first():
            result = {
                "code": 200,
                'realcode': 500,
                "msg": '草地编号已存在'
            }
            return jsonify(result)
    elif prop == 'pre_num':
        if BasicBasicinfo.query.filter_by(pre_num=value).first():
            result = {
                "code": 200,
                'realcode': 500,
                "msg": '地块编号已存在'
            }
            return jsonify(result)
    elif prop == 'f_ele_num':
        if value == '000000000000000':
            result = {
                "code": 200,
                'realcode': 200,
                'data': {
                    'f_pre_num': 0,
                },
                "msg": '父不在草场中,验证成功'
            }
            return jsonify(result)
        info = BasicBasicinfo.query.filter_by(ele_num=value).first()
        if info is None:
            result = {
                "code": 200,
                'realcode': 500,
                "msg": '父本草地编号不存在'
            }
            return jsonify(result)
        else:
            result = {
                "code": 200,
                'realcode': 200,
                'data': {
                    'f_pre_num': info.pre_num,
                },
                "msg": '父本草地编号存在, 验证成功'
            }
            return jsonify(result)
    elif prop == 'f_pre_num' and value != '0':
        info = BasicBasicinfo.query.filter_by(pre_num=value).first()
        if info is None:
            result = {
                "code": 200,
                'realcode': 500,
                "msg": '父本地块编号不存在'
            }
            return jsonify(result)
    elif prop == 'm_ele_num':
        if value == '000000000000000':
            result = {
                "code": 200,
                'realcode': 200,
                'data': {
                    'm_pre_num': 0,
                },
                "msg": '母不在草场中,验证成功'
            }
            return jsonify(result)
        info = BasicBasicinfo.query.filter_by(ele_num=value).first()
        if info is None:
            result = {
                "code": 200,
                'realcode': 500,
                "msg": '母本草地编号不存在'
            }
            return jsonify(result)
        else:
            result = {
                "code": 200,
                'realcode': 200,
                'data': {
                    'm_pre_num': info.pre_num,
                },
                "msg": '母本草地编号存在, 验证成功'
            }
            return jsonify(result)
    elif prop == 'm_pre_num' and value != '0':
        info = BasicBasicinfo.query.filter_by(pre_num=value).first()
        if info is None:
            result = {
                "code": 200,
                'realcode': 500,
                "msg": '母本地块编号不存在'
            }
            return jsonify(result)
    result = {
        "code": 200,
        'realcode': 200,
        "msg": '验证成功'
    }
    return jsonify(result)


# http://127.0.0.1:5000/basic/basicinfo/edit
@Statistic.route('/statistic/basicinfo/edit', methods=['POST'])
def edit_basic_info():
    data = request.get_json()
    # print("--data-->", data)
    ele_num = data['ele_num']
    #在标记淘汰的过程，把棚舍更改为淘汰舍
    if data['state']:
        state = data['state']
        if (state == -1):
            dieoutHurdle_info = ColonyHouseinfo.query.filter_by(name="淘汰栏").first()
            dieoutHouse_info = ColonyHouseinfo.query.filter_by(id=dieoutHurdle_info.pid).first()
            data['house_id'] = dieoutHouse_info.id
            data['house_name'] = dieoutHouse_info.name
            data['hurdle_id'] = dieoutHurdle_info.id
            data['hurdle_name'] = dieoutHurdle_info.name
    # print('--------------------------test--------------------------------')
    # print(data['img_positive'])
    # print(data['img_left'])
    # print(data['img_right'])

    if 'img_positive' in data and data['img_positive'] is not None and data['img_positive'] != '':
        old_name = os.path.join(os.getcwd(), 'App', 'basic', 'img', data['img_positive'].split('=')[-1])
        new_name = os.path.join(os.getcwd(), 'App', 'basic', 'img',
                                data['ele_num'] + '-' + 'img_positive.' + data['img_positive'].split('.')[-1])
        # print('ooooooooooookkkkkkkkkk')
        shutil.move(old_name, new_name)
        data['img_positive'] = data['ele_num'] + '-' + 'img_positive.' + data['img_positive'].split('.')[-1]

    if 'img_left' in data and data['img_left'] is not None and data['img_left'] != '':
        old_name = os.path.join(os.getcwd(), 'App', 'basic', 'img', data['img_left'].split('=')[-1])
        new_name = os.path.join(os.getcwd(), 'App', 'basic', 'img',
                                data['ele_num'] + '-' + 'img_left.' + data['img_left'].split('.')[-1])
        shutil.move(old_name, new_name)
        data['img_left'] = data['ele_num'] + '-' + 'img_left.' + data['img_left'].split('.')[-1]

    if 'img_right' in data and data['img_right'] is not None and data['img_right'] != '':
        old_name = os.path.join(os.getcwd(), 'App', 'basic', 'img', data['img_right'].split('=')[-1])
        new_name = os.path.join(os.getcwd(), 'App', 'basic', 'img',
                                data['ele_num'] + '-' + 'img_right.' + data['img_right'].split('.')[-1])
        shutil.move(old_name, new_name)
        data['img_right'] = data['ele_num'] + '-' + 'img_right.' + data['img_right'].split('.')[-1]


    # 在修改基本信息表时，更新成坪信息到新草地表和成坪信息表
    #这里防止报错加了一个逻辑，先判断有没有新草地和成坪信息（）因为外购肯定没有，所以很有必要加这个判断
    birth = data['birth']
    bir_weighht = data['bir_weight']
    wea_weight = data['wea_weight']
    wea_date = data['wea_date']

    lamb_info = db.session.query(EBreedLambinfo).filter_by(pre_num=data['pre_num']).first()
    if lamb_info:
        lamb_id = lamb_info.id
        lamb_info.wea_weight = wea_weight
        lamb_info.wea_date = wea_date
        lamb_info.birth = birth
        lamb_info.bir_weight = bir_weighht
        db.session.commit()

        weaning_info = db.session.query(EBreedWeaninginfo).filter_by(lamb_id=lamb_id).first()

        if weaning_info:
                weaning_info.wea_weight = wea_weight
                weaning_info.Delivery_date = wea_date
                weaning_info.Bir_weight = bir_weighht
                db.session.commit()
    else:
        # 当 lamb_info 为 None 时，不执行依赖 lamb_id 的操作
        pass
    try:
        BasicBasicinfo.query.filter_by(ele_num=ele_num).update(data)
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


# 系谱
@Statistic.route('/statistic/basicinfo/familyTree', methods=['POST'])
def get_family_tree():
    def get_family_member_info(member):
        if member:
            return {
                "id": member.id,
                "ele_num": member.ele_num,
                "birth": member.birth.isoformat(),
                "variety": member.variety,
                "img_positive": member.img_positive,
            }
        return None

    basic_info = BasicBasicinfo.query.filter(BasicBasicinfo.id == int(request.json.get('id'))).first()

    father_info = BasicBasicinfo.query.filter(BasicBasicinfo.id == basic_info.father_id).first()
    mother_info = BasicBasicinfo.query.filter(BasicBasicinfo.id == basic_info.mother_id).first()
    grandfather_info = BasicBasicinfo.query.filter(
        BasicBasicinfo.id == father_info.father_id).first() if father_info else None
    grandmother_info = BasicBasicinfo.query.filter(
        BasicBasicinfo.id == father_info.mother_id).first() if father_info else None
    maternal_grandfather_info = BasicBasicinfo.query.filter(
        BasicBasicinfo.id == mother_info.father_id).first() if mother_info else None
    maternal_grandmother_info = BasicBasicinfo.query.filter(
        BasicBasicinfo.id == mother_info.mother_id).first() if mother_info else None

    family_tree = {
        "selected_grass": get_family_member_info(basic_info),
        "father": get_family_member_info(father_info),
        "mother": get_family_member_info(mother_info),
        "grandfather": get_family_member_info(grandfather_info),
        "grandmother": get_family_member_info(grandmother_info),
        "maternal_grandfather": get_family_member_info(maternal_grandfather_info),
        "maternal_grandmother": get_family_member_info(maternal_grandmother_info),
    }

    return jsonify(family_tree)


# 导出
@Statistic.route('/statistic/basicinfo/export', methods=['POST'])
def export_basic_info():
    key_value = load_data_from_yaml()
    query = BasicBasicinfo.query.filter(BasicBasicinfo.state != -1)
    basic_infos = query.order_by(desc(BasicBasicinfo.f_date))
    # total = query.count()
    list = []
    for info in basic_infos:
        purpose_value = key_value["purpose"].get(info.purpose, None)
        variety_value = key_value["variety"].get(info.variety, None)
        color_value = key_value["color_type"].get(info.color, None)
        sex_value = key_value["sex_type"].get(info.sex, None)
        state_value = key_value["state_type"].get(info.state, None)
        rank_value = key_value["rank_type"].get(info.rank, None)
        gen_a_value = key_value["gene_a_type"].get(info.gene_a, None)
        gen_b_value = key_value["gene_b_type"].get(info.gene_b, None)
        gen_c_value = key_value["gene_c_type"].get(info.gene_c, None)
        list.append({
            '草地编号': info.ele_num,
            '地块编号': info.pre_num,
            '用途': purpose_value,
            '草地类型': variety_value,
            '草地颜色': color_value,
            '作物类型': sex_value,
            '种植日期': info.birth.isoformat() if info.birth else None,
            '生长月数': info.mon_age,
            '原产地': info.manu_info_name,
            '状态': state_value,
            '所属监测区域': info.house_name,
            '监测地块': info.hurdle_name,
            '出生体重(kg)': info.bir_weight,
            '成坪重(kg)': info.wea_weight,
            '受灾等级': rank_value,
            '父草地编号': info.f_ele_num,
            '父地块编号': info.f_pre_num,
            '母草地编号': info.m_ele_num,
            '母地块编号': info.m_pre_num,
            '录入人员': info.f_staff,
            '创建日期': info.f_date.isoformat() if info.f_date else None,
            '正面照片': info.img_positive,
            '左侧照片': info.img_left,
            '右侧照片': info.img_right,
            '备注': info.note,
            '抗虫基因': gen_a_value,
            '抗病基因': gen_b_value,
            '耐旱基因': gen_c_value,
            '综合评分': info.score,
            '2月生长评分': info.score_2,
            '6月生长评分': info.score_6,
            '12月生长评分': info.score_12,
            '24月生长评分': info.score_24
        })
    dataframes = pd.DataFrame(list)
    # filename = r'.\App\basic\export_excel\basic_info.xlsx'
    filename = os.path.join(os.getcwd(), 'App', 'statistic', 'export_excel', 'basic_info.xlsx')
    # export_filename = r'.\basic\export_excel\basic_info.xlsx'
    export_filename = os.path.join(os.getcwd(), 'App', 'statistic', 'export_excel', 'basic_info.xlsx')
    dataframes.to_excel(filename, index=False)
    return send_file(export_filename, as_attachment=True)


@Statistic.route('/statistic/basicinfo/import_template', methods=['POST'])
def import_template():
    filename = os.path.join(os.getcwd(), 'App', 'basic', 'temp_excel', '草地基本信息导入模板.xls')
    return send_file(filename, as_attachment=True)


#批量导入
@Statistic.route('/statistic/basicinfo/import', methods=['POST'])
def import_basic_info():

    file_path = os.path.join(os.getcwd(), 'App', 'statistic', 'imported_excel', request.files['file'].filename)
    file = request.files['file']
    # print(request.files)
    file.save(file_path)
    df = pd.read_excel(file)

    # 生成ele_num的函数
    def generate_ele_num(pre_num, birth_date, variety_label):
        # 固定的前6位
        prefix = "131102"

        # # 获取当前日期的后两位年份和月日
        # current_date = datetime.now()
        # year = str(current_date.year)[2:]  # 获取年份的后两位
        # month_day = current_date.strftime("%m%d")  # 获取月日部分
        # 获取出生日期的后两位年份和月日
        year = str(birth_date.year)[2:]  # 获取年份的后两位
        month_day = birth_date.strftime("%m%d")  # 获取月日部分

        # 获取variety的对应value
        variety_value = None
        for variety in variety_type:
            if variety['label'] == variety_label:
                variety_value = variety['value']
                break

        if variety_value is None:
            raise ValueError(f"未找到匹配的品种: {variety_label}")

            # 拼接生成ele_num，直接将pre_num拼接
        ele_num = prefix + year + month_day + str(variety_value) + str(pre_num)  # 直接拼接pre_num

        return ele_num

    try:
        list = []
        for r in range(len(df)):
            basic_info = BasicBasicinfo()
            # basic_info.ele_num = df.iloc[r, 0]
            # 如果没有ele_num，根据pre_num生成ele_num
            # if not df.iloc[r, 0]:  # 如果ele_num为空
            if pd.isna(df.iloc[r, 0]) or df.iloc[r, 0] == '':
                print('--------------------------------')
                # basic_info.ele_num = generate_ele_num(df.iloc[r, 1], df.iloc[r, 2])  # 根据pre_num和variety生成ele_num
                birth_date = df.iloc[r, 9]  # 获取出生日期
                variety_label = df.iloc[r, 2]  # 获取品种标签
                pre_num = df.iloc[r, 1]  # 获取地块编号
                basic_info.ele_num = generate_ele_num(pre_num, birth_date, variety_label)  # 根据birth和variety生成ele_num
            else:
                print('----111++++++++++++++++++++++++++++')
                basic_info.ele_num = df.iloc[r, 0]  # 保留Excel中已有的ele_num

            basic_info.pre_num = df.iloc[r, 1]

            for i in purpose_type:
                if i['label'] == df.iloc[r, 4]:
                    basic_info.purpose = i['value']
            for i in variety_type:
                if i['label'] == df.iloc[r, 2]:
                    basic_info.variety = i['value']
            for i in sex_type:
                if i['label'] == df.iloc[r, 3]:
                    basic_info.sex = i['value']
            # 来源填什么?
            basic_info.manu_info_id = BasicManuinfo.query.filter_by(manu_name=df.iloc[r, 5]).first().id
            basic_info.manu_info_name = df.iloc[r, 5]
            for i in state_type:
                if i['label'] == df.iloc[r, 6]:
                    basic_info.state = i['value']
            # 时间如果是Timestamp
            # 时间如果是str

            if type(df.iloc[r, 9]) == str:
                basic_info.birth = datetime.strptime(df.iloc[r, 9], '%Y/%m/%d')
            else:
                basic_info.birth = df.iloc[r, 9]
            basic_info.bir_weight = df.iloc[r, 10]
            basic_info.wea_weight = df.iloc[r, 11]
            basic_info.house_id = ColonyHouseinfo.query.filter_by(name=df.iloc[r, 7]).first().id
            basic_info.house_name = df.iloc[r, 7]
            basic_info.hurdle_id = ColonyHouseinfo.query.filter_by(name=df.iloc[r, 8]).first().id
            basic_info.hurdle_name = df.iloc[r, 8]
            basic_info.mon_age = df.iloc[r, 12]
            # 如果父母id在数据库里没有怎么办,
            # 如果一个一个提交到数据库然后找id,但是excel里是乱序的儿子在父亲前面怎么办
            # 分两步,先不填父母id,数据库提交完成后填
            # basic_info.father_id = BasicBasicinfo.query.filter_by(ele_num=df.iloc[r, 15]).first().id
            # basic_info.mother_id = BasicBasicinfo.query.filter_by(ele_num=df.iloc[r, 17]).first().id
            basic_info.f_ele_num = df.iloc[r, 15]
            basic_info.f_pre_num = df.iloc[r, 16]
            basic_info.m_ele_num = df.iloc[r, 17]
            basic_info.m_pre_num = df.iloc[r, 18]
            # basic_info.f_staff = df.iloc[0, 17]
            basic_info.f_date = datetime.now()
            # basic_info.note = df.iloc[0, 19]
            basic_info.belong = 0
            for i in color_type:
                if i['label'] == df.iloc[r, 13]:
                    basic_info.color = i['value']
            for i in rank_type:
                if i['label'] == df.iloc[r, 14]:
                    basic_info.rank = i['value']
            for i in gene_a_type:
                if i['label'] == df.iloc[r, 19]:
                    basic_info.gene_a = i['value']
            for i in gene_b_type:
                if i['label'] == df.iloc[r, 20]:
                    basic_info.gene_b = i['value']
            for i in gene_c_type:
                if i['label'] == df.iloc[r, 21]:
                    basic_info.gene_c = i['value']
            list.append(basic_info)

        db.session.add_all(list)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        result = {
            'code': 500,
            'msg': f'导入失败 {str(e)}'
        }
        return jsonify(result)

    # 填父母id
    basic_infos = BasicBasicinfo.query.filter(
        or_(BasicBasicinfo.father_id == None, BasicBasicinfo.mother_id == None)).all()
    for info in basic_infos:
        father = BasicBasicinfo.query.filter_by(ele_num=info.f_ele_num).first()
        mother = BasicBasicinfo.query.filter_by(ele_num=info.m_ele_num).first()
        if father is not None:
            info.father_id = father.id
        # else:
        #     info.father_id = 0
        if mother is not None:
            info.mother_id = mother.id
        # else:
        #     info.mother_id = 0
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        result = {
            "code": 500,
            "msg": f'父母id填入失败 {str(e)}'
        }
        return jsonify(result)
    result = {
        "code": 200,
        "msg": '导入成功'
    }
    return jsonify(result)



# 更新月龄
@Statistic.route('/statistic/basicinfo/updateMonAge', methods=['POST'])
def update_mon_age():
    # basic_infos = BasicBasicinfo.query.filter(BasicBasicinfo.state != -1)
    # for info in basic_infos:
    #     info.mon_age = round((datetime.now().date() - info.birth).days / 30, 1)
    query = '''
    UPDATE basic_basicinfo set mon_age = ROUND((DATEDIFF(CURRENT_DATE,basic_basicinfo.birth)/30),1) WHERE basic_basicinfo.state !=-1
    '''
    try:
        db.session.execute(text(query))
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        result = {
            "code": 500,
            "msg": f'更新月龄失败 {str(e)}'
        }
        return jsonify(result)
    result = {
        "code": 200,
        "msg": '更新月龄成功'
    }
    return jsonify(result)


@Statistic.route('/statistic/basicinfo/updateHouseAndHurdle', methods=['POST'])
def update_house_and_hurdle():
    colony_infos = ColonyHouseinfo.query.all()
    for info in colony_infos:
        if info.pid == 0:
            info.grass_quantity = BasicBasicinfo.query.filter_by(house_id=info.id).count()
        else:
            info.grass_quantity = BasicBasicinfo.query.filter_by(hurdle_id=info.id).count()
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        result = {
            "code": 500,
            "msg": f'更新圈舍失败 {str(e)}'
        }
        return jsonify(result)
    result = {
        "code": 200,
        "msg": '更新圈舍成功'
    }
    return jsonify(result)


# 标记绝收
@Statistic.route('/statistic/basicinfo/markGrassDeath', methods=['POST'])
def mark_grass_death():
    basic_infos = request.get_json()
    print(basic_infos)
    list = []
    deathHurdle_info = ColonyHouseinfo.query.filter_by(name="死亡栏").first()
    deathHouse_info = ColonyHouseinfo.query.filter_by(id=deathHurdle_info.pid).first()
    for info in basic_infos:
        print(info)
        BasicBasicinfo.query.filter_by(id=info['basic_id']).update(
            {'state': 0,'house_id':deathHouse_info.id,'house_name':deathHouse_info.name,
             'hurdle_id':deathHurdle_info.id,'hurdle_name':deathHurdle_info.name})
        # 查找并更新 BasicObsoleteGrassinfo 表的记录
        obsolete_info = BasicObsoleteGrassinfo.query.filter_by(basic_id=info['basic_id']).first()
        print(obsolete_info)
        if obsolete_info:
            obsolete_info.obsolete_type = 0
            obsolete_info.dead_date = info['date']
            # db.session.commit()
        death_info = DHealthDeathinfo()
        for key, value in info.items():
            setattr(death_info, key, value)
            death_info.belong = 0
            death_info.f_date = datetime.now()
            death_info.age = (datetime.now().year - BasicBasicinfo.query.filter_by(
                id=info['basic_id']).first().birth.year)
        list.append(death_info)
    try:
        db.session.add_all(list)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        result = {
            "code": 500,
            "msg": f'标记绝收失败 {str(e)}'
        }
        return jsonify(result)
    result = {
        "code": 200,
        "msg": '标记绝收成功'
    }
    return jsonify(result)



# 标记已处理
@Statistic.route('/statistic/basicinfo/markGrassSale', methods=['POST'])
def mark_grass_sale():
    basic_infos = request.get_json()
    print(basic_infos)
    list = []
    saleHurdle_info = ColonyHouseinfo.query.filter_by(name="销售栏").first()
    saleHouse_info = ColonyHouseinfo.query.filter_by(id=saleHurdle_info.pid).first()
    today = datetime.today()

    for info in basic_infos:
        print(info)
        BasicBasicinfo.query.filter_by(id=info['basic_id']).update(
            {'state': 2, 'house_id': saleHouse_info.id, 'house_name': saleHouse_info.name,
             'hurdle_id': saleHurdle_info.id, 'hurdle_name': saleHurdle_info.name})

        # 查找并更新 BasicObsoleteGrassinfo 表的记录
        obsolete_info = BasicObsoleteGrassinfo.query.filter_by(basic_id=info['basic_id']).first()
        print(obsolete_info)
        if obsolete_info:
            obsolete_info.obsolete_type = 2
            obsolete_info.sales_date = info['sales_date']
            # db.session.commit()
        sales_info = GSlaughterSSalesinfo()
        for key, value in info.items():
            setattr(sales_info, key, value)

            # 获取 basic_id 对应的 BasicBasicinfo 记录
            basic_info = BasicBasicinfo.query.filter_by(id=info['basic_id']).first()

            if basic_info:
                sales_info.ele_num = basic_info.ele_num
                sales_info.belong = 0

                # 计算月龄
                if basic_info.birth:
                    birth_date = basic_info.birth
                    age_in_months = (today.year - birth_date.year) * 12 + (today.month - birth_date.month)
                    sales_info.age = age_in_months  # 存入 GSlaughterSSalesinfo

            list.append(sales_info)
            # sales_info.belong = 0
            # sales_info.ele_num = BasicBasicinfo.query.filter_by(id=info['basic_id']).first().ele_num

    try:
        db.session.add_all(list)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        result = {
            "code": 500,
            "msg": f'标记售出失败 {str(e)}'
        }
        return jsonify(result)
    result = {
        "code": 200,
        "msg": '标记售出成功'
    }
    return jsonify(result)


def fun(param):
    id1 = param.id
    return id1


# http://127.0.0.1:5000/basic/basicinfo/update_grandparents
@Statistic.route('/basic/basicinfo/update_grandparents', methods=['POST'])
def update_grandparents():
    # 查询 BasicBasicinfo 表中的所有记录
    all_records = BasicBasicinfo.query.all()
    print(all_records)

    # 如果没有找到任何记录，返回404错误
    if not all_records:
        return jsonify({"code": 404, "msg": "获取记录出错"})

    total_rows_affected = 0  # 初始化计数器

    try:
        for record in all_records:
            # 获取父母ID
            father_id = record.father_id if record.father_id else 0
            mother_id = record.mother_id if record.mother_id else 0

            # 初始化祖父母信息为默认值
            father_grandfather_id = 0
            father_grandfather_ele_num = "0000000000000000"
            father_grandfather_pre_num = "00000000000"

            father_grandmother_id = 0
            father_grandmother_ele_num = "0000000000000000"
            father_grandmother_pre_num = "00000000000"

            mother_grandfather_id = 0
            mother_grandfather_ele_num = "0000000000000000"
            mother_grandfather_pre_num = "00000000000"

            mother_grandmother_id = 0
            mother_grandmother_ele_num = "0000000000000000"
            mother_grandmother_pre_num = "00000000000"

            # 查询父亲的父母（祖父母）信息
            if father_id != 0:
                father_record = BasicBasicinfo.query.filter_by(id=father_id).first()
                if father_record:
                    # 父亲的父信息（祖父）
                    father_grandfather_id = father_record.father_id if father_record.father_id else 0
                    father_grandfather_ele_num = father_record.f_ele_num if father_record.f_ele_num else "0000000000000000"
                    father_grandfather_pre_num = father_record.f_pre_num if father_record.f_pre_num else "00000000000"

                    # 父亲的母信息（祖母）
                    father_grandmother_id = father_record.mother_id if father_record.mother_id else 0
                    father_grandmother_ele_num = father_record.m_ele_num if father_record.m_ele_num else "0000000000000000"
                    father_grandmother_pre_num = father_record.m_pre_num if father_record.m_pre_num else "00000000000"

            # 查询母亲的父母（祖父母）信息
            if mother_id != 0:
                mother_record = BasicBasicinfo.query.filter_by(id=mother_id).first()
                if mother_record:
                    # 母亲的父信息（祖父）
                    mother_grandfather_id = mother_record.father_id if mother_record.father_id else 0
                    mother_grandfather_ele_num = mother_record.f_ele_num if mother_record.f_ele_num else "0000000000000000"
                    mother_grandfather_pre_num = mother_record.f_pre_num if mother_record.f_pre_num else "00000000000"

                    # 母亲的母信息（祖母）
                    mother_grandmother_id = mother_record.mother_id if mother_record.mother_id else 0
                    mother_grandmother_ele_num = mother_record.m_ele_num if mother_record.m_ele_num else "0000000000000000"
                    mother_grandmother_pre_num = mother_record.m_pre_num if mother_record.m_pre_num else "00000000000"

            # 更新当前记录的祖父母信息
            rows_affected = BasicBasicinfo.query.filter_by(id=record.id).update({
                'ram_grandfather_id': father_grandfather_id,
                'ram_grandfather_ele_num': father_grandfather_ele_num,
                'ram_grandfather_pre_num': father_grandfather_pre_num,
                'ewe_grandfather_id': mother_grandfather_id,
                'ewe_grandfather_ele_num': mother_grandfather_ele_num,
                'ewe_grandfather_pre_num': mother_grandfather_pre_num,
                'ram_grandmother_id': father_grandmother_id,
                'ram_grandmother_ele_num': father_grandmother_ele_num,
                'ram_grandmother_pre_num': father_grandmother_pre_num,
                'ewe_grandmother_id': mother_grandmother_id,
                'ewe_grandmother_ele_num': mother_grandmother_ele_num,
                'ewe_grandmother_pre_num': mother_grandmother_pre_num
            })
            total_rows_affected += rows_affected  # 累加影响行数

        # 提交事务
        db.session.commit()
        print(f'提交了！！！！！！！！！ 总影响行数：{total_rows_affected}')

        result = {
            "code": 200,
            "msg": f'更新成功，总影响行数：{total_rows_affected}'
        }
        return jsonify(result)

    except Exception as e:
        # 出现异常时回滚
        db.session.rollback()
        print(f"更新失败: {str(e)}")
        result = {
            "code": 500,
            "msg": f'更新失败 {str(e)}'
        }
        return jsonify(result)













# —————————————————————————————————————以下是根据1.0系谱档案的代码更改成的flask的代码，应该能用，报错不知道咋解决，反正能打分和传递数据了————————————————————————————————————————

@Statistic.route('/statistic/makescore', methods=['POST'])     #草地评分标准
def get_makescoreTable():
    # pageNum = int(request.json.get('pageNum'))
    # pageNum = 1
    # # pageNum = int(request.form.get('pageNum'))
    # # pageSize = int(request.json.get('pageSize'))
    # pageSize = 12
    # 分页不用了，只返回数据
    conditions = []
    search_params = {
        'variety': BasicMakescore.variety,
        'sex': BasicMakescore.sex,
        'gene_a': BasicMakescore.gene_a,
        'small_rum': BasicMakescore.small_rum,
        'fmd': BasicMakescore.fmd,
        'grass_pox': BasicMakescore.grass_pox,
        'tnq': BasicMakescore.tnq,
        'brucella':BasicMakescore.brucella,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            conditions.append(column == value)

        # 使用 and_() 组合条件
    if conditions:
        query = BasicMakescore.query.filter(and_(*conditions))
    else:
        query = BasicMakescore.query  # 如果没有条件，查询所有

    # 筛选出没有被移除的草(状态-1)和没有枯萎的草(状态0)
    # 并且根据id降序排列

    # 并且根据id降序排列

    query = query.filter(BasicMakescore.belong == 0)
    infos = query.order_by(desc(BasicMakescore.id)).paginate(error_out=False)
    # total = query.count()

    list = []
    for info in infos:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        data = json.loads(data)
        list.append(data)
    result = {
        "code": 200,
        "data": {
            "list": list,
            # "pageNum": pageNum,
            # "pageSize": pageSize,
            # "total": total
        },
        "msg": '成功'
    }
    return jsonify(result)


@Statistic.route('/statistic/makescore/edit', methods=['POST'])   #修改草地评分标准
def edit_makescore():
    data = request.get_json()
    print("--data-->", data)
    id = data['id']
    # ele_id = data['ele_num']
    # pre_id = data['pre_num']

    # BasicBasicinfo.query.filter_by(ele_id = ele_id,pre_id = pre_id).update(data)
    try:
        # 更新草地生长监测信息表
        BasicMakescore.query.filter_by(id=id).update(data)
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



@Statistic.route('/statistic/xipu/scoremake', methods=['POST'])     #草地打分逻辑
def scoremake(basic_id):
        # 1. 参数校验
        # req_data = request.get_json()
        # print(req_data)
        # if not req_data or 'basic_id' not in req_data:
        #     return jsonify({"code": 400, "msg": "参数错误: 缺少basic_id"}), 400
        #
        # basic_id = req_data['basic_id']

        basic = db.session.query(BasicBasicinfo).filter(BasicBasicinfo.id == basic_id).first()
        breeder = db.session.query(BasicBreederconditioninfo).filter(
            BasicBreederconditioninfo.basic_id == basic_id).first()
        first = db.session.query(BasicBreederconditioninfo).filter(
            BasicBreederconditioninfo.basic_id == basic_id).order_by(BasicBreederconditioninfo.age).all()
        postnatal = []
        lambs = []

        immu = db.session.query(DHealthImmunizationinfo).filter(DHealthImmunizationinfo.basic_id == basic_id).all()
        quar = db.session.query(DHealthQuarantineinfo).filter(DHealthQuarantineinfo.basic_id == basic_id).all()

        together_num = 1
        if basic:
            lamb_self = db.session.query(EBreedLambinfo).filter(EBreedLambinfo.basic_id == basic_id).first()
            if lamb_self:  # 如果新草地信息表中存在该basic_id
                breed_id = lamb_self.breeding_id  # 获取培育信息id
                postna = db.session.query(EBreedPostnatalinfo).filter(
                    EBreedPostnatalinfo.breeding_id == breed_id).first()  # 获取self的生长记录
                postnatal = db.session.query(EBreedPostnatalinfo).filter(
                    EBreedPostnatalinfo.breeding_id == breed_id).all()
                lambs = db.session.query(EBreedLambinfo).filter(EBreedLambinfo.breeding_id == breed_id).all()

                if postna:
                    together_num = postna.live_num  # 获取self的出生数
        score_all = 0
        basic_score = 0
        benshen_score = 0
        houyi_score = 0
        fangyi_score = 0

        mu = True
        Bplus = False
        if basic:
            variety = basic.variety
            sex = basic.sex
            gene_a = basic.gene_a
            if sex == 0:
                mu = False
            if gene_a != 2 or gene_a is None:
                standard = db.session.query(BasicMakescore).filter(
                    or_(
                        and_(
                            BasicMakescore.variety == variety,
                            BasicMakescore.sex == sex
                        ),
                        BasicMakescore.gene_a == gene_a
                    )
                ).first()
                if gene_a == 1:
                    Bplus = True
            else:
                return [0, 0, 0, 0, 60, False]

        if together_num >= 2:
            basic_score += 2

        eryue = False
        if len(first) == 0:
            benshen_score += 30
            eryue = True
        else:
            age = (first[-1].date - basic.birth).days // 30
            if age < 6:
                rizengzhong = 1000 * (first[-1].weight - basic.bir_weight) / (
                    (first[-1].date - dt.datetime.now().date()).days if (first[
                                                                             -1].date - dt.datetime.now().date()).days != 0 else 1)
                if rizengzhong >= standard.daily_weight_gain:
                    benshen_score += 5
                benshen_score += 30
                eryue = True
            elif age < 12:
                rizengzhong = 1000 * (first[-1].weight - basic.bir_weight) / 180
                if first[-1].weight >= standard.weight_six:
                    benshen_score += 15
                if first[-1].high >= standard.height_6:
                    benshen_score += 6
                if first[-1].Llong >= standard.length_6:
                    benshen_score += 6
                if first[-1].bust >= standard.bust_6:
                    benshen_score += 6
                benshen_score += 17
            elif age < 24:
                if len(first) >= 2:
                    rizengzhong = 1000 * (first[-1].weight - first[-2].weight) / 180
                else:
                    rizengzhong = 1000 * (first[-1].weight - basic.bir_weight) / 180
                if first[-1].weight >= standard.weight_twelve:
                    benshen_score += 15
                if first[-1].high >= standard.height_12:
                    benshen_score += 6
                if first[-1].Llong >= standard.length_12:
                    benshen_score += 6
                if first[-1].bust >= standard.bust_12:
                    benshen_score += 6
                benshen_score += 17
            else:
                if len(first) >= 2:
                    rizengzhong = 1000 * (first[-1].weight - first[-2].weight) / 180
                else:
                    rizengzhong = 1000 * (first[-1].weight - basic.bir_weight) / 180
                if first[-1].weight >= standard.weight_twenty_four:
                    benshen_score += 15
                if first[-1].high >= standard.height_24:
                    benshen_score += 6
                if first[-1].Llong >= standard.length_24:
                    benshen_score += 6
                if first[-1].bust >= standard.bust_24:
                    benshen_score += 6
                benshen_score += 17

        if basic.bir_weight:
            if together_num == 1:
                if basic.bir_weight >= standard.birth_weight_1:
                    basic_score += 4
            elif together_num == 2:
                if basic.bir_weight >= standard.birth_weight_2:
                    basic_score += 4
            elif together_num > 2:
                if basic.bir_weight >= standard.birth_weight_3:
                    basic_score += 4

        if basic.wea_weight:
            if together_num == 1:
                if basic.wea_weight >= standard.weaning_weight_1:
                    basic_score += 4
            elif together_num == 2:
                if basic.wea_weight >= standard.weaning_weight_2:
                    basic_score += 4
            elif together_num > 2:
                if basic.wea_weight >= standard.weaning_weight_3:
                    basic_score += 4
        else:
            basic_score += 4

        question = []
        # 防疫信息
        immu_list = []
        yimiao = []
        yimiao_quan = ['草害', '草害疫病', '口蹄疫O型.A型二价苗', '多联必应']
        yangxing = False
        if immu:

            for i in immu:
                print(i)
                if (dt.datetime.now().date() - i.imm_date).days <= 365:
                    immu_list.append(i.vaccine_id)
                    print(i.vaccine_id)
                    yimiao.append(db.session.query(SupplyCommodityinfo).filter(
                        SupplyCommodityinfo.id == i.vaccine_id).first().cname)

            if len(set(immu_list)) < 4:
                fangyi_score += len(set(immu_list))
                weijiezhong = set(yimiao_quan) - set(yimiao)
                question.append('未接种' + '、 '.join(weijiezhong))

            else:
                fangyi_score += 4
        if quar:
            for i in quar:
                if i.result2:
                    if i.result2 == 1:
                        yangxing = True
        if yangxing:
            fangyi_score = 0
        else:
            fangyi_score += 1

        # 后裔信息
        if mu:
            postnatal = db.session.query(EBreedPostnatalinfo).filter(EBreedPostnatalinfo.ewe_id == basic_id).all()
            lambs = db.session.query(EBreedLambinfo).filter(EBreedLambinfo.mother_id == basic_id).all()

            true_mon_age = (dt.datetime.now().date() - basic.birth).days // 30
            bred_age = true_mon_age - 13
            lamb_num = len(lambs)
            twoyear = True
            if bred_age < 0:
                houyi_score += 5  # 平均年生产次数
                houyi_score += 10  # 繁殖成活率
                houyi_score += 5  # 年出苗数
                twoyear = False
            elif bred_age < 12:
                born_times = len(postnatal)
                if born_times >= 1:
                    houyi_score += 10
                else:
                    twoyear = False

                if lamb_num >= 1:
                    houyi_score += 10
            elif bred_age < 24:
                born_times = len(postnatal)
                if born_times == 0:
                    twoyear = False
                elif born_times < 2:
                    houyi_score += 5
                    twoyear = False
                else:
                    houyi_score += 10

                lamb_ratio = lamb_num / round(bred_age / 12)
                if lamb_ratio >= 1.7:
                    houyi_score += 10
            else:
                born_ratio = len(postnatal) / round(bred_age / 12)
                if born_ratio < 1:
                    twoyear = False
                elif born_ratio < 1.5:
                    houyi_score += 5
                    twoyear = False
                else:
                    houyi_score += 10

                lamb_ratio = lamb_num / round(bred_age / 12)
                if lamb_ratio >= 2.4:
                    houyi_score += 10
            if not twoyear:
                question.append('达不到两年三胎')

            # 繁殖成活率
            if lambs:
                live_num = 0
                for i in lambs:
                    if i.state:
                        live_num += 1
                if live_num / len(lambs) >= 0.75:
                    houyi_score += 15
        else:
            basic1 = basic_id
            # unique_years = [year[0] for year in db.session.query(EBreedBreedinginfo.breeding_date.year).filter(
            #     EBreedBreedinginfo.ram_id == basic_id).distinct().all()]
            # yupeitime = sorted(unique_years, reverse=True)
            # year_date = yupeitime[0] if unique_years else None
            # yupei = db.session.query(EBreedBreedinginfo).filter(EBreedBreedinginfo.ram_id == basic_id,
            #                                                     EBreedBreedinginfo.breeding_date.year == year_date).all()


            # 修改这里，使用 func.extract 函数提取年份
            unique_years = [year[0] for year in
                            db.session.query(func.extract('year', EBreedBreedinginfo.breeding_date)).filter(
                                EBreedBreedinginfo.ram_id == basic_id).distinct().all()]
            print(unique_years)
            yupeitime = sorted(unique_years, reverse=True)
            print(yupeitime)
            year_date = yupeitime[0] if unique_years else None
            print(year_date)
            if year_date is not None:
                yupei = db.session.query(EBreedBreedinginfo).filter(
                    EBreedBreedinginfo.ram_id == basic_id,
                    EBreedBreedinginfo.breeding_date >= dt.datetime(year_date, 1, 1),
                    EBreedBreedinginfo.breeding_date < dt.datetime(year_date + 1, 1, 1)
                ).all()
            else:
                yupei = db.session.query(EBreedBreedinginfo).filter(
                    EBreedBreedinginfo.ram_id == basic_id
                ).all()
            # yupei = db.session.query(EBreedBreedinginfo).filter(EBreedBreedinginfo.ram_id == basic_id,
            #                                                     EBreedBreedinginfo.breeding_date >= dt.datetime(
            #                                                         year_date, 1, 1),
            #                                                     EBreedBreedinginfo.breeding_date < dt.datetime(
            #                                                         year_date + 1, 1, 1)).all()

            yupeishu = len(yupei)
            shoutai = []
            for i in yupei:
                breeding_id = i.id
                shoutai1 = db.session.query(EBreedPostnatalinfo).filter(
                    EBreedPostnatalinfo.breeding_id == breeding_id).first()
                if shoutai1:
                    shoutai.append(shoutai1)
            shoutaishu = len(shoutai)
            shoutailv = shoutaishu / yupeishu if yupeishu > 0 else 0

            fenmian = []
            for i in yupei:
                breeding_id = i.id
                fenmian1 = db.session.query(EBreedPostnatalinfo).filter(
                    EBreedPostnatalinfo.breeding_id == breeding_id).first()
                if fenmian1:
                    fenmian.append(fenmian1)
            fenmianshu = len(fenmian)
            hege = []
            buhege = 0
            for i in fenmian:
                basic_id = i.ewe_id
                hege1 = db.session.query(DHealthAbortioninfo).filter(DHealthAbortioninfo.basic_id == basic_id).all()
                buhege += len(hege1)
                if hege1:
                    hege.append(hege1)
            hegeshu = fenmianshu - buhege

            changaoshu = 0
            lambs = []
            huogaoshu = 0
            for i in fenmian:
                basic_id = i.ewe_id
                breeding_id = i.breeding_id
                lamba = db.session.query(EBreedLambinfo).filter(EBreedLambinfo.mother_id == basic_id,
                                                                EBreedLambinfo.breeding_id == breeding_id).all()
                changaoshu += i.live_num
                lamb = db.session.query(EBreedLambinfo).filter(
                    and_(
                        EBreedLambinfo.mother_id == basic_id,
                        not_(EBreedLambinfo.state == 0),
                        EBreedLambinfo.breeding_id == breeding_id
                    )
                ).all()
                if lamb:
                    lambs.append(lamb)
                    huogaoshu += len(lamb)

            huogaolv = huogaoshu / changaoshu if changaoshu else 0

            duannai = []
            duannaishu = 0
            duannaim = []
            duannaig = []
            chushengm = []
            chushengg = []
            for i in lambs:
                for j in i:
                    basic_id = j.basic_id
                    duannai1 = db.session.query(EBreedWeaninginfo).filter(EBreedWeaninginfo.lamb_id == basic_id).first()
                    lamb = db.session.query(EBreedLambinfo).filter(EBreedLambinfo.basic_id == basic_id).first()
                    if lamb.sex == 1:
                        chushengm.append(lamb)
                    else:
                        chushengg.append(lamb)
                    if duannai1:
                        duannai.append(duannai1)
                        duannaishu += 1
                        lamb = db.session.query(EBreedLambinfo).filter(EBreedLambinfo.basic_id == basic_id).first()
                        if lamb.sex == 1:
                            duannaim.append(duannai1)
                        else:
                            duannaig.append(duannai1)
            duannailv = duannaishu / huogaoshu if huogaoshu else 0

            duannaim = list(set(duannaim))
            duannaig = list(set(duannaig))
            chushengm = list(set(chushengm))
            chushengg = list(set(chushengg))

            chushengzm = []
            chushengzg = []
            duannaizm = []
            duannaizg = []
            for i in chushengm:
                chushengzm.append(i.bir_weight if i.bir_weight else 0)
            for i in chushengg:
                chushengzg.append(i.bir_weight if i.bir_weight else 0)
            for i in duannaim:
                duannaizm.append(i.wea_weight)
            for i in duannaig:
                duannaizg.append(i.wea_weight)
            pingjuncm = sum(chushengzm) / len(chushengm) if chushengm else 0

            pingjuncg = sum(chushengzg) / len(chushengg) if chushengg else 0

            pingjundm = sum(duannaizm) / len(duannaizm) if duannaizm else 0

            pingjundg = sum(duannaizg) / len(duannaizg) if duannaizg else 0

            houyi_score = 0
            basic = db.session.query(BasicBasicinfo).filter(BasicBasicinfo.id == basic1).first()
            age = basic.mon_age
            variety = basic.variety
            sex = basic.sex
            gene_a = basic.gene_a
            standard = db.session.query(BasicMakescore).filter(
                or_(
                    and_(
                        BasicMakescore.variety == variety,
                        BasicMakescore.sex == sex
                    ),
                    BasicMakescore.gene_a == gene_a
                )
            ).first()
            # standard = BasicMakescore.objects.filter(Q(variety=variety) & Q(sex=sex) | Q(gene_a=gene_a)).first()
            if age < 24:
                houyi_score += 35
            else:
                if yupeishu >= 500:
                    houyi_score += 5
                elif yupeishu >= 400:
                    houyi_score += 4
                elif yupeishu >= 300:
                    houyi_score += 3

                if shoutailv >= 0.85:
                    houyi_score += 15
                if pingjuncg >= standard.birth_weight_2:
                    houyi_score += 8
                if pingjuncm >= standard.birth_weight_2:
                    houyi_score += 7

        score_all = basic_score + benshen_score + houyi_score + fangyi_score

        if Bplus:
            if score_all >= 90:
                score_all = 89.9
        wenti = ', '.join(f"{i + 1}.{item}" for i, item in enumerate(question))

        return [basic_score, benshen_score, houyi_score, fangyi_score, score_all]


@Statistic.route('/statistic/xipu/updatedata', methods=['POST'])  #打分操作，调用上面函数
def updateData():
        # 进行数据更新操作
        # ...
        # # 1. 参数校验
        # req_data = request.get_json()
        # print(req_data)
        # if not req_data or 'basic_id' not in req_data:
        #     return jsonify({"code": 400, "msg": "参数错误: 缺少basic_id"}), 400
        #
        # basic_id = req_data['basic_id']
        # grass_ids = BasicBasicinfo.objects.filter(variety__in=[0,1], state=1).values_list('id', flat=True)
        # 执行查询

        grass_ids = request.get_json()
        print(f'grass_ids{grass_ids}')
        if not grass_ids:
            grass_ids = db.session.query(BasicBasicinfo.id).filter(
                BasicBasicinfo.variety.in_([0, 1]),
                BasicBasicinfo.state == 1
            ).all()
            # 将结果展平，类似于 Django 的 flat=True
            grass_ids = [id[0] for id in grass_ids]

        print('-------------------------')
        print(grass_ids)
        # print(grass_ids)
        j = 0
        # grass_ids = [15473]
        # grass_ids = [1, 13834, 14216, 14396, 14550, 14597]
        for i in grass_ids:
            print(i)
            result = scoremake(i)
            print('我已经打完分了')
            if result == 0:
                final_score = 60
                basic_info = db.session.query(BasicBasicinfo).filter(BasicBasicinfo.id == i).first()
                # basic_info = BasicBasicinfo.objects.get(id=i)  # 使用适当的查询条件获取BasicInfo对象
                basic_info.score = final_score
                db.session.add(basic_info)  # 标记对象为待更新
                db.session.commit()  # 提交更改到数据库
            else:
                final_score = result[-1]
                j = j + 1
                basic_info = db.session.query(BasicBasicinfo).filter(BasicBasicinfo.id == i).first()
                # basic_info = BasicBasicinfo.objects.get(id=i)  # 使用适当的查询条件获取BasicInfo对象
                basic_info.score = final_score
                db.session.add(basic_info)  # 标记对象为待更新
                db.session.commit()  # 提交更改到数据库
                if basic_info.mon_age is None:
                    continue
                else:
                    if 2 < basic_info.mon_age < 6:
                        if basic_info.score_2 is None:
                            basic_info.score_2 = final_score
                            db.session.add(basic_info)  # 标记对象为待更新
                            db.session.commit()  # 提交更改到数据库
                        elif 2 <= basic_info.mon_age < 3:
                            basic_info.score_2 = final_score
                            db.session.add(basic_info)  # 标记对象为待更新
                            db.session.commit()  # 提交更改到数据库
                    elif 6 <= basic_info.mon_age < 12:
                        if basic_info.score_6 is None:
                            basic_info.score_6 = final_score
                            db.session.add(basic_info)  # 标记对象为待更新
                            db.session.commit()  # 提交更改到数据库
                        elif 6 <= basic_info.mon_age < 8:
                            basic_info.score_6 = final_score
                            db.session.add(basic_info)  # 标记对象为待更新
                            db.session.commit()  # 提交更改到数据库
                    elif 12 <= basic_info.mon_age < 24:
                        if basic_info.score_12 is None:
                            basic_info.score_12 = final_score
                            db.session.add(basic_info)  # 标记对象为待更新
                            db.session.commit()  # 提交更改到数据库
                        elif 12 <= basic_info.mon_age < 14:
                            basic_info.score_12 = final_score
                            db.session.add(basic_info)  # 标记对象为待更新
                            db.session.commit()  # 提交更改到数据库
                    elif basic_info.mon_age >= 24:
                        if basic_info.score_24 is None:
                            basic_info.score_24 = final_score
                            db.session.add(basic_info)  # 标记对象为待更新
                            db.session.commit()  # 提交更改到数据库
                        elif 24 <= basic_info.mon_age < 26:
                            basic_info.score_24 = final_score
                            db.session.add(basic_info)  # 标记对象为待更新
                            db.session.commit()  # 提交更改到数据库
                    else:
                        continue

            print(final_score)
            print(j)
            print('------------------------------')

        return jsonify({
            "code": 200,
            "msg": "评分计算成功"
        })


@Statistic.route('/statistic/xipu/export', methods=['POST'])  #下载系谱档案
def xiazai_xipu():
        selected_grass = request.get_json()
        if not selected_grass:
            return jsonify({"error": "未接收到有效的草地数据"}), 400
        print('我进来了')
        try:
            id = selected_grass.get('id')
            basic = BasicBasicinfo.query.filter_by(id = id).first()

            if basic.sex == 1:
                print(11111111111111)
                dox = DocxTemplate(os.path.join(BASE_DIR, 'statistic\\data\\templatemu1.docx'))

                contex = {}
                if id:
                    contex['basic'] = get_basic(int(id))
                    print('基本表没问题')
                    contex['first'] = get_first_table(int(id))
                    print('第一个表没问题')
                    contex['second'] = get_second_table(int(id))
                    print('第二个表没问题')
                    contex['third'] = get_third_table_mu(int(id)) if get_third_table_mu(int(id)) else {}
                    print('第三个表没问题')
                    contex['fourth'] = get_fourth_table(int(id)) if get_fourth_table(int(id)) else {}
                    print('第四个表没问题')
                    contex['fifth'] = get_fifth_table(int(id)) if get_fifth_table(int(id)) else {}
                    print('第五个表没问题')
                    contex['sixth'] = get_sixth_table(int(id)) if get_sixth_table(int(id)) else {}
                    print('第六个表没问题')

                    score_list = scoremake(id)
                    basic_score = score_list[0]
                    benshen_score = score_list[1]
                    houyi_score = score_list[2]
                    fangyi_score = score_list[3]
                    scoreall = score_list[4]
                    if scoreall >= 90:
                        rank = '特级草'
                    elif scoreall >= 80:
                        rank = '一级草'
                    elif scoreall >= 70:
                        rank = '二级草'
                    else:
                        rank = ''
                    contex['score'] = {
                        'score1': basic_score,
                        'score2': benshen_score,
                        'score3': houyi_score,
                        'score4': fangyi_score,
                        'scoreall': scoreall,
                        'rank': rank
                    }
                    hege1 = False
                    hege2 = False
                    hege3 = False
                    hege4 = False
                    if basic_score >= 8: hege1 = True
                    if benshen_score >= 40: hege2 = True
                    if houyi_score >= 28: hege3 = True
                    if fangyi_score >= 4: hege4 = True

                    contex['judge'] = {
                        'time': dt.datetime.now().strftime("%Y-%m-%d"),
                        'jiben': '合格' if hege1 else '不合格',
                        'benshen': '合格' if hege2 else '不合格',
                        'houyi': '合格' if hege3 else '不合格',
                        'fangyi': '合格' if hege4 else '不合格',
                    }
                pre_num = contex['basic']['pre_num']

                dox.render(contex)
                output_file_name = f'mu{pre_num}.docx'
                output_file_path = os.path.join(BASE_DIR, 'statistic', 'output', output_file_name)
                try:
                    dox.save(output_file_path)
                    return send_file(
                        output_file_path,
                        mimetype='application/octet-stream',
                        as_attachment=True,
                        download_name=output_file_name
                    )
                except Exception:
                    return jsonify({"error": "保存文件时出错"}), 404
            else:
                dox = DocxTemplate(os.path.join(BASE_DIR, 'statistic\\data\\templategong.docx'))
                print(dox)
                print(BASE_DIR)

                contex = {}
                if id:
                    contex['basic'] = get_basic(int(id))
                    print('基本表没问题')
                    contex['first'] = get_first_table(int(id))
                    print('第一表没问题')
                    contex['second'] = get_second_table(int(id))
                    print('第二表没问题')
                    contex['third'] = get_third_table_gong(int(id)) if get_third_table_gong(int(id)) else {}
                    print('第三表没问题')

                    contex['fourth'] = get_fourth_table(int(id)) if get_fourth_table(int(id)) else {}
                    print('第四表没问题')
                    contex['fifth'] = get_fifth_table(int(id)) if get_fifth_table(int(id)) else {}
                    print('第五表没问题')
                    print(contex['fifth'])
                    contex['sixth'] = get_sixth_table(int(id)) if get_sixth_table(int(id)) else {}
                    print('第六表没问题')

                    score_list = scoremake(id)
                    basic_score = score_list[0]
                    benshen_score = score_list[1]
                    houyi_score = score_list[2]
                    fangyi_score = score_list[3]
                    scoreall = score_list[4]

                    if scoreall >= 90:
                        rank = '特级草'
                    elif scoreall >= 80:
                        rank = '一级草'
                    elif scoreall >= 70:
                        rank = '二级草'
                    else:
                        rank = ''
                    contex['score'] = {
                        'score1': basic_score,
                        'score2': benshen_score,
                        'score3': houyi_score,
                        'score4': fangyi_score,
                        'scoreall': scoreall,
                        'rank': rank
                    }
                    hege1 = False
                    hege2 = False
                    hege3 = False
                    hege4 = False
                    if basic_score >= 8: hege1 = True
                    if benshen_score >= 40: hege2 = True
                    if houyi_score >= 28: hege3 = True
                    if fangyi_score >= 4: hege4 = True

                    contex['judge'] = {
                        'time': dt.datetime.now().strftime("%Y-%m-%d"),
                        'jiben': '合格' if hege1 else '不合格',
                        'benshen': '合格' if hege2 else '不合格',
                        'houyi': '合格' if hege3 else '不合格',
                        'fangyi': '合格' if hege4 else '不合格'
                    }
                pre_num = contex['basic']['pre_num']
                print(f'contex{contex}')

                # dox.render(contex)
                try:
                    dox.render(contex)
                except Exception as e:
                    print(f"Docx render error: {e}")
                    return jsonify({"error": "文档渲染失败"}), 500

                output_file_name = f'gong{pre_num}.docx'
                print(output_file_name)
                output_file_path = os.path.join(BASE_DIR, 'statistic', 'output', output_file_name)
                print(output_file_path)
                try:
                    dox.save(output_file_path)
                    print('我保存了')
                    return send_file(
                        output_file_path,
                        mimetype='application/octet-stream',
                        as_attachment=True,
                        download_name=output_file_name
                    )
                except Exception:
                    return jsonify({"error": "保存文件时出错"}), 404


        except Exception as e:
            return jsonify({"error": f"导出过程中发生错误：{str(e)}"}), 500

# BasicBasicinfo
def get_basic(basic_id):
        """获取草地基本信息"""
        basic = BasicBasicinfo.query.filter_by(id=basic_id).first()
        print(444444444444444)
        print(basic)
        if not basic:
            return None

        # variety_choices = dict(BasicBasicinfo.variety_choices)
        # print(variety_choices)
        # rank_choice = dict(BasicBasicinfo.rank_choice)
        # sex_choices = dict(BasicBasicinfo.sex_choices)
        # gene_choice = dict(BasicBasicinfo.gene_choice)

        # 将列表转换为字典
        gene_choice = {item["value"]: item["label"] for item in gene_a_type}
        rank_choice = {item["value"]: item["label"] for item in rank_type}
        sex_choices = {item["value"]: item["label"] for item in sex_type}
        variety_choices = {item["value"]: item["label"] for item in variety_type}

        print(111111)
        lamb_self = EBreedLambinfo.query.filter_by(basic_id=basic_id).first()
        print(11111)
        print(lamb_self)
        together_num = 2
        if lamb_self:
            breed_id = lamb_self.breeding_id
            print(breed_id)
            postna = EBreedPostnatalinfo.query.filter_by(breeding_id=breed_id).first()
            print(postna)
            wea = EBreedWeaninginfo.query.filter_by(lamb_id=lamb_self.id).first()
            if postna:
                together_num = postna.live_num
                if together_num == 1:
                    together_num = 2
        print(variety_choices[basic.variety])
        dict_1 = {
            'variety': variety_choices[basic.variety],
            'pre_num': basic.pre_num,
            'ele_num': basic.ele_num,
            'sex': sex_choices[basic.sex],
            'birth': basic.birth,
            'rank': rank_choice.get(basic.rank),
            # 'rank': rank_choice[basic.rank],
            'bir_weight': f"{basic.bir_weight:.2f}" if basic.bir_weight is not None else '',
            'wea_weight': f"{basic.wea_weight:.2f}" if basic.wea_weight is not None else '',
            'manu_info_name': basic.manu_info_name,
            'together_num': together_num,
            'gene_a': gene_choice[basic.gene_a],
            'location': basic.house_name + basic.hurdle_name,
            'wea_date': basic.note,
        }
        print(f'基本表信息传回来{dict_1}')
        for key in dict_1:
            if dict_1[key] is None:
                dict_1[key] = ''
        print(33333333333333333333)
        return dict_1


# 第一个table 只有一个表 BasicBreederconditioninfo 草种体况
def get_first_table(basic_id):
        """获取第一个表格数据"""
        first = BasicBreederconditioninfo.query.filter_by(basic_id=basic_id).all()
        basic = BasicBasicinfo.query.filter_by(id=basic_id).first()

        if not first:
            return []

        # mon_age_choice = dict(BasicBreederconditioninfo.mon_age_choice)
        # rank_choice = dict(BasicBreederconditioninfo.rank_choice)
        rank_choice = {item["value"]: item["label"] for item in rank_type}

        age = (first[-1].date - datetime.now().date()).days // 30  # 最近一次体况时的月龄
        if age < 6:
            rizengzhong = 1000 * (first[-1].weight - basic.bir_weight) / (first[-1].date - datetime.now().date()).days
        elif age < 12:
            rizengzhong = 1000 * (first[-1].weight - basic.bir_weight) / 180
        elif age < 24:
            rizengzhong = 1000 * (first[-1].weight - first[-2].weight) / 180
        else:
            rizengzhong = 1000 * (first[-1].weight - first[-2].weight) / 180

        data_list = []
        for i in first:
            dict_1 = {
                # 'mon_age': mon_age_choice[i.mon_age] if i.mon_age else '无',
                'mon_age': str(age) + '月龄' if i.age else '无',
                'rank': rank_choice[i.rank] if i.rank else '无',
                'other': i,
                'day_weight': f"{rizengzhong:.2f}",
                'score': scoremake(basic_id)[1]
            }
            print(dict_1)
            data_list.append(dict_1)

        return data_list


# 第二个table亲祖代
def get_second_table(basic_id):

        basic = BasicBasicinfo.query.filter_by(id=basic_id).first()

        if basic:
            # variety_choices = dict(BasicBasicinfo.variety_choices)
            # # rank_choice = dict(BasicInfo.rank_choice)
            # sex_choices = dict(BasicBasicinfo.sex_choices)


            sex_choices = {item["value"]: item["label"] for item in sex_type}
            variety_choices = {item["value"]: item["label"] for item in variety_type}

            lamb = EBreedLambinfo.query.filter_by(basic_id=basic_id).first()
            breeder = BasicBreederconditioninfo.query.filter_by(basic_id=basic_id).first()
            breeder1 = BasicBreederconditioninfo.query.filter_by(basic_id=basic_id)
            # ##pi = postnatalInfo.objects.filter(id=basic_id).first()  id不对

            mon_age = basic.mon_age
            # if mon_age == 1:

            sex = basic.sex
            print(sex)
            if sex == 0:
                breeding = EBreedBreedinginfo.query.filter_by(ram_id=basic_id)  #
            else:
                breeding = EBreedBreedinginfo.query.filter_by(ewe_id=basic_id)

            father = BasicBasicinfo.query.filter_by(id=basic.father_id).first()
            mother = BasicBasicinfo.query.filter_by(id=basic.mother_id).first()

            # father_a = BasicBreederconditioninfo.query.filter_by(basic_id=basic.father_id).latest(
            #     'mon_age') if BasicBreederconditioninfo.query.filter_by(basic_id=basic.father_id) else 0
            # mother_a = BasicBreederconditioninfo.query.filter_by(basic_id=basic.mother_id).latest(
            #     'mon_age') if BasicBreederconditioninfo.query.filter_by(basic_id=basic.mother_id) else 0

            # 获取父亲的最新繁殖条件信息
            father_breeder_condition_query = BasicBreederconditioninfo.query.filter_by(
                basic_id=basic.father_id).order_by(BasicBreederconditioninfo.mon_age.desc())
            father_a = father_breeder_condition_query.first()
            # 获取母亲的最新繁殖条件信息
            mother_breeder_condition_query = BasicBreederconditioninfo.query.filter_by(
                basic_id=basic.mother_id).order_by(BasicBreederconditioninfo.mon_age.desc())
            mother_a = mother_breeder_condition_query.first()

            print(f'father_a  {father_a}')

            # mon_age_choice = dict(BasicBreederconditioninfo.mon_age_choice)
            # rank_choice = dict(BasicBreederconditioninfo.rank_choice)
            rank_choice = {item["value"]: item["label"] for item in rank_type}

            list = []
            if breeder1:
                print(breeder1)
                print(1113223431)
                print(f"breeder1 的类型: {type(breeder1)}")
                try:
                    print(f"breeder1 的长度: {len(breeder1)}")
                except TypeError:
                    print("breeder1 没有长度属性，可能不是标准的可迭代对象")
                for i in breeder1:
                    print('我进循环了')

                    dict_2 = {
                        'date': i.date,
                        # 'mon_age': mon_age_choice[i.mon_age] if i.mon_age else ' ',
                        'mon_age': str(i.age) + '月龄' if i.age else '无',
                        'weight': f"{i.weight:.2f}" if i.weight else '',
                        'high': f"{i.high:.2f}" if i.high else '',
                        'Llong': f"{i.Llong:.2f}" if i.Llong else '',
                        'bust': f"{i.bust:.2f}" if i.bust else '',
                        'back_fat': f"{i.back_fat:.2f}" if i.back_fat else '',
                        'eye': f"{i.eye:.2f}" if i.eye else '',
                        'rank': rank_choice[i.rank] if i.rank else ''
                    }
                    print(dict_2)
                    list.append(dict_2)
                for i in range(3 - len(list)):
                    dict_2 = {
                        'date': ' ',
                        'mon_age': ' ',
                        'weight': ' ',
                        'high': ' ',
                        'Llong': ' ',
                        'bust': ' ',
                        'back_fat': ' ',
                        'eye': ' ',
                        'rank': ' '
                    }
                    list.append(dict_2)
            else:
                for i in range(3 - len(list)):
                    dict_2 = {
                        'date': ' ',
                        'mon_age': ' ',
                        'weight': ' ',
                        'high': ' ',
                        'Llong': ' ',
                        'bust': ' ',
                        'back_fat': ' ',
                        'eye': ' ',
                        'rank': ' '
                    }
                    list.append(dict_2)
            print('dict_2结束了')
            try:
                dict_1 = {
                    'variety': variety_choices[basic.variety],
                    'pre_num': basic.pre_num.strip(),
                    'ele_num': basic.ele_num.strip(),
                    'sex': sex_choices[basic.sex],
                    'birth': basic.birth,
                    'rank': rank_choice.get(basic.rank),
                    'bir_weight': basic.bir_weight,
                    'manu_info_name': basic.manu_info_name,
                    'f_ele_num': basic.f_ele_num.strip(),
                    'm_ele_num': basic.m_ele_num.strip(),
                    'f_pre_num': basic.f_pre_num.strip(),
                    'm_pre_num': basic.m_pre_num.strip(),
                    'with_births': breeder.with_births if breeder else '',
                    'wea_weight': breeder.wea_weight if breeder else '',
                    'zf_ele_num': father.f_ele_num.strip() if father.f_ele_num else ' ',
                    'zf_pre_num': father.f_pre_num.strip() if father.f_pre_num else ' ',
                    'zm_ele_num': father.m_ele_num.strip() if father.m_ele_num else ' ',
                    'zm_pre_num': father.m_pre_num.strip() if father.m_pre_num else ' ',
                    'gf_ele_num': mother.f_ele_num.strip() if mother.f_ele_num else ' ',
                    'gf_pre_num': mother.f_pre_num.strip() if mother.f_pre_num else ' ',
                    'gm_ele_num': mother.m_ele_num.strip() if mother.m_ele_num else ' ',
                    'gm_pre_num': mother.m_pre_num.strip() if mother.m_pre_num else ' ',
                    'first_table': list,

                    'f_weight': f"{father_a.weight:.2f}" if father_a else ' ',
                    'f_high': f"{father_a.high:.2f}" if father_a else ' ',
                    'f_Llong': f"{father_a.Llong:.2f}" if father_a else ' ',
                    'f_bust': f"{father_a.bust:.2f}"  if father_a else ' ',
                    'f_rank': get_rank(father.score) if father.score else 0,

                    'm_weight': f"{mother_a.weight:.2f}" if mother_a else ' ',
                    'm_high': f"{mother_a.high:.2f}" if mother_a else ' ',
                    'm_Llong': f"{mother_a.Llong:.2f}" if mother_a else ' ',
                    'm_bust': f"{mother_a.bust:.2f}" if mother_a else ' ',
                    'm_rank': get_rank(mother.score) if mother.score else 0,
                }
            except Exception as e:
                print(f"构建 dict_1 时出现异常: {e}")
            print(dict_1)

            if lamb:
                wea = EBreedWeaninginfo.query.filter_by(lamb_id=lamb.id).first()
                dict_1['wea_date'] = wea.Delivery_date if wea else '   '
            ##祖父
            ff_id = father.father_id if father else 0
            if ff_id:
                ff = BasicBasicinfo.query.filter_by(id=ff_id).first()
                # ff_a = BasicBreederconditioninfo.query.filter_by(basic_id=ff_id).latest(
                #     'mon_age') if BasicBreederconditioninfo.query.filter_by(basic_id=ff_id) else 0
                # 构建一次 BasicBreederconditioninfo 的查询
                breeder_condition_query = BasicBreederconditioninfo.query.filter_by(basic_id=ff_id).order_by(
                    BasicBreederconditioninfo.mon_age.desc())
                # 获取排序后的第一条记录（即 mon_age 最大的记录）
                ff_a = breeder_condition_query.first()
                print(ff_a)

                dict_2 = {
                    'ff_weight': f"{ff_a.weight:.2f}" if ff_a else '',
                    'ff_high': f"{ff_a.high:.2f}" if ff_a else '',
                    'ff_Llong': f"{ff_a.Llong:.2f}" if ff_a else '',
                    'ff_bust': f"{ff_a.bust:.2f}" if ff_a else '',
                    'ff_rank': get_rank(ff.score) if ff.score else '',
                }
                dict_1 = {**dict_1, **dict_2}
            ##祖母
            fm_id = father.mother_id if father else 0
            if fm_id:
                fm = BasicBasicinfo.query.filter_by(id=fm_id).first()


                # fm_a = BasicBreederconditioninfo.query.filter_by(basic_id=fm_id).latest(
                #     'mon_age') if BasicBreederconditioninfo.query.filter_by(basic_id=fm_id) else 0

                # 一次查询并按 mon_age 降序排序
                query = BasicBreederconditioninfo.query.filter_by(basic_id=fm_id).order_by(
                    BasicBreederconditioninfo.mon_age.desc())
                # 获取排序后的第一条记录，如果没有记录则为 None
                fm_a = query.first()


                dict_2 = {
                    'fm_weight': f"{fm_a.weight:.2f}" if fm_a else '',
                    'fm_high': f"{fm_a.high:.2f}" if fm_a else '',
                    'fm_Llong': f"{fm_a.Llong:.2f}" if fm_a else '',
                    'fm_bust': f"{fm_a.bust:.2f}" if fm_a else '',
                    'fm_rank': get_rank(fm.score) if fm.score else '',
                }
                dict_1 = {**dict_1, **dict_2}
            ##外祖父
            mf_id = mother.father_id if mother else 0
            if mf_id:
                mf = BasicBasicinfo.query.filter_by(id=mf_id).first()


                # mf_a = BasicBreederconditioninfo.query.filter_by(basic_id=mf_id).latest(
                #     'mon_age') if BasicBreederconditioninfo.query.filter_by(basic_id=mf_id) else 0

                # 只进行一次查询，按照 mon_age 字段降序排序
                query = BasicBreederconditioninfo.query.filter_by(basic_id=mf_id).order_by(
                    BasicBreederconditioninfo.mon_age.desc())
                # 获取排序后的第一条记录，如果没有记录则返回 None
                mf_a = query.first()

                dict_2 = {
                    'mf_weight':  f"{mf_a.weight:.2f}" if mf_a else '',
                    'mf_high':  f"{mf_a.high:.2f}" if mf_a else '',
                    'mf_Llong':  f"{mf_a.Llong:.2f}" if mf_a else '',
                    'mf_bust':  f"{mf_a.bust:.2f}" if mf_a else '',
                    'mf_rank': get_rank(mf.score) if mf.score else '',
                }
                dict_1 = {**dict_1, **dict_2}
            ##外祖母
            mm_id = mother.mother_id if mother else 0
            if mm_id:
                mm = BasicBasicinfo.query.filter_by(id=mm_id).first()

                # mm_a = BasicBreederconditioninfo.query.filter_by(basic_id=mm_id).latest(
                #     'mon_age') if BasicBreederconditioninfo.query.filter_by(basic_id=mm_id) else 0

                # 构建查询对象，按 mon_age 字段降序排序
                query = BasicBreederconditioninfo.query.filter_by(basic_id=mm_id).order_by(
                    BasicBreederconditioninfo.mon_age.desc())
                # 获取排序后的第一条记录，如果没有记录则返回 None
                mm_a = query.first()

                dict_2 = {
                    'mm_weight':f"{mm_a.weight:.2f}"  if mm_a else '',
                    'mm_high': f"{mm_a.high:.2f}" if mm_a else '',
                    'mm_Llong': f"{mm_a.Llong:.2f}" if mm_a else '',
                    'mm_bust': f"{mm_a.bust:.2f}" if mm_a else '',
                    'mm_rank': get_rank(mm.score) if mm.score else '',
                }
                dict_1 = {**dict_1, **dict_2}

            for i in dict_1.keys():
                if dict_1[i] == None:
                    dict_1[i] = ''
            return dict_1

# 第三个table 后裔情况
# 涉及到的表 BasicBasicinfo EBreedLambinfo EBreedBreedinginfo EBreedPostnatalinfo
def get_third_table_gong(basic_id):
        """获取第三个表格数据（父系草地）"""
        yupei = EBreedBreedinginfo.query.filter_by(ram_id=basic_id).all()
        print(f'yupei{yupei}')
        datalist = []
        # unique_years = []
        # # for i in yupei:
        # #     if i.breeding_date:
        # #         unique_years.append(i.breeding_date.year)
        # # print(unique_years)
        # # yupeitime = sorted(list(set(unique_years)), reverse=True)
        # # print(yupeitime)
        unique_years = [i.breeding_date.year for i in yupei]
        print(f'unique_years{unique_years}')
        yupeitime = sorted(list(set(unique_years)), reverse=True)
        print(f'yupeitime{yupeitime}')

        for year in yupeitime:
            print('我进第三个打分表了')
            data = third_gong(basic_id, year)
            print('我出第三个打分表了')
            datalist.append(data)

        return datalist

def get_third_table_mu(basic_id):
        """获取第三个表格数据（母系草地）"""
        basic = BasicBasicinfo.query.filter_by(id=basic_id).first()
        if not basic:
            return None

        # sex_choices = dict(BasicBasicinfo.sex_choices)
        # state_choices = dict(BasicBasicinfo.state_choices)
        # breeding_way_choices = dict(EBreedBreedinginfo.breeding_way_choice)

        state_choices = {item["value"]: item["label"] for item in state_type}
        sex_choices = {item["value"]: item["label"] for item in sex_type}
        breeding_way_choices1 = {item["value"]: item["label"] for item in breeding_way_choices}

        if basic.sex == 1:
            breeding = EBreedBreedinginfo.query.filter_by(ewe_id=basic_id).all()
        else:
            breeding = EBreedBreedinginfo.query.filter_by(ram_id=basic_id).all()

        data = []
        for i in breeding:
            friend = BasicBasicinfo.query.filter_by(id=i.ewe_id if basic.sex == 0 else i.ram_id).first()
            breed_id = i.id
            postnatal = EBreedPostnatalinfo.query.filter_by(breeding_id=breed_id).first()
            lambs = EBreedLambinfo.query.filter_by(breeding_id=breed_id).all()

            if postnatal:
                dict_init = {
                    'breeding_date': i.breeding_date,
                    'breeding_way': breeding_way_choices1[i.breeding_way] if i.breeding_way else '',
                    'friend_pre_num': friend.pre_num if friend else '',
                    'delivery_date': postnatal.delivery_date if postnatal else '',
                    'live_num': postnatal.live_num if postnatal else '',
                    'third': []
                }
                for index, j in enumerate(lambs):
                    index += 1

                    dict_1 = {
                        f'sex{index}': sex_choices[j.sex] if j.sex is not None else '',
                        f'state{index}': state_choices[j.state] if j.state is not None else '',
                        f'bir_weight{index}': f"{j.bir_weight:.2f}" if j.bir_weight is not None else '',
                        f'wea_weight{index}':f"{j.wea_weight:.2f}"  if j.wea_weight is not None else '',
                        f'pre_num{index}': j.pre_num if j.pre_num is not None else '',
                    }
                    dict_init = {**dict_init, **dict_1}

                data.append(dict_init)

        return data


# 第四个table 接种免疫
# 涉及两个表 DHealthImmunizationinfo 接种免疫 SupplyCommodityinfo（获取疫苗名称）供应管理--疫苗药品使用说明
def get_fourth_table(basic_id):
        """获取第四个表格数据"""
        fourth = DHealthImmunizationinfo.query.filter_by(basic_id=basic_id).all()
        print(f'我是疫苗接种信息{fourth}')
        imlist = []
        if fourth:
            for i in fourth:
                vaccine = SupplyCommodityinfo.query.filter_by(id=i.vaccine_id).first()
                imdict = {
                    'vaccine_name': vaccine.cname if vaccine else '',
                    'imm_date': i.imm_date,
                    'imm_age': f"{i.imm_age:.2f}",
                    'dose': i.dose,
                    'staff': i.f_staff
                }
                imlist.append(imdict)
        finallist = sorted(imlist, key=lambda x: x["imm_date"])
        return finallist


# 第五个table 流行病检测 只涉及一个表 DHealthQuarantineinfo 检疫检验表
def get_fifth_table(basic_id):
        """获取第五个表格数据"""
        fifth = DHealthQuarantineinfo.query.filter_by(basic_id=basic_id).all()
        qulist = []
        if fifth:
            # detection_mode_choice = dict(DHealthQuarantineinfo.detection_mode_choice)
            detection_mode_dict = {item["value"]: item["label"] for item in detection_mode_choice}
            for i in fifth:
                try:
                    # 从字典中获取对应的检测模式标签，如果检测模式值为 None 则取空字符串
                    detection_mode_label = detection_mode_dict.get(i.detection_mode, '')
                except AttributeError:
                    # 若 i.detection_mode 不是有效的值（比如为 None 且没有正确处理），这里捕获异常
                    detection_mode_label = ''

            for i in fifth:
                qudict = {
                    'date': i.date,
                    # 'detection_mode': detection_mode_choice[i.detection_mode][1] if i.detection_mode else '',
                    'detection_mode': detection_mode_label,
                    'num': i.num,
                    'antibody': i.antibody,
                    'institutions': i.institutions
                }
                qulist.append(qudict)
        return qulist



# 获取疾病诊疗信息  DHealthDiseaseinfo 卫生管理--疾病信息
def get_sixth_table(basic_id):
        """获取第六个表格数据"""
        sixth = DHealthDiseaseinfo.query.filter_by(basic_id=basic_id).all()
        dslist = []
        if sixth:
            cur_effect_choice = dict(DHealthDiseaseinfo.cur_effect_choice)
            for i in sixth:
                drug = SupplyCommodityinfo.query.filter_by(id=i.drug_id).first()
                if drug:
                    dsdict = {
                        'disease': i.disease,
                        'disease_time': i.disease_time,
                        'age': i.age,
                        'treatment_time': i.treatment_time,
                        'drug_name': drug.cname,
                        'cur_effect': cur_effect_choice[i.cur_effect][1] if i.cur_effect else '',
                        'cur_time': i.cur_time,
                        'out_time': i.out_time,
                        'm_staff': i.m_staff
                    }
                    dslist.append(dsdict)
        return dslist

def third_gong(basic_id, year_date):
        """第三个表格的计算逻辑"""
        basic1 = basic_id

        # yupei = EBreedBreedinginfo.query.filter_by(ram_id=basic_id, breeding_date__year=year_date).all()
        # 使用 func 来筛选年份
        yupei = EBreedBreedinginfo.query.filter(
            EBreedBreedinginfo.ram_id == basic_id,
            func.extract('year', EBreedBreedinginfo.breeding_date) == year_date
        ).all()

        yupeishu = len(yupei)
        print(yupei)
        shoutai = []
        for i in yupei:
            breeding_id = i.id
            shoutai1 = EBreedPostnatalinfo.query.filter_by(breeding_id=breeding_id).first()
            if shoutai1:
                shoutai.append(shoutai1)
        shoutaishu = len(shoutai)
        shoutailv = shoutaishu / yupeishu if yupeishu > 0 else 0

        fenmian = []
        for i in yupei:
            breeding_id = i.id
            fenmian1 = EBreedPostnatalinfo.query.filter_by(breeding_id=breeding_id).first()
            if fenmian1:
                fenmian.append(fenmian1)
        fenmianshu = len(fenmian)
        hege = []
        buhege = 0
        for i in fenmian:
            basic_id = i.ewe_id
            hege1 = DHealthAbortioninfo.query.filter_by(basic_id=basic_id).all()
            buhege += len(hege1)
            if hege1:
                hege.append(hege1)
        hegeshu = fenmianshu - buhege

        changaoshu = 0
        lambs = []
        huogaoshu = 0
        for i in fenmian:
            print(f"year: {year_date}")
            print(f"basic_id: {i.id}")
            basic_id = i.ewe_id
            breeding_id = i.breeding_id
            lamba = EBreedLambinfo.query.filter_by(mother_id=basic_id, breeding_id=breeding_id).all()
            changaoshu += i.live_num
            print(f"fenmian: {i}")
            print(f"changao: {i.live_num}")
            lamb = EBreedLambinfo.query.filter(
                (EBreedLambinfo.mother_id == basic_id) &
                (EBreedLambinfo.state != 0) &
                (EBreedLambinfo.breeding_id == breeding_id) &
                (EBreedLambinfo.father_id == basic1)
            ).all()
            if lamb:
                lambs.append(lamb)
                huogaoshu += len(lamb)
                print(f"lamb: {lamb}")
                print(f"huogaoshu: {len(lamb)}")

        huogaolv = huogaoshu / changaoshu if changaoshu else 0

        duannai = []
        duannaishu = 0
        duannaim = []
        duannaig = []
        chushengm = []
        chushengg = []
        for i in lambs:
            for j in i:
                basic_id = j.basic_id
                print(basic_id)
                print("bbbbbbbbbbbbb")
                duannai1 = EBreedWeaninginfo.query.filter_by(lamb_id=basic_id).first()
                lamb = EBreedLambinfo.query.filter_by(basic_id=basic_id).first()
                if lamb.sex == 1:
                    chushengm.append(lamb)
                else:
                    chushengg.append(lamb)
                if duannai1:
                    duannai.append(duannai1)
                    duannaishu += 1
                    lamb = EBreedLambinfo.query.filter_by(basic_id=basic_id).first()
                    if lamb.sex == 1:
                        duannaim.append(duannai1)
                    else:
                        duannaig.append(duannai1)
        duannailv = duannaishu / huogaoshu if huogaoshu else 0
        print('我完成这一步计算了')

        duannaim = list(set(duannaim))
        duannaig = list(set(duannaig))
        chushengm = list(set(chushengm))
        chushengg = list(set(chushengg))

        chushengzm = []
        chushengzg = []
        duannaizm = []
        duannaizg = []
        for i in chushengm:
            chushengzm.append(i.bir_weight if i.bir_weight else 0)
        for i in chushengg:
            chushengzg.append(i.bir_weight if i.bir_weight else 0)
        for i in duannaim:
            duannaizm.append(i.wea_weight)
        for i in duannaig:
            duannaizg.append(i.wea_weight)
        pingjuncm = sum(chushengzm) / len(chushengm) if chushengm else 0
        pingjuncg = sum(chushengzg) / len(chushengg) if chushengg else 0
        pingjundm = sum(duannaizm) / len(duannaizm) if duannaizm else 0
        pingjundg = sum(duannaizg) / len(duannaizg) if duannaizg else 0
        print('我又完成下一步了')
        houyi_score = 0
        basic = BasicBasicinfo.query.filter_by(id=basic1).first()
        age = basic.mon_age
        variety = basic.variety
        sex = basic.sex
        gene_a = basic.gene_a
        standard = BasicMakescore.query.filter(
            (BasicMakescore.variety == variety) & (BasicMakescore.sex == sex) | (BasicMakescore.gene_a == gene_a)).first()
        if age < 24:
            houyi_score += 35
        else:
            if yupeishu >= 500:
                houyi_score += 5
            elif yupeishu >= 400:
                houyi_score += 4
            elif yupeishu >= 300:
                houyi_score += 3

            if shoutailv >= 0.85:
                houyi_score += 15
            if pingjuncg >= standard.birth_weight_2:
                houyi_score += 8
            if pingjuncm >= standard.birth_weight_2:
                houyi_score += 7
        shoutailv = f"{shoutailv:.1%}"
        huogaolv = f"{huogaolv:.1%}"
        duannailv = f"{duannailv:.1%}"
        pingjuncm = f"{pingjuncm:.1f}"
        pingjuncg = f"{pingjuncg:.1f}"
        pingjundm = f"{pingjundm:.1f}"
        pingjundg = f"{pingjundg:.1f}"
        print('我打完分了')
        data = {
            'yupeishu': yupeishu,
            'shoutaishu': shoutaishu,
            'shoutailv': shoutailv,
            'fenmianshu': fenmianshu,
            'hegeshu': hegeshu,
            'changaoshu': changaoshu,
            'huogaolv': huogaolv,
            'duannaishu': duannaishu,
            'duannailv': duannailv,
            'pingjuncg': pingjuncg,
            'pingjuncm': pingjuncm,
            'pingjundm': pingjundm,
            'pingjundg': pingjundg,
            'houyi_score': houyi_score,
            'year': year_date
        }
        print(data)
        return data

def get_rank(scorea):
        """获取等级"""
        if scorea >= 90:
            return '特级'
        elif scorea >= 80:
            return '一级'
        elif scorea >= 70:
            return '二级'
        elif scorea >= 60:
            return '三级'
        else:
            return '无'



@Statistic.route('/statistic/xipu/chakan', methods=['POST'])  #查看系谱档案
def chakan_xipu():
    data = request.get_json()
    id = data['id']
    basic = BasicBasicinfo.query.filter_by(id=id).first()
    if basic.sex == 1:
        contex = {}
        if id:
            # try:
            #     code_url = code(id, request)
            # except:
            #     code_url = ''
            contex['basic'] = get_basic(int(id))
            contex['first'] = get_first_table(int(id))

            # contex['first'] = [item.to_dict() for item in get_first_table(int(id))]
            contex['second'] = get_second_table(int(id))
            contex['third'] = get_third_table_mu(int(id)) if get_third_table_mu(int(id)) else {}
            contex['fourth'] = get_fourth_table(int(id)) if get_fourth_table(int(id)) else {}
            contex['fifth'] = get_fifth_table(int(id)) if get_fifth_table(int(id)) else {}
            contex['sixth'] = get_sixth_table(int(id)) if get_sixth_table(int(id)) else {}

            score_list = scoremake(id)
            basic_score = score_list[0]
            benshen_score = score_list[1]
            houyi_score = score_list[2]
            fangyi_score = score_list[3]
            scoreall = score_list[4]
            if scoreall >= 90:
                rank = '特级草'
            elif scoreall >= 80:
                rank = '一级草'
            elif scoreall >= 70:
                rank = '二级草'
            else:
                rank = ''
            contex['score'] = {
                'time': dt.datetime.now().strftime("%Y"),
                'score1': basic_score,
                'score2': benshen_score,
                'score3': houyi_score,
                'score4': fangyi_score,
                'scoreall': scoreall,
                'rank': rank
            }
            hege1 = False
            hege2 = False
            hege3 = False
            hege4 = False
            if basic_score >= 8: hege1 = True
            if benshen_score >= 40: hege2 = True
            if houyi_score >= 28: hege3 = True
            if fangyi_score >= 4: hege4 = True

            contex['judge'] = {
                'time': dt.datetime.now().strftime("%Y-%m-%d"),
                'jiben': '合格' if hege1 else '不合格',
                'benshen': '合格' if hege2 else '不合格',
                'houyi': '合格' if hege3 else '不合格',
                'fangyi': '合格' if hege4 else '不合格',
            }

        print(contex)
        a = render_template('home/xipumu.html', **contex)
        print(a)

        return render_template('home/xipumu.html', **contex)
        #     # 将查询到的数据以 JSON 格式返回
        #     print(f'contex我要测试向前端返回的格式{contex}')
        #     # result = {
        #     #     "code": 200,
        #     #     "data":{
        #     #         'contex':contex
        #     #     },
        #     #     "msg": '计算系谱档案成功'
        #     # }
        #     # print(result)
        #     # return jsonify(result)
        #     return contex
        # else:
        #     return jsonify({'error': 'No data found'}), 404
    else:
        # try:
        #     code_url = code(id, request)
        # except:
        #     code_url = ''
        contex = {}

        if id:
            contex['basic'] = get_basic(int(id))
            contex['first'] = get_first_table(int(id))
            # contex['first'] = [item.to_dict() for item in get_first_table(int(id))]
            contex['second'] = get_second_table(int(id))

            contex['third'] = get_third_table_gong(int(id)) if get_third_table_gong(int(id)) else {}

            contex['fourth'] = get_fourth_table(int(id)) if get_fourth_table(int(id)) else {}
            contex['fifth'] = get_fifth_table(int(id)) if get_fifth_table(int(id)) else {}
            print(contex['fifth'])
            print("sssbsbbs")
            contex['sixth'] = get_sixth_table(int(id)) if get_sixth_table(int(id)) else {}

            score_list = scoremake(id)
            basic_score = score_list[0]
            benshen_score = score_list[1]
            houyi_score = score_list[2]
            fangyi_score = score_list[3]
            scoreall = score_list[4]

            if scoreall >= 90:
                rank = '特级草'
            elif scoreall >= 80:
                rank = '一级草'
            elif scoreall >= 70:
                rank = '二级草'
            else:
                rank = ''
            contex['score'] = {
                'time': dt.datetime.now().strftime("%Y"),
                'score1': basic_score,
                'score2': benshen_score,
                'score3': houyi_score,
                'score4': fangyi_score,
                'scoreall': scoreall,
                'rank': rank
            }
            hege1 = False
            hege2 = False
            hege3 = False
            hege4 = False
            if basic_score >= 8: hege1 = True
            if benshen_score >= 40: hege2 = True
            if houyi_score >= 28: hege3 = True
            if fangyi_score >= 4: hege4 = True

            contex['judge'] = {
                'time': dt.datetime.now().strftime("%Y-%m-%d"),
                'jiben': '合格' if hege1 else '不合格',
                'benshen': '合格' if hege2 else '不合格',
                'houyi': '合格' if hege3 else '不合格',
                'fangyi': '合格' if hege4 else '不合格'
            }
        print(contex)
        b  = render_template('home/xipugong.html', **contex)
        print(b)
            # contex['code_url'] = code_url
        return render_template('home/xipugong.html', **contex)







    # 11111111111111111111111
    # data = request.get_json()
    # basic_id = data.get('id')

    # try:
    #     basic = BasicBasicinfo.query.get_or_404(basic_id)
    #     response_data = {
    #         'basic': get_basic(basic_id),
    #         'first_table': [item.to_dict() for item in get_first_table(basic_id)],
    #         'second_table': get_second_table(basic_id),
    #         'third_table': get_third_table_gong(basic_id) if basic.sex == 0 else get_third_table_mu(basic_id),
    #         'fourth_table': get_fourth_table(basic_id),
    #         'fifth_table': get_fifth_table(basic_id),
    #         'sixth_table': get_sixth_table(basic_id),
    #         'score': calculate_score(basic_id),
    #         'judge': calculate_judge(basic_id),
    #         'sex': basic.sex  # 0-父系 1-母系
    #     }
    #     return jsonify({'code': 200, 'data': response_data})
    # except Exception as e:
    #     return jsonify({'code': 500, 'message': str(e)})


def calculate_score(basic_id):
    score_list = scoremake(basic_id)
    return {
        'time': datetime.now().strftime("%Y"),
        'basic_score': score_list[0],
        'self_score': score_list[1],
        'offspring_score': score_list[2],
        'health_score': score_list[3],
        'total_score': score_list[4],
        'rank': '特级草' if score_list[4] >= 90 else '一级草' if score_list[4] >= 80 else '二级草'
    }


def calculate_judge(basic_id):
    scores = scoremake(basic_id)
    return {
        'time': datetime.now().strftime("%Y-%m-%d"),
        'basic_pass': scores[0] >= 8,
        'self_pass': scores[1] >= 40,
        'offspring_pass': scores[2] >= 28,
        'health_pass': scores[3] >= 4
    }



@Statistic.route('/statistic/obsoletegrassinfo', methods=['POST'])  #查看系谱档案
def get_obsoletegrassinfo():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))
    print(pageSize)

    conditions = []
    search_params = {
        'ele_num': BasicObsoleteGrassinfo.ele_num,
        'pre_num': BasicObsoleteGrassinfo.pre_num,
        'obsolete_type': BasicObsoleteGrassinfo.obsolete_type,
        'obsolete_date': BasicObsoleteGrassinfo.obsolete_date,
        'dead_date': BasicObsoleteGrassinfo.dead_date,
        'sales_date': BasicObsoleteGrassinfo.sales_date

    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'obsolete_date' or param == 'dead_date' or param == 'sales_date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))

            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = BasicObsoleteGrassinfo.query.filter(and_(*conditions))
    else:
        query = BasicObsoleteGrassinfo.query  # 如果没有条件，查询所有

    # 并且根据id降序排列

    query = query.filter(BasicObsoleteGrassinfo.belong == 0)
    # query = query.filter(BasicObsoleteGrassinfo.belong == 0).order_by(BasicObsoleteGrassinfo.basic_id.desc())
    print(query)
    print('我要开始排序了')
    infos = query.order_by(desc(BasicObsoleteGrassinfo.id)).paginate(page=pageNum, per_page=pageSize,
                                                                  error_out=False)
    print('我排好序了')
    total = query.count()

    list = []
    for info in infos:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        data = json.loads(data)
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