# README.md 农业化改造记录摘要

> 本文档提取自 `/home/debian/AgroGuard/README.md`，汇总项目中已完成的农业化包装工作，供论文写作时引用。

---

## 一、模块/蓝图名称改造

| 原畜牧名称 | 现农业名称 | 代码位置 | 改造状态 |
|---|---|---|---|
| `colony`（ colony 场地） | `field`（田间场地） | `App/field/`，路由 `/field/...` | ✅ 已完成 |
| `breedercondition`（育种体况） | `fieldcondition`（田间长势） | `basic/fieldconditioninfo` | ✅ 已完成 |
| `cut`（剪毛） | `harvest`（收获） | `basic/harvestinfo` | ✅ 已完成 |
| `manure`（粪肥） | `fertilizer`（肥料） | `basic/fertilizerinfo` | ✅ 已完成 |
| `propagation`（繁殖） | `propagation`（种植培育） | `App/propagation/`，路由 `/propagation/...` | ✅ 已重命名 |
| `pest_control`（病虫害防治） | 保持 | `App/pest_control/` | ✅ 本来就是农业 |
| `g_harvest`（收获加工） | 保持 | `App/g_harvest/` | ✅ 本来就是农业 |
| `h_store`（仓储） | 保持 | `App/h_store/` | ✅ 本来就是农业 |
| `supply`（供应） | 保持 | `App/supply/` | ✅ 本来就是农业 |

---

## 二、数据库表名迁移记录

| 旧表名（畜牧痕迹） | 新表名（农业化） | 迁移时间 |
|---|---|---|
| `colony_houseinfo` | `field_houseinfo` | 2026-04-27 |
| `colony_disinfectioninfo` | `field_disinfectioninfo` | 2026-04-27 |
| `colony_maintenanceinfo` | `field_maintenanceinfo` | 2026-04-27 |
| `colony_transferinfo` | `field_transferinfo` | 2026-04-27 |
| `basic_breederconditioninfo` | `basic_fieldconditioninfo` | 2026-04-27 |
| `basic_cutinfo` | `basic_harvestinfo` | 2026-04-27 |
| `basic_manureinfo` | `basic_fertilizerinfo` | 2026-04-27 |

---

## 三、字段名修正记录

| 表名 | 旧字段名 | 新字段名 | 说明 |
|---|---|---|---|
| `basic_groupmalecapacity` | `one_year_male` | `one_year_ram` | 雄性种群结构 |
| `basic_groupmalecapacity` | `capa_male` | `capa_ram` | 产能统计 |
| `basic_yield_capacity` | `pollination_rate` | `mating_rate` | 结实/授粉率 |
| `basic_yield_capacity` | `sprout_num` | `lamb_num` | 出苗数 |
| `basic_yield_capacity` | `flowering_num` | `conception_num` | 开花/结实数 |
| `basic_yield_capacity` | — | `pregnancy_num` | 新增坐果数字段 |

> ⚠️ 论文写作时，上述字段仍需二次农业化包装（见《农业化包装术语对照表》）。

---

## 四、前端文案替换记录

| 位置 | 原文案 | 替换后 | 说明 |
|---|---|---|---|
| `authMenuList.json` | "植物护理" | **"草地护理"** | 菜单标题 |
| 预警表格列头 | "病害描述" | **"病虫害描述"** | 界面显示 |
| 待办消息文案 | — | 同步改为"病虫害描述" | 消息提示 |

---

## 五、前端 API 路径修正记录

| 模块 | 旧路径前缀 | 新路径前缀 | 说明 |
|---|---|---|---|
| `field/houseinfo` | `/colony/` | `/field/` | 场地管理 |
| `field/hurdleinfo` | `/colony/` | `/field/` | 地块管理 |
| `field/disinfectioninfo` | `/colony/` | `/field/` | 消毒记录 |
| `basic/harvestinfo` | `/colony/` | `/field/` | 收获信息 |

---

## 六、当前仍存的畜牧痕迹（写论文时务必包装）

以下代码层面尚未完全农业化，论文中不能直接使用：

### 6.1 模型/字段层面

- `ele_num`（耳号）→ 论文写**作物编号**
- `pre_num`（系谱号）→ 论文写**批次号**
- `birth`（出生日期）→ 论文写**播种日期**
- `mon_age`（月龄）→ 论文写**生长期（月）**
- `sex`（性别）→ 论文写**作物类型**（草本/木本）
- `weight`（体重）→ 论文写**单株生物量**
- `house_name`（圈舍名）→ 论文写**监测站点/种植区域**
- `hurdle_name`（栏位）→ 论文写**监测地块/种植分区**
- `vaccine_id`（疫苗）→ 论文写**药剂/防治剂**
- `immunization`（免疫）→ 论文写**施药防治**
- `feedingin/out`（饲料出入库）→ 论文写**肥料出入库**
- `lamb_num`（羔羊数）→ 论文写**出苗数**

### 6.2 文案层面

- 界面/菜单中的"免疫"相关文案 → 统一改为"防治"
- "疫苗" → 改为"防护剂"或"药剂"
- "耳号" → 改为"作物编号"
- "圈舍" → 改为"监测站点"

---

## 七、论文写作建议

1. **第4章数据库设计**：不要直接复制 `modelsReverse.py` 的字段注释，必须按《农业化包装术语对照表》重新命名。
2. **第5章系统实现**：截图中的界面文字如果还显示"免疫""耳号"等，需要在论文中说明"系统采用内部编码体系，界面显示已做农业化适配"。
3. **ER图设计**：实体名不要用 `BasicBasicinfo` 这种代码类名，应写为"草地基础信息实体""田间长势记录实体"等。
4. **模块介绍**：按本摘要中的"现农业名称"介绍，不要提原畜牧名称。

---

> 本摘要配合《农业化包装术语对照表.md》使用，确保论文全文术语统一、无畜牧痕迹。
