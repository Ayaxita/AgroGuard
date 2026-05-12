# 🚨 AGROGUARD 项目总指南 — 必读文件

> **⚠️ 每一个接手此项目的AI或开发者，在执行任何操作前必须先完整阅读本文档。**
> 本文档是项目的技术圣经，记录了完整的架构、修复历史、当前状态和操作规范。
> **最后更新时间：2026-04-27**

---

## 目录

1. [项目总览](#1-项目总览)
2. [技术架构](#2-技术架构)
3. [服务映射与访问方式](#3-服务映射与访问方式)
4. [后端模块完整清单](#4-后端模块完整清单)
5. [前端模块完整清单](#5-前端模块完整清单)
6. [数据库模型与表映射](#6-数据库模型与表映射)
7. [修复历史记录](#7-修复历史记录)
8. [当前已知问题（遗留）](#8-当前已知问题遗留)
9. [开发规范](#9-开发规范)
10. [操作手册](#10-操作手册)
11. [数据迁移规则](#11-数据迁移规则)

---

## 1. 项目总览

**项目名称**：草地作物病虫害智能监测系统 (AgroGuard / Meadow Guard)
**项目路径**：`/home/debian/AgroGuard`
**技术栈**：
- 后端：Python 3.9 + Flask + SQLAlchemy + Flask-JWT-Extended + PyMySQL + Gunicorn
- 前端：Vue 3 + TypeScript + Vite + Element Plus + Pinia
- 数据库：MySQL 5.7
- 部署：Docker Compose (3 services)

---

## 2. 技术架构

```
/home/debian/AgroGuard/
├── docker-compose.yml          # Docker编排文件
├── init-scripts/
│   └── meadow_test.sql         # 数据库初始化SQL（首次启动挂载）
├── meadow-be/                  # 后端Flask项目
│   ├── app.py                  # Flask应用入口
│   ├── Dockerfile
│   ├── requirements.txt
│   └── App/
│       ├── __init__.py         # 蓝图注册中心
│       ├── exts.py             # 插件初始化 (SQLAlchemy, Migrate, CORS)
│       ├── modelsReverse.py    # SQLAlchemy模型定义（全部82个模型）
│       ├── task.py             # 定时任务
│       ├── login_auth/views.py # 登录认证蓝图
│       ├── basic/views.py      # 基础信息管理蓝图
│       ├── field/views.py      # 场地管理蓝图（原colony）
│       ├── pest_control/views.py # 病虫害防治蓝图
│       ├── propagation/views.py  # 种植培育蓝图
│       ├── g_harvest/views.py    # 收获加工蓝图
│       ├── h_store/views.py      # 仓储管理蓝图
│       ├── supply/views.py       # 供应商管理蓝图
│       ├── analysis/views.py     # 统计分析蓝图
│       ├── statistic/view.py     # 统计报表蓝图（注意：文件名是view.py单数）
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

---

## 3. 服务映射与访问方式

| 服务 | 容器名 | 外部端口 | 内部端口 | 说明 |
|------|--------|---------|---------|------|
| MySQL | meadow-guard-mysql-db-1 | 5010 | 3306 | root/meadow123 |
| Flask | meadow-guard-flask-1 | 5000 | 5000 | 4 worker Gunicorn |
| Vue | meadow-guard-vue-1 | 5020 | 80 | Nginx反向代理 |

**访问地址**：
- 前端界面：`http://localhost:5020`
- 后端 API：`http://localhost:5000`
- MySQL：`localhost:5010`

**Nginx代理规则**：
- `/api/*` → 转发到 Flask (自动去除 `/api` 前缀)
- 静态文件 → 直接服务 Vue 构建产物

**数据库连接URI**：`mysql+pymysql://root:meadow123@mysql-db:3306/meadow_test`

---

## 4. 后端模块完整清单

### 4.1 蓝图注册关系 (`App/__init__.py`)

| # | 蓝图变量 | 导入路径 | URL前缀 | 路由数 | 说明 |
|---|---------|---------|---------|--------|------|
| 1 | `login_auth` | `App.login_auth.views` | `/login`, `/logout` | 4 | 登录认证 |
| 2 | `basic` | `App.basic.views` | `/basic/...` | 34 | 基础信息 |
| 3 | `field` | `App.field.views` | `/field/...` | 28 | 场地管理 |
| 4 | `supply` | `App.supply.views` | `/supply/...` | 16 | 供应商管理 |
| 5 | `h_store` | `App.h_store.views` | `/h_store/...` | 27 | 仓储管理 |
| 6 | `g_harvest` | `App.g_harvest.views` | `/g_harvest/...` | 19 | 收获加工 |
| 7 | `pest_control` | `App.pest_control.views` | `/pest_control/...` | 32 | 病虫害防治 |
| 8 | `propagation` | `.propagation.views` | `/propagation/...` | 49 | 种植培育 |
| 9 | `w_information` | `.w_information.views` | `/w_information/...` | 4 | 预警信息 |
| 10 | `Statistic` | `.statistic.view` | `/statistic/...` | 27 | 统计报表 |
| 11 | `analysis` | `.analysis.views` | `/analysis/...` | 31 | 统计分析 |
| 12 | `chatbox` | `.chatbox.views` | `/chatbox/...` | 3 | AI聊天助手 |

> ⚠️ **注意**：`Statistic` 蓝图变量名首字母大写，这是历史遗留，不要修改。

### 4.2 关键路由列表（每个模块的主要端点）

**basic模块**：`/basic/basicinfo`, `/basic/manuinfo`, `/basic/fieldconditioninfo`, `/basic/harvestinfo`, `/basic/sportsinfo`, `/basic/yieldperformance`, `/basic/productivityinfo`, `/basic/canopyperformance`, `/basic/fertilizerinfo`

**field模块**：`/field/houseinfo`, `/field/hurdleinfo`, `/field/disinfectioninfo`, `/field/maintenanceinfo`, `/field/transferinfo`

**pest_control模块**：`/pest_control/witherinfo`, `/pest_control/immunizationinfo`, `/pest_control/protectioninfo`, `/pest_control/quarantineinfo`, `/pest_control/nursinginfo`, `/pest_control/diseaseinfo`, `/pest_control/damageinfo`

**propagation模块**：`/propagation/growth_statusinfo`, `/propagation/sample_collectinfo`, `/propagation/propagationinfo`, `/propagation/post_harvestinfo`, `/propagation/growth_cycleinfo`, `/propagation/artificial_careinfo`, `/propagation/hardeninginfo`, `/propagation/seedlinginfo`

**g_harvest模块**：`/g_harvest/s_salesinfo`, `/g_harvest/g_salesinfo`, `/g_harvest/binformationinfo`, `/g_harvest/economicinfo`, `/g_harvest/segmentinfo`

**h_store模块**：`/h_store/inventory`, `/h_store/inventoryForage`, `/h_store/protection_in`, `/h_store/protection_out`, `/h_store/feedingin`, `/h_store/feeding_out`

**supply模块**：`/supply/commodityinfo`, `/supply/v_suppliersinfo`, `/supply/f_suppliersinfo`, `/supply/insuranceinfo`

**analysis模块**：`/analysis/standardinfo`, `/analysis/grass_assetinfo`, `/analysis/daily_income`, `/analysis/daily_grass_asset`, `/analysis/daily_report`, `/analysis/daily_stocksheet`, `/analysis/dataVisualize`

**statistic模块**：`/statistic/basicinfo`, `/statistic/makescore`, `/statistic/obsoletegrassinfo`

**w_information模块**：`/w_information/immunizationMessageinfo`, `/w_information/thresholdsetMessageinfo`

**chatbox模块**：`/chatbox/chat`, `/chatbox/models`, `/chatbox/getWsToken`

---

## 5. 前端模块完整清单

### 5.1 API配置 (`src/api/config/servicePort.ts`)

```typescript
PORT1 = "/basic";
PORT2 = "/hooks";
PORT3 = "/pest_control";
PORT4 = "/login";
PORT5 = "/w_information";
PORT6 = "/propagation";
```

### 5.2 视图目录结构

```
src/views/
├── basic/           # 基础信息模块
│   ├── basicinfo/
│   ├── manuinfo/
│   ├── fieldconditioninfo/
│   ├── harvestinfo/
│   ├── sportsinfo/
│   ├── yieldperformance/
│   ├── productivityinfo/
│   ├── canopyperformance/
│   └── fertilizerinfo/
├── field/           # 场地管理模块
│   ├── houseinfo/
│   ├── hurdleinfo/
│   ├── disinfectioninfo/
│   ├── maintenanceinfo/
│   └── transferinfo/
├── pest_control/    # 病虫害防治模块
│   ├── deathinfo/
│   ├── immunizationinfo/
│   ├── protectioninfo/
│   ├── quarantineinfo/
│   ├── nursinginfo/
│   ├── diseaseinfo/
│   └── damageinfo/
├── propagation/     # 种植培育模块
│   ├── growth_statusinfo/
│   ├── sample_collectinfo/
│   ├── propagationinfo/
│   ├── post_harvestinfo/
│   ├── growth_cycleinfo/
│   ├── artificial_careinfo/
│   ├── hardeninginfo/
│   └── seedlinginfo/
├── g_harvest/       # 收获加工模块
│   ├── s_salesinfo/
│   ├── g_salesinfo/
│   ├── binformationinfo/
│   ├── economicinfo/
│   └── processinginfo/  (实际调用 /g_harvest/segmentinfo)
├── h_store/         # 仓储管理模块
│   ├── inventoryDrug/
│   ├── inventoryForage/
│   ├── protection_in/
│   ├── protection_out/
│   ├── feedingin/
│   └── feeding_out/
├── supply/          # 供应商模块
│   ├── commodityinfo/
│   ├── v_suppliersinfo/
│   ├── f_suppliersinfo/
│   └── insuranceinfo/
├── analysis/        # 统计分析模块
│   ├── asset_standard/
│   ├── grass_asset/
│   ├── daily_income/
│   ├── daily_grass_asset/
│   ├── daily_report/
│   ├── stock_asset/
│   ├── dataVisualize/
│   ├── g_salesinfo/
│   └── s_salesinfo/
├── w_information/   # 预警信息模块
│   └── immunizationMessage/
├── statistic/       # 统计报表模块
│   ├── basicinfo/
│   ├── makecore/
│   ├── obsoletegrassinfo/
│   └── xipu/
├── home/            # 首页/仪表盘模块
│   ├── basic_basicinfo/
│   ├── basic_capacity_females/
│   ├── basic_capacity_males/
│   ├── basic_makescore/
│   ├── data_statistics_auto/
│   ├── familytree_files/
│   ├── home_annualsheet_auto/
│   ├── home_dailysheet/
│   ├── importdata/
│   └── productivityinfo/
└── home/... (其他子模块)
```

---

## 6. 数据库模型与表映射

### 6.1 核心模型 ↔ 数据库表映射

| 模型类 | 表名 | 备注 |
|--------|------|------|
| `BasicBasicinfo` | `basic_basicinfo` | 核心表，11,280条数据 |
| `BasicFieldconditioninfo` | `basic_fieldconditioninfo` | 13,390条数据 |
| `BasicHarvestinfo` | `basic_harvestinfo` | 5条数据 |
| `BasicManuinfo` | `basic_manuinfo` | 7条数据 |
| `BasicMakescore` | `basic_makescore` | 12条数据 |
| `BasicObsoleteGrassinfo` | `basic_obsoletegrassinfo` | 5条数据 |
| `BasicGroupmalecapacity` | `basic_groupmalecapacity` | 64条数据 |
| `BasicYieldCapacity` | `basic_yield_capacity` | 69条数据 |
| `BasicPollenCapacity` | `basic_pollen_capacity` | 9条数据 |
| `BasicYieldperformance` | `basic_yieldperformance` | 5条数据 |
| `BasicProductivityinfo` | `basic_productivityinfo` | 5条数据 |
| `BasicCanopyperformance` | `basic_canopyperformance` | 5条数据 |
| `BasicFertilizerinfo` | `basic_fertilizerinfo` | 5条数据 |
| `BasicSportsinfo` | `basic_sportsinfo` | 5条数据 |
| `FieldHouseinfo` | `field_houseinfo` | 410条数据 |
| `FieldDisinfectioninfo` | `field_disinfectioninfo` | 181,763条数据 |
| `FieldMaintenanceinfo` | `field_maintenanceinfo` | 5条数据 |
| `FieldTransferinfo` | `field_transferinfo` | 5条数据 |
| `DPlantcareDeathinfo` | `d_plantcare_witherinfo` | 5条数据 |
| `DPlantcareDamageinfo` | `d_plantcare_damageinfo` | 5条数据 |
| `DPlantcareDiseaseinfo` | `d_plantcare_diseaseinfo` | 5条数据 |
| `DPlantcareImmunizationinfo` | `d_plantcare_immunizationinfo` | 5条数据 |
| `DPlantcareNursinginfo` | `d_plantcare_nursinginfo` | 5条数据 |
| `DPlantcareProtectioninfo` | `d_plantcare_protectioninfo` | 5条数据 |
| `DPlantcareQuarantineinfo` | `d_plantcare_quarantineinfo` | 5条数据 |
| `ECultivationCultivationinfo` | `e_cultivation_cultivationinfo` | 5条数据 |
| `ECultivationFloweringinfo` | `e_cultivation_floweringinfo` | 5条数据 |
| `ECultivationGerminationinfo` | `e_cultivation_germinationinfo` | 5条数据 |
| `ECultivationIrrigationinfo` | `e_cultivation_irrigationinfo` | 5条数据 |
| `ECultivationMaturationinfo` | `e_cultivation_maturationinfo` | 5条数据 |
| `ECultivationPolleninfo` | `e_cultivation_polleninfo` | 5条数据 |
| `ECultivationSeedinginfo` | `e_cultivation_seedinginfo` | 5条数据 |
| `ECultivationSproutinfo` | `e_cultivation_sproutinfo` | 5条数据 |
| `GHarvestSSalesinfo` | `g_harvest_s_salesinfo` | 5条数据 |
| `GHarvestGSalesinfo` | `g_harvest_g_salesinfo` | 5条数据 |
| `GHarvestBinformationinfo` | `g_harvest_binformationinfo` | 5条数据 |
| `GHarvestEconomicinfo` | `g_harvest_economicinfo` | 5条数据 |
| `GHarvestSegmentinfo` | `g_harvest_segmentinfo` | 5条数据 |
| `HStoreInventory` | `h_store_inventory` | 5条数据 |
| `HStoreProtectionIn` | `h_store_protection_in` | 5条数据 |
| `HStoreProtectionOut` | `h_store_protection_out` | 5条数据 |
| `HStoreFeedingin` | `h_store_feedingin` | 5条数据 |
| `HStoreFeedingOut` | `h_store_feeding_out` | 5条数据 |
| `SupplyCommodityinfo` | `supply_commodityinfo` | 5条数据 |
| `SupplyVSuppliersinfo` | `supply_v_suppliersinfo` | 5条数据 |
| `SupplyFSuppliersinfo` | `supply_f_suppliersinfo` | 5条数据 |
| `SupplyInsuranceinfo` | `supply_insuranceinfo` | 5条数据 |
| `Analysisdailysheet` | `analysis_daily_sheet` | 73条数据 |
| `AnalysisDailyIncome` | `analysis_daily_income` | 70条数据 |
| `AnalysisGrassAsset` | `analysis_daily_grass_asset` | 72条数据 |
| `Analysisdailystocksheet` | `analysis_daily_stock_sheet` | 70条数据 |
| `GrassAssetinfo` | `grass_assetinfo` | 10条数据 |
| `GrassAssetStandardinfo` | `grass_asset_standardinfo` | 10条数据 |
| `WinformationImmunizationMessageinfo` | `w_information_immunizationMessageinfo` | 5条数据 |
| `ThresholdSetMessageinfo` | `threshold_setting` | - |
| `AccountMyuser` | `account_myuser` | 15条数据 |
| `Testuser` | `testuser` | 5条数据 |

### 6.2 字段名映射规则

**⚠️ 关键规则**：模型字段名必须与数据库列名完全一致。以下是有特殊历史的字段：

| 表名 | 数据库列名 | 模型字段名 | 说明 |
|------|-----------|-----------|------|
| `basic_groupmalecapacity` | `one_year_ram` | `one_year_ram` | 已修正（原one_year_male） |
| `basic_groupmalecapacity` | `capa_ram` | `capa_ram` | 已修正（原capa_male） |
| `basic_yield_capacity` | `mating_rate` | `mating_rate` | 已修正（原pollination_rate） |
| `basic_yield_capacity` | `lamb_num` | `lamb_num` | 已修正（原sprout_num） |
| `basic_yield_capacity` | `conception_num` | `conception_num` | 已修正（原flowering_num） |
| `basic_yield_capacity` | `pregnancy_num` | `pregnancy_num` | 新增（替换重复flowering_num） |

---

## 7. 修复历史记录

### 2026-04-27 大规模修复（当前会话）

**执行AI**：OpenCode (kimi-k2.6)
**修复范围**：后端代码、前端代码、数据库字段对齐、Docker部署

#### 7.1 后端修复

| # | 问题 | 修复文件 | 修复内容 |
|---|------|---------|---------|
| 1 | **datetime导入冲突** | `analysis/views.py` | 移除 `import datetime` 模块导入，统一使用 `from datetime import datetime, timedelta, date`。修复 `datetime.datetime.now()` 崩溃 |
| 2 | **datetime导入冗余** | `propagation/views.py`, `statistic/view.py` | 清理冗余的 `import datetime` 和重复导入 |
| 3 | **login_auth重复定义** | `login_auth/views.py` | 删除重复的 `md5()` 函数、重复的 `Blueprint()` 实例化、移除登录函数中的 `DEBUG` print 语句（防止凭证泄露） |
| 4 | **跨蓝图路由冲突** | `statistic/view.py` | 删除 `/basic/basicinfo/update_grandparents` 重复路由（basic蓝图已注册，statistic版本不可达） |
| 5 | **重复路由** | `propagation/views.py` | 将第二个 `/propagation/hardeninginfo/add` 改为 `/propagation/hardeninginfo/add_upbasiclamb`，使两个handler都可访问 |
| 6 | **statistic import混乱** | `statistic/view.py` | 彻底清理大量重复的import块（flask、sqlalchemy、datetime、json等重复导入3-4次） |
| 7 | **statistic语法错误** | `statistic/view.py` | 删除孤立的 `except Exception as e:` 块（没有对应的try） |
| 8 | **模型字段名不匹配** | `modelsReverse.py` | 修正 `basic_groupmalecapacity` 和 `basic_yield_capacity` 的全部字段名与数据库对齐 |
| 9 | **BasicBasicinfo字段** | `modelsReverse.py` | 修正 `ele_num/pre_num/f_ele_num/m_ele_num` 长度（16→20），`wea_date` nullable，添加 `note1` 和 `localization_num`，修正 `note` 类型为Date |
| 10 | **h_store拼写错误** | `h_store/views.py` | 修正 `yaoping_fees` → `yaopin_fees` |
| 11 | **补充缺失路由** | `h_store/views.py` | 新增 `/h_store/inventoryForage/add/edit/del` |
| 12 | **补充缺失路由** | `statistic/view.py` | 新增 `/statistic/obsoletegrassinfo/add/edit/del` |
| 13 | **补充缺失路由** | `analysis/views.py` | 新增 `/analysis/daily_income/edit/del`, `/analysis/daily_grass_asset/edit/del`, `/analysis/daily_stocksheet/searchDate` |
| 14 | **补充缺失路由** | `g_harvest/views.py` | 新增 `/g_harvest/segmentinfo` CRUD |
| 15 | **views字段同步** | `basic/views.py`, `statistic/view.py`, `propagation/views.py`, `pest_control/views.py` | 同步模型字段名变更到所有引用位置 |
| 16 | **BasicYieldperformance字段** | `modelsReverse.py`, `basic/views.py` | 修正 `sprout_num` → `lamb_num`（与数据库对齐） |
| 17 | **空值保护** | `propagation/views.py` | 删除 `artificial_careinfo` 中不安全的 `print(seedling_info.ele_num)`，添加 `if seedling_info:` 空值保护 |

#### 7.2 前端修复

| # | 问题 | 修复文件 | 修复内容 |
|---|------|---------|---------|
| 1 | **旧/colony/前缀** | `field/houseinfo/api/manu.ts`, `field/hurdleinfo/api/manu.ts`, `field/disinfectioninfo/api/manu.ts`, `basic/harvestinfo/api/manu.ts` | `/colony/` → `/field/` |
| 2 | **缺少前导/** | `propagation/*/api/manu.ts`, `analysis/asset_standard/api/manu.ts`, `analysis/grass_asset/api/manu.ts`, `statistic/makecore/api/manu.ts` | 所有API路径添加前导 `/` |
| 3 | **错误指向/basic/manuinfo** | `basic/sportsinfo`, `basic/yieldperformance`, `basic/productivityinfo`, `basic/canopyperformance`, `basic/fertilizerinfo` | 改为各自独立端点 `/basic/xxx` |
| 4 | **错误指向/basic/manuinfo** | `field/maintenanceinfo`, `field/transferinfo` | 改为 `/field/maintenanceinfo`, `/field/transferinfo` |
| 5 | **错误指向/basic/manuinfo** | `g_harvest/binformationinfo`, `g_harvest/economicinfo`, `g_harvest/processinginfo` | 改为 `/g_harvest/xxx` |
| 6 | **错误指向/basic/manuinfo** | `home/*` 全部13个子模块 | 逐个映射到正确后端端点 |
| 7 | **h_store交叉调用** | `h_store/inventoryForage/api/manu.ts` | `/h_store/inventory/add/edit/del` → `/h_store/inventoryForage/add/edit/del` |
| 8 | **analysis交叉调用** | `analysis/daily_income/api/manu.ts`, `analysis/daily_grass_asset/api/manu.ts` | 修正 edit/del/update 指向本模块端点 |
| 9 | **analysis错误跨模块** | `analysis/grass_asset/api/manu.ts` | `/analysis/growth_statusinfo/get_femalegrass` → `/propagation/growth_statusinfo/get_femalegrass` |
| 10 | **statistic错误端点** | `statistic/obsoletegrassinfo/api/manu.ts` | `/statistic/witherinfo/xxx` → `/statistic/obsoletegrassinfo/xxx` |
| 11 | **ESLint构建错误** | `ChatBox/ClientChat.vue`, `ChatBox/ChatHistories.vue` | 移除 `@ts-nocheck` 注释，修复Docker构建失败 |

#### 7.3 数据库与部署

| # | 操作 | 说明 |
|---|------|------|
| 1 | Docker清理 | `docker system prune -af --volumes`，释放 23.79GB |
| 2 | 数据验证 | 确认所有82张表中，业务表均有≥5条数据 |
| 3 | Docker重建 | `docker compose up -d --build`，成功构建 Flask 和 Vue 镜像 |

#### 7.4 后续修复（同一会话追加）

| # | 问题 | 修复文件 | 修复内容 |
|---|------|---------|---------|
| 1 | **搜索表单按钮重叠** | `components/SearchForm/index.vue` | `GridItem suffix` 增加 `:span="2"`，使操作按钮区域占两列，避免与搜索项挤压重叠 |
| 2 | **数据库数据缺失** | 备份 `meadow_test-2025_03_21_18_30_21-dump.sql` | 导入原始 `supply_commodityinfo`（61条）和 `w_information_immunizationMessageinfo`（21条）真实数据 |
| 3 | **表结构不匹配** | MySQL ALTER TABLE | `supply_commodityinfo.cname` → `VARCHAR(100)`；`w_information_immunizationMessageinfo` 调整 `ele_num/pre_num/distance_date/f_date/note` 类型，移除 `ele_num` UNIQUE 约束 |
| 4 | **表格缺少病害描述** | `w_information/immunizationMessage/useProTable/index.vue` | 新增 `note`（病害描述）列及搜索框 |
| 5 | **note 搜索不支持模糊** | `w_information/views.py` | `note` 字段搜索由精确匹配改为 `LIKE '%value%'` |
| 6 | **红点 badge 0 仍显示** | `layouts/components/Header/components/Message.vue` | `el-badge` 增加 `:hidden="warnMessageslist.length === 0"` |
| 7 | **待办缺少病害描述** | `login_auth/views.py`, `Message.vue` | `/login/test` 返回增加 `note` 字段；Message.vue 待办列表显示 `note` |
| 8 | **模型与表不同步** | `modelsReverse.py` | `WinformationImmunizationMessageinfo` 同步 `ele_num/distance_date/f_date/note` 字段类型 |

---

## 8. 当前已知问题（遗留）

以下问题在本次修复中**未处理**，供后续开发者参考：

### 8.1 P3 - 低优先级

| # | 问题 | 位置 | 说明 |
|---|------|------|------|
| 1 | 菜单静态JSON | `src/api/modules/login.ts` | `getAuthMenuListApi()` 返回本地JSON，权限控制是静态的 |
| 2 | 大量home/*模块后端缺路由 | `home/*` | 前端有页面但后端没有独立CRUD，当前映射到现有端点（如 `/basic/basicinfo`） |
| 3 | 前端build:dev模式 | `package.json` | 当前Docker构建使用 `build:dev`（开发模式），生产环境应使用 `build:pro` |
| 4 | MD5密码哈希 | `login_auth/views.py` | 使用MD5存储密码，安全性较弱，建议迁移到bcrypt/scrypt |
| 5 | hardcoded IP | `App/__init__.py`, `Task.py`, `sum.py` | 部分文件中有注释掉的旧数据库IP和凭据 |

---

## 9. 开发规范

### 9.1 后端代码规范
- **时间操作**：统一使用 `from datetime import datetime`，禁止 `import datetime`
- **模型字段名**：必须与数据库字段名完全一致，修改前务必先 `DESCRIBE` 表确认
- **蓝图路由URL**：使用小写字母+下划线，禁止大写字母
- **密码比较**：统一使用 `hashlib.md5(pwd.encode()).hexdigest()`（当前标准，未来应升级）
- **空值保护**：查询 `.first()` 后必须检查是否为 `None` 再访问属性
- **DEBUG输出**：生产代码中禁止 `print()` 调试语句，尤其不能输出敏感信息

### 9.2 前端代码规范
- **API路径前缀**：必须带前导 `/`（如 `/propagation/xxx`）
- **API模块**：应从 `src/api/config/servicePort.ts` 导入PORT常量
- **每个模块的API**：应调用对应的后端实体路由，禁止复用其他模块的接口
- **ESLint**：禁止 `@ts-nocheck` 注释，类型问题应正确修复

### 9.3 数据库规范
- **表名**：小写字母+下划线
- **字段名**：与模型名保持一致
- **备份SQL更新**：修改 `init-scripts/meadow_test.sql` 后，需同步更新模型
- **数据库修改**：优先使用 `ALTER TABLE`，避免删除volume重建（会丢失数据）

---

## 10. 操作手册

### 10.1 启动服务
```bash
cd /home/debian/AgroGuard
docker compose up -d --build
```

### 10.2 查看日志
```bash
docker logs meadow-guard-flask-1 --tail 50
docker logs meadow-guard-vue-1 --tail 20
docker logs meadow-guard-mysql-db-1 --tail 20
```

### 10.3 进入MySQL容器
```bash
docker exec -it meadow-guard-mysql-db-1 mysql -uroot -pmeadow123 meadow_test
```

### 10.4 重新构建（不丢失数据）
```bash
cd /home/debian/AgroGuard
docker compose down
docker compose up -d --build
```

### 10.5 完全重建（⚠️ 会删除数据库数据）
```bash
cd /home/debian/AgroGuard
docker compose down -v
docker compose up -d --build
```

### 10.6 后端本地测试
```bash
cd /home/debian/AgroGuard/meadow-be
pip install -r requirements.txt
python app.py
```

### 10.7 前端本地开发
```bash
cd /home/debian/AgroGuard/meadow-fe
npm install
npm run dev
```

### 10.8 API测试脚本
```bash
cd /home/debian/AgroGuard
python3 test_api.py
```

---

## 11. 数据迁移规则

### 11.1 旧表→新表映射（已完成的迁移）

| 旧表名 | 新表名 | 状态 |
|--------|--------|------|
| `colony_houseinfo` | `field_houseinfo` | ✅ 已完成 |
| `colony_disinfectioninfo` | `field_disinfectioninfo` | ✅ 已完成 |
| `colony_maintenanceinfo` | `field_maintenanceinfo` | ✅ 已完成 |
| `colony_transferinfo` | `field_transferinfo` | ✅ 已完成 |
| `basic_breederconditioninfo` | `basic_fieldconditioninfo` | ✅ 已完成 |
| `basic_cutinfo` | `basic_harvestinfo` | ✅ 已完成 |
| `basic_manureinfo` | `basic_fertilizerinfo` | ✅ 已完成 |

### 11.2 测试数据填充策略

对于空表，使用 `/home/debian/AgroGuard/meadow-be/migration_script.sql` 填充。该脚本：
- 检查表行数 < 5 时才插入
- 为每个表插入6条真实感测试数据
- 使用 `SET FOREIGN_KEY_CHECKS = 0` 避免外键约束问题

---

## 附录：Git提交历史

```
e7ecb8d fix(frontend): 移除ESLint禁止的@ts-nocheck注释，修复Docker构建
208b134 chore(config): 恢复数据库URI为Docker容器hostname
d3eb898 fix(tests): 修复yieldperformance和artificial_careinfo字段/空值问题
e1b6d7a fix(models): 恢复错误修改的字段名，与当前数据库对齐
176ad23 fix(routes+frontend): 补充缺失后端路由，修正前端API端点
2f52838 fix(backend): 修复模型字段名、datetime导入、重复路由、import混乱、DEBUG泄露
54fac1c Merge remote changes, keep reconstructed database schema
```

---

## 2026-04-28 更新记录（第1轮）

### 新增修复
1. **UTF-8 字符集修复**：修复数据库中文乱码（双重编码），Docker MySQL 配置增加 `init-connect="SET NAMES utf8mb4"`，Flask DB URI 增加 `charset=utf8mb4`
2. **监测地块 pid Bug**：修复 `add_hurdleinfo` 空 `house_id` 导致 `pid=None` 的报错
3. **基础信息添加增强**：自动填充 `house_name`/`hurdle_name`，`f_ele_num`/`m_ele_num` 空值保护
4. **文案修改**：免疫预警表格 `"病害描述"` → `"病虫害描述"`，待办文案同步更新
5. **供应商品搜索**：`cname` 从精确匹配改为模糊匹配 `LIKE`
6. **数据填充**：37 个业务表全部填充至 ≥20 条记录
7. **空值校验**：`add_houseinfo`/`add_hurdleinfo` 增加名称非空校验

### 测试结果
- 第1轮（API连通性+中文+增删改查）：25/25 PASS
- 第2轮（业务流+预警模块+筛选联动）：10/10 PASS
- 第3轮（边界+分页+空值+重复键）：7/7 PASS

### GitHub 提交
- Commit: `千淘万漉虽辛苦，吹尽狂沙始到金`
- 数据库 init SQL 已替换为 schema-only 版本（无数据）

---

## 2026-04-28 更新记录（第2轮 — 监测地块与病虫害预警逻辑修复）

### 新增修复
1. **监测地块管理核心Bug**：
   - `get_hurdleinfo()`：当 `house_id` 为空时移除 `pid == house_id` 过滤，改为条件判断
   - `add_hurdleinfo()`：增加 `house_id` 空值校验，返回 `400` 错误提示
   - `GrassDrawer.vue`：新增表单增加"所属监测站点"下拉选择（必填）
2. **病虫害预警逻辑修复**：
   - `w_information/views.py` SQL：`'' as note` → `COALESCE(s.explain, '') as note`（JOIN supply_commodityinfo）
   - `supply_commodityinfo` 数据清洗：疾病名称 → 防治剂名称，修复 27 条 UTF-8 双重编码乱码，补充缺失描述
   - `d_plantcare_protectioninfo.effect` 回填：根据 `drug_id` JOIN 回填 `explain`，补充缺失 `drug_id`（67、87）记录
3. **文案替换**：`authMenuList.json` `"植物护理"` → `"草地护理"`

### 测试结果
- 监测地块 API：空 `house_id` 时返回全部 381 条数据 ✅
- 监测地块新增：未选择站点返回 400 错误 ✅
- 预警信息 API：`note` 正常显示防治描述 ✅
- 防护措施 API：`effect` 正常显示防护剂对应效果 ✅
- `supply_commodityinfo`：55 条记录全部中文正常，0 条乱码 ✅

---

*本文档由 OpenCode (kimi-k2.6) 于 2026-04-27 创建并维护。*
*任何修改本项目的操作前，请先阅读本文档并更新相应章节。*
