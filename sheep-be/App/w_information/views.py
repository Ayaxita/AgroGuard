# views.py: 路由 + 视图函数
import datetime
import random
import os
from flask import Blueprint, render_template, request, make_response, Response, redirect, url_for, session, jsonify, \
    send_file
from sqlalchemy import desc, and_, or_, not_, text
import pandas as pd

from ..modelsReverse import *
import json
from ..utils.AlchemyEncoder import AlchemyEncoder

w_information = Blueprint('w_information', __name__)


@w_information.route('/w_information/immunizationMessageinfo', methods=['POST', "GET"])  # 疫苗预警 后端接口
def get_immunizationMessageinfo():
    pageNum = int(request.json.get('pageNum'))
    pageSize = int(request.json.get('pageSize'))

    conditions = []
    search_params = {
        # 'basic_id': DHealthDeathinfo.basic_id,
        'ele_num': WinformationImmunizationMessageinfo.basic_id,
        'pre_num': WinformationImmunizationMessageinfo.basic_id,
        'sex': WinformationImmunizationMessageinfo.sex,
        'variety': WinformationImmunizationMessageinfo.variety,
        'mon_age': WinformationImmunizationMessageinfo.mon_age,
        'house': WinformationImmunizationMessageinfo.house,
        'hurdle_name': WinformationImmunizationMessageinfo.hurdle_name,
        'vaccine_id': WinformationImmunizationMessageinfo.vaccine_id,

        'cname': WinformationImmunizationMessageinfo.vaccine_id,

        'birth': WinformationImmunizationMessageinfo.birth,
        "imm_date": WinformationImmunizationMessageinfo.imm_date,
        "distance_date": WinformationImmunizationMessageinfo.distance_date,
        'dead_date': WinformationImmunizationMessageinfo.dead_date,
        'f_staff': WinformationImmunizationMessageinfo.f_staff,
        'f_date': WinformationImmunizationMessageinfo.f_date,
        'note': WinformationImmunizationMessageinfo.note
    }
    for param, column in search_params.items():
        value = request.json.get(param)
        if value is not None:  # 检查值不为 None
            if param == 'birth' or param == 'dead_date' or param == 'imm_date' or param == 'distance_date' or param == 'f_date':  # 日期需要转换
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
        print(conditions)
        query = WinformationImmunizationMessageinfo.query.filter(and_(*conditions))
    else:
        query = WinformationImmunizationMessageinfo.query  # 如果没有条件，查询所有

    # 并且根据id降序排列

    # query = query.filter(WinformationImmunizationMessageinfo.state == 1)
    infos = query.order_by(desc(WinformationImmunizationMessageinfo.id)).paginate(page=pageNum, per_page=pageSize,
                                                                                  error_out=False)
    total = query.count()

    list = []
    for info in infos:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        data = json.loads(data)
        supplycommodityinfo = SupplyCommodityinfo.query.filter_by(id=data['vaccine_id']).first()
        if supplycommodityinfo:
            data['cname'] = supplycommodityinfo.cname
        del data["state"]
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


@w_information.route('/w_information/thresholdsetMessageinfo', methods=['POST'])  # 阈值设置 后端接口
def get_thresholdsetMessageinfo():
    query = ThresholdSetMessageinfo.query  # 如果没有条件，查询所有
    total = query.count()

    list = []
    for info in query:
        data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
        data = json.loads(data)
        supplycommodityinfo = SupplyCommodityinfo.query.filter_by(id=data['vaccine_id']).first()
        if supplycommodityinfo:
            data['cname'] = supplycommodityinfo.cname
        list.append(data)
    result = {
        "code": 200,
        "data": {
            "list": list,
            "total": total
        },
        "msg": '成功'
    }
    print(list)
    return jsonify(result)


@w_information.route('/w_information/thresholdsetMessageinfo/edit', methods=['POST'])  # 阈值设置 后端接口
def edit_thresholdsetMessageinfo():
    data = request.get_json()
    print("--data-->", data)

    try:
        for i in range(len(data)):
            if "cname" in data[i]:
                del data[i]["cname"]
            t = ThresholdSetMessageinfo.query.filter_by(id=data[i]['id']).first().ifyear
            if data[i]["ifyear"] != t:
                data[i]["ifchange"] = 1
    except Exception as e:
        print("--data-->", data)
        print("--Exception-->", str(e))
    print('--------------------------test--------------------------------')

    try:
        db.session.bulk_update_mappings(ThresholdSetMessageinfo, data)
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


@w_information.route('/w_information/thresholdsetMessageinfo/update', methods=['POST'])  # 手动更新信息 后端接口
def update_thresholdsetMessageinfo():
    print("更新数据库的时间:", datetime.now())
    try:
        # 开始一个事务
        db.session.begin()
        # 执行第一个 SQL 语句
        # 插入语句
        query_one = '''
                select vaccine_id,ifyear,ifchange from threshold_setting
        '''
        # query1指的是每种循环接种的疫苗对于已经在疫苗表中的信息添加
        query01 = '''
                SELECT threshold INTO @vaccine_threshold
                FROM threshold_setting
                WHERE vaccine_id = :id;
        '''
        query1 = '''
                INSERT into w_information_immunizationMessageinfo (basic_id , ele_num,pre_num, sex,variety,mon_age,house,hurdle_name,vaccine_id,birth,imm_date,distance_date,dead_date,state,f_staff,f_date,note)

                SELECT
                d.basic_id AS basic_id,
                b.ele_num AS ele_num,
                b.pre_num AS pre_num,
                b.sex AS sex,
                b.variety AS variety,
                ROUND((DATEDIFF(NOW(),b.birth)/30),1) AS mon_age,

                b.house_name AS house_name,
                b.hurdle_name AS hurdle_name,

                d.vaccine_id AS vaccine_id,
                b.birth AS birth,
                d.max_immdate as imm_date,
                DATEDIFF(NOW(),d.max_immdate) as distance_date,
                DATE_ADD(d.max_immdate,INTERVAL @vaccine_threshold day ) as dead_date,
                1 as state,
                'System' as f_staff,
                NOW() as f_date,
                '' as note

                FROM
                basic_basicinfo as b
                LEFT JOIN (select basic_id ,vaccine_id,MAX(imm_date) as max_immdate from d_health_immunizationinfo where vaccine_id= :id GROUP BY basic_id) as d
                ON b.id = d.basic_id
                LEFT JOIN supply_commodityinfo ON supply_commodityinfo.id = d.vaccine_id
                where d.vaccine_id = :id and b.state=1 and b.variety in (0,1)
                ORDER BY
                b.id ASC
            '''
        # query2指的是每种循环接种的疫苗对于从没有出现过疫苗表中的信息添加
        query2 = '''
                INSERT into w_information_immunizationMessageinfo (basic_id , ele_num,pre_num, sex,variety,mon_age,house,hurdle_name,vaccine_id,birth,imm_date,distance_date,dead_date,state,f_staff,f_date,note)
                SELECT
                b.id,
                b.ele_num AS ele_num,
                b.pre_num AS pre_num,
                b.sex AS sex,
                b.variety AS variety,
                ROUND((DATEDIFF(NOW(),b.birth)/30),1) AS mon_age,

                b.house_name AS house_name,
                b.hurdle_name AS hurdle_name,

                :id AS vaccine_id,
                b.birth AS birth,
                b.birth as imm_date,
                DATEDIFF(NOW(),b.birth) as distance_date,
                DATE_ADD(b.birth,INTERVAL @vaccine_threshold day ) as dead_date,
                1 as state,
                'System' as f_staff,
                NOW() as f_date,
                '' as note
                FROM
                basic_basicinfo AS b
                WHERE
                b.state = 1 AND
                b.variety IN (1,0) and
                id not in (select basic_id from d_health_immunizationinfo)
            '''
        # query11删除表中原来的记录
        query11 = '''
                DELETE w
                FROM
                w_information_immunizationMessageinfo AS w
                WHERE
                w.vaccine_id = :id;
        '''
        # 设置初始化结束的ifchange为0
        query12 = '''
            UPDATE threshold_setting AS t
            SET
            ifchange = 0
            where
            t.vaccine_id= :id;
        '''
        # 后续更新query3指的是跟新下次信息，query4是日常更新
        query3 = '''
                update w_information_immunizationMessageinfo w 
                INNER JOIN d_health_immunizationinfo  d
                ON w.basic_id = d.basic_id AND w.vaccine_id = d.vaccine_id
                inner join threshold_setting t
                on t.vaccine_id = w.vaccine_id
                set w.imm_date = d.imm_date, w.mon_age = ROUND((DATEDIFF(CURRENT_DATE,w.birth)/30),1) , w.distance_date = DATEDIFF(CURRENT_DATE,d.imm_date), 
                w.dead_date = DATE_ADD(d.imm_date,INTERVAL threshold day ),
                w.f_date = NOW()
                WHERE w.imm_date < d.imm_date and t.ifyear = 0
            '''
        query4 = '''
                UPDATE w_information_immunizationMessageinfo AS w
                INNER JOIN   basic_basicinfo b 
                on b.id = w.basic_id                
                SET
                    w.mon_age = ROUND(DATEDIFF(CURRENT_DATE, b.birth) / 30, 1),
                    w.distance_date = DATEDIFF(CURRENT_DATE, w.imm_date),
                    w.house = b.house_name,
                    w.hurdle_name = b.hurdle_name;
            '''
        # 删除 query是删除不正常的羊
        query5 = '''
                DELETE w
                FROM
                w_information_immunizationMessageinfo AS w
                INNER JOIN basic_basicinfo AS b ON w.basic_id = b.id
                WHERE
                b.state != 1
            '''
        # 删除一生只打一次的羊
        query6 = '''
            delete w
            FROM
            w_information_immunizationMessageinfo AS w
            INNER JOIN d_health_immunizationinfo AS d ON d.basic_id = w.basic_id and w.vaccine_id = d.vaccine_id
            inner join threshold_setting as t
            on t.vaccine_id = w.vaccine_id
            WHERE
            t.ifyear =1 and d.imm_date is not null
        '''
        result_one = db.session.execute(text(query_one)).all()
        list = []  # 不需要初始化的
        list_init = []  # 需要初始化的列表
        for i in result_one:
            if (i[2] == 1):
                list_init.append({
                    "vaccine_id": i[0],
                    "ifyear": i[1],
                    "ifchange": i[2],
                })
            else:
                list.append({
                    "vaccine_id": i[0],
                    "ifyear": i[1],
                    "ifchange": i[2],
                })
        for li in list_init:  # 初始化循环
            result11 = db.session.execute(text(query11), {'id': li["vaccine_id"]})
            print(f"{li['vaccine_id']}的SQL 11 执行成功: {result11.rowcount} rows affected.")
            if (li["ifyear"] == 0):
                result01 = db.session.execute(text(query01), {'id': li["vaccine_id"]})
                print(f"{li['vaccine_id']}的SQL 01 执行成功: {result01.rowcount} rows affected.")
                result1 = db.session.execute(text(query1), {'id': li["vaccine_id"]})
                print(f"{li['vaccine_id']}的SQL 1 执行成功: {result1.rowcount} rows affected.")
            result2 = db.session.execute(text(query2), {'id': li["vaccine_id"]})
            print(f"{li['vaccine_id']}的SQL 2 执行成功: {result2.rowcount} rows affected.")
            result12 = db.session.execute(text(query12), {'id': li["vaccine_id"]})
            print(f"{li['vaccine_id']}的SQL 12 执行成功: {result12.rowcount} rows affected.")

        # 构造日常更新
        list.append(list_init)

        # 执行第二个 SQL 语句
        result3 = db.session.execute(text(query3))
        print(f"SQL 3 执行成功: {result3.rowcount} rows affected.")
        result4 = db.session.execute(text(query4))
        print(f"SQL 4 执行成功: {result4.rowcount} rows affected.")
        result5 = db.session.execute(text(query5))
        print(f"SQL 5 执行成功: {result5.rowcount} rows affected.")
        result6 = db.session.execute(text(query6))
        print(f"SQL 6 执行成功: {result6.rowcount} rows affected.")
        # 提交事务，若两个SQL都成功，提交所有更改
        db.session.commit()  # 提交事务

    except Exception as e:
        # 错误处理
        db.session.rollback()
        db.session.flush()
        result = {
            "code": 500,
            "msg": f'更新预警信息失败 {str(e)}'
        }
        return jsonify(result)
    result = {
        "code": 200,
        "msg": '更新预警信息成功'
    }
    return jsonify(result)
