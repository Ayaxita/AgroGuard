TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "query_disease",
            "description": "查询病害记录。可根据病害名称、作物电子编号、发病日期范围来筛选查询。返回病害类型、治疗药物、治愈效果等信息。",
            "parameters": {
                "type": "object",
                "properties": {
                    "disease_name": {"type": "string", "description": "病害名称（模糊匹配），如：口蹄疫、肺炎等"},
                    "ele_num": {"type": "string", "description": "作物的电子编号（模糊匹配）"},
                    "start_date": {"type": "string", "description": "发病日期起始（格式：YYYY-MM-DD）"},
                    "end_date": {"type": "string", "description": "发病日期截止（格式：YYYY-MM-DD）"},
                    "page": {"type": "integer", "description": "页码，默认1"},
                    "page_size": {"type": "integer", "description": "每页数量，默认10"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "query_drug",
            "description": "查询药物/疫苗/饲料目录。可根据名称或类型筛选。type: 0=疫苗, 1=药物, 2=饲料。也支持中文名称筛选如'疫苗'、'药物'、'饲料'。",
            "parameters": {
                "type": "object",
                "properties": {
                    "drug_name": {"type": "string", "description": "药物/疫苗名称（模糊匹配）"},
                    "drug_type": {"type": "string", "description": "类型：0=疫苗, 1=药物, 2=饲料，也支持中文'疫苗'、'药物'、'饲料'"},
                    "page": {"type": "integer", "description": "页码，默认1"},
                    "page_size": {"type": "integer", "description": "每页数量，默认10"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "query_warning",
            "description": "查询施药预警信息。查看哪些作物需要施药、预警状态(state: 0=正常, 1=需要施药)、距上次施药天数等。可按疫苗名称、状态、作物编号筛选。",
            "parameters": {
                "type": "object",
                "properties": {
                    "vaccine_id": {"type": "string", "description": "疫苗ID或疫苗名称（模糊匹配）"},
                    "state": {"type": "string", "description": "预警状态：0=正常, 1=需要施药"},
                    "ele_num": {"type": "string", "description": "作物电子编号（模糊匹配）"},
                    "page": {"type": "integer", "description": "页码，默认1"},
                    "page_size": {"type": "integer", "description": "每页数量，默认10"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "query_immunization",
            "description": "查询施药防治记录。可根据作物编号、疫苗名称、施药日期范围来查询历史施药记录，含施药时间、剂量、抗体水平等信息。",
            "parameters": {
                "type": "object",
                "properties": {
                    "ele_num": {"type": "string", "description": "作物电子编号（模糊匹配）"},
                    "vaccine_name": {"type": "string", "description": "疫苗/药物名称（模糊匹配）"},
                    "start_date": {"type": "string", "description": "施药日期起始（格式：YYYY-MM-DD）"},
                    "end_date": {"type": "string", "description": "施药日期截止（格式：YYYY-MM-DD）"},
                    "page": {"type": "integer", "description": "页码，默认1"},
                    "page_size": {"type": "integer", "description": "每页数量，默认10"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "query_quarantine",
            "description": "查询检疫记录。可根据害虫检测结果(result1: 0=未发现害虫,1=发现害虫)、疫病检测(result2: 0=阴性,1=阳性)、处理状态(situation: 0=正常生长,1=需要治疗,2=观察中,3=销毁处理)来筛选。",
            "parameters": {
                "type": "object",
                "properties": {
                    "ele_num": {"type": "string", "description": "作物电子编号（模糊匹配）"},
                    "result1": {"type": "string", "description": "害虫检测结果：0=未发现害虫, 1=发现害虫，也支持中文"},
                    "result2": {"type": "string", "description": "疫病检测结果：0=检疫阴性, 1=检疫阳性，也支持中文"},
                    "situation": {"type": "string", "description": "处理状态：0=正常生长,1=需要治疗,2=观察中,3=销毁处理，也支持中文"},
                    "page": {"type": "integer", "description": "页码，默认1"},
                    "page_size": {"type": "integer", "description": "每页数量，默认10"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "query_crop",
            "description": "查询作物基本信息。可根据电子编号、品种(variety: 0=小麦,1=玉米,2=水稻,3=大豆,4=苜蓿,5=黑麦草,6=燕麦,7=高粱,8=谷子,9=油菜,10=其他)、用途、受灾等级(rank: 0=重度受灾,1=中度受灾,2=轻度受灾,3=疑似受灾,9=未评级)来筛选。",
            "parameters": {
                "type": "object",
                "properties": {
                    "ele_num": {"type": "string", "description": "作物电子编号（模糊匹配）"},
                    "variety": {"type": "string", "description": "品种编号或中文名称，如：0/小麦,1/玉米,2/水稻等"},
                    "purpose": {"type": "string", "description": "用途编号或中文名称，如：0/粮食作物,1/经济作物等"},
                    "rank": {"type": "string", "description": "受灾等级编号或中文名称，如：0/重度受灾,1/中度受灾等"},
                    "page": {"type": "integer", "description": "页码，默认1"},
                    "page_size": {"type": "integer", "description": "每页数量，默认10"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "query_statistics",
            "description": "获取系统统计概览。返回作物总数、病害总数、活跃预警数、绝收/死亡数、检疫数、药物总数、病害类型分布、疫苗目录、预警阈值配置、库存告警等信息。无需参数。",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "query_threshold",
            "description": "查询施药预警阈值配置。返回每种疫苗的预警天数阈值（threshold：天数阈值）、月阈值、年阈值等信息。",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "query_drug_bath",
            "description": "查询药浴免疫记录。药浴是草地作物病虫害防治中的一种重要施药方式。可根据作物编号、药物名称筛选。",
            "parameters": {
                "type": "object",
                "properties": {
                    "ele_num": {"type": "string", "description": "作物电子编号（模糊匹配）"},
                    "drug_name": {"type": "string", "description": "药物名称（模糊匹配）"},
                    "page": {"type": "integer", "description": "页码，默认1"},
                    "page_size": {"type": "integer", "description": "每页数量，默认10"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "query_death",
            "description": "查询绝收/死亡记录。可根据作物编号、原因(cause: 0=病害,1=意外,2=老化,3=其他)、日期范围筛选。",
            "parameters": {
                "type": "object",
                "properties": {
                    "ele_num": {"type": "string", "description": "作物电子编号（模糊匹配）"},
                    "cause": {"type": "string", "description": "原因：0=病害,1=意外,2=老化,3=其他，也支持中文"},
                    "start_date": {"type": "string", "description": "日期起始（格式：YYYY-MM-DD）"},
                    "end_date": {"type": "string", "description": "日期截止（格式：YYYY-MM-DD）"},
                    "page": {"type": "integer", "description": "页码，默认1"},
                    "page_size": {"type": "integer", "description": "每页数量，默认10"}
                },
                "required": []
            }
        }
    }
]

SYSTEM_PROMPT = """你是AgroGuard草地作物病虫害智能监测系统的AI助手。你的职责是帮助用户查询和分析系统中的病虫害、药物、预警、检疫等数据。

## 你可以使用的查询工具：
1. **query_disease** - 查询病害记录（按病害名、作物编号、日期范围）
2. **query_drug** - 查询药物/疫苗/饲料目录
3. **query_warning** - 查询施药预警（哪些作物需要施药）
4. **query_immunization** - 查询施药防治记录
5. **query_quarantine** - 查询检疫记录
6. **query_crop** - 查询作物基本信息
7. **query_statistics** - 获取系统统计概览
8. **query_threshold** - 查询预警阈值配置
9. **query_drug_bath** - 查询药浴免疫记录
10. **query_death** - 查询绝收/死亡记录

## 编码说明：
- 品种(variety): 0=小麦,1=玉米,2=水稻,3=大豆,4=苜蓿,5=黑麦草,6=燕麦,7=高粱,8=谷子,9=油菜,10=其他
- 用途(purpose): 0=粮食作物,1=经济作物,2=饲草作物,5=蔬菜作物,6=牧草,8=幼苗期
- 受灾等级(rank): 0=重度受灾,1=中度受灾,2=轻度受灾,3=疑似受灾,9=未评级
- 药物类型(type): 0=疫苗,1=药物,2=饲料
- 预警状态(state): 0=正常,1=需要施药
- 绝收原因(cause): 0=病害,1=意外,2=老化,3=其他

## 回答规则：
1. 当用户提问涉及系统中的数据时，你应该调用相应的查询工具获取实时数据
2. 对于统计数据、趋势分析等问题，优先使用query_statistics
3. 回答时将编码转换为可读的中文（如品种0应表述为"小麦"）
4. 如果查询结果为空，如实告知用户
5. 只做数据查询和解读，绝不修改数据库中的任何数据
6. 对于普通闲聊问题，不需要调用工具，直接回答即可"""
