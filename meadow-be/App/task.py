from datetime import datetime
from sqlalchemy import text

from App.exts import db


# 定时事件
def update_database(app):
    print("更新数据库的时间:", datetime.now())
    with app.app_context():
        try:
            # 开始一个事务
            db.session.begin()
            # 执行第一个 SQL 语句
            # 插入语句
            query_one = '''
                    select vaccine_id,ifyear,ifchange from threshold_setting
            '''
            # query1指的是每种循环防护的防护剂对于已经在防护表中的信息添加
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
                    COALESCE(s.explain, '') as note

                    FROM
                    basic_basicinfo as b
                    LEFT JOIN (select basic_id ,vaccine_id,MAX(imm_date) as max_immdate from d_plantcare_immunizationinfo where vaccine_id= :id GROUP BY basic_id) as d
                    ON b.id = d.basic_id
                    LEFT JOIN supply_commodityinfo s ON s.id = d.vaccine_id
                    where d.vaccine_id = :id and b.state=1 and b.variety in (0,1)
                    ORDER BY
                    b.id ASC
                '''
            # query2指的是每种循环防护的防护剂对于从没有出现过防护表中的信息添加
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
                    COALESCE(s.explain, '') as note
                    FROM
                    basic_basicinfo AS b
                    LEFT JOIN supply_commodityinfo s ON s.id = :id
                    WHERE
                    b.state = 1 AND
                    b.variety IN (1,0) and
                    b.id not in (select basic_id from d_plantcare_immunizationinfo)
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
            # 后续更新query3指的是更新下次信息，query4是日常更新
            query3 = '''
                    update w_information_immunizationMessageinfo w 
                    INNER JOIN d_plantcare_immunizationinfo  d
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
            # 删除 query是删除不正常的草
            query5 = '''
                    DELETE w
                    FROM
                    w_information_immunizationMessageinfo AS w
                    INNER JOIN basic_basicinfo AS b ON w.basic_id = b.id
                    WHERE
                    b.state != 1
                '''
            # 删除一生只打一次的草
            query6 = '''
                delete w
                FROM
                w_information_immunizationMessageinfo AS w
                INNER JOIN d_plantcare_immunizationinfo AS d ON d.basic_id = w.basic_id and w.vaccine_id = d.vaccine_id
                inner join threshold_setting as t
                on t.vaccine_id = w.vaccine_id
                WHERE
                t.ifyear =1 and d.imm_date is not null
            '''
            result_one = db.session.execute(text(query_one)).all()
            list_init = []
            list_normal = []
            for i in result_one:
                if i[2] == 1:
                    list_init.append({
                        "vaccine_id": i[0],
                        "ifyear": i[1],
                        "ifchange": i[2],
                    })
                else:
                    list_normal.append({
                        "vaccine_id": i[0],
                        "ifyear": i[1],
                        "ifchange": i[2],
                    })
            for li in list_init:
                result11 = db.session.execute(text(query11), {'id': li["vaccine_id"]})
                print(f"{li['vaccine_id']}的SQL 11 执行成功: {result11.rowcount} rows affected.")
                if li["ifyear"] == 0:
                    result01 = db.session.execute(text(query01), {'id': li["vaccine_id"]})
                    print(f"{li['vaccine_id']}的SQL 01 执行成功: {result01.rowcount} rows affected.")
                    result1 = db.session.execute(text(query1), {'id': li["vaccine_id"]})
                    print(f"{li['vaccine_id']}的SQL 1 执行成功: {result1.rowcount} rows affected.")
                result2 = db.session.execute(text(query2), {'id': li["vaccine_id"]})
                print(f"{li['vaccine_id']}的SQL 2 执行成功: {result2.rowcount} rows affected.")
                result12 = db.session.execute(text(query12), {'id': li["vaccine_id"]})
                print(f"{li['vaccine_id']}的SQL 12 执行成功: {result12.rowcount} rows affected.")

            # 构造日常更新
            list_normal.extend(list_init)

            result3 = db.session.execute(text(query3))
            print(f"SQL 3 执行成功: {result3.rowcount} rows affected.")
            result4 = db.session.execute(text(query4))
            print(f"SQL 4 执行成功: {result4.rowcount} rows affected.")
            result5 = db.session.execute(text(query5))
            print(f"SQL 5 执行成功: {result5.rowcount} rows affected.")
            result6 = db.session.execute(text(query6))
            print(f"SQL 6 执行成功: {result6.rowcount} rows affected.")
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            db.session.flush()
            print(f"Error occurred: {e}")


# 处理 APScheduler 的任务事件（成功或失败）
def job_listener(event):
    if event.exception:
        print(f"Job failed: {event.job_id}")
    else:
        print(f"Job executed successfully: {event.job_id}")


def init_scheduler(app):
    try:
        from apscheduler.schedulers.background import BackgroundScheduler
        from apscheduler.triggers.cron import CronTrigger
        from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
        
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            func=lambda: update_database(app),
            trigger=CronTrigger(hour=2, minute=0),
            id='update_task',
            name='定时更新病虫害防护预警任务',
            replace_existing=True
        )
        scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        scheduler.start()
        print("Scheduler 已启动")
    except ImportError as e:
        print(f"[警告] 未安装 apscheduler，定时任务未启动: {e}")
    except Exception as e:
        print(f"[错误] 启动定时任务失败: {e}")
