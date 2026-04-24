# views.py: 路由 + 视图函数
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

# 蓝图
basic = Blueprint('basic', __name__)


def load_data_from_yaml():
    filename = os.path.join(os.getcwd(), 'App', 'basic', 'datafiles', 'data.yaml')
    with open(filename, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    return data


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


# 获取数据库数据
@basic.route('/basic/basicinfo', methods=['POST'])
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
        print(value)
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

    # 筛选出未淘汰(状态-1)和未绝收(状态0)的田块记录
    # 并且根据id降序排列

    query = query.filter(and_(BasicBasicinfo.state == 1, BasicBasicinfo.belong == 0))
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

@basic.route('/basic/basicinfo/initHouseAndHurdle', methods=['POST'])
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


@basic.route('/basic/basicinfo/initManu', methods=['POST'])
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


@basic.route('/basic/basicinfo/sheepTransfer', methods=['POST'])
def sheepTransfer():
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
            "msg": f'分区调整失败 {str(e)}'
        }
        return jsonify(result)
    result = {
        "code": 200,
        "msg": '分区调整成功'
    }
    return jsonify(result)


@basic.route('/basic/file/upload/img', methods=['POST'])
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


@basic.route('/basic/file/download/img', methods=['GET'])
def download_img():
    # print('download---------------------------------------')
    filename = request.args.get('filename')
    file_path = os.path.join(os.getcwd(), 'App', 'basic', 'img', filename)
    return send_file(file_path, as_attachment=True)


@basic.route('/basic/basicinfo/detail', methods=['POST'])
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


@basic.route('/basic/basicinfo/addImmunization', methods=['POST'])
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
@basic.route('/basic/basicinfo/add', methods=['POST'])
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
        if house_info.sheep_quantity is None:
            house_info.sheep_quantity = 1
            hurdle_info.sheep_quantity = 1
        else:
            house_info.sheep_quantity += 1
            hurdle_info.sheep_quantity += 1
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


@basic.route('/basic/basicinfo/validateSheepNum', methods=['POST'])
def validate_sheep_num():
    prop = request.json.get('prop')
    value = request.json.get('value')
    if prop == 'ele_num':
        if BasicBasicinfo.query.filter_by(ele_num=value).first():
            result = {
                "code": 200,
                'realcode': 500,
                "msg": '电子耳号已存在'
            }
            return jsonify(result)
    elif prop == 'pre_num':
        if BasicBasicinfo.query.filter_by(pre_num=value).first():
            result = {
                "code": 200,
                'realcode': 500,
                "msg": '防疫耳号已存在'
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
                "msg": '父不在羊场中,验证成功'
            }
            return jsonify(result)
        info = BasicBasicinfo.query.filter_by(ele_num=value).first()
        if info is None:
            result = {
                "code": 200,
                'realcode': 500,
                "msg": '父电子耳号不存在'
            }
            return jsonify(result)
        else:
            result = {
                "code": 200,
                'realcode': 200,
                'data': {
                    'f_pre_num': info.pre_num,
                },
                "msg": '父电子耳号存在, 验证成功'
            }
            return jsonify(result)
    elif prop == 'f_pre_num' and value != '0':
        info = BasicBasicinfo.query.filter_by(pre_num=value).first()
        if info is None:
            result = {
                "code": 200,
                'realcode': 500,
                "msg": '父防疫耳号不存在'
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
                "msg": '母不在羊场中,验证成功'
            }
            return jsonify(result)
        info = BasicBasicinfo.query.filter_by(ele_num=value).first()
        if info is None:
            result = {
                "code": 200,
                'realcode': 500,
                "msg": '母电子耳号不存在'
            }
            return jsonify(result)
        else:
            result = {
                "code": 200,
                'realcode': 200,
                'data': {
                    'm_pre_num': info.pre_num,
                },
                "msg": '母电子耳号存在, 验证成功'
            }
            return jsonify(result)
    elif prop == 'm_pre_num' and value != '0':
        info = BasicBasicinfo.query.filter_by(pre_num=value).first()
        if info is None:
            result = {
                "code": 200,
                'realcode': 500,
                "msg": '母防疫耳号不存在'
            }
            return jsonify(result)
    result = {
        "code": 200,
        'realcode': 200,
        "msg": '验证成功'
    }
    return jsonify(result)


# http://127.0.0.1:5000/basic/basicinfo/edit
@basic.route('/basic/basicinfo/edit', methods=['POST'])
def edit_basic_info():
    data = request.get_json()
    # print("--data-->", data)
    ele_num = data['ele_num']
    # 在标记淘汰过程中，将田块归入淘汰分区
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



# 标记田块淘汰，写入信息到淘汰记录，在标记绝收和标记淘汰时复写该条记录
@basic.route('/basic/basicinfo/obsolete', methods=['POST'])
def obsolete_sheep():
    data = request.get_json()
    print(data)

    # 在标记淘汰过程中，将田块归入淘汰分区
    state = data['state']
    ele_num = data['ele_num']
    if (state == -1):
            dieoutHurdle_info = ColonyHouseinfo.query.filter_by(name="淘汰栏").first()
            dieoutHouse_info = ColonyHouseinfo.query.filter_by(id=dieoutHurdle_info.pid).first()
            original_data = BasicBasicinfo.query.filter_by(ele_num=ele_num).first()
            data['house_id'] = dieoutHouse_info.id
            data['house_name'] = dieoutHouse_info.name
            data['hurdle_id'] = dieoutHurdle_info.id
            data['hurdle_name'] = dieoutHurdle_info.name
    try:
        # 开始事务
        with db.session.begin_nested():
            # 执行 update 操作
            BasicBasicinfo.query.filter_by(ele_num=ele_num).update(data)
            # 执行 add 操作
            belong = 0
            basic_id = data['id']
            obsolete_type = data['state']
            obsolete_date = datetime.now()
            ele_num = data['ele_num']
            pre_num = data['pre_num']

            insert_data = {
                'obsolete_date': obsolete_date,
                'belong': belong,
                'basic_id': basic_id,
                'obsolete_type': obsolete_type,
                'ele_num': ele_num,
                'pre_num': pre_num
            }

            # '''
            # ** insert_data 是Pythoninsert_data结合使用的写法。
            # 把 insert_data 字典中的每个键值对解包成关键字参数。
            # 把这些关键字参数传递给 BasicObsoleteSheepinfo 类的构造函数。
            # BasicObsoleteSheepinfo(**insert_data)
            # 就相当于
            # BasicObsoleteSheepinfo(obsolete_date=datetime.now(), belong=0, basic_id=123)。
            # '''


            obsoletesheep_info = BasicObsoleteSheepinfo(**insert_data)
            db.session.add(obsoletesheep_info)
            db.session.commit()
    except Exception as e:
        # 事务中任何操作出错，都会回滚整个事务
        db.session.rollback()
        result = {
            "code": 500,
            "msg": f'操作失败: {str(e)}'
        }
        return jsonify(result)

    result = {
        "code": 200,
        "msg": '标记淘汰成功'
    }
    return jsonify(result)

    #     BasicBasicinfo.query.filter_by(ele_num=ele_num).update(data)
    #     print('我要提交了')
    #     db.session.commit()
    # except Exception as e:
    #     db.session.rollback()
    #     db.session.flush()
    #     result = {
    #         "code": 500,
    #         "msg": f'修改失败 {str(e)}'
    #     }
    #     return jsonify(result)
    #
    # belong = 0
    # basic_id = data['id']
    # obsolete_type = data['state']
    # obsolete_date = datetime.now()
    # ele_num = data['ele_num']
    # pre_num = data['pre_num']
    #
    # # 创建一个字典来存储需要插入的数据
    # insert_data = {
    #     'obsolete_date': obsolete_date,
    #     'belong': belong,
    #     'basic_id': basic_id,
    #     'obsolete_type': obsolete_type,
    #     'ele_num': ele_num,
    #     'pre_num': pre_num
    # }



    # obsoletesheep_info= BasicObsoleteSheepinfo(**insert_data)
    #
    # try:
    #     db.session.add(obsoletesheep_info)
    #     print('我要添加了')
    #     db.session.commit()
    # except Exception as e:
    #     # 补偿操作：撤销之前的 update 操作
    #     try:
    #         if 'original_data' in locals():
    #             for key, value in original_data.__dict__.items():
    #                 if key != '_sa_instance_state':
    #                     setattr(BasicBasicinfo.query.filter_by(ele_num=ele_num).first(), key, value)
    #             db.session.commit()
    #     except Exception as inner_e:
    #         result = {
    #             "code": 500,
    #             "msg": f'标记淘汰失败，且回滚修改信息失败: {str(e)} {str(inner_e)}'
    #         }
    #     else:
    #         result = {
    #             "code": 500,
    #             "msg": f'标记淘汰失败，已回滚修改信息: {str(e)}'
    #         }
    #     return jsonify(result)
    # result = {
    #     "code": 200,
    #     "msg": '标记淘汰成功'
    # }
    # return jsonify(result)

# 系谱
@basic.route('/basic/basicinfo/familyTree', methods=['POST'])
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
        "selected_sheep": get_family_member_info(basic_info),
        "father": get_family_member_info(father_info),
        "mother": get_family_member_info(mother_info),
        "grandfather": get_family_member_info(grandfather_info),
        "grandmother": get_family_member_info(grandmother_info),
        "maternal_grandfather": get_family_member_info(maternal_grandfather_info),
        "maternal_grandmother": get_family_member_info(maternal_grandmother_info),
    }

    return jsonify(family_tree)


# 导出
@basic.route('/basic/basicinfo/export', methods=['POST'])
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
    filename = os.path.join(os.getcwd(), 'App', 'basic', 'export_excel', 'basic_info.xlsx')
    # export_filename = r'.\basic\export_excel\basic_info.xlsx'
    export_filename = os.path.join(os.getcwd(), 'App', 'basic', 'export_excel', 'basic_info.xlsx')
    dataframes.to_excel(filename, index=False)
    return send_file(export_filename, as_attachment=True)


@basic.route('/basic/basicinfo/import_template', methods=['POST'])
def import_template():
    filename = os.path.join(os.getcwd(), 'App', 'basic', 'temp_excel', '草地基本信息导入模板.xls')
    return send_file(filename, as_attachment=True)


#批量导入
@basic.route('/basic/basicinfo/import', methods=['POST'])
def import_basic_info():

    file_path = os.path.join(os.getcwd(), 'App', 'basic', 'imported_excel', request.files['file'].filename)
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
                pre_num = df.iloc[r, 1]  # 获取防疫耳号
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
@basic.route('/basic/basicinfo/updateMonAge', methods=['POST'])
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


@basic.route('/basic/basicinfo/updateHouseAndHurdle', methods=['POST'])
def update_house_and_hurdle():
    colony_infos = ColonyHouseinfo.query.all()
    for info in colony_infos:
        if info.pid == 0:
            info.sheep_quantity = BasicBasicinfo.query.filter_by(house_id=info.id).count()
        else:
            info.sheep_quantity = BasicBasicinfo.query.filter_by(hurdle_id=info.id).count()
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
@basic.route('/basic/basicinfo/markSheepDeath', methods=['POST'])
def mark_sheep_death():
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
        # 查找并更新 BasicObsoleteSheepinfo 表的记录
        obsolete_info = BasicObsoleteSheepinfo.query.filter_by(basic_id=info['basic_id']).first()
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



# 标记售出
@basic.route('/basic/basicinfo/markSheepSale', methods=['POST'])
def mark_sheep_sale():
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

        # 查找并更新 BasicObsoleteSheepinfo 表的记录
        obsolete_info = BasicObsoleteSheepinfo.query.filter_by(basic_id=info['basic_id']).first()
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


@basic.route('/basic/manuinfo', methods=['POST'])
def get_manu_info():
    pageNum = int(request.json.get('pageNum'))
    # pageNum = int(request.form.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))
    conditions = []
    search_params = {
        'id': BasicManuinfo.id,
        'manu_name': BasicManuinfo.manu_name,
        'scale': BasicManuinfo.scale,
        'type': BasicManuinfo.type,
        'BP_license_num': BasicManuinfo.BP_license_num,
        'AP_certificate_num': BasicManuinfo.AP_certificate_num,
        'BL_num': BasicManuinfo.BL_num,
        'legal': BasicManuinfo.legal,
        'address': BasicManuinfo.address,
        'contact': BasicManuinfo.contact,
        'province': BasicManuinfo.province,
        'city': BasicManuinfo.city,
        'belong': BasicManuinfo.belong,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = BasicManuinfo.query.filter(and_(*conditions))
    else:
        query = BasicManuinfo.query  # 如果没有条件，查询所有

    manuinfos = query.filter(BasicManuinfo.belong == 0).paginate(page=pageNum, per_page=pageSize, error_out=False)
    total = query.count()
    list = []
    for info in manuinfos:
        list.append({
            'id': info.id,
            'manu_name': info.manu_name,
            'scale': info.scale,
            'type': info.type,
            'BP_license_num': info.BP_license_num,
            'AP_certificate_num': info.AP_certificate_num,
            'BL_num': info.BL_num,
            'legal': info.legal,
            'address': info.address,
            'contact': info.contact,
            'province': info.province,
            'city': info.city,
            'belong': info.belong,
        })

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


# 添加产地信息
# {
#         "manu_name": "test01",
#         "scale": 1,
#         "type": 1,
#         "BP_license_num": 1,
#         "AP_certificate_num": 1,
#         "BL_num": 1,
#         "legal": 1,
#         "address": 1,
#         "contact": 1,
#         "province": 1,
#         "city": 1,
#         "belong": 1
#     }
# http://127.0.0.1:5000/basic/manuinfo/add
@basic.route('/basic/manuinfo/add', methods=['POST'])
def add_manu_info():
    data = request.get_json()
    data['belong'] = 0
    # print(data)
    manuinfo = BasicManuinfo()
    for key, value in data.items():
        setattr(manuinfo, key, value)
    try:
        db.session.add(manuinfo)
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


# 修改产地信息（不用传belong）
# {
#         "id": "14",
#         "manu_name": "test01_to_edit",
#         "scale": 1,
#         "type": 1,
#         "BP_license_num": 1,
#         "AP_certificate_num": 1,
#         "BL_num": 1,
#         "legal": 1,
#         "address": 1,
#         "contact": 1,
#         "province": 1,
#         "city": 1
#     }
# http://127.0.0.1:5000/basic/manuinfo/edit
@basic.route('/basic/manuinfo/edit', methods=['POST'])
def edit_manu_info():
    data = request.get_json()
    # print("--data-->", data)
    id = data['id']
    BasicManuinfo.query.filter_by(id=id).update(data)
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


def fun(param):
    id1 = param.id
    return id1


@basic.route('/basic/breederconditioninfo', methods=['POST'])
def get_breedercondition_info():
    pageNum = int(request.json.get('pageNum'))
    # pageNum = int(request.form.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))
    conditions = []
    search_params = {
        'id': BasicBreederconditioninfo.id,
        'date': BasicBreederconditioninfo.date,
        'basic_id': BasicBreederconditioninfo.basic_id,
        'age': BasicBreederconditioninfo.age,
        'mon_age': BasicBreederconditioninfo.mon_age,
        # 'color': BasicBreederconditioninfo.color,
        'rank': BasicBreederconditioninfo.rank,
        'high': BasicBreederconditioninfo.high,
        'weight': BasicBreederconditioninfo.weight,
        'Llong': BasicBreederconditioninfo.Llong,
        'bust': BasicBreederconditioninfo.bust,
        'back_fat': BasicBreederconditioninfo.back_fat,
        'eye': BasicBreederconditioninfo.eye,
        'testis_shape': BasicBreederconditioninfo.testis_shape,
        't_staff': BasicBreederconditioninfo.t_staff,
        'AE': BasicBreederconditioninfo.AE,
        'performance_traits': BasicBreederconditioninfo.performance_traits,
        'with_births': BasicBreederconditioninfo.with_births,
        'wea_weight': BasicBreederconditioninfo.wea_weight,
        'June_heavy': BasicBreederconditioninfo.June_heavy,
        'health': BasicBreederconditioninfo.health,
        'f_date': BasicBreederconditioninfo.f_date,
        'f_staff': BasicBreederconditioninfo.f_staff,
        'notes': BasicBreederconditioninfo.notes,
        'belong': BasicBreederconditioninfo.belong,

        'ele_num': BasicBreederconditioninfo.basic_id,
        'variety': BasicBreederconditioninfo.basic_id,
        'color': BasicBreederconditioninfo.basic_id
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'date' or param == 'f_date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            # 十分费时的查询
            elif param == 'ele_num' or param == 'variety' or param == 'color':
                basic_info = BasicBasicinfo.query.filter(getattr(BasicBasicinfo, param) == value).all()
                basic_ids = [i.id for i in basic_info]
                conditions.append(column.in_(basic_ids))
            else:
                conditions.append(column == value)

    # # 实现外表查询,查询关联外键的所给参数的basic_id
    # # 这个查询十分费时
    # basic_conditions = []
    # basic_search_params = {
    #     'color': BasicBasicinfo.color,
    #     'ele_num': BasicBasicinfo.ele_num,
    #     'variety': BasicBasicinfo.variety,
    # }
    # for param, column in basic_search_params.items():
    #     value = request.json.get(param)
    #     if value is not None:  # 检查值不为 None
    #         basic_conditions.append(column == value)
    # # 如果有三个条件:电子耳号,品种,毛色,则查询basic表的id,并将条件添加到conditions
    # if basic_conditions:
    #     basic_query = BasicBasicinfo.query.filter(and_(*basic_conditions))
    #     # 如果没有，什么也不干
    #
    #     basic_ids = []
    #     for info in basic_query:
    #         basic_ids.append(info.id)
    #     # print(basic_ids)
    #     conditions.append(BasicBreederconditioninfo.basic_id.in_(basic_ids))
    # 使用 and_() 组合条件
    if conditions:
        query = BasicBreederconditioninfo.query.filter(and_(*conditions))
    else:
        query = BasicBreederconditioninfo.query  # 如果没有条件，查询所有

    breederconditioninfos = query.filter(BasicBreederconditioninfo.belong == 0).paginate(page=pageNum,
                                                                                         per_page=pageSize,
                                                                                         error_out=False)
    total = query.count()
    list = []
    for info in breederconditioninfos:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        data = json.loads(data)
        data['ele_num'] = BasicBasicinfo.query.filter_by(id=data['basic_id']).first().ele_num
        data['variety'] = BasicBasicinfo.query.filter_by(id=data['basic_id']).first().variety
        data['color'] = BasicBasicinfo.query.filter_by(id=data['basic_id']).first().color
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


@basic.route('/basic/breederconditioninfo/add', methods=['POST'])
def add_breedercondition_info():
    data = request.get_json()
    ctime = datetime.now().strftime("%Y-%m-%d")
    data['belong'] = 0
    data['f_date'] = ctime
    if data['date']:
        date_obj = datetime.strptime(data['date'], '%Y-%m-%d')
        # 将 datetime 对象转换为指定格式的字符串
        formatted_date = date_obj.strftime('%Y-%m-%d')
        data['date'] = formatted_date
    if data['ele_num']:
        data['basic_id'] = BasicBasicinfo.query.filter_by(ele_num = data['ele_num']).first().id
        del data['ele_num']

    # print(f'data----->{data}')
    # print(type(data))
    # print(data.keys())
    breeder_condition_info = BasicBreederconditioninfo()

    for key, value in data.items():
        if value == "":
            setattr(breeder_condition_info, key, None)  # 或者设置一个默认值
        else:
            setattr(breeder_condition_info, key, value)

    try:
        db.session.add(breeder_condition_info)
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


@basic.route('/basic/breederconditioninfo/edit', methods=['POST'])
def edit_breedercondition_info():
    data = request.get_json()
    # print("--data-->", data)

    # 前端传过来的数据有修改过的basic_id
    data.pop('ele_num')
    data.pop('variety')
    data.pop('color')
    BasicBreederconditioninfo.query.filter_by(id=data['id']).update(data)
    # breeder_condition_info = BasicBreederconditioninfo()
    # breederconditioninfo = BasicBreederconditioninfo.query.filter(
    #     BasicBreederconditioninfo.id == request.json.get('id')).first()
    #
    # id = data['id']
    # date_obj = datetime.strptime(data['date'], '%m/%d/%Y')
    # # 将 datetime 对象转换为指定格式的字符串
    # formatted_date = date_obj.strftime('%Y-%m-%d')
    # data['date'] = formatted_date
    #
    # date_obj = datetime.strptime(data['f_date'], '%m/%d/%Y')
    # # 将 datetime 对象转换为指定格式的字符串
    # formatted_date = date_obj.strftime('%Y-%m-%d')
    # data['f_date'] = formatted_date
    #
    # data['back_fat'] = breederconditioninfo.back_fat
    # data['eye'] = breederconditioninfo.eye

    # breeder_condition_info.query.filter_by(id=id).update(data)

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


@basic.route('/basic/breederconditioninfo/del', methods=['POST'])
def del_breederconditioninfo():
    ids = request.get_json()
    for i in ids:
        BasicBreederconditioninfo.query.filter_by(id=i).delete()
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


# http://127.0.0.1:5000/basic/basicinfo/update_grandparents
@basic.route('/basic/basicinfo/update_grandparents', methods=['POST'])
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

#获取状态为健康的羊的基本信息
@basic.route('/basic/breederconditioninfo/get_Goodsheep', methods=['POST'])
def get_Goodsheep():
    pageNum = int(request.json.get('pageNum'))
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
        query = BasicBasicinfo.query.filter(and_(
            *conditions,  # 原有的动态条件
            BasicBasicinfo.state == 1 # 固定条件：状态为1
        ))
    else:
        query = BasicBasicinfo.query.filter(and_(
            BasicBasicinfo.state == 1  # 固定条件：状态为1
        ))  # 如果没有动态条件，只筛选固定条件

    # 筛选出未淘汰(状态-1)和未绝收(状态0)的田块记录
    # 并且根据id降序排列

    query = query.filter(and_(BasicBasicinfo.state != -1, BasicBasicinfo.state != 0, BasicBasicinfo.belong == 0))

    # # 获取所有记录（不分页）
    # all_records = query.all()

    basic_infos = query.order_by(desc(BasicBasicinfo.id)).paginate(page=pageNum, per_page=pageSize, error_out=False)
    total = query.count()


    list = []

    for info in basic_infos:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        list.append(json.loads(data))
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

#通过父系id和母系id和出生日期寻找生长记录，然后找出苗数
@basic.route('/basic/breederconditioninfo/getWith_births', methods=['POST'])
def getWith_births():
    ewe_id = request.json.get('m_id')
    # pageNum = int(request.form.get('pageNum'))
    ram_id = request.json.get('f_id')

    birth = request.json.get('birth')

    # 构造查询条件
    conditions = []

    conditions.append(EBreedPostnatalinfo.ewe_id == ewe_id)
    conditions.append(EBreedPostnatalinfo.ram_id == ram_id)
    conditions.append(EBreedPostnatalinfo.delivery_date == birth)

    # 查询数据库，获取符合条件的记录
    num = EBreedPostnatalinfo.query.filter(and_(*conditions)).first().live_num

    result = {
        "code": 200,
        "data": num,
        "msg": '成功'
    }
    return jsonify(result)

@basic.route('/basic/cutinfo/add', methods=['POST'])
def add_cut_info():
    data = request.get_json()
    ctime = datetime.now().strftime("%Y-%m-%d")
    data['belong'] = 0
    data['f_date'] = ctime
    if data['cut_time']:
        date_obj = datetime.strptime(data['cut_time'], '%Y-%m-%d')
        # 将 datetime 对象转换为指定格式的字符串
        formatted_date = date_obj.strftime('%Y-%m-%d')
        data['cut_time'] = formatted_date
    if data['house_name']:
        del data['house_name']

    # print(f'data----->{data}')
    # print(type(data))
    # print(data.keys())
    cut_info = BasicCutinfo()

    for key, value in data.items():
        if value == "":
            setattr(cut_info, key, None)  # 或者设置一个默认值
        else:
            setattr(cut_info, key, value)

    try:
        db.session.add(cut_info)
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

@basic.route('/basic/cutinfo', methods=['POST'])
def get_cut_info():
    pageNum = int(request.json.get('pageNum'))
    # pageNum = int(request.form.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        'house_name': BasicCutinfo.id,
        'ele_quantity': BasicCutinfo.ele_quantity,
        'variety': BasicCutinfo.variety,
        'cut_time': BasicCutinfo.cut_time,
        'rank': BasicCutinfo.rank,
        'color': BasicCutinfo.color,
        'weight': BasicCutinfo.weight,
        'staff': BasicCutinfo.staff,
        'notes': BasicCutinfo.notes,
        'f_date': BasicCutinfo.f_date,
        'cut_num': BasicCutinfo.cut_num,
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'cut_time' or param == 'f_date':  # 日期需要转换
                conditions.append(column >= datetime.fromisoformat(value[0]))
                conditions.append(column <= datetime.fromisoformat(value[1]))
            elif param == 'house_name':
                house_id = ColonyHouseinfo.query.filter(
                    ColonyHouseinfo.house_name.like(f'%{value}%')).first().id
                conditions.append(column == house_id)
            else:
                conditions.append(column == value)

    # 使用 and_() 组合条件
    if conditions:
        query = BasicCutinfo.query.filter(and_(*conditions))
    else:
        query = BasicCutinfo.query  # 如果没有条件，查询所有

    # 筛选出未淘汰(状态-1)和未绝收(状态0)的田块记录
    # 并且根据id降序排列

    query = query.filter(and_(BasicCutinfo.belong == 0))
    cut_infos = query.order_by(desc(BasicCutinfo.id)).paginate(page=pageNum, per_page=pageSize, error_out=False)
    total = query.count()

    list = []
    for info in cut_infos:
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
        data = json.loads(data)
        print(data)
        house_info = ColonyHouseinfo.query.filter_by(id=data['house_id']).first()
        if house_info:
            data['house_name'] = house_info.name
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
    # return jsonify({
    #     "method": 'GET'
    # })

@basic.route('/basic/cutinfo/edit', methods=['POST'])
def edit_cut_info():
    data = request.get_json()
    # print("--data-->", data)

    # 前端传过来的数据有修改过的basic_id
    if data['house_name']:
        del data['house_name']
    BasicCutinfo.query.filter_by(id=data['id']).update(data)
    # breeder_condition_info = BasicBreederconditioninfo()
    # breederconditioninfo = BasicBreederconditioninfo.query.filter(
    #     BasicBreederconditioninfo.id == request.json.get('id')).first()
    #
    # id = data['id']
    # date_obj = datetime.strptime(data['date'], '%m/%d/%Y')
    # # 将 datetime 对象转换为指定格式的字符串
    # formatted_date = date_obj.strftime('%Y-%m-%d')
    # data['date'] = formatted_date
    #
    # date_obj = datetime.strptime(data['f_date'], '%m/%d/%Y')
    # # 将 datetime 对象转换为指定格式的字符串
    # formatted_date = date_obj.strftime('%Y-%m-%d')
    # data['f_date'] = formatted_date
    #
    # data['back_fat'] = breederconditioninfo.back_fat
    # data['eye'] = breederconditioninfo.eye

    # breeder_condition_info.query.filter_by(id=id).update(data)

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

@basic.route('/basic/cutinfo/del', methods=['POST'])
def del_cut_info():
    ids = request.get_json()
    for i in ids:
        BasicCutinfo.query.filter_by(id=i).delete()
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