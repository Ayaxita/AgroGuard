import itertools
from datetime import datetime, date, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from sqlalchemy import text
from App.modelsReverse import *
from decimal import Decimal
from sqlalchemy import func
from sqlalchemy import and_
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import traceback
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc, and_, or_, not_, text, func, asc

# ================== 配置区 ==================
SMTP_SERVER = "smtp.qq.com"        # SMTP服务器地址
SMTP_PORT = 465                    # SSL加密端口
FROM_EMAIL = "1115721320@qq.com"         # 发件邮箱
EMAIL_PASSWORD = "ctququnccketffdd"  # 邮箱授权码
TO_EMAIL = "1923088415@qq.com"  # 收件邮箱
# ============================================

#  {
#     label: "母本(待分类)",
#     value: 0
#   },
#   {
#     label: "育肥",
#     value: 1
#   },
#   {
#     label: "哺乳幼苗",
#     value: 2
#   },
#   {
#     label: "繁殖期公株",
#     value: 5
#   },
#   {
#     label: "繁殖期母株",
#     value: 6
#   },
#   {
#     label: "成熟草",
#     value: 8
#   }
# ];

# 数据库配置
DATABASE_URI = 'mysql+pymysql://root:hscjtCemt2024$@182.92.207.3:3306/sheep_test'

# 创建 SQLAlchemy 引擎
engine = create_engine(DATABASE_URI)

# 创建基础类
# Base = declarative_base()

# 创建会话工厂
SessionLocal = sessionmaker(bind=engine)
# def send_email(job_name, success=True):
#     """发送通知邮件"""
#     subject = f"任务通知 - {job_name} {'完成' if success else '失败'}"
#     content = f"""
#     <h3>任务执行报告</h3>
#     <p>任务名称：{job_name}</p>
#     <p>执行状态：{'✅ 成功完成' if success else '❌ 发生错误'}</p>
#     {'<p>错误信息请查看日志</p>' if not success else ''}
#     """
#
#     message = MIMEText(content, "html", "utf-8")
#     message["Subject"] = Header(subject, "utf-8")
#     message["From"] = FROM_EMAIL
#     message["To"] = TO_EMAIL
#
#     try:
#         with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
#             server.login(FROM_EMAIL, EMAIL_PASSWORD)
#             server.sendmail(FROM_EMAIL, [TO_EMAIL], message.as_string())
#         print(f"{job_name} 邮件发送成功")
#     except Exception as e:
#         print(f"邮件发送失败: {str(e)}")
#     # try:
#     #     with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
#     #         server.login(FROM_EMAIL, EMAIL_PASSWORD)
#     #         # 测试性发送空邮件
#     #         server.sendmail(FROM_EMAIL, [TO_EMAIL], "Test email body")
#     #         print("基础连接测试成功")
#     # except smtplib.SMTPResponseException as e:
#     #     print(f"SMTP协议错误 [{e.smtp_code}]: {e.smtp_error.decode()}")
#     # except smtplib.SMTPAuthenticationError:
#     #     print("认证失败：用户名/授权码错误")
#     # except Exception as e:
#     #     print(f"未知错误: {repr(e)}")
#     #     print(f"错误类型: {type(e).__name__}")
#     #     print(f"错误详情: {str(e)}")
#     #     print(f"堆栈跟踪:\n{traceback.format_exc()}")

# ___________________________定时更新草地库存资产数据，每天生成16条记录到草地库存资产表_____________________________
def calculate_assets():
    """主计算函数：统计草地资产价值并入库"""

    try:
        # 初始化统计字典结构
        # 键是元组（品种，用途，性别），值包含总价值、总重量、数量
        stats = {}
        log_filename = 'missing_weight.log'
        missing_weight_data = []  # 用于存储缺失体重记录

        # -------------------------- 第一部分：处理正常记录（除了purpose=2的） --------------------------
        # 子查询 2：在每个 basic_id 对应的最大日期下，找到 id 最大的记录
        latest_date_subquery = (
            db.session.query(
                BasicBreederconditioninfo.basic_id,
                func.max(BasicBreederconditioninfo.date).label('max_date')
            )
                .group_by(BasicBreederconditioninfo.basic_id)
                .subquery()
        )
        latest_condition_subquery = (
            db.session.query(
                BasicBreederconditioninfo.basic_id,
                func.max(BasicBreederconditioninfo.id).label('max_id')
            )
                .join(
                latest_date_subquery,
                and_(
                    BasicBreederconditioninfo.basic_id == latest_date_subquery.c.basic_id,
                    BasicBreederconditioninfo.date == latest_date_subquery.c.max_date
                )
            )
                .group_by(BasicBreederconditioninfo.basic_id)
                .subquery()
        )

        # 主查询：以BasicBasicinfo为主表，左连接获取最新体重
        normal_query = (
            db.session.query(
                BasicBasicinfo.id.label('basic_id'),
                BasicBasicinfo.ele_num,
                BasicBasicinfo.house_name,
                BasicBasicinfo.hurdle_name,
                BasicBasicinfo.state,  # 添加这行
                BasicBasicinfo.variety,
                BasicBasicinfo.sex,
                BasicBasicinfo.purpose,
                BasicBasicinfo.mon_age,
                BasicBasicinfo.rank,
                func.coalesce(BasicBreederconditioninfo.weight, 0).label('weight'),
                BasicBreederconditioninfo.basic_id.is_(None).label('has_no_weight')
            )
                .outerjoin(
                latest_condition_subquery,
                BasicBasicinfo.id == latest_condition_subquery.c.basic_id
            )
                .outerjoin(
                BasicBreederconditioninfo,
                and_(
                    BasicBreederconditioninfo.id == latest_condition_subquery.c.max_id
                )
            )
                .filter(
                or_(
                    (BasicBasicinfo.state == 1) & (BasicBasicinfo.purpose != 2),
                    (BasicBasicinfo.state == -1)
                )  # 排除purpose=2的记录，由第二部分处理

                # BasicBasicinfo.birth <= today  # 新增的过滤条件
            )
                .distinct()  # 添加去重操作
        )

        page_size = 1000
        with open(log_filename, 'w') as log_file:
            for page in itertools.count(start=0):
                records = normal_query.offset(page * page_size).limit(page_size).all()
                if not records:
                    break

                for record in records:
                    # 记录无体重信息的basic_id
                    if record.has_no_weight:
                        missing_weight_data.append({
                            'basic_id': record.basic_id,
                            '耳号': record.ele_num,  # 添加中文列名
                            '所属草地棚': record.house_name,
                            '所属栏位': record.hurdle_name
                        })
                        log_file.write(f"{record.basic_id, record.ele_num, record.house_name, record.hurdle_name}\n")
                    else:
                        # 更新BasicBasicinfo的weight字段
                        basic_info = db.session.query(BasicBasicinfo).filter(
                            BasicBasicinfo.id == record.basic_id
                        ).first()
                        if basic_info:
                            basic_info.weight = record.weight
                            db.session.commit()  # 提交更新

                    # -------------------------- 用途调整逻辑 --------------------------
                    # 处理state=-1的情况：强制设置purpose=1
                    if record.state == -1:
                        adjusted_purpose = 1
                    else:
                        adjusted_purpose = record.purpose
                        # 原用途为5、6转为母本（0），8育成转为育肥（1）
                        if record.purpose in (5, 6):
                            adjusted_purpose = 0
                        elif record.purpose == 8:
                            adjusted_purpose = 1

                    # -------------------------- 价值计算 --------------------------
                    standard = get_standard_info(
                        variety=record.variety,
                        sex=record.sex,
                        purpose=adjusted_purpose
                    )
                    if not standard:
                        continue

                    # 计算单只价值（根据是否有体重）
                    if record.has_no_weight:
                        value = Decimal(0)  # 无体重记录，价值为0
                        effective_weight = 0  # 不计入重量总和
                    else:
                        value = calculate_value_with_weight(
                            weight=record.weight,
                            standard=standard,
                            rank=record.rank
                        )
                        effective_weight = record.weight

                    # 更新统计信息
                    update_stats(
                        stats_dict=stats,
                        variety=record.variety,
                        purpose=adjusted_purpose,
                        sex=record.sex,
                        value=value,
                        weight=effective_weight  # 无体重记录时传0
                    )

        # -------------------------- 第二部分：处理purpose=2的特殊记录 --------------------------
        # 直接查询基础信息表（这些记录没有饲养条件信息）
        special_query = db.session.query(
            BasicBasicinfo.variety,
            BasicBasicinfo.sex,
            BasicBasicinfo.mon_age,
            BasicBasicinfo.rank
        ).filter(
            BasicBasicinfo.purpose == 2,  # 指定特殊用途
            BasicBasicinfo.state == 1  # 有效记录
        )

        # 分页处理特殊记录
        for page in itertools.count(start=0):
            records = special_query.offset(page * page_size).limit(page_size).all()
            if not records:
                break

            for record in records:
                # -------------------------- 用途调整逻辑 --------------------------
                # 特殊处理：月龄>1时调整为3，否则保持2
                adjusted_purpose = 3 if record.mon_age > 1 else 2

                # -------------------------- 价值计算 --------------------------
                standard = get_standard_info(
                    variety=record.variety,
                    sex=record.sex,
                    purpose=adjusted_purpose
                )
                if not standard:
                    continue

                # 特殊记录价值计算（不乘体重）
                value = calculate_value_without_weight(
                    standard=standard,
                    rank=record.rank
                )

                # 更新统计信息（weight传0）
                update_stats(
                    stats_dict=stats,
                    variety=record.variety,
                    purpose=adjusted_purpose,
                    sex=record.sex,
                    value=value,
                    weight=0  # 特殊记录不计入总重量
                )

        # -------------------------- 数据持久化 --------------------------
        today = datetime.today().date()
        # 构建批量插入数据列表
        bulk_insert = [
            {
                'variety': key[0],  # 品种代码
                'purpose': key[1],  # 调整后的用途
                'sex': key[2],  # 性别
                'sum_value': values['sum_value'],  # 总价值
                'sum_weight': values['sum_weight'],  # 总重量（特殊记录为0）
                'number': values['count'],  # 数量
                'f_date': today,  # 统计日期
                'belong': 0  # 归属标识
            }
            for key, values in stats.items()
        ]

        if bulk_insert:
            # 批量插入数据库
            db.session.bulk_insert_mappings(SheepAssetinfo, bulk_insert)
            db.session.commit()
            print(f"成功插入{len(bulk_insert)}条统计记录")
        print("草地库存资产计算成功")
        # send_email("草地库存资产计算", True)

    except Exception as e:
        # 异常处理：回滚事务并记录错误
        db.session.rollback()
        print(f"处理失败: {str(e)}")
        # send_email("草地库存资产计算", False)
        raise  # 可根据需要决定是否重新抛出异常



def get_standard_info(variety, sex, purpose):
    """获取最新版本的标准信息
    Args:
        variety: 品种代码
        sex: 性别（1/2）
        purpose: 调整后的用途代码

    Returns:
        SheepAssetStandardinfo对象 或 None
    """
    return db.session.query(SheepAssetStandardinfo).filter(
        SheepAssetStandardinfo.variety == variety,
        SheepAssetStandardinfo.sex == sex,
        SheepAssetStandardinfo.purpose == purpose
    ).order_by(
        SheepAssetStandardinfo.f_date.desc()  # 按日期降序获取最新标准
    ).first()


def calculate_value_with_weight(weight, standard, rank):
    """带体重的价值计算
    Formula: 价值 = 体重(kg) * 2 * 单价 * 品级系数
    """
    rank_value = Decimal(getattr(standard, f'rank_{rank}', '1.0'))  # 获取品级系数
    return Decimal(weight) * 2 * Decimal(standard.unit_price) * rank_value


def calculate_value_without_weight(standard, rank):
    """不带体重的价值计算（用于特殊记录）
    Formula: 价值 = 单价 * 品级系数（相当于体重按1kg计算）
    """
    rank_value = Decimal(getattr(standard, f'rank_{rank}', '1.0'))
    return Decimal(standard.unit_price) * rank_value


def update_stats(stats_dict, variety, purpose, sex, value, weight):
    """更新统计字典
    Args:
        stats_dict: 统计字典
        variety: 品种代码
        purpose: 调整后的用途
        sex: 性别
        value: 单只价值
        weight: 单只重量（特殊记录传0）
    """
    key = (variety, purpose, sex)
    if key not in stats_dict:
        # 初始化统计项
        stats_dict[key] = {
            'sum_value': Decimal(0),
            'sum_weight': Decimal(0),
            'count': 0
        }

    # 累加统计值
    stats_dict[key]['sum_value'] += value
    stats_dict[key]['sum_weight'] += Decimal(weight)
    stats_dict[key]['count'] += 1

# def update_daily_sheep_asset():
#     try:
#         # 获取今天的日期
#         today = datetime.now().date()
#
#         # 查询今日所有的SheepAssetinfo记录
#         today_assets = SheepAssetinfo.query.filter(
#             db.func.date(SheepAssetinfo.f_date) == today
#         ).all()
#
#         # 初始化分析记录字段字典
#         analysis_fields = {
#             # 初始化hu系列字段
#             **{f'hu_{p}_{s}': 0 for p in range(4) for s in range(2)},
#             # 初始化xw系列字段
#             **{f'xw_{p}_{s}': 0 for p in range(4) for s in range(2)},
#             'other': 0
#         }
#
#         # 填充数据
#         for asset in today_assets:
#             # 只处理variety为0或1的有效数据
#             if asset.variety not in [0, 1]:
#                 analysis_fields['other'] += asset.sum_value  # 使用累加而非覆盖
#                 continue
#
#             # 确定字段前缀
#             prefix = 'hu' if asset.variety == 0 else 'xw'
#
#             # 只处理purpose在0-3范围内的有效数据
#             if 0 <= asset.purpose <= 3 and asset.sex in [0, 1]:
#                 field_name = f"{prefix}_{asset.purpose}_{asset.sex}"
#                 if field_name in analysis_fields:
#                     analysis_fields[field_name] = asset.sum_value
#
#         # 查询或创建分析记录
#         analysis_record = AnalysisSheepAsset.query.filter_by(
#             f_date=today,
#             belong=0
#         ).first()
#         # 更新或新建记录
#         if analysis_record:
#             # 更新现有记录
#             for field, value in analysis_fields.items():
#                 setattr(analysis_record, field, value)
#             analysis_record.update_time = datetime.now()
#         else:
#             # 创建新记录
#             analysis_record = AnalysisSheepAsset(
#                 f_date=today,
#                 belong=0,
#                 # create_time=datetime.now(),
#                 **analysis_fields
#             )
#             db.session.add(analysis_record)
#
#         db.session.commit()
#         print("更新草地库存资产成功！")
#         # send_email("草地库存资产计算更新", True)
#
#         # # 创建新分析记录
#         # new_analysis = AnalysisSheepAsset(
#         #     f_date=today,
#         #     belong=0,
#         #     **analysis_fields
#         # )
#         #
#         # # 添加到数据库并提交
#         # db.session.add(new_analysis)
#         # db.session.commit()
#
#
#
#     except Exception as e:
#         db.session.rollback()
#         # send_email("草地库存资产计算更新", False)


def update_stocksheet():
    try:
        # 获取当前日期，用于后续插入或更新 Analysisdailystocksheet 表中的记录
        today = date.today()


        # 检查 Analysisdailystocksheet 表中是否已经存在当天日期的记录
        # 如果存在，则将该记录从数据库中删除，以便后续插入最新计算结果
        existing_record = db.session.query(Analysisdailystocksheet).filter_by(date=today).first()
        if existing_record:
            db.session.delete(existing_record)
            db.session.flush()  # 刷新会话，确保删除操作同步到数据库事务中

        # 初始化一个字典 result，用于存储各类物品的数量和价值信息
        # 这些信息将用于后续创建或更新 Analysisdailystocksheet 表中的记录
        result = {
            "garlicskin_num": 0,
            "garlicskin_val": 0,
            "peanutseedling_num": 0,
            "peanutseedling_val": 0,
            "ensilage_num": 0,
            "ensilage_val": 0,
            "otherforage_num": 0,
            "otherforage_val": 0,
            "corn_num": 0,
            "corn_val": 0,
            "premix_num": 0,
            "premix_val": 0,
            "bran_num": 0,
            "bran_val": 0,
            "soybeanmeal_num": 0,
            "soybeanmeal_val": 0,
            "salt_num": 0,
            "salt_val": 0,
            "bakingsoda_num": 0,
            "bakingsoda_val": 0,
            "calciumlactate_num": 0,
            "calciumlactate_val": 0,
            "otherfinefodder_num": 0,
            "otherfinefodder_val": 0,
            "smallvaccine_num": 0,
            "smallvaccine_val": 0,
            "threePfourD_num": 0,
            "threePfourD_val": 0,
            "footAmouthdisease_num": 0,
            "footAmouthdisease_val": 0,
            "duolianbiying_num": 0,
            "duolianbiying_val": 0,
            "othervaccine_num": 0,
            "othervaccine_val": 0,
            "gentamicin_num": 0,
            "gentamicin_val": 0,
            "zhongling_num": 0,
            "zhongling_val": 0,
            "tilmicosin_num": 0,
            "tilmicosin_val": 0,
            "othermedicine_num": 0,
            "othermedicine_val": 0
        }

        # 处理草料相关数据
        # 定义需要分别统计的草料名称列表
        forage_goods = ["蒜皮", "花生秧", "青贮"]
        # 用于存储已统计的草料记录的 id，以便后续筛选出“其他草料”
        forage_ids = []
        for good in forage_goods:
            # 从 HStoreInventory 表中查询 type 为 2（代表草料）且 goods 字段包含当前草料名称的所有记录
            records = db.session.query(HStoreInventory).filter(
                HStoreInventory.type == 2,
                HStoreInventory.goods.like(f"%{good}%")
            ).all()
            # 计算该草料的总数量，即所有相关记录的 quantity 字段之和
            num = sum([record.quantity for record in records])
            # 计算该草料的总价值，即每条记录的 quantity 乘以 stockPrice 后再求和
            val = sum([record.quantity * record.stockPrice for record in records])
            # 将已统计的记录的 id 加入到 forage_ids 列表中
            for record in records:
                forage_ids.append(record.id)
            # 根据当前草料名称，将计算得到的数量和价值存储到 result 字典的对应键中
            if good == "蒜皮":
                result["garlicskin_num"] = num
                result["garlicskin_val"] = val
            elif good == "花生秧":
                result["peanutseedling_num"] = num
                result["peanutseedling_val"] = val
            elif good == "青贮":
                result["ensilage_num"] = num
                result["ensilage_val"] = val

        # 从 HStoreInventory 表中筛选出 type 为 2 且 id 不在 forage_ids 列表中的记录，即“其他草料”
        other_forage_records = db.session.query(HStoreInventory).filter(
            HStoreInventory.type == 2,
            ~HStoreInventory.id.in_(forage_ids)
        ).all()
        # 计算“其他草料”的总数量
        result["otherforage_num"] = sum([record.quantity for record in other_forage_records])
        # 计算“其他草料”的总价值
        result["otherforage_val"] = sum([record.quantity * record.stockPrice for record in other_forage_records])

        # 处理精料相关数据
        # 定义需要分别统计的精料名称列表
        finefodder_goods = ["玉米", "预混料", "麸皮", "豆粕", "盐", "小苏打", "乳酸钙"]
        # 用于存储已统计的精料记录的 id，以便后续筛选出“其他精料”
        finefodder_ids = []
        for good in finefodder_goods:
            # 从 HStoreInventory 表中查询 type 为 3（代表精料）且 goods 字段包含当前精料名称的所有记录
            records = db.session.query(HStoreInventory).filter(
                HStoreInventory.type == 3,
                HStoreInventory.goods.like(f"%{good}%")
            ).all()
            # 计算该精料的总数量
            num = sum([record.quantity for record in records])
            # 计算该精料的总价值
            val = sum([record.quantity * record.stockPrice for record in records])
            # 将已统计的记录的 id 加入到 finefodder_ids 列表中
            for record in records:
                finefodder_ids.append(record.id)
            # 根据当前精料名称，将计算得到的数量和价值存储到 result 字典的对应键中
            if good == "玉米":
                result["corn_num"] = num
                result["corn_val"] = val
            elif good == "预混料":
                result["premix_num"] = num
                result["premix_val"] = val
            elif good == "麸皮":
                result["bran_num"] = num
                result["bran_val"] = val
            elif good == "豆粕":
                result["soybeanmeal_num"] = num
                result["soybeanmeal_val"] = val
            elif good == "盐":
                result["salt_num"] = num
                result["salt_val"] = val
            elif good == "小苏打":
                result["bakingsoda_num"] = num
                result["bakingsoda_val"] = val
            elif good == "乳酸钙":
                result["calciumlactate_num"] = num
                result["calciumlactate_val"] = val

        # 从 HStoreInventory 表中筛选出 type 为 3 且 id 不在 finefodder_ids 列表中的记录，即“其他精料”
        other_finefodder_records = db.session.query(HStoreInventory).filter(
            HStoreInventory.type == 3,
            ~HStoreInventory.id.in_(finefodder_ids)
        ).all()
        # 计算“其他精料”的总数量
        result["otherfinefodder_num"] = sum([record.quantity for record in other_finefodder_records])
        # 计算“其他精料”的总价值
        result["otherfinefodder_val"] = sum(
            [record.quantity * record.stockPrice for record in other_finefodder_records])

        # 处理疫苗相关数据
        # 定义需要分别统计的疫苗名称列表
        vaccine_goods = ["小反刍山羊痘二联苗", "三联四防", "口蹄疫", "多联必应"]
        # 用于存储已统计的疫苗记录的 id，以便后续筛选出“其他疫苗”
        vaccine_ids = []
        for good in vaccine_goods:
            # 从 HStoreInventory 表中查询 type 为 0（代表疫苗）且 goods 字段包含当前疫苗名称的所有记录
            records = db.session.query(HStoreInventory).filter(
                HStoreInventory.type == 0,
                HStoreInventory.goods.like(f"%{good}%")
            ).all()
            # 计算该疫苗的总数量
            num = sum([record.quantity for record in records])
            # 计算该疫苗的总价值
            val = sum([record.quantity * record.stockPrice for record in records])
            # 将已统计的记录的 id 加入到 vaccine_ids 列表中
            for record in records:
                vaccine_ids.append(record.id)
            # 根据当前疫苗名称，将计算得到的数量和价值存储到 result 字典的对应键中
            if good == "小反刍山羊痘二联苗":
                result["smallvaccine_num"] = num
                result["smallvaccine_val"] = val
            elif good == "三联四防":
                result["threePfourD_num"] = num
                result["threePfourD_val"] = val
            elif good == "口蹄疫":
                result["footAmouthdisease_num"] = num
                result["footAmouthdisease_val"] = val
            elif good == "多联必应":
                result["duolianbiying_num"] = num
                result["duolianbiying_val"] = val

        # 从 HStoreInventory 表中筛选出 type 为 0 且 id 不在 vaccine_ids 列表中的记录，即“其他疫苗”
        other_vaccine_records = db.session.query(HStoreInventory).filter(
            HStoreInventory.type == 0,
            ~HStoreInventory.id.in_(vaccine_ids)
        ).all()
        # 计算“其他疫苗”的总数量
        result["othervaccine_num"] = sum([record.quantity for record in other_vaccine_records])
        # 计算“其他疫苗”的总价值
        result["othervaccine_val"] = sum([record.quantity * record.stockPrice for record in other_vaccine_records])

        # 处理药品相关数据
        # 定义需要分别统计的药品名称列表
        medicine_goods = ["庆大霉素", "中灵", "替米考星"]
        # 用于存储已统计的药品记录的 id，以便后续筛选出“其他药品”
        medicine_ids = []
        for good in medicine_goods:
            # 从 HStoreInventory 表中查询 type 为 1（代表药品）且 goods 字段包含当前药品名称的所有记录
            records = db.session.query(HStoreInventory).filter(
                HStoreInventory.type == 1,
                HStoreInventory.goods.like(f"%{good}%")
            ).all()
            # 计算该药品的总数量
            num = sum([record.quantity for record in records])
            # 计算该药品的总价值
            val = sum([record.quantity * record.stockPrice for record in records])
            # 将已统计的记录的 id 加入到 medicine_ids 列表中
            for record in records:
                medicine_ids.append(record.id)
            # 根据当前药品名称，将计算得到的数量和价值存储到 result 字典的对应键中
            if good == "庆大霉素":
                result["gentamicin_num"] = num
                result["gentamicin_val"] = val
            elif good == "中灵":
                result["zhongling_num"] = num
                result["zhongling_val"] = val
            elif good == "替米考星":
                result["tilmicosin_num"] = num
                result["tilmicosin_val"] = val

        # 从 HStoreInventory 表中筛选出 type 为 1 且 id 不在 medicine_ids 列表中的记录，即“其他药品”
        other_medicine_records = db.session.query(HStoreInventory).filter(
            HStoreInventory.type == 1,
            ~HStoreInventory.id.in_(medicine_ids)
        ).all()
        # 计算“其他药品”的总数量
        result["othermedicine_num"] = sum([record.quantity for record in other_medicine_records])
        # 计算“其他药品”的总价值
        result["othermedicine_val"] = sum([record.quantity * record.stockPrice for record in other_medicine_records])

        # 将当天日期添加到 result 字典中，用于后续插入到 Analysisdailystocksheet 表中
        result["date"] = today
        # 使用 result 字典创建一个新的 Analysisdailystocksheet 记录对象
        new_record = Analysisdailystocksheet(**result)
        # 将新记录添加到数据库会话中
        db.session.add(new_record)
        db.session.flush()  # 刷新会话，确保插入操作同步到数据库事务中

        # 提交数据库会话，将新记录保存到数据库中
        db.session.commit()
        print("库存资产计算成功")
        # send_email("物料库存资产计算", True)
    except Exception as e:
        print(f"处理失败: {str(e)}")
        # 错误处理
        db.session.rollback()
        # send_email("物料库存资产计算", False)
    finally:
        # 确保关闭数据库连接
        db.session.close()

def daily_sheetinit():
    # 获取第二天的日期
    next_day = (datetime.now() + timedelta(days=1)).date()
    # 创建 Analysisdailysheet 对象并初始化
    new_entry = Analysisdailysheet(
        date=next_day,
        buysheep_fees=0,
        caoliao_fees=0,
        jingliao_fees=0,
        yimiao_fees=0,
        yaopin_fees=0,
        food_fees=0,
        drug_fees=0,
        test_fees=0,
        labor_fees=0,
        waterEle_fees=0,
        land_fees=0,
        maintenance_fees=0,
        cheep_fees=0,
        manage_fees=0,
        research_fees=0,
        other_fees=0,
        other_text='',
        day_compute=0,
        directtotal_fees=0,
        indirecttotal_fees=0,
        total_fees=0,
        f_date=next_day,
        f_staff='',
        belong=0
    )

    # 将对象添加到会话中
    db.session.add(new_entry)

    try:
        # 提交会话到数据库
        db.session.commit()
        print("日支出报表初始化完成。")
        # send_email("日支出报表",True)
    except Exception as e:
        # 发生错误时回滚会话
        db.session.rollback()
        print(f"插入数据时发生错误: {e}")
        # send_email("日支出报表", False)

def update_daily_income():  # 按照总价去分，再根据类型去分
    try:
        today = datetime.now().strftime('%Y-%m-%d')

        analysis_data = {
            'f_date': today,
            'belong': 0,
            'number_0': 0, 'value_0': 0.0,
            'number_1': 0, 'value_1': 0.0,
            'number_2': 0, 'value_2': 0.0,
            'number_3': 0, 'value_3': 0.0,
            'number_9': 0, 'value_9': 0.0,
            'dung_value': 0.0,
            'wool_value': 0.0,
            'skin_value': 0.0,
            'manure_value': 0.0,
            'feed_value': 0.0,
            'producted_value': 0.0,
            'other_value': 0.0
        }

        # 处理GSlaughterSSalesinfo数据（草地销售）
        ssales_records = db.session.query(
            GSlaughterSSalesinfo.type,
            GSlaughterSSalesinfo.total_price
        ).filter(
            GSlaughterSSalesinfo.sales_date == today
        ).all()

        # 按total_price分组
        from collections import defaultdict
        price_groups = defaultdict(list)
        for record in ssales_records:
            price_groups[record.total_price].append(record.type)
        print('-----------------------------')
        print(f'price_groups{price_groups}')
        # 处理每个价格组
        for total_price, types in price_groups.items():
            # 统计类型数量
            type_counts = defaultdict(int)
            for type_ in types:
                type_counts[type_] += 1

            total_records = len(types)
            if total_records == 0:
                continue
            # 将 Decimal 转换为浮点数
            total_price_float = float(total_price)  # 关键转换
            # 计算每个类型的占比并分配金额
            for type_, count in type_counts.items():
                ratio = count / total_records
                allocated_value = total_price_float * ratio

                # 确定字段后缀
                if type_ in {0, 1, 2, 3}:
                    field_suffix = str(type_)
                else:
                    field_suffix = '9'

                # 累加统计结果
                analysis_data[f'number_{field_suffix}'] += count
                analysis_data[f'value_{field_suffix}'] += allocated_value

        # 处理GSlaughterGSalesinfo数据（其他产品销售）
        gsales_totals = db.session.query(
            GSlaughterGSalesinfo.type,
            func.sum(GSlaughterGSalesinfo.total_price).label('total')
        ).filter(
            GSlaughterGSalesinfo.sales_date == today
        ).group_by(GSlaughterGSalesinfo.type).all()

        type_mapping = {
            0: 'dung_value',
            1: 'wool_value',
            2: 'skin_value',
            3: 'manure_value',
            4: 'feed_value',
            5: 'producted_value'
        }

        for type_, total in gsales_totals:
            field = type_mapping.get(type_, 'other_value')
            analysis_data[field] = total or 0.0

        # 创建或更新记录
        existing_record = AnalysisDailyIncome.query.filter_by(f_date=today).first()

        if existing_record:
            for key, value in analysis_data.items():
                setattr(existing_record, key, value)
        else:
            new_record = AnalysisDailyIncome(**analysis_data)
            db.session.add(new_record)

        db.session.commit()
        print("更新日收入报表成功")
        # send_email("日销售报表", True)

    except Exception as e:
        db.session.rollback()
        # send_email("日支出报表", False)


def update_daily_sheep_asset(session):
    try:
        print("开始更新草地库存资产")
        # 获取今天的日期
        today = datetime.now().date()
        print(f"获取到今天的日期: {today}")

        # 查询今日所有的SheepAssetinfo记录
        # today_assets = SheepAssetinfo.query.filter(
        #     db.func.date(SheepAssetinfo.f_date) == today
        # ).all()
        # 使用传入的会话进行查询
        today_assets = session.query(SheepAssetinfo).filter(
            func.date(SheepAssetinfo.f_date) == today
        ).all()
        print(f"查询到今日的SheepAssetinfo记录数量: {len(today_assets)}")

        # 初始化分析记录字段字典
        analysis_fields = {
            # 初始化hu系列字段
            **{f'hu_{p}_{s}': 0 for p in range(4) for s in range(2)},
            # 初始化xw系列字段
            **{f'xw_{p}_{s}': 0 for p in range(4) for s in range(2)},
            'other': 0
        }

        # 填充数据
        for asset in today_assets:
            # 只处理variety为0或1的有效数据
            if asset.variety not in [0, 1]:
                analysis_fields['other'] += asset.sum_value  # 使用累加而非覆盖
                continue

            # 确定字段前缀
            prefix = 'hu' if asset.variety == 0 else 'xw'

            # 只处理purpose在0-3范围内的有效数据
            if 0 <= asset.purpose <= 3 and asset.sex in [0, 1]:
                field_name = f"{prefix}_{asset.purpose}_{asset.sex}"
                if field_name in analysis_fields:
                    analysis_fields[field_name] = asset.sum_value

        # 查询或创建分析记录
        # analysis_record = AnalysisSheepAsset.query.filter_by(
        #     f_date=today,
        #     belong=0
        # ).first()
        analysis_record = session.query(AnalysisSheepAsset).filter_by(
            f_date=today,
            belong=0
        ).first()
        print(f"查询到的分析记录: {analysis_record}")

        # 更新或新建记录
        if analysis_record:
            # 更新现有记录
            for field, value in analysis_fields.items():
                setattr(analysis_record, field, value)
            analysis_record.update_time = datetime.now()
        else:
            # 创建新记录
            analysis_record = AnalysisSheepAsset(
                f_date=today,
                belong=0,
                # create_time=datetime.now(),
                **analysis_fields
            )
            db.session.add(analysis_record)

        db.session.commit()
        print("更新草地库存资产成功！")
        # send_email("草地库存资产计算更新", True)

    except Exception as e:
        db.session.rollback()
        print(f"更新草地库存资产失败: {e}")
        import traceback
        traceback.print_exc()
        # send_email("草地库存资产计算更新", False)
# ____________________________________________________________________________________________
def Task():
    db.session = SessionLocal()
    print("开始执行任务，已获取数据库会话")
    # daily_sheetinit() #初始化日支出报表
    # update_daily_income() # 初始化收入报表
    # calculate_assets() #计算草地库存资产 16 条
    update_daily_sheep_asset(db.session) # 更新草地库存资产
    print("任务执行完成")
    # update_stocksheet() #计算物料库存资产


# 定时任务
def init_scheduler():
    # 初始化定时任务调度器
    scheduler = BackgroundScheduler()
    # 设置每日凌晨0:30执行资产计算任务
    scheduler.add_job(
        func=Task,
        trigger=CronTrigger(hour=11, minute=2),  # 定时触发时间
        id='asset_calculation',  # 任务ID
        name='每日资产计算任务',  # 任务名称
        max_instances=1  # 最大实例数
    )
    scheduler.start()  # 启动调度器
    print("定时任务调度器已启动")


if __name__ == '__main__':
    init_scheduler()  # 启动定时任务调度器
    try:
        while True:
            pass  # 保持主线程运行，等待定时任务执行
    except (KeyboardInterrupt, SystemExit):
        print("定时任务已停止")  # 捕获终止信号，停止定时任务
