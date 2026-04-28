# AgroGuard 项目开发维护文档 (AGENTS.md)

> **⚠️ 必读提示**：此文档是本项目的技术圣经。任何接手此项目的AI或开发者，在执行任何修改前必须先完整阅读本文档。文档包含项目架构、模块映射、已知问题、修复记录和数据迁移规则。

---

## 1. 项目总览

**项目名称**：草地作物病虫害智能监测系统 (AgroGuard / Meadow Guard)
**技术栈**：
- 后端：Python 3.9 + Flask + SQLAlchemy + Flask-JWT-Extended + PyMySQL
- 前端：Vue 3 + TypeScript + Vite + Element Plus + Pinia
- 数据库：MySQL 5.7
- 部署：Docker Compose (3 services: mysql-db, flask, vue)

**项目目录结构**：
```
/home/debian/AgroGuard/
├── docker-compose.yml          # Docker编排文件
├── init-scripts/
│   └── meadow_test.sql         # 数据库初始化SQL（首次启动时挂载到MySQL容器）
├── meadow-be/                  # 后端Flask项目
│   ├── app.py                  # Flask应用入口
│   ├── Dockerfile
│   ├── requirements.txt
│   └── App/
│       ├── __init__.py         # 蓝图注册中心
│       ├── exts.py             # 插件初始化 (SQLAlchemy, Migrate, CORS)
│       ├── modelsReverse.py    # SQLAlchemy模型定义（全部78个模型）
│       ├── task.py             # 定时任务
│       ├── login_auth/views.py # 登录认证蓝图
│       ├── basic/views.py      # 基础信息管理蓝图
│       ├── field/views.py      # 场地管理蓝图（原colony）
│       ├── pest_control/views.py # 病虫害防治蓝图（原d_health/d_plantcare）
│       ├── propagation/views.py  # 种植培育蓝图（原e_cultivation）
│       ├── g_harvest/views.py    # 收获加工蓝图
│       ├── h_store/views.py      # 仓储管理蓝图
│       ├── supply/views.py       # 供应商管理蓝图
│       ├── analysis/views.py     # 统计分析蓝图
│       ├── statistic/view.py     # 统计报表蓝图
│       ├── w_information/views.py # 预警信息蓝图
│       └── chatbox/views.py      # AI聊天蓝图
└── meadow-fe/                  # 前端Vue3项目
    ├── Dockerfile
    ├── nginx.conf
    ├── vite.config.ts
    └── src/
        ├── api/                # 全局API配置
        ├── views/              # 页面视图（按模块分目录）
        ├── routers/            # 路由配置
        └── stores/             # Pinia状态管理
```

**Docker服务映射**：
| 服务 | 容器名 | 外部端口 | 内部端口 | 说明 |
|------|--------|---------|---------|------|
| MySQL | meadow-guard-mysql-db-1 | 5010 | 3306 | root/meadow123 |
| Flask | meadow-guard-flask-1 | 5000 | 5000 | 4 worker Gunicorn |
| Vue | meadow-guard-vue-1 | 5020 | 80 | Nginx反向代理 |

**数据库连接URI**：`mysql+pymysql://root:meadow123@mysql-db:3306/meadow_test`

---

## 2. 后端模块详细映射

### 2.1 蓝图注册关系 (`App/__init__.py`)

| # | 蓝图变量 | 导入路径 | URL前缀 | 说明 |
|---|---------|---------|---------|------|
| 1 | `login_auth` | `App.login_auth.views` | `/login`, `/logout` | 登录认证 |
| 2 | `basic` | `App.basic.views` | `/basic/...` | 基础信息（草株、体况、收获、生产商） |
| 3 | `field` | `App.field.views` | `/field/...` | 场地管理（棚舍、围栏、消毒、维护、转场） |
| 4 | `supply` | `App.supply.views` | `/supply/...` | 供应商管理 |
| 5 | `h_store` | `App.h_store.views` | `/h_store/...` | 仓储管理（库存、疫苗出入库、饲料出入库） |
| 6 | `g_harvest` | `App.g_harvest.views` | `/g_harvest/...` | 收获加工（销售、胴体、经济分析） |
| 7 | `pest_control` | `App.pest_control.views` | `/pest_control/...` | 病虫害防治（死亡、免疫、防治、检疫、护理、病害、虫害） |
| 8 | `propagation` | `.propagation.views` | `/propagation/...` | 种植培育（发情、配种、产仔、断奶、人工照料、鉴定、采精、 seedlings） |
| 9 | `w_information` | `.w_information.views` | `/w_information/...` | 预警信息（免疫提醒、阈值设置） |
| 10 | `Statistic` | `.statistic.view` | `/statistic/...` | 统计报表（系谱、评分、淘汰草） |
| 11 | `analysis` | `.analysis.views` | `/analysis/...` | 统计分析（日报、库存、资产、可视化） |
| 12 | `chatbox` | `.chatbox.views` | `/chatbox/...` | AI聊天助手 |

> ⚠️ **注意**：`Statistic` 蓝图变量名首字母大写，这是历史遗留，不要修改。

### 2.2 关键模型 ↔ 数据库表映射 (`modelsReverse.py`)

**基础信息模块**：
| 模型类 | 表名 | 说明 |
|--------|------|------|
| `BasicBasicinfo` | `basic_basicinfo` | 草株基本信息（核心表，1万+条数据） |
| `BasicFieldconditioninfo` | `basic_fieldconditioninfo` | 草株体况测定（原breederconditioninfo） |
| `BasicHarvestinfo` | `basic_harvestinfo` | 收获信息（原cutinfo） |
| `BasicManuinfo` | `basic_manuinfo` | 生产商信息 |
| `BasicMakescore` | `basic_makescore` | 评分标准 |
| `BasicObsoleteGrassinfo` | `basic_obsoletegrassinfo` | 淘汰草记录 |
| `BasicGroupmalecapacity` | `basic_groupmalecapacity` | 群种公草能力（原groupramcapacity） |
| `BasicYieldCapacity` | `basic_yield_capacity` | 产草能力 |
| `BasicPollenCapacity` | `basic_pollen_capacity` | 授粉能力 |
| `BasicFertilizerinfo` | `basic_fertilizerinfo` | 施肥信息（原manureinfo） |
| `BasicYieldperformance` | `basic_yieldperformance` | 产草性能 |
| `BasicProductivityinfo` | `basic_productivityinfo` | 生产力 |
| `BasicCanopyperformance` | `basic_canopyperformance` | 冠层性能 |
| `BasicSportsinfo` | `basic_sportsinfo` | 运动性能 |

**场地管理模块**（原colony_* → field_*）：
| 模型类 | 表名 | 旧表名 |
|--------|------|--------|
| `FieldHouseinfo` | `field_houseinfo` | `colony_houseinfo` |
| `FieldDisinfectioninfo` | `field_disinfectioninfo` | `colony_disinfectioninfo` |
| `FieldMaintenanceinfo` | `field_maintenanceinfo` | `colony_maintenanceinfo` |
| `FieldTransferinfo` | `field_transferinfo` | `colony_transferinfo` |

**病虫害防治模块**（原d_health_* → d_plantcare_*）：
| 模型类 | 表名 | 旧表名 |
|--------|------|--------|
| `DPlantcareDeathinfo` | `d_plantcare_witherinfo` | `d_health_deathinfo` |
| `DPlantcareDamageinfo` | `d_plantcare_damageinfo` | `d_health_diseaseinfo` 等 |
| `DPlantcareDiseaseinfo` | `d_plantcare_diseaseinfo` | `d_health_diseaseinfo` |
| `DPlantcareImmunizationinfo` | `d_plantcare_immunizationinfo` | `d_health_immunizationinfo` |
| `DPlantcareNursinginfo` | `d_plantcare_nursinginfo` | `d_health_nursinginfo` |
| `DPlantcareProtectioninfo` | `d_plantcare_protectioninfo` | `d_health_protectioninfo` |
| `DPlantcareQuarantineinfo` | `d_plantcare_quarantineinfo` | `d_health_quarantineinfo` |
| `DPlantcareImmunizationBS` | `d_plantcare_immunization_b_s` | 免疫记录汇总 |

**种植培育模块**（e_cultivation_* → 保留原名）：
| 模型类 | 表名 |
|--------|------|
| `ECultivationCultivationinfo` | `e_cultivation_cultivationinfo` |
| `ECultivationFloweringinfo` | `e_cultivation_floweringinfo` |
| `ECultivationGerminationinfo` | `e_cultivation_germinationinfo` |
| `ECultivationIrrigationinfo` | `e_cultivation_irrigationinfo` |
| `ECultivationMaturationinfo` | `e_cultivation_maturationinfo` |
| `ECultivationPolleninfo` | `e_cultivation_polleninfo` |
| `ECultivationSeedinginfo` | `e_cultivation_seedinginfo` |
| `ECultivationSproutinfo` | `e_cultivation_sproutinfo` |

**收获加工模块**（g_harvest_*）：
| 模型类 | 表名 |
|--------|------|
| `GHarvestSSalesinfo` | `g_harvest_s_salesinfo` |
| `GHarvestGSalesinfo` | `g_harvest_g_salesinfo` |
| `GHarvestBinformationinfo` | `g_harvest_binformationinfo` |
| `GHarvestEconomicinfo` | `g_harvest_economicinfo` |
| `GHarvestSegmentinfo` | `g_harvest_segmentinfo` |

**仓储管理模块**（h_store_*）：
| 模型类 | 表名 |
|--------|------|
| `HStoreInventory` | `h_store_inventory` |
| `HStoreProtectionIn` | `h_store_protection_in` |
| `HStoreProtectionOut` | `h_store_protection_out` |
| `HStoreFeedingin` | `h_store_feedingin` |
| `HStoreFeedingOut` | `h_store_feeding_out` |

**供应商模块**（supply_*）：
| 模型类 | 表名 |
|--------|------|
| `SupplyCommodityinfo` | `supply_commodityinfo` |
| `SupplyVSuppliersinfo` | `supply_v_suppliersinfo` |
| `SupplyFSuppliersinfo` | `supply_f_suppliersinfo` |
| `SupplyInsuranceinfo` | `supply_insuranceinfo` |

**分析报表模块**：
| 模型类 | 表名 |
|--------|------|
| `Analysisdailysheet` | `analysis_daily_sheet` |
| `AnalysisDailyIncome` | `analysis_daily_income` |
| `AnalysisGrassAsset` | `analysis_daily_grass_asset` |
| `Analysisdailystocksheet` | `analysis_daily_stock_sheet` |
| `GrassAssetinfo` | `grass_assetinfo` |
| `GrassAssetStandardinfo` | `grass_asset_standardinfo` |

**预警信息模块**：
| 模型类 | 表名 |
|--------|------|
| `WinformationImmunizationMessageinfo` | `w_information_immunizationMessageinfo` |
| `ThresholdSetMessageinfo` | `threshold_setting` |

**Django遗留认证表**：
| 模型类 | 表名 | 说明 |
|--------|------|------|
| `AccountMyuser` | `account_myuser` | 用户表 |
| `AuthGroup` | `auth_group` | 权限组 |
| `AuthPermission` | `auth_permission` | 权限 |
| `DjangoContentType` | `django_content_type` | 内容类型 |
| `DjangoMigrations` | `django_migrations` | 迁移记录 |
| `DjangoSession` | `django_session` | Session |

---

## 3. 前端模块详细映射

### 3.1 后端API前缀配置 (`src/api/config/servicePort.ts`)

```typescript
PORT1 = "/basic";
PORT2 = "/hooks";
PORT3 = "/pest_control";
PORT4 = "/login";
PORT5 = "/w_information";
PORT6 = "/propagation";
```

> ⚠️ **问题**：很多视图层API文件没有从servicePort.ts导入，而是自己重新定义了PORT1，导致不一致。

### 3.2 视图 ↔ API ↔ 后端路由完整映射

**basic模块** (`src/views/basic/`)：
| 前端视图 | API文件 | 调用端点 | 后端路由 | 状态 |
|---------|---------|---------|---------|------|
| basicinfo | api/grass.ts | `/basic/basicinfo` | `basic.get_basic_info` | ✅ |
| basicinfo | api/grass.ts | `/basic/basicinfo/add` | `basic.add_basic_info` | ✅ |
| basicinfo | api/grass.ts | `/basic/basicinfo/edit` | `basic.edit_basic_info` | ✅ |
| fieldconditioninfo | api/manu.ts | `/basic/fieldconditioninfo` | `basic.get_fieldcondition_info` | ✅ |
| fieldconditioninfo | api/manu.ts | `/basic/fieldconditioninfo/add` | `basic.add_fieldcondition_info` | ✅ |
| harvestinfo | api/manu.ts | `/basic/harvestinfo` | `basic.get_harvest_info` | ✅ |
| harvestinfo | api/manu.ts | `/colony/houseinfo` | `field.get_houseinfo` | ❌ 应为 `/field/houseinfo` |
| manuinfo | api/manu.ts | `/basic/manuinfo` | `basic.get_manu_info` | ✅ |
| sportsinfo | api/manu.ts | `/basic/manuinfo` | `basic.get_manu_info` | ❌ 应为 `/basic/sportsinfo` |
| yieldperformance | api/manu.ts | `/basic/manuinfo` | `basic.get_manu_info` | ❌ 应为 `/basic/yieldperformance` |
| productivityinfo | api/manu.ts | `/basic/manuinfo` | `basic.get_manu_info` | ❌ 应为 `/basic/productivityinfo` |
| canopyperformance | api/manu.ts | `/basic/manuinfo` | `basic.get_manu_info` | ❌ 应为 `/basic/canopyperformance` |
| fertilizerinfo | api/manu.ts | `/basic/manuinfo` | `basic.get_manu_info` | ❌ 应为 `/basic/fertilizerinfo` |

**field模块** (`src/views/field/`)：
| 前端视图 | API文件 | 调用端点 | 后端路由 | 状态 |
|---------|---------|---------|---------|------|
| houseinfo | api/manu.ts | `/colony/houseinfo` | `field.get_houseinfo` | ❌ 应为 `/field/houseinfo` |
| houseinfo | api/manu.ts | `/colony/houseinfo/updateHouseNumber` | `field.update_house_number` | ❌ 应为 `/field/houseinfo/updateHouseNumber` |
| hurdleinfo | api/manu.ts | `/colony/hurdleinfo` | `field.get_hurdleinfo` | ❌ 应为 `/field/hurdleinfo` |
| hurdleinfo | api/manu.ts | `/colony/hurdleinfo/initHouse` | `field.init_house` | ❌ 应为 `/field/hurdleinfo/initHouse` |
| disinfectioninfo | api/manu.ts | `/colony/disinfectioninfo` | `field.get_disinfectioninfo` | ❌ 应为 `/field/disinfectioninfo` |
| maintenanceinfo | api/manu.ts | `/basic/manuinfo` | `basic.get_manu_info` | ❌ 应为 `/field/maintenanceinfo` |
| transferinfo | api/manu.ts | `/basic/manuinfo` | `basic.get_manu_info` | ❌ 应为 `/field/transferinfo` |

**pest_control模块** (`src/views/pest_control/`)：
| 前端视图 | API文件 | 调用端点 | 后端路由 | 状态 |
|---------|---------|---------|---------|------|
| deathinfo | api/manu.ts | `/pest_control/witherinfo` | `pest_control.get_witherinfo` | ✅ |
| immunizationinfo | api/manu.ts | `/pest_control/immunizationinfo` | `pest_control.get_immunizationinfo` | ✅ |
| protectioninfo | api/manu.ts | `/pest_control/protectioninfo` | `pest_control.get_protectioninfo` | ✅ |
| quarantineinfo | api/manu.ts | `/pest_control/quarantineinfo` | `pest_control.get_quarantineinfo` | ✅ |
| nursinginfo | api/manu.ts | `/pest_control/nursinginfo` | `pest_control.get_nursinginfo` | ✅ |
| diseaseinfo | api/manu.ts | `/pest_control/diseaseinfo` | `pest_control.get_diseaseinfo` | ✅ |
| damageinfo | api/manu.ts | `/pest_control/damageinfo` | `pest_control.get_damageinfo` | ✅ |

**propagation模块** (`src/views/propagation/`)：
| 前端视图 | API文件 | 调用端点 | 后端路由 | 状态 |
|---------|---------|---------|---------|------|
| seedlinginfo | api/manu.ts | `propagation/seedlinginfo` | `propagation.get_seedlinginfo` | ⚠️ 缺前导 `/` |
| hardeninginfo | api/manu.ts | `propagation/hardeninginfo` | `propagation.get_hardeninginfo` | ⚠️ 缺前导 `/` |
| post_harvestinfo | api/manu.ts | `propagation/post_harvestinfo` | `propagation.get_post_harvestinfo` | ⚠️ 缺前导 `/` |
| ... | ... | ... | ... | ⚠️ 全部缺 `/` |

**h_store模块** (`src/views/h_store/`)：
| 前端视图 | API文件 | 调用端点 | 后端路由 | 状态 |
|---------|---------|---------|---------|------|
| protection_in | api/manu.ts | `/h_store/protection_in` | `h_store.get_vaccine_in` | ✅ |
| protection_out | api/manu.ts | `/h_store/protection_out` | `h_store.get_vaccine_out` | ✅ |
| feedingin | api/manu.ts | `/h_store/feedingin` | `h_store.get_feedingin` | ✅ |
| feeding_out | api/manu.ts | `/h_store/feeding_out` | `h_store.get_feeding_out` | ✅ |
| inventoryDrug | api/manu.ts | `/h_store/inventory` | `h_store.get_inventory` | ✅ |
| inventoryForage | api/manu.ts | `/h_store/inventoryForage` | `h_store.get_inventoryForage` | ✅ |

**supply模块** (`src/views/supply/`)：
| 前端视图 | API文件 | 调用端点 | 后端路由 | 状态 |
|---------|---------|---------|---------|------|
| commodityinfo | api/manu.ts | `/supply/commodityinfo` | `supply.get_commodity_info` | ✅ |
| v_suppliersinfo | api/manu.ts | `/supply/v_suppliersinfo` | `supply.get_v_suppliers_info` | ✅ |
| f_suppliersinfo | api/manu.ts | `/supply/f_suppliersinfo` | `supply.get_f_suppliers_info` | ✅ |
| insuranceinfo | api/manu.ts | `/supply/insuranceinfo` | `supply.get_insurance_info` | ✅ |

**analysis模块** (`src/views/analysis/`)：
| 前端视图 | API文件 | 调用端点 | 后端路由 | 状态 |
|---------|---------|---------|---------|------|
| daily_report | api/manu.ts | `/analysis/daily_report` | `analysis.get_dailyReport` | ✅ |
| daily_income | api/manu.ts | `/analysis/daily_income` | `analysis.get_daily_income` | ✅ |
| daily_grass_asset | api/manu.ts | `/analysis/daily_grass_asset` | `analysis.get_daily_grass_asset` | ✅ |
| stock_asset | api/manu.ts | `/analysis/daily_stocksheet` | `analysis.daily_stocksheet` | ✅ |
| asset_standard | api/manu.ts | `analysis/standardinfo` | `analysis.get_standardinfo` | ⚠️ 缺 `/` |
| grass_asset | api/manu.ts | `analysis/grass_assetinfo` | `analysis.get_grass_assetinfo` | ⚠️ 缺 `/` |
| dataVisualize | api/manu.ts | `/analysis/dataVisualize` | `analysis.get_daily_financial_data` | ✅ |

**w_information模块** (`src/views/w_information/`)：
| 前端视图 | API文件 | 调用端点 | 后端路由 | 状态 |
|---------|---------|---------|---------|------|
| immunizationMessage | api/manu.ts | `/w_information/immunizationMessageinfo` | `w_information.get_immunizationMessageinfo` | ✅ |

**home模块** (`src/views/home/`)：
> ⚠️ **严重问题**：所有home/*子模块都错误地调用 `/basic/manuinfo`，这会导致数据类型完全错误。
> 受影响模块：basic_basicinfo, basic_capacity_females, basic_capacity_males, familytree_files, importdata, productivityinfo, data_statistics_auto, home_dailysheet, home_annualsheet_auto, basic_makescore

**statistic模块** (`src/views/statistic/`)：
| 前端视图 | API文件 | 调用端点 | 后端路由 | 状态 |
|---------|---------|---------|---------|------|
| basicinfo | api/grass.ts | `/statistic/basicinfo` | `statistic.get_basic_info` | ✅ |
| makescore | api/manu.ts | `statistic/makescore` | `statistic.get_makescoreTable` | ⚠️ 缺 `/` |
| obsoletegrassinfo | api/manu.ts | `/statistic/obsoletegrassinfo` | `statistic.get_obsoletegrassinfo` | ✅ |
| xipu | api/grass.ts | `/statistic/xipu/updatedata` | `statistic.updateData` | ✅ |

**g_harvest模块** (`src/views/g_harvest/`)：
> ⚠️ **严重问题**：binformationinfo, processinginfo, economicinfo 都调用 `/basic/manuinfo`，应为各自的 `/g_harvest/xxx` 端点。

---

## 4. 已知问题清单（按优先级排序）

### 🔴 P0 - 致命错误（会导致系统完全不可用）

#### P0-1: `import datetime` 模块调用类方法
**位置**：8个views文件
- `App/basic/views.py`
- `App/pest_control/views.py`
- `App/field/views.py`
- `App/g_harvest/views.py`
- `App/supply/views.py`
- `App/w_information/views.py`
- `App/statistic/view.py`
- `App/login_auth/views.py`

**问题**：这些文件顶部写 `import datetime`，但代码中调用 `datetime.now()`, `datetime.strptime()`, `datetime.fromisoformat()`。`datetime` 是模块，不是类，这些方法是 `datetime.datetime` 类的。

**错误表现**：`AttributeError: module 'datetime' has no attribute 'now'`

**修复方案**：将 `import datetime` 改为 `from datetime import datetime`

**修复状态**：⏳ 待执行

---

#### P0-2: 模型字段名与数据库字段名严重不匹配
**位置**：`modelsReverse.py` 中定义的字段 vs `init-scripts/meadow_test.sql` 中的实际字段

**具体不匹配**：

| 表名 | 模型字段 | 数据库字段 | 状态 |
|------|---------|-----------|------|
| `basic_basicinfo` | `paternal_grandfather_id` | `ram_grandfather_id` | ❌ |
| `basic_basicinfo` | `paternal_grandfather_ele_num` | `ram_grandfather_ele_num` | ❌ |
| `basic_basicinfo` | `paternal_grandfather_pre_num` | `ram_grandfather_pre_num` | ❌ |
| `basic_basicinfo` | `maternal_grandfather_id` | `ewe_grandfather_id` | ❌ |
| `basic_basicinfo` | `maternal_grandfather_ele_num` | `ewe_grandfather_ele_num` | ❌ |
| `basic_basicinfo` | `maternal_grandfather_pre_num` | `ewe_grandfather_pre_num` | ❌ |
| `basic_basicinfo` | `paternal_grandmother_id` | `ram_grandmother_id` | ❌ |
| `basic_basicinfo` | `paternal_grandmother_ele_num` | `ram_grandmother_ele_num` | ❌ |
| `basic_basicinfo` | `paternal_grandmother_pre_num` | `ram_grandmother_pre_num` | ❌ |
| `basic_basicinfo` | `maternal_grandmother_id` | `ewe_grandmother_id` | ❌ |
| `basic_basicinfo` | `maternal_grandmother_ele_num` | `ewe_grandmother_ele_num` | ❌ |
| `basic_basicinfo` | `maternal_grandmother_pre_num` | `ewe_grandmother_pre_num` | ❌ |
| `basic_fieldconditioninfo` | `root_shape` | `testis_shape` | ❌ |
| `basic_fieldconditioninfo` | `with_plantings` | `with_births` | ❌ |
| `basic_harvestinfo` | `harvest_time` | `cut_time` | ❌ |
| `basic_harvestinfo` | `harvest_num` | `cut_num` | ❌ |

**错误表现**：`(1054, "Unknown column 'xxx' in 'field list'")` → HTTP 500

**修复方案**：
- 方案A（保留数据）：对运行中的MySQL执行 `ALTER TABLE ... CHANGE COLUMN old_name new_name type`
- 方案B（重建）：删除数据库卷，用修正后的SQL重建，再导入数据

**修复状态**：⏳ 待执行（采用方案A保留数据）

---

### 🟠 P1 - 严重错误（会导致模块功能不可用）

#### P1-1: 前端API仍调用旧 `/colony/` 前缀
**位置**：
- `src/views/basic/harvestinfo/api/manu.ts` → `/colony/houseinfo`
- `src/views/field/houseinfo/api/manu.ts` → `/colony/houseinfo`
- `src/views/field/hurdleinfo/api/manu.ts` → `/colony/hurdleinfo`
- `src/views/field/disinfectioninfo/api/manu.ts` → `/colony/disinfectioninfo`

**修复方案**：将 `/colony/` 替换为 `/field/`

**修复状态**：⏳ 待执行

---

#### P1-2: 大量前端模块错误调用 `/basic/manuinfo`
**位置**：
- `src/views/home/*/api/manu.ts`（10+个home子模块）
- `src/views/basic/sportsinfo/api/manu.ts`
- `src/views/basic/yieldperformance/api/manu.ts`
- `src/views/basic/productivityinfo/api/manu.ts`
- `src/views/basic/canopyperformance/api/manu.ts`
- `src/views/basic/fertilizerinfo/api/manu.ts`
- `src/views/field/maintenanceinfo/api/manu.ts`
- `src/views/field/transferinfo/api/manu.ts`
- `src/views/g_harvest/binformationinfo/api/manu.ts`
- `src/views/g_harvest/processinginfo/api/manu.ts`
- `src/views/g_harvest/economicinfo/api/manu.ts`

**问题**：这些模块应该调用各自独立的API端点（如 `/basic/sportsinfo`、`/field/maintenanceinfo` 等），但都错误地指向了生产商管理接口 `/basic/manuinfo`。

**修复方案**：
1. 在后端为每个缺失的实体创建独立的CRUD路由（如果后端views.py中已有则直接映射）
2. 或者在前端修正API端点指向正确的后端路由

**注意**：经审查后端代码，上述模块中很多在后端 **确实没有对应的独立路由**。例如 `/basic/sportsinfo` 路由在 `basic/views.py` 中不存在。这说明这些模块可能是**占位符/未开发完成**的。

**修复状态**：⏳ 待执行（需要判断是补后端路由还是前端隐藏模块）

---

#### P1-3: 密码重置未进行MD5哈希比较
**位置**：`App/login_auth/views.py` line 103

**问题**：`reset_password` 比较 `pwd_old != user.password` 时，`user.password` 存储的是MD5哈希值，但 `pwd_old` 是明文，没有先MD5再比较。

**修复方案**：比较前对 `pwd_old` 执行 `hashlib.md5(pwd_old.encode()).hexdigest()`

**修复状态**：⏳ 待执行

---

### 🟡 P2 - 中等问题

#### P2-1: 路由重复定义
**位置**：`App/propagation/views.py` line 2889 和 2995

**问题**：`/propagation/hardeninginfo/add` 定义了两次，第二个 handler `add_hardeninginfo_upbasiclamb` 永不可达。

**修复方案**：合并两个handler或给第二个改URL

**修复状态**：⏳ 待执行

---

#### P2-2: 跨蓝图路由冲突
**位置**：`App/statistic/view.py`

**问题**：`/basic/basicinfo/update_grandparents` 同时存在于 `basic` 和 `statistic` 蓝图。由于 `basic` 先注册，`statistic` 版本不可达。

**修复方案**：删除 `statistic` 蓝图中的重复路由

**修复状态**：⏳ 待执行

---

#### P2-3: 拼写错误
**位置**：`App/h_store/views.py` line 776

**问题**：`dailySheet.yaoping_fees` 应为 `dailySheet.yaopin_fees`

**修复状态**：⏳ 待执行

---

#### P2-4: 部分API路径缺少前导 `/`
**位置**：
- `src/views/propagation/*/api/manu.ts` → `propagation/xxx` (应为 `/propagation/xxx`)
- `src/views/analysis/asset_standard/api/manu.ts` → `analysis/xxx`
- `src/views/analysis/grass_asset/api/manu.ts` → `analysis/xxx`
- `src/views/statistic/makecore/api/manu.ts` → `statistic/xxx`

**修复方案**：所有API前缀统一加 `/`

**修复状态**：⏳ 待执行

---

### 🟢 P3 - 低优先级问题

#### P3-1: 菜单从本地JSON加载
**位置**：`src/api/modules/login.ts`

**问题**：`getAuthMenuListApi()` 和 `getAuthButtonListApi()` 返回的是本地 JSON 文件，不是从后端获取。这意味着权限控制是静态的。

**修复状态**：⏹️ 暂不处理（需要设计后端菜单API）

#### P3-2: 大量模块前端存在但后端缺少对应路由
**问题**：`home/*` 下很多模块、`basic/sportsinfo` 等模块，前端有页面但后端没有对应CRUD接口。

**修复状态**：⏹️ 暂不处理（可能是未开发完成的功能）

---

## 5. 数据库数据迁移规则

### 5.1 数据迁移映射表（从旧备份到新项目）

**来源**：`/home/debian/AgroBuckup/AgroGuard_20260427_085106/AgroGuard/init-scripts/meadow_test.sql`
**目标**：当前运行的 MySQL 容器 `meadow-guard-mysql-db-1`

| 备份表（旧） | 新表 | 字段映射（旧→新） | 迁移方式 |
|-------------|------|-----------------|---------|
| `colony_houseinfo` | `field_houseinfo` | 字段基本相同，直接复制 | INSERT ... SELECT |
| `colony_disinfectioninfo` | `field_disinfectioninfo` | 字段基本相同 | INSERT ... SELECT |
| `colony_maintenanceinfo` | `field_maintenanceinfo` | 字段基本相同 | INSERT ... SELECT |
| `colony_transferinfo` | `field_transferinfo` | 字段基本相同 | INSERT ... SELECT |
| `basic_breederconditioninfo` | `basic_fieldconditioninfo` | `testis_shape`→`root_shape`, `with_births`→`with_plantings` | 字段名转换后插入 |
| `basic_cutinfo` | `basic_harvestinfo` | `cut_time`→`harvest_time`, `cut_num`→`harvest_num` | 字段名转换后插入 |
| `basic_manureinfo` | `basic_fertilizerinfo` | 字段基本相同 | INSERT ... SELECT |

### 5.2 空表填充策略

对于当前项目中存在但备份中没有对应表的模块（如 `e_cultivation_*` 系列），需要手工生成测试数据插入，确保每个表至少有5条记录。

待填充的空表清单：
- `field_houseinfo`, `field_disinfectioninfo`, `field_maintenanceinfo`, `field_transferinfo`
- `e_cultivation_cultivationinfo`, `e_cultivation_floweringinfo`, `e_cultivation_germinationinfo`, `e_cultivation_irrigationinfo`, `e_cultivation_maturationinfo`, `e_cultivation_polleninfo`, `e_cultivation_seedinginfo`, `e_cultivation_sproutinfo`
- `d_plantcare_damageinfo`, `d_plantcare_diseaseinfo`, `d_plantcare_immunizationinfo`, `d_plantcare_nursinginfo`, `d_plantcare_protectioninfo`, `d_plantcare_quarantineinfo`, `d_plantcare_witherinfo`
- `g_harvest_binformationinfo`, `g_harvest_economicinfo`, `g_harvest_g_salesinfo`, `g_harvest_s_salesinfo`, `g_harvest_segmentinfo`
- `h_store_feedingin`, `h_store_feeding_out`, `h_store_inventory`, `h_store_protection_in`, `h_store_protection_out`
- `supply_commodityinfo`, `supply_f_suppliersinfo`, `supply_insuranceinfo`, `supply_v_suppliersinfo`
- `grass_assetinfo`, `grass_asset_standardinfo`
- `w_information_immunizationMessageinfo`

---

## 6. 操作日志

### 2024-04-27 深度审查与修复启动
**执行AI**：OpenCode (kimi-k2.6)
**执行内容**：
1. 完成后端12个蓝图的182个路由全量扫描
2. 完成前端68个API模块的250+个接口调用全量扫描
3. 完成数据库新旧schema对比（82张表 vs 65张备份表）
4. 识别出20项问题（4项P0致命、4项P1严重、4项P2中等）
5. 发现前端大量模块调用错误的 `/basic/manuinfo` 端点
6. 发现前端4个模块仍使用旧的 `/colony/` 前缀
7. 确认数据库模型与表结构存在字段名不匹配（71个模型全部受影响）

**待执行修复**：
- [ ] 修复8个views文件的datetime导入
- [ ] 修复模型字段名与数据库字段名不匹配（通过ALTER TABLE）
- [ ] 修复前端 /colony/ → /field/ 路径
- [ ] 修复前端缺少前导 / 的API路径
- [ ] 修复h_store views.py中的typo
- [ ] 修复login_auth密码重置MD5比较
- [ ] 从备份迁移数据到新表
- [ ] 为所有空表填充至少5条测试数据
- [ ] Docker重建并全链路测试

---

## 7. 开发规范

### 7.1 后端代码规范
- 所有时间操作使用 `from datetime import datetime`，禁止 `import datetime`
- 模型字段名必须与数据库字段名完全一致
- 蓝图路由URL使用小写字母+下划线，禁止大写字母
- 密码比较必须统一使用 `hashlib.md5(pwd.encode()).hexdigest()`
- 跨蓝图模型操作应通过API调用，避免直接import其他蓝图的模型

### 7.2 前端代码规范
- API路径前缀必须带前导 `/`（如 `/propagation/xxx`，禁止 `propagation/xxx`）
- API模块必须从 `src/api/config/servicePort.ts` 导入PORT常量
- 每个前端模块的API应调用对应的后端实体路由，禁止复用其他模块的接口

### 7.3 数据库规范
- 表名使用小写字母+下划线
- 字段名与模型名保持一致
- 备份SQL文件更新后，必须同步更新 `init-scripts/meadow_test.sql`
- 数据库初始化仅在首次挂载时执行，后续修改需通过 ALTER TABLE 或数据迁移脚本

---

## 8. 快速参考

**启动Docker服务**：
```bash
cd /home/debian/AgroGuard
docker-compose up -d --build
```

**查看服务日志**：
```bash
docker logs meadow-guard-flask-1 --tail 50
docker logs meadow-guard-vue-1 --tail 20
docker logs meadow-guard-mysql-db-1 --tail 20
```

**进入MySQL容器**：
```bash
docker exec -it meadow-guard-mysql-db-1 mysql -uroot -pmeadow123 meadow_test
```

**重新构建镜像**：
```bash
cd /home/debian/AgroGuard
docker-compose down -v  # 注意：这会删除数据库数据！
docker-compose up -d --build
```

**前端开发模式**：
```bash
cd /home/debian/AgroGuard/meadow-fe
npm install
npm run dev
```

**后端本地运行**：
```bash
cd /home/debian/AgroGuard/meadow-be
pip install -r requirements.txt
python app.py
```

---

## 9. Build 操作流程规范（强制）

> **⚠️ 任何 AI 或开发者在对本项目执行 Build 前，必须严格遵守以下流程。**

### 9.1 Build 前 —— 必须先写任务清单

在 `/home/debian/AgroGuard/2026-04-27_操作记录.md` 中追加新的章节，明确记录：

1. **用户反馈的问题**（逐条列出）
2. **执行计划**（分阶段，带复选框）
3. **用户决策确认**（保留/删除哪些数据、药剂名称、数量限制等）
4. **预计影响的文件和表**

**不允许**在未写任务清单的情况下直接修改代码或执行数据库操作。

### 9.2 Build 中 —— 分阶段执行，及时验证

1. **每完成一个阶段，必须验证结果**：
   - 代码修改后，检查语法正确性
   - 数据库操作后，查询数据量确认符合预期
   - 前端修改后，确认文件路径和路由匹配
2. **发现问题立即修正**，不要累积到后面统一处理
3. **核心大表（`basic_basicinfo`、`basic_fieldconditioninfo`）禁止随意清理**，除非用户明确同意

### 9.3 Build 后 —— 必须写完成总结

在操作记录的同一章节中追加：

1. **实际完成的修改**（与计划对照）
2. **验证结果**（数据条数、API测试结果、页面是否正常打开）
3. **遗留说明**（未解决的问题、注意事项）
4. **部署状态**（Docker 是否重建成功）

### 9.4 历史 Build 记录归档格式

```markdown
## N、模块名称修复（YYYY-MM-DD 追加）

### N.1 任务清单（Build前）
...

### N.2 修复内容
...

### N.3 验证结果
...

### N.4 部署结果
...
```

---

*本文档最后更新：2026-04-28*
*下次更新：随项目持续维护*
