import json
import datetime
from flask import current_app
from App.exts import db
from App.modelsReverse import (
    BasicBasicinfo,
    DPlantcareDiseaseinfo,
    DPlantcareImmunizationinfo,
    DPlantcareProtectioninfo,
    DPlantcareQuarantineinfo,
    DPlantcareDeathinfo,
    DPlantcareNursinginfo,
    DPlantcareDamageinfo,
    DPlantcareImmunizationBS,
    SupplyCommodityinfo,
    SupplyVSuppliersinfo,
    WinformationImmunizationMessageinfo,
    ThresholdSetMessageinfo,
    HStoreInventory,
    HStoreProtectionIn,
    HStoreProtectionOut,
    FieldDisinfectioninfo,
)

VARIETY_MAP = {0: "小麦", 1: "玉米", 2: "水稻", 3: "大豆", 4: "苜蓿", 5: "黑麦草", 6: "燕麦", 7: "高粱", 8: "谷子", 9: "油菜", 10: "其他"}
PURPOSE_MAP = {0: "粮食作物", 1: "经济作物", 2: "饲草作物", 5: "蔬菜作物", 6: "牧草", 8: "幼苗期"}
GENE_A_MAP = {0: "抗虫型(RR)", 1: "杂合型(Rr)", 2: "感虫型(rr)"}
GENE_B_MAP = {0: "抗病型A", 1: "抗病型B", 2: "感病型"}
GENE_C_MAP = {0: "耐旱型A", 1: "耐旱型B", 2: "普通型"}
RANK_MAP = {0: "重度受灾", 1: "中度受灾", 2: "轻度受灾", 3: "疑似受灾", 9: "未评级"}
SEX_MAP = {0: "雄", 1: "雌", 2: "未知"}
STATE_MAP = {0: "正常", 1: "死亡", 2: "已出售", 3: "淘汰"}
CAUSE_MAP = {0: "病害", 1: "意外", 2: "老化", 3: "其他"}
DETECTION_MAP = {0: "肉眼检测", 1: "实验室检测"}
RESULT1_MAP = {0: "未发现害虫", 1: "发现害虫"}
RESULT2_MAP = {0: "检疫阴性", 1: "检疫阳性"}
RESULT3_MAP = {0: "正常预警", 1: "触发预警"}
SITUATION_MAP = {0: "正常生长", 1: "需要治疗", 2: "观察中", 3: "销毁处理"}
COMMODITY_TYPE_MAP = {0: "疫苗", 1: "药物", 2: "饲料"}
WARNING_STATE_MAP = {0: "正常", 1: "需要施药"}
CUR_EFFECT_MAP = {1: "好转", 2: "治愈", 3: "无效"}


def _serialize(model_obj, field_map=None):
    if model_obj is None:
        return None
    result = {}
    for col in model_obj.__class__.__table__.columns:
        val = getattr(model_obj, col.key, None)
        if isinstance(val, datetime.datetime):
            val = val.isoformat()
        elif isinstance(val, datetime.date):
            val = val.isoformat()
        elif val is not None and hasattr(val, '__float__'):
            try:
                val = float(val)
            except (TypeError, ValueError):
                val = str(val)
        result[col.key] = val
    if field_map:
        for k, v in field_map.items():
            if k in result and v and result[k] in v:
                result[k] = v[result[k]]
    return result


def _paginate(query, page=1, per_page=10):
    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    return total, items


def query_disease(disease_name=None, ele_num=None, start_date=None, end_date=None, page=1, page_size=10):
    query = DPlantcareDiseaseinfo.query.filter(DPlantcareDiseaseinfo.belong == 0)
    if disease_name:
        query = query.filter(DPlantcareDiseaseinfo.disease.like(f"%{disease_name}%"))
    if ele_num:
        basic = BasicBasicinfo.query.filter(BasicBasicinfo.ele_num.like(f"%{ele_num}%")).first()
        if basic:
            query = query.filter(DPlantcareDiseaseinfo.basic_id == basic.id)
        else:
            return {"total": 0, "records": [], "message": f"未找到编号为 {ele_num} 的作物"}
    if start_date:
        query = query.filter(DPlantcareDiseaseinfo.disease_time >= start_date)
    if end_date:
        query = query.filter(DPlantcareDiseaseinfo.disease_time <= end_date)
    query = query.order_by(DPlantcareDiseaseinfo.id.desc())
    total, items = _paginate(query, page, page_size)
    records = []
    for item in items:
        d = _serialize(item, {"cur_effect": CUR_EFFECT_MAP})
        basic = BasicBasicinfo.query.filter_by(id=item.basic_id).first()
        if basic:
            d["ele_num"] = basic.ele_num
            d["pre_num"] = basic.pre_num
            d["variety_text"] = VARIETY_MAP.get(basic.variety, str(basic.variety))
        if item.drug_id:
            drug = SupplyCommodityinfo.query.filter_by(id=item.drug_id).first()
            if drug:
                d["drug_name"] = drug.cname
        records.append(d)
    return {"total": total, "records": records}


def query_drug(drug_name=None, drug_type=None, page=1, page_size=10):
    query = SupplyCommodityinfo.query
    if drug_name:
        query = query.filter(SupplyCommodityinfo.cname.like(f"%{drug_name}%"))
    if drug_type is not None:
        try:
            drug_type_int = int(drug_type)
            query = query.filter(SupplyCommodityinfo.type == drug_type_int)
        except (ValueError, TypeError):
            type_map = {"疫苗": 0, "药物": 1, "饲料": 2}
            t = type_map.get(drug_type)
            if t is not None:
                query = query.filter(SupplyCommodityinfo.type == t)
    query = query.order_by(SupplyCommodityinfo.id.desc())
    total, items = _paginate(query, page, page_size)
    records = [_serialize(item, {"type": COMMODITY_TYPE_MAP}) for item in items]
    return {"total": total, "records": records}


def query_warning(vaccine_id=None, state=None, ele_num=None, page=1, page_size=10):
    query = WinformationImmunizationMessageinfo.query
    if vaccine_id is not None:
        try:
            vid = int(vaccine_id)
            query = query.filter(WinformationImmunizationMessageinfo.vaccine_id == vid)
        except (ValueError, TypeError):
            drug = SupplyCommodityinfo.query.filter(SupplyCommodityinfo.cname.like(f"%{vaccine_id}%")).first()
            if drug:
                query = query.filter(WinformationImmunizationMessageinfo.vaccine_id == drug.id)
    if state is not None:
        try:
            s = int(state)
            query = query.filter(WinformationImmunizationMessageinfo.state == s)
        except (ValueError, TypeError):
            pass
    if ele_num:
        basic = BasicBasicinfo.query.filter(BasicBasicinfo.ele_num.like(f"%{ele_num}%")).first()
        if basic:
            query = query.filter(WinformationImmunizationMessageinfo.basic_id == basic.id)
    query = query.order_by(WinformationImmunizationMessageinfo.id.desc())
    total, items = _paginate(query, page, page_size)
    records = []
    for item in items:
        d = _serialize(item, {"state": WARNING_STATE_MAP, "variety": VARIETY_MAP, "sex": SEX_MAP})
        vaccine = SupplyCommodityinfo.query.filter_by(id=item.vaccine_id).first()
        if vaccine:
            d["vaccine_name"] = vaccine.cname
        records.append(d)
    return {"total": total, "records": records}


def query_immunization(ele_num=None, vaccine_name=None, start_date=None, end_date=None, page=1, page_size=10):
    query = DPlantcareImmunizationBS.query
    if ele_num:
        query = query.filter(DPlantcareImmunizationBS.ele_num.like(f"%{ele_num}%"))
    if vaccine_name:
        query = query.filter(DPlantcareImmunizationBS.cname.like(f"%{vaccine_name}%"))
    if start_date:
        query = query.filter(DPlantcareImmunizationBS.imm_date >= start_date)
    if end_date:
        query = query.filter(DPlantcareImmunizationBS.imm_date <= end_date)
    query = query.order_by(DPlantcareImmunizationBS.id.desc())
    total, items = _paginate(query, page, page_size)
    records = [_serialize(item) for item in items]
    return {"total": total, "records": records}


def query_quarantine(ele_num=None, result1=None, result2=None, situation=None, page=1, page_size=10):
    query = DPlantcareQuarantineinfo.query.filter(DPlantcareQuarantineinfo.belong == 0)
    if ele_num:
        basic = BasicBasicinfo.query.filter(BasicBasicinfo.ele_num.like(f"%{ele_num}%")).first()
        if basic:
            query = query.filter(DPlantcareQuarantineinfo.basic_id == basic.id)
    if result1 is not None:
        try:
            query = query.filter(DPlantcareQuarantineinfo.result1 == int(result1))
        except (ValueError, TypeError):
            r1_map = {"未发现害虫": 0, "发现害虫": 1}
            v = r1_map.get(result1)
            if v is not None:
                query = query.filter(DPlantcareQuarantineinfo.result1 == v)
    if result2 is not None:
        try:
            query = query.filter(DPlantcareQuarantineinfo.result2 == int(result2))
        except (ValueError, TypeError):
            r2_map = {"检疫阴性": 0, "检疫阳性": 1}
            v = r2_map.get(result2)
            if v is not None:
                query = query.filter(DPlantcareQuarantineinfo.result2 == v)
    if situation is not None:
        try:
            query = query.filter(DPlantcareQuarantineinfo.situation == int(situation))
        except (ValueError, TypeError):
            sit_map = {"正常生长": 0, "需要治疗": 1, "观察中": 2, "销毁处理": 3}
            v = sit_map.get(situation)
            if v is not None:
                query = query.filter(DPlantcareQuarantineinfo.situation == v)
    query = query.order_by(DPlantcareQuarantineinfo.id.desc())
    total, items = _paginate(query, page, page_size)
    records = []
    for item in items:
        d = _serialize(item, {
            "detection_mode": DETECTION_MAP,
            "result1": RESULT1_MAP,
            "result2": RESULT2_MAP,
            "result3": RESULT3_MAP,
            "situation": SITUATION_MAP,
        })
        basic = BasicBasicinfo.query.filter_by(id=item.basic_id).first()
        if basic:
            d["ele_num"] = basic.ele_num
            d["variety_text"] = VARIETY_MAP.get(basic.variety, str(basic.variety))
        records.append(d)
    return {"total": total, "records": records}


def query_crop(ele_num=None, variety=None, purpose=None, rank=None, page=1, page_size=10):
    query = BasicBasicinfo.query
    if ele_num:
        query = query.filter(BasicBasicinfo.ele_num.like(f"%{ele_num}%"))
    if variety is not None:
        try:
            query = query.filter(BasicBasicinfo.variety == int(variety))
        except (ValueError, TypeError):
            v = {v: k for k, v in VARIETY_MAP.items()}.get(variety)
            if v is not None:
                query = query.filter(BasicBasicinfo.variety == v)
    if purpose is not None:
        try:
            query = query.filter(BasicBasicinfo.purpose == int(purpose))
        except (ValueError, TypeError):
            p = {v: k for k, v in PURPOSE_MAP.items()}.get(purpose)
            if p is not None:
                query = query.filter(BasicBasicinfo.purpose == p)
    if rank is not None:
        try:
            query = query.filter(BasicBasicinfo.rank == int(rank))
        except (ValueError, TypeError):
            r = {v: k for k, v in RANK_MAP.items()}.get(rank)
            if r is not None:
                query = query.filter(BasicBasicinfo.rank == r)
    query = query.filter(BasicBasicinfo.cunzai == 0) if hasattr(BasicBasicinfo, 'cunzai') else query
    query = query.order_by(BasicBasicinfo.id.desc())
    total, items = _paginate(query, page, page_size)
    records = []
    for item in items:
        d = _serialize(item, {
            "variety": VARIETY_MAP,
            "purpose": PURPOSE_MAP,
            "gene_a": GENE_A_MAP,
            "gene_b": GENE_B_MAP,
            "gene_c": GENE_C_MAP,
            "rank": RANK_MAP,
            "sex": SEX_MAP,
            "state": STATE_MAP,
        })
        records.append(d)
    return {"total": total, "records": records}


def query_statistics():
    disease_count = DPlantcareDiseaseinfo.query.filter(DPlantcareDiseaseinfo.belong == 0).count()
    warning_count = WinformationImmunizationMessageinfo.query.filter(WinformationImmunizationMessageinfo.state == 1).count()
    crop_count = BasicBasicinfo.query.count()
    death_count = DPlantcareDeathinfo.query.filter(DPlantcareDeathinfo.belong == 0).count()
    quarantine_count = DPlantcareQuarantineinfo.query.filter(DPlantcareQuarantineinfo.belong == 0).count()
    drug_count = SupplyCommodityinfo.query.count()
    vaccines = SupplyCommodityinfo.query.filter(SupplyCommodityinfo.type == 0).all()
    vaccine_list = [{"id": v.id, "name": v.cname, "description": v.explain or ""} for v in vaccines]
    disease_records = DPlantcareDiseaseinfo.query.filter(DPlantcareDiseaseinfo.belong == 0).all()
    disease_type_counts = {}
    for r in disease_records:
        name = r.disease
        disease_type_counts[name] = disease_type_counts.get(name, 0) + 1
    threshold_records = ThresholdSetMessageinfo.query.all()
    threshold_list = []
    for t in threshold_records:
        drug = SupplyCommodityinfo.query.filter_by(id=t.vaccine_id).first()
        threshold_list.append({
            "vaccine_id": t.vaccine_id,
            "vaccine_name": drug.cname if drug else "未知",
            "threshold_days": t.threshold,
            "threshold_mon": t.threshold_mon,
            "threshold_year": t.threshold_year
        })
    inventory_records = HStoreInventory.query.all()
    low_stock = []
    for inv in inventory_records:
        if inv.alert and inv.quantity is not None and inv.quantity <= inv.alert:
            low_stock.append({
                "goods": inv.goods or "",
                "quantity": float(inv.quantity) if inv.quantity else 0,
                "alert_level": float(inv.alert) if inv.alert else 0
            })
    return {
        "crop_total": crop_count,
        "disease_total": disease_count,
        "warning_active_count": warning_count,
        "death_total": death_count,
        "quarantine_total": quarantine_count,
        "drug_total": drug_count,
        "disease_type_distribution": disease_type_counts,
        "vaccine_catalog": vaccine_list,
        "warning_thresholds": threshold_list,
        "low_stock_alerts": low_stock
    }


def query_threshold():
    records = ThresholdSetMessageinfo.query.all()
    result = []
    for t in records:
        drug = SupplyCommodityinfo.query.filter_by(id=t.vaccine_id).first()
        result.append({
            "id": t.id,
            "vaccine_id": t.vaccine_id,
            "vaccine_name": drug.cname if drug else "未知",
            "threshold_days": t.threshold,
            "threshold_mon": t.threshold_mon,
            "threshold_year": t.threshold_year,
            "ifyear": t.ifyear,
            "ifchange": t.ifchange
        })
    return {"records": result}


def query_drug_bath(ele_num=None, drug_name=None, page=1, page_size=10):
    query = DPlantcareProtectioninfo.query.filter(DPlantcareProtectioninfo.belong == 0)
    if ele_num:
        basic = BasicBasicinfo.query.filter(BasicBasicinfo.ele_num.like(f"%{ele_num}%")).first()
        if basic:
            query = query.filter(DPlantcareProtectioninfo.basic_id == basic.id)
    if drug_name:
        drug = SupplyCommodityinfo.query.filter(SupplyCommodityinfo.cname.like(f"%{drug_name}%")).first()
        if drug:
            query = query.filter(DPlantcareProtectioninfo.drug_id == drug.id)
    query = query.order_by(DPlantcareProtectioninfo.id.desc())
    total, items = _paginate(query, page, page_size)
    records = []
    for item in items:
        d = _serialize(item)
        drug = SupplyCommodityinfo.query.filter_by(id=item.drug_id).first()
        if drug:
            d["drug_name"] = drug.cname
        basic = BasicBasicinfo.query.filter_by(id=item.basic_id).first()
        if basic:
            d["ele_num"] = basic.ele_num
        records.append(d)
    return {"total": total, "records": records}


def query_death(ele_num=None, cause=None, start_date=None, end_date=None, page=1, page_size=10):
    query = DPlantcareDeathinfo.query.filter(DPlantcareDeathinfo.belong == 0)
    if ele_num:
        basic = BasicBasicinfo.query.filter(BasicBasicinfo.ele_num.like(f"%{ele_num}%")).first()
        if basic:
            query = query.filter(DPlantcareDeathinfo.basic_id == basic.id)
    if cause is not None:
        try:
            query = query.filter(DPlantcareDeathinfo.cause == int(cause))
        except (ValueError, TypeError):
            c = CAUSE_MAP.get(cause)
            if c is not None:
                query = query.filter(DPlantcareDeathinfo.cause == c)
    if start_date:
        query = query.filter(DPlantcareDeathinfo.date >= start_date)
    if end_date:
        query = query.filter(DPlantcareDeathinfo.date <= end_date)
    query = query.order_by(DPlantcareDeathinfo.id.desc())
    total, items = _paginate(query, page, page_size)
    records = []
    for item in items:
        d = _serialize(item, {"cause": CAUSE_MAP})
        basic = BasicBasicinfo.query.filter_by(id=item.basic_id).first()
        if basic:
            d["ele_num"] = basic.ele_num
            d["pre_num"] = basic.pre_num
        records.append(d)
    return {"total": total, "records": records}


TOOL_FUNCTION_MAP = {
    "query_disease": query_disease,
    "query_drug": query_drug,
    "query_warning": query_warning,
    "query_immunization": query_immunization,
    "query_quarantine": query_quarantine,
    "query_crop": query_crop,
    "query_statistics": query_statistics,
    "query_threshold": query_threshold,
    "query_drug_bath": query_drug_bath,
    "query_death": query_death,
}
