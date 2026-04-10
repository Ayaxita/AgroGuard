# views.py: 路由 + 视图函数
import datetime
from datetime import timedelta
import os
import random
import json
import hashlib
import flask_jwt_extended

from flask import Blueprint, render_template, request, make_response, Response, redirect, url_for, session, jsonify, \
    send_file
from sqlalchemy import desc, and_, or_, not_, func
import pandas as pd
from .models import *
from ..modelsReverse import *
from ..utils.AlchemyEncoder import AlchemyEncoder


def md5(text):
    return hashlib.md5(text.encode()).hexdigest()

# 蓝图
login_auth = Blueprint('login_auth', __name__)


def md5(text):
    return hashlib.md5(text.encode()).hexdigest()

# 蓝图
login_auth = Blueprint('login_auth', __name__)


@login_auth.route('/login', methods=['GET', 'POST'])
def login():
    import sys
    print(f"DEBUG: sys.version = {sys.version}", flush=True)
    data = request.get_json()
    name = data['username']
    pwd = data['password']
    print(f"DEBUG: name={name}, pwd={pwd}, pwd type={type(pwd)}", flush=True)
    user = Testuser.query.filter_by(username=name).first()
    if user:
        print(f"DEBUG: user.username={user.username}, user.password={user.password}, type={type(user.password)}", flush=True)
        print(f"DEBUG: pwd==user.password: {pwd == user.password}", flush=True)
        print(f"DEBUG: md5(pwd)={md5(pwd)}, user.password={user.password}", flush=True)
        print(f"DEBUG: md5(pwd)==user.password: {md5(pwd) == user.password}", flush=True)
    if user and name == user.username and pwd == user.password:
        # 'b8f994d0c9e22cb4c365915254cb0d2c'
        ctime = datetime.now()
        # expire_date = ctime + timedelta(days=2)
        # exptime = expire_date.strftime('%Y-%m-%dT%H:%M:%S')
        # payload = {"name": name, "expire_date": exptime}
        # access_token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        # access_token = flask_jwt_extended.create_access_token(identity=name, additional_claims=payload)
        access_token = flask_jwt_extended.create_access_token(identity=name)
        refresh_token = flask_jwt_extended.create_refresh_token(identity=name)
        user.last_login = ctime
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            result = {
                'code': 500,
                'msg': '数据库出现未知错误',
            }
            return jsonify(result)
        result = {
            'code': 200,
            'data': {
                'access_token': access_token,
                'refresh_token': refresh_token,
            },
            'msg': '登录成功',
        }
        return jsonify(result)
    else:
        result = {
            'code': 400,
            'msg': '用户名或密码错误',
        }
        return jsonify(result)


@login_auth.route('/logout', methods=['GET', 'POST'])
def logout():
    result = {
        'code': 200,
        'data': {
            'access_token': 123456
        },
        'msg': '登出成功',
    }
    return jsonify(result)


@login_auth.route('/user/reset_password', methods=['GET', 'POST'])
def reset_password():
    data = request.get_json()
    name = data['username']
    pwd_old = data['password_old']
    user = Testuser.query.filter_by(username=name).first()
    if pwd_old != user.password:
        result = {
            'code': 400,
            'msg': '旧密码错误',
        }
        return jsonify(result)
    pwd_new = data['password_new']
    user.password = pwd_new
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        result = {
            'code': 500,
            'msg': '数据库出现未知错误',
        }
        return jsonify(result)
    result = {
        'code': 200,
        'msg': '密码修改成功',
    }
    return jsonify(result)


@login_auth.route('/login/test', methods=['POST'])
def test():
    '''
    返回需要处理的预警信息长度,按照数据库的顺序排列
    :return: MessageLength
    '''
    list = []
    nowtime = datetime.now()
    nowtime = nowtime.strftime('%Y-%m-%d')
    # 按 vaccine_id 分组，并统计每组的数量
    query = db.session.query(
        WinformationImmunizationMessageinfo.vaccine_id,
        func.count(WinformationImmunizationMessageinfo.id).label('count')
    ).filter(WinformationImmunizationMessageinfo.dead_date <= nowtime).group_by(WinformationImmunizationMessageinfo.vaccine_id)

    # 执行查询并获取结果
    results = query.all()

    for vaccine_id, count in results:
        cname = SupplyCommodityinfo.query.filter_by(id=vaccine_id).first().cname
        list.append({
            "vaccine_id": vaccine_id,
            "cname": cname,
            "Messagelength": count
        })
    '''
    这里的注释是之前写的内容，功能是查询到所有的预警信息，将详细信息在消息界面显示，现在要更新这种做法
    :return: 
    '''
    '''
    data1 = [{"ele_num": "131102202240632", "house": "A区", "hurdle_name": "1栏", "imm_name": "防犬疫苗",
             "date": "2024-12-12"}]
    list = []
    #疫苗信息
    
        1.第Ⅱ号炭疽芽胞苗 2.布氏杆菌病猪型疫苗 3.羔羊大肠杆菌病灭活疫苗 7.布氏杆菌病羔羊型疫苗 9.O型口蹄疫
        10.多联必应 12.小反刍兽疫 22.口蹄疫O型.A型二价苗 25.羊痘 30.山羊痘活疫苗 62.六联干粉灭活疫苗 63.六联干粉灭活疫苗
    
    infos = ["第Ⅱ号炭疽芽胞苗", "布氏杆菌病猪型疫苗", "羔羊大肠杆菌病灭活疫苗" ,"布氏杆菌病羔羊型疫苗","O型口蹄疫",
        "多联必应","小反刍兽疫","口蹄疫O型.A型二价苗","羊痘","山羊痘活疫苗","六联干粉灭活疫苗","六联干粉灭活疫苗"]
    for info in infos:

        query = db.session.query(BasicBasicinfo.ele_num, BasicBasicinfo.house_name,BasicBasicinfo.hurdle_name,
                                 BasicBasicinfo.birth,SupplyCommodityinfo.cname) \
            .outerjoin(DHealthImmunizationinfo, BasicBasicinfo.id == DHealthImmunizationinfo.basic_id) \
            .outerjoin(SupplyCommodityinfo, DHealthImmunizationinfo.vaccine_id == SupplyCommodityinfo.id) \
            .filter(BasicBasicinfo.mon_age<6 ,SupplyCommodityinfo.cname !=info)\
            .limit(10).all()
        for res in query:
            list.append({
                "ele_num": res[0],
                "house":res[1],
                "hurdle_name":res[2],
                "imm_name":info,
                "date":res[3].strftime("%Y-%m-%d")
            })
    '''
    result = {
        "code": 200,
        "data": list,
        "msg": "预警信息获取成功"
    }
    return jsonify(result)
