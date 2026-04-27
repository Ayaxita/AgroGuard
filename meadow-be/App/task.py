# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.triggers.cron import CronTrigger
# from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
# from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import text
#
# from App.exts import db
#
#
# # 定时事件
# def update_database(app):
#     print("更新数据库的时间:", datetime.now())
#     with app.app_context():
#         try:
#             # 开始一个事务
#             # 执行第一个 SQL 语句
#             # 插入语句
#             query1 = '''
#                 SELECT threshold INTO @vaccine_threshold
#                     FROM threshold_setting
#                     WHERE vaccine_id = :id;
#
#                     INSERT into w_information_immunizationMessageinfo (basic_id , ele_num,pre_num, sex,variety,mon_age,house,hurdle_name,vaccine_id,birth,imm_date,distance_date,dead_date,state,f_staff,f_date,note)
#
#                     SELECT
#                     d.basic_id AS basic_id,
#                     b.ele_num AS ele_num,
#                     b.pre_num AS pre_num,
#                     b.sex AS sex,
#                     b.variety AS variety,
#                     ROUND((DATEDIFF(NOW(),b.birth)/30),1) AS mon_age,
#
#                     b.house_name AS house_name,
#                     b.hurdle_name AS hurdle_name,
#
#                     d.vaccine_id AS vaccine_id,
#                     b.birth AS birth,
#                     d.max_immdate as imm_date,
#                     DATEDIFF(NOW(),d.max_immdate) as distance_date,
#                     DATE_ADD(d.max_immdate,INTERVAL @vaccine_threshold day ) as dead_date,
#                     1 as state,
#                     'Lonty' as f_staff,
#                     NOW() as f_date,
#                     '' as note
#
#                     FROM
#                     basic_basicinfo as b
#                     LEFT JOIN (select basic_id ,vaccine_id,MAX(imm_date) as max_immdate from d_plantcare_immunizationinfo where vaccine_id= :id GROUP BY basic_id) as d
#                     ON b.id = d.basic_id
#                     LEFT JOIN supply_commodityinfo ON supply_commodityinfo.id = d.vaccine_id
#                     where d.vaccine_id = :id and b.state=1 and b.variety in (0,1)
#                     ORDER BY
#                     b.id ASC
#                 '''
#             query2 = '''
#                     SELECT threshold INTO @vaccine_threshold
#                     FROM threshold_setting
#                     WHERE vaccine_id = :id;
#                     INSERT into w_information_immunizationMessageinfo (basic_id , ele_num,pre_num, sex,variety,mon_age,house,hurdle_name,vaccine_id,birth,imm_date,distance_date,dead_date,state,f_staff,f_date,note)
#                     SELECT
#                     b.id,
#                     b.ele_num AS ele_num,
#                     b.pre_num AS pre_num,
#                     b.sex AS sex,
#                     b.variety AS variety,
#                     ROUND((DATEDIFF(NOW(),b.birth)/30),1) AS mon_age,
#
#                     b.house_name AS house_name,
#                     b.hurdle_name AS hurdle_name,
#
#                     :id AS vaccine_id,
#                     b.birth AS birth,
#                     b.birth as imm_date,
#                     DATEDIFF(NOW(),b.birth) as distance_date,
#                     DATE_ADD(b.birth,INTERVAL @vaccine_threshold day ) as dead_date,
#                     1 as state,
#                     'Lonty' as f_staff,
#                     NOW() as f_date,
#                     '' as note
#                     FROM
#                     basic_basicinfo AS b
#                     WHERE
#                     b.state = 1 AND
#                     b.variety IN (1,0) and
#                     id not in (select basic_id from d_plantcare_immunizationinfo)
#                 '''
#             # 后续更新query3指的是跟新下次信息，query4是日常更新
#             query3 = '''
#                     update w_information_immunizationMessageinfo w
#                     INNER JOIN d_plantcare_immunizationinfo  d
#                     ON w.basic_id = d.basic_id AND w.vaccine_id = d.vaccine_id
#                     inner join threshold_setting t
#                     on t.vaccine_id = w.vaccine_id
#                     set w.imm_date = d.imm_date, w.mon_age = ROUND((DATEDIFF(NOW(),w.birth)/30),1) , w.distance_date = DATEDIFF(NOW(),d.imm_date),
#                     w.dead_date = DATE_ADD(d.imm_date,INTERVAL threshold day ),
#                     w.f_date = NOW()
#                     WHERE w.imm_date < d.imm_date
#                 '''
#             query4 = '''
#                     UPDATE w_information_immunizationMessageinfo AS w
#                     SET
#                         mon_age = ROUND(DATEDIFF(CURRENT_DATE, w.birth) / 30, 1),
#                         distance_date = DATEDIFF(CURRENT_DATE, w.imm_date);
#                 '''
#             # 删除 query是删除不正常的草
#             query5 = '''
#                     DELETE w
#                     FROM
#                     w_information_immunizationMessageinfo AS w
#                     INNER JOIN basic_basicinfo AS b ON w.basic_id = b.id
#                     WHERE
#                     b.state != 1
#                 '''
#             list = [9, 11, 12, 25]
#             # for i in list:
#             # result1 = db.session.execute(query1,{'id':i})
#             # print(f"SQL 1 执行成功: {result1.rowcount} rows affected.")
#             # result2 = db.session.execute(query2,{'id':i})
#             # print(f"SQL 2 执行成功: {result2.rowcount} rows affected.")
#
#             # 执行第二个 SQL 语句
#             result3 = db.session.execute(text(query3))
#             print(f"SQL 3 执行成功: {result3.rowcount} rows affected.")
#             result4 = db.session.execute(text(query4))
#             print(f"SQL 3 执行成功: {result4.rowcount} rows affected.")
#             result5 = db.session.execute(text(query5))
#             print(f"SQL 3 执行成功: {result5.rowcount} rows affected.")
#             # 提交事务，若两个SQL都成功，提交所有更改
#             db.session.commit()  # 提交事务
#         except Exception as e:
#             # 错误处理
#             db.session.rollback()
#             print(f"Error occurred: {e}")
#
#
# # 处理 APScheduler 的任务事件（成功或失败）
# def job_listener(event):
#     if event.exception:
#         print(f"Job failed: {event.job_id}")
#     else:
#         print(f"Job executed successfully: {event.job_id}")
#
#
# def init_scheduler(app):
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(
#         func=update_database(app),
#         trigger=CronTrigger(hour=22, minute=27),  # 每天 21:36 执行
#         id='update_task',
#         name='定时更新数据库任务',
#         replace_existing=True
#     )
#
#
#     scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
#     scheduler.start()
#     print("Scheduler 已启动")
# # if __name__ == '__main__':
# #
# #     # 配 置并启动调度器
# #     scheduler = BackgroundScheduler()
# #     # 添加定时任务：每天凌晨 1 点执行一次
# #     scheduler.add_job(
# #         func=update_database(db),
# #         trigger=CronTrigger(hour=21, minute=56),  # 每天 1 点 0 分执行
# #         id='update_task',
# #         name='定时更新数据库任务',
# #         replace_existing=True
# #     )
# #
# #
# #     scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
# #     print("Scheduler 已启动，等待任务执行...")
# #     try:
# #         scheduler.start()
# #     except (KeyboardInterrupt, SystemExit):
# #         print("Scheduler 停止")
