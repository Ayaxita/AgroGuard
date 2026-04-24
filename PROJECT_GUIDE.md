# AgroGuard 项目全解指南

> 本文档涵盖项目每一层代码、每一个参数、每一条函数调用链，满足完全掌握的要求。

---

## 1. 项目总览

| 项目 | 说明 |
|------|------|
| 名称 | 草地作物病虫害智能监测系统（AgroGuard） |
| 原名 | 牧场病虫害管理系统 |
| 定位 | 基于 Web 技术的前后端分离信息管理系统 |
| 部署方式 | Docker Compose 三容器编排 |

### 技术栈精确版本

| 层 | 技术 | 版本 |
|----|------|------|
| 后端框架 | Flask | 3.0.3 |
| ORM | SQLAlchemy | 2.0.34 |
| 数据库 | MySQL | 5.7 |
| 数据库驱动 | PyMySQL | 1.1.1 |
| 认证 | Flask-JWT-Extended | 4.6.0 |
| 跨域 | Flask-CORS | 4.0.1 |
| 数据迁移 | Flask-Migrate (Alembic) | 4.0.7 |
| 数据处理 | Pandas | 2.2.2 |
| Excel | openpyxl | 3.1.5 |
| DOCX | python-docx / docxtpl | 1.1.2 / 0.19.1 |
| AI | 智谱AI SDK (zhipuai) | 2.1.5 |
| Python | CPython | 3.9.21 (Alpine) |
| 前端框架 | Vue | 3.4.31 |
| UI 组件库 | Element Plus | 2.9.8 |
| 状态管理 | Pinia | 2.1.7 |
| 路由 | Vue Router | 4.4.0 |
| 构建 | Vite | 5.3.2 |
| 图表 | ECharts | 5.5.1 |
| CSS | Tailwind CSS | 3.4.14 + SCSS |
| HTTP 客户端 | Axios | 1.7.2 |
| Node.js | Node | 23.6.0 (Alpine) |
| Web 服务器 | Nginx | 1.27.3 (Alpine) + Brotli |

### 整体架构

```
┌─────────────────────────────────────────────────────┐
│                    用户浏览器                        │
│              http://localhost:5020                   │
└────────────────────┬────────────────────────────────┘
                     │ HTTP(S)
                     ▼
┌─────────────────────────────────────────────────────┐
│              Nginx (vue 容器 :80)                    │
│  ┌─────────────────────────────────────────────┐    │
│  │  静态资源: Vue3 SPA (build 产物)             │    │
│  └─────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────┐    │
│  │  /api/* → proxy_pass http://flask:5000/      │    │
│  └─────────────────────────────────────────────┘    │
└────────────────────┬────────────────────────────────┘
                     │ /api/ 请求转发
                     ▼
┌─────────────────────────────────────────────────────┐
│              Flask (flask 容器 :5000)                │
│  ┌─────────────────────────────────────────────┐    │
│  │  JWT before_request 拦截器                    │    │
│  │  ↓ 白名单放行 /login /register /logout /refresh│    │
│  │  ↓ 其他请求验证 JWT                           │    │
│  └─────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────┐    │
│  │  11 个 Blueprint 路由分发                     │    │
│  └─────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────┐    │
│  │  SQLAlchemy ORM → PyMySQL                   │    │
│  └─────────────────────────────────────────────┘    │
└────────────────────┬────────────────────────────────┘
                     │ TCP/IP (mysql-db:3306)
                     ▼
┌─────────────────────────────────────────────────────┐
│              MySQL 5.7 (mysql-db 容器 :3306)        │
│  数据库: sheep_test                                 │
│  数据卷: mysql-data                                  │
│  初始化: /docker-entrypoint-initdb.d/*.sql          │
└─────────────────────────────────────────────────────┘
```

---

## 2. 目录结构

```
AgroGuard/
├── docker-compose.yml                  # Docker Compose 编排文件
├── init-scripts/
│   └── sheep_test-2025_03_21_18_30_21-dump.sql  # MySQL 初始化数据
├── meadow-be/                          # 后端项目
│   ├── Dockerfile                      # Python 3.9 Alpine 容器
│   ├── requirements.txt                # 58 个 Python 依赖
│   ├── app.py                          # 应用入口 + before_request 拦截器
│   ├── App/
│   │   ├── __init__.py                 # create_app() 工厂函数，注册 11 个蓝图
│   │   ├── exts.py                     # SQLAlchemy + Migrate + CORS 初始化
│   │   ├── models.py                   # 旧模型（未使用）
│   │   ├── modelsReverse.py            # 主模型文件（50+ 模型，2896 行）
│   │   ├── task.py                     # 定时任务（已注释）
│   │   ├── utils/
│   │   │   └── AlchemyEncoder.py       # SQLAlchemy 模型 JSON 序列化编码器
│   │   ├── login_auth/
│   │   │   ├── models.py               # Testuser 模型
│   │   │   └── views.py                # 登录/注册/登出/刷新/修改密码
│   │   ├── basic/
│   │   │   └── views.py                # 田块基本信息 CRUD + 导入导出 (2067 行)
│   │   ├── colony/
│   │   │   └── views.py                # 草地分区管理 (777 行)
│   │   ├── supply/
│   │   │   └── views.py                # 供应商管理 (527 行)
│   │   ├── h_store/
│   │   │   └── views.py                # 物资仓库管理 (1297 行)
│   │   ├── g_slaughter/
│   │   │   └── views.py                # 损失评估 (283 行)
│   │   ├── d_health/
│   │   │   └── views.py                # 病虫害管理 (约1400 行)
│   │   ├── e_breed/
│   │   │   └── views.py                # 生长监测管理 (3615 行)
│   │   ├── analysis/
│   │   │   └── views.py                # 数据分析 (3145 行)
│   │   ├── statistic/
│   │   │   └── view.py                 # 统计报表 (3013 行)
│   │   ├── w_information/
│   │   │   └── views.py                # 预警信息 (356 行)
│   │   └── chatbox/
│   │       └── views.py                # AI 问答 (78 行)
│   └── migrations/                     # Alembic 数据库迁移
├── meadow-fe/                          # 前端项目
│   ├── Dockerfile                      # 多阶段构建 (Node → Nginx+Brotli)
│   ├── package.json                    # 前端依赖定义
│   ├── vite.config.ts                  # Vite 构建配置
│   ├── .env                            # VITE_GLOB_APP_TITLE=草地病虫害监测系统
│   ├── .env.development                # VITE_API_URL=/api, hash 路由
│   ├── .env.production                 # 生产环境 API（需配置）
│   ├── tailwind.config.js              # Tailwind CSS 配置
│   ├── tsconfig.json                   # TypeScript 配置
│   ├── .eslintrc.cjs                   # ESLint 配置
│   ├── .prettierrc.cjs                 # Prettier 配置
│   ├── .stylelintrc.cjs                # Stylelint 配置
│   ├── commitlint.config.cjs           # Git 提交规范
│   ├── husky/                          # Git hooks
│   └── src/
│       ├── main.ts                     # 应用入口
│       ├── App.vue                     # 根组件
│       ├── config/index.ts             # 全局配置
│       ├── routers/
│       │   ├── index.ts                # 路由实例 + beforeEach 守卫
│       │   └── modules/
│       │       ├── staticRouter.ts     # 静态路由（登录/布局/详情/测试）
│       │       └── dynamicRouter.ts    # 动态路由（从 authMenuList.json 加载）
│       ├── api/
│       │   ├── index.ts               # Axios 封装（拦截器/刷新/token）
│       │   ├── config/servicePort.ts  # API 路径前缀常量
│       │   └── modules/
│       │       ├── login.ts            # 登录/菜单/按钮权限 API
│       │       ├── user.ts             # 用户 API
│       │       └── upload.ts           # 文件上传 API
│       ├── stores/
│       │   ├── index.ts               # Pinia 实例 + 持久化
│       │   └── modules/
│       │       ├── auth.ts             # 权限 Store
│       │       ├── user.ts             # 用户 Store（token/refresh_token/userInfo）
│       │       ├── global.ts           # 全局 UI Store
│       │       ├── tabs.ts             # 标签页 Store
│       │       ├── keepAlive.ts        # 缓存 Store
│       │       └── apiStore.ts         # API 调用状态 Store
│       ├── views/                      # 15 个功能模块（详见第 5 节）
│       ├── components/                 # 通用组件库（详见第 6 节）
│       ├── layouts/                    # 4 种布局模式
│       ├── languages/                  # i18n 国际化
│       ├── directives/                 # 自定义指令
│       ├── utils/                      # 工具函数
│       ├── enums/                      # 枚举定义
│       ├── styles/                     # 全局样式
│       └── assets/                     # 静态资源（图标/字体/图片）
└── README.md
```

---

## 3. Docker 部署详解

### docker-compose.yml 逐行解析

```yaml
name: agroguard                    # Compose 项目名

services:
  flask:                           # 后端服务
    hostname: flask                # 容器主机名（内部 DNS 解析为 flask）
    depends_on:
      - mysql-db                   # 依赖 mysql-db 先启动
    build: ./meadow-be             # 从 meadow-be/Dockerfile 构建
    ports:
      - "5000:5000"                # 宿主机 5000 → 容器 5000
    command: python app.py         # 启动命令

  mysql-db:                        # 数据库服务
    hostname: mysql-db             # 容器主机名（内部 DNS 解析为 mysql-db）
    image: m.daocloud.io/docker.io/library/mysql:5.7  # MySQL 5.7 镜像（DaoCloud 镜像加速）
    environment:
      MYSQL_ROOT_PASSWORD: sheep123    # root 密码
      MYSQL_DATABASE: sheep_test       # 初始化创建的数据库
    ports:
      - "5010:3306"                # 宿主机 5010 → 容器 3306
    volumes:
      - mysql-data:/var/lib/mysql     # 持久化数据卷
      - ./init-scripts:/docker-entrypoint-initdb.d:Z  # 初始化 SQL 脚本

  vue:                             # 前端服务
    hostname: vue
    depends_on:
      - flask                      # 依赖 flask 先启动
    build: ./meadow-fe             # 从 meadow-fe/Dockerfile 构建
    ports:
      - "5020:80"                  # 宿主机 5020 → 容器 80

volumes:
  mysql-data:                      # 命名数据卷
```

### 端口映射总结

| 服务 | 容器端口 | 宿主机端口 | 说明 |
|------|---------|-----------|------|
| Flask | 5000 | 5000 | 后端 API |
| MySQL | 3306 | 5010 | 数据库 |
| Nginx/Vue | 80 | 5020 | 前端页面 |

### meadow-be/Dockerfile

```dockerfile
FROM python:3.9.21-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

### meadow-fe/Dockerfile（多阶段构建）

```
阶段1: node:23.6.0-alpine  →  pnpm install + pnpm build:dev
阶段2: 构建 Nginx + Brotli 压缩模块
阶段3: nginx:1.27.3-alpine  →  复制构建产物 + Nginx 配置
```

Nginx 配置关键：`/api/` 路径代理到 `http://flask:5000/`，其余路径返回 Vue SPA 静态文件。

### 常用 Docker 命令

```bash
# 启动全部服务
docker compose up -d

# 重建并启动单个服务
docker compose build flask && docker compose up -d flask

# 查看容器日志
docker compose logs -f flask

# 进入 Flask 容器调试
docker compose exec flask sh

# 进入 MySQL 容器
docker compose exec mysql-db mysql -uroot -psheep123 sheep_test
```

---

## 4. 后端架构详解

### 4.1 应用入口 — app.py

```python
from App import create_app
app = create_app()

# 全局拦截器：JWT 认证 + 请求预处理
@app.before_request
def before_request():
    path = request.path
    url = request.url
    suffix = url.endswith('.png') or url.endswith('.jpg') or url.endswith('.css') or url.endswith('.js')
    method = request.method
    # 白名单路径：不需要 JWT 验证
    passUrl = ['/login', '/register', '/logout', '/refresh',
               '/basic/basicinfo/import_template',
               '/basic/basicinfo/detail',
               '/login/test',
               '/w_information/immunizationMessage/index']
    if method != 'OPTIONS':
        if path not in passUrl and not suffix:
            verify_jwt_in_request()          # 强制验证 JWT
            username = get_jwt_identity()    # 从 token 提取用户名
    # POST 请求 JSON 数据去除字符串两端空格
    if request.method == 'POST' and request.content_type == 'application/json':
        data = request.get_json()
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str):
                    data[key] = value.strip()
            request._json = data             # 更新请求数据

# JWT Token 刷新端点
@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)                 # 需要 refresh_token
def refresh():
    identity = get_jwt_identity()
    accesstoken = create_access_token(identity=identity)
    return jsonify({"code": 200, "data": accesstoken, "msg": "刷新成功"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

**执行流程：**
1. `create_app()` 初始化 Flask 应用、数据库、JWT、CORS、蓝图
2. `before_request` 拦截所有请求，白名单路径跳过验证，其余验证 JWT
3. POST JSON 请求自动 `.strip()` 所有字符串值
4. `/refresh` 端点使用 refresh_token 换取新 access_token

### 4.2 应用工厂 — App/__init__.py

```python
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'nihaoshijie'
    app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=30)

    # 注册 11 个蓝图
    app.register_blueprint(login_auth)      # /login, /register, /logout, /refresh
    app.register_blueprint(basic)           # /basic/*
    app.register_blueprint(colony)          # /colony/*
    app.register_blueprint(supply)          # /supply/*
    app.register_blueprint(h_store)         # /h_store/*
    app.register_blueprint(g_slaughter)     # /g_slaughter/*
    app.register_blueprint(d_health)        # /d_health/*
    app.register_blueprint(e_breed)         # /e_breed/*
    app.register_blueprint(w_information)   # /w_information/*
    app.register_blueprint(Statistic)       # /statistic/*
    app.register_blueprint(analysis)         # /analysis/*
    app.register_blueprint(chatbox)          # /chatbox/*

    # 数据库配置
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:sheep123@mysql-db:3306/sheep_test'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # JWT 配置
    app.config['JWT_SECRET_KEY'] = 'nihaoshijie'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=15)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(days=30)
    JWTManager(app)

    # 初始化插件
    init_exts(app)  # db.init_app(app) + migrate.init_app(app, db) + CORS(app)
    return app
```

**关键配置参数：**

| 参数 | 值 | 说明 |
|------|---|------|
| SECRET_KEY | `nihaoshijie` | Flask 密钥 + JWT 签名密钥 |
| JWT_ACCESS_TOKEN_EXPIRES | 15 分钟 | 短期 token 过期时间 |
| JWT_REFRESH_TOKEN_EXPIRES | 30 天 | 长期 token 过期时间 |
| SQLALCHEMY_DATABASE_URI | `mysql+pymysql://root:sheep123@mysql-db:3306/sheep_test` | 数据库连接串 |
| SQLALCHEMY_TRACK_MODIFICATIONS | False | 关闭 SQLAlchemy 事件通知 |

### 4.3 插件初始化 — App/exts.py

```python
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()          # ORM 实例（全局变量，被所有模块引用）
migrate = Migrate()        # 数据迁移实例

def init_exts(app):
    db.init_app(app=app)                    # 将 ORM 绑定到 Flask app
    migrate.init_app(app=app, db=db)        # 将迁移绑定到 app 和 db
    CORS(app, supports_credentials=True)     # 允许跨域携带凭证
```

**`db` 对象的使用模式：**
- 所有模型文件 `from App.exts import db` 引入
- 查询：`Model.query.filter_by(xxx=yyy).all()`
- 新增：`db.session.add(obj)` → `db.session.commit()`
- 删除：`db.session.delete(obj)` → `db.session.commit()`
- 回滚：`db.session.rollback()` → `db.session.flush()`

### 4.4 JSON 序列化 — AlchemyEncoder

```python
class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                if field in ("query", "query_class", "registry"):
                    continue
                if isinstance(data, datetime):
                    data = data.strftime("%Y-%m-%d %H:%M:%S")  # datetime → 字符串
                if isinstance(data, decimal.Decimal):
                    data = "{:.2f}".format(data)                  # Decimal → 2 位小数
                try:
                    json.dumps(data)                              # 验证可序列化
                    fields[field] = data
                except TypeError:
                    fields[field] = str(data)                     # 不可序列化的转字符串
            return fields
```

**使用方式：**
```python
data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
data = json.loads(data)
list.append(data)
```

**序列化链路：** SQLAlchemy Model 实例 → `json.dumps(cls=AlchemyEncoder)` → Python dict → 加入响应结果集

### 4.5 蓝图路由完整列表

#### login_auth（登录认证）

| 路由 | 方法 | 函数 | 说明 |
|------|------|------|------|
| `/login` | POST | `login()` | 登录验证，返回 access_token + refresh_token |
| `/register` | POST | `register()` | 用户注册 |
| `/logout` | GET/POST | `logout()` | 登出（前端清除 token） |
| `/refresh` | POST | `refresh()` | 用 refresh_token 换取新 access_token |
| `/login/test` | POST | `test()` | 返回预警信息按 vaccine_id 分组统计 |
| `/user/reset_password` | POST | `reset_password()` | 修改密码 |

**登录流程调用链：**
```
前端 loginApi({username, password})
  → POST /login
    → request.get_json() 获取 {username, password}
    → Testuser.query.filter_by(username=name).first()
    → 比较 pwd == user.password（明文比较）
    → create_access_token(identity=name) 生成 access_token
    → create_refresh_token(identity=name) 生成 refresh_token
    → user.last_login = datetime.now()
    → db.session.commit()
    → 返回 {code: 200, data: {access_token, refresh_token}, msg: "登录成功"}
```

#### basic（田块/作物基本信息）

| 路由 | 方法 | 说明 |
|------|------|------|
| `/basic/basicinfo` | POST | 分页查询田块信息列表 |
| `/basic/basicinfo/add` | POST | 新增田块信息 |
| `/basic/basicinfo/edit` | POST | 编辑田块信息 |
| `/basic/basicinfo/obsolete` | POST | 淘汰（标记为已淘汰） |
| `/basic/basicinfo/detail` | POST | 查看田块详情 |
| `/basic/basicinfo/validateSheepNum` | POST | 验证编号唯一性 |
| `/basic/basicinfo/familyTree` | POST | 查询系谱（家系树） |
| `/basic/basicinfo/export` | POST | 导出 Excel |
| `/basic/basicinfo/import` | POST | 导入 Excel |
| `/basic/basicinfo/import_template` | GET | 下载导入模板 |
| `/basic/basicinfo/updateMonAge` | POST | 批量更新月龄 |
| `/basic/basicinfo/updateHouseAndHurdle` | POST | 更新区域栏位 |
| `/basic/basicinfo/markSheepDeath` | POST | 标记死亡 |
| `/basic/basicinfo/markSheepSale` | POST | 标记出售 |
| `/basic/basicinfo/addImmunization` | POST | 新增防疫记录 |
| `/basic/basicinfo/file/upload/img` | GET | 上传图片 |
| `/basic/basicinfo/file/download/img` | GET | 下载图片 |
| `/basic/manuinfo` | POST | 产地信息列表 |
| `/basic/manuinfo/add` | POST | 新增产地 |
| `/basic/manuinfo/edit` | POST | 编辑产地 |

**列表查询通用模式（所有 POST 列表接口）：**
```python
pageNum = int(request.json.get('pageNum'))      # 当前页码
pageSize = int(request.json.get('pageSize'))    # 每页条数
conditions = []
# 动态构建过滤条件
search_params = {'field1': Model.field1, 'field2': Model.field2, ...}
for param, column in search_params.items():
    value = request.json.get(param)
    if value is not None:
        conditions.append(column == value)
# 组合过滤
if conditions:
    query = Model.query.filter(and_(*conditions))
else:
    query = Model.query
# 过滤已淘汰/死亡
query = query.filter(Model.belong == 0)
# 分页
infos = query.order_by(desc(Model.id)).paginate(page=pageNum, per_page=pageSize, error_out=False)
# 序列化
list = []
for info in infos:
    data = json.dumps(info, cls=AlchemyEncoder, ensure_ascii=False)
    data = json.loads(data)
    list.append(data)
result = {"code": 200, "data": {"list": list, "pageNum": pageNum, "pageSize": pageSize, "total": total}, "msg": "成功"}
```

**导出流程通用模式（所有 export 接口）：**
```python
# Excel 导出流程
selected_ids = request.json.get('selected_ids')     # 选中导出的 ID 列表
if selected_ids:
    query = Model.query.filter(Model.id.in_(selected_ids))
else:
    # 无选中时导出全部（或当前筛选条件下的全部）
    query = Model.query.filter(Model.belong == 0)

infos = query.outerjoin(RelatedModel, ...).all()    # outerjoin 关联表
df = pd.DataFrame([{...} for info in infos])        # 构建 DataFrame
output = BytesIO()
df.to_excel(output, index=False)                     # 写入 Excel
output.seek(0)
return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                 as_attachment=True, download_name='xxx.xlsx')
```

#### e_breed（生长监测）

| 路由 | 方法 | 说明 |
|------|------|------|
| `/e_breed/rutinfo` | POST | 生长监测信息列表 |
| `/e_breed/rutinfo/add` | POST | 新增 |
| `/e_breed/rutinfo/edit` | POST | 编辑 |
| `/e_breed/rutinfo/export` | POST | 导出 Excel |
| `/e_breed/rutinfo/detail` | POST | 详情 |
| `/e_breed/breedinginfo` | POST | 繁殖记录列表 |
| `/e_breed/breedinginfo/add` | POST | 新增 |
| `/e_breed/breedinginfo/edit` | POST | 编辑 |
| `/e_breed/breedinginfo/export` | POST | 导出 |
| `/e_breed/pregnantinfo` | POST | 怀孕监测列表 |
| `/e_breed/pregnantinfo/add` | POST | 新增 |
| `/e_breed/pregnantinfo/edit` | POST | 编辑 |
| `/e_breed/pregnantinfo/export` | POST | 导出 |
| `/e_breed/lambinfo` | POST | 新生记录列表 |
| `/e_breed/lambinfo/add` | POST | 新增 |
| `/e_breed/lambinfo/edit` | POST | 编辑 |
| `/e_breed/lambinfo/export` | POST | 导出 |
| `/e_breed/weaninginfo` | POST | 断奶记录列表 |
| `/e_breed/weaninginfo/add` | POST | 新增 |
| `/e_breed/weaninginfo/edit` | POST | 编辑 |
| `/e_breed/weaninginfo/export` | POST | 导出 |
| `/e_breed/postnatalinfo` | POST | 产后记录列表 |
| `/e_breed/postnatalinfo/add` | POST | 新增 |
| `/e_breed/postnatalinfo/edit` | POST | 编辑 |
| `/e_breed/postnatalinfo/export` | POST | 导出 |
| `/e_breed/artificialfeedinginfo` | POST | 人工喂养列表 |
| `/e_breed/artificialfeedinginfo/add` | POST | 新增 |
| `/e_breed/artificialfeedinginfo/edit` | POST | 编辑 |
| `/e_breed/artificialfeedinginfo/export` | POST | 导出 |
| `/e_breed/semencollectinfo` | POST | 采集记录列表 |
| `/e_breed/semencollectinfo/add` | POST | 新增 |
| `/e_breed/semencollectinfo/edit` | POST | 编辑 |
| `/e_breed/semencollectinfo/export` | POST | 导出 |

**数据同步机制：** e_breed 模块的 `add` 和 `edit` 操作在写入当前表后，会同步更新 `basic_basicinfo` 表的关联字段（如 `mon_age`、`house_name`、`hurdle_name`、`state` 等）。

#### d_health（病虫害管理）

| 路由 | 方法 | 说明 |
|------|------|------|
| `/d_health/immunizationinfo` | POST | 免疫记录列表 |
| `/d_health/immunizationinfo/add` | POST | 新增 |
| `/d_health/immunizationinfo/edit` | POST | 编辑 |
| `/d_health/immunizationinfo/export` | POST | 导出 |
| `/d_health/drugbathinfo` | POST | 药浴记录列表 |
| `/d_health/drugbathinfo/add` | POST | 新增 |
| `/d_health/drugbathinfo/edit` | POST | 编辑 |
| `/d_health/drugbathinfo/export` | POST | 导出 |
| `/d_health/quarantineinfo` | POST | 检疫记录列表 |
| `/d_health/quarantineinfo/add` | POST | 新增 |
| `/d_health/quarantineinfo/edit` | POST | 编辑 |
| `/d_health/quarantineinfo/export` | POST | 导出 |
| `/d_health/nursinginfo` | POST | 护理记录列表 |
| `/d_health/nursinginfo/add` | POST | 新增 |
| `/d_health/nursinginfo/edit` | POST | 编辑 |
| `/d_health/nursinginfo/export` | POST | 导出 |
| `/d_health/diseaseinfo` | POST | 疾病记录列表 |
| `/d_health/diseaseinfo/add` | POST | 新增 |
| `/d_health/diseaseinfo/edit` | POST | 编辑 |
| `/d_health/diseaseinfo/export` | POST | 导出 |
| `/d_health/abortioninfo` | POST | 流产记录列表 |
| `/d_health/abortioninfo/add` | POST | 新增 |
| `/d_health/abortioninfo/edit` | POST | 编辑 |
| `/d_health/abortioninfo/export` | POST | 导出 |

#### colony（草地分区管理）

| 路由 | 方法 | 说明 |
|------|------|------|
| `/colony/houseinfo` | POST | 区域列表 |
| `/colony/houseinfo/add` | POST | 新增区域 |
| `/colony/houseinfo/edit` | POST | 编辑区域 |
| `/colony/houseinfo/del` | POST | 删除区域 |
| `/colony/houseinfo/updateHouseNumber` | POST | 更新区域编号 |
| `/colony/hurdleinfo` | POST | 栏位列表 |
| `/colony/hurdleinfo/add` | POST | 新增栏位 |
| `/colony/hurdleinfo/edit` | POST | 编辑栏位 |
| `/colony/hurdleinfo/del` | POST | 删除栏位 |
| `/colony/hurdleinfo/set` | POST | 合并栏位 |
| `/colony/hurdleinfo/unseal` | POST | 拆分栏位 |
| `/colony/hurdleinfo/updateHurdleNumber` | POST | 更新栏位编号 |
| `/colony/disinfectioninfo` | POST | 消毒记录列表 |
| `/colony/disinfectHurdle` | POST | 消毒操作 |

#### supply（供应商管理）

| 路由 | 方法 | 说明 |
|------|------|------|
| `/supply/v_suppliersinfo` | POST | 疫苗供应商列表 |
| `/supply/v_suppliersinfo/add` | POST | 新增 |
| `/supply/v_suppliersinfo/edit` | POST | 编辑 |
| `/supply/v_suppliersinfo/del` | POST | 删除 |
| `/supply/f_suppliersinfo` | POST | 饲料供应商列表 |
| `/supply/f_suppliersinfo/add` | POST | 新增 |
| `/supply/f_suppliersinfo/edit` | POST | 编辑 |
| `/supply/f_suppliersinfo/del` | POST | 删除 |
| `/supply/commodityinfo` | POST | 商品目录列表 |
| `/supply/commodityinfo/add` | POST | 新增 |
| `/supply/commodityinfo/edit` | POST | 编辑 |
| `/supply/commodityinfo/del` | POST | 删除 |
| `/supply/insuranceinfo` | POST | 保险记录列表 |
| `/supply/insuranceinfo/add` | POST | 新增 |
| `/supply/insuranceinfo/edit` | POST | 编辑 |
| `/supply/insuranceinfo/del` | POST | 删除 |

#### h_store（物资管理）

| 路由 | 方法 | 说明 |
|------|------|------|
| `/h_store/feedingin` | POST | 饲料入库列表 |
| `/h_store/feedingin/add` | POST | 新增入库 |
| `/h_store/feedingin/edit` | POST | 编辑 |
| `/h_store/feedingin/del` | POST | 删除 |
| `/h_store/feeding_out` | POST | 饲料出库列表 |
| `/h_store/feeding_out/add` | POST | 新增出库 |
| `/h_store/feeding_out/edit` | POST | 编辑 |
| `/h_store/feeding_out/del` | POST | 删除 |
| `/h_store/vaccine_in` | POST | 疫苗入库列表 |
| `/h_store/vaccine_in/add` | POST | 新增入库 |
| `/h_store/vaccine_in/edit` | POST | 编辑 |
| `/h_store/vaccine_in/del` | POST | 删除 |
| `/h_store/vaccine_out` | POST | 疫苗出库列表 |
| `/h_store/vaccine_out/add` | POST | 新增出库 |
| `/h_store/vaccine_out/edit` | POST | 编辑 |
| `/h_store/vaccine_out/del` | POST | 删除 |
| `/h_store/inventoryDrug` | POST | 药品库存列表 |
| `/h_store/inventoryForage` | POST | 饲料库存列表 |
| `/h_store/generate_outbound_no` | POST | 生成出库单号 |

#### g_slaughter（损失评估）

| 路由 | 方法 | 说明 |
|------|------|------|
| `/g_slaughter/s_salesinfo` | POST | 单笔销售列表 |
| `/g_slaughter/s_salesinfo/add` | POST | 新增 |
| `/g_slaughter/s_salesinfo/edit` | POST | 编辑 |
| `/g_slaughter/s_salesinfo/del` | POST | 删除 |
| `/g_slaughter/g_salesinfo` | POST | 批量销售列表 |
| `/g_slaughter/g_salesinfo/add` | POST | 新增 |
| `/g_slaughter/g_salesinfo/edit` | POST | 编辑 |
| `/g_slaughter/g_salesinfo/del` | POST | 删除 |
| `/g_slaughter/binformationinfo` | POST | 体测信息列表 |
| `/g_slaughter/binformationinfo/add` | POST | 新增 |
| `/g_slaughter/binformationinfo/edit` | POST | 编辑 |
| `/g_slaughter/binformationinfo/del` | POST | 删除 |
| `/g_slaughter/slaughtersegmentinfo` | POST | 分割信息列表 |
| `/g_slaughter/slaughtersegmentinfo/add` | POST | 新增 |
| `/g_slaughter/slaughtersegmentinfo/edit` | POST | 编辑 |
| `/g_slaughter/slaughtersegmentinfo/del` | POST | 删除 |
| `/g_slaughter/economicinfo` | POST | 经济信息列表 |
| `/g_slaughter/economicinfo/add` | POST | 新增 |
| `/g_slaughter/economicinfo/edit` | POST | 编辑 |
| `/g_slaughter/economicinfo/del` | POST | 删除 |

#### analysis（数据分析）

| 路由 | 方法 | 说明 |
|------|------|------|
| `/analysis/standardinfo` | POST | 资产评价标准列表 |
| `/analysis/standardinfo/add` | POST | 新增 |
| `/analysis/standardinfo/edit` | POST | 编辑 |
| `/analysis/standardinfo/del` | POST | 删除 |
| `/analysis/sheep_asset` | POST | 资产信息列表 |
| `/analysis/sheep_asset/add` | POST | 新增 |
| `/analysis/daily_income` | POST | 日收入列表 |
| `/analysis/daily_income/export` | POST | 导出 |
| `/analysis/daily_sheep_asset` | POST | 日资产列表 |
| `/analysis/daily_sheep_asset/export` | POST | 导出 |
| `/analysis/stock_asset` | POST | 库存资产列表 |
| `/analysis/daily_report` | POST | 日报列表 |
| `/analysis/daily_report/export` | POST | 导出 |
| `/analysis/g_salesinfo` | POST | 批量销售统计 |
| `/analysis/s_salesinfo` | POST | 单笔销售统计 |

#### statistic（统计报表）

| 路由 | 方法 | 说明 |
|------|------|------|
| `/statistic/basicinfo` | POST | 基本信息统计 |
| `/statistic/obsoletesheepinfo` | POST | 淘汰信息统计 |
| `/statistic/makecore` | POST | 评分统计 |
| `/statistic/xipu` | POST | 系谱图统计 |
| `/statistic/export_xipu` | POST | 导出系谱图 DOCX |

#### w_information（预警信息）

| 路由 | 方法 | 说明 |
|------|------|------|
| `/w_information/immunizationMessageinfo` | POST | 预警信息列表 |
| `/w_information/immunizationMessage/index` | POST | 预警信息（公开，免鉴权） |

#### chatbox（AI 问答）

| 路由 | 方法 | 说明 |
|------|------|------|
| `/chatbox/chat` | POST | AI 对话（流式响应 SSE） |
| `/chatbox/models` | GET | 获取可用模型列表 |
| `/chatbox/getWsToken` | GET | 获取 WebSocket Token（模拟） |

**AI 问答调用链：**
```
前端发送 {message, model_type}
  → POST /chatbox/chat
    → ZhipuAI(api_key=ZHIPU_API_KEY).chat.completions.create(
        model=MODEL_MAP.get(model_type, "glm-4-flash"),
        messages=[{"role": "user", "content": message}],
        stream=True
      )
    → 生成器逐块返回 → Response(generate(), content_type='text/event-stream')
  → 前端通过 SSE 逐块渲染
```

### 4.6 数据模型

#### 核心业务表（按模块分组）

**basic 模块 — 田块/作物基础**

| 模型类 | 表名 | 核心字段 |
|--------|------|----------|
| `BasicBasicinfo` | `basic_basicinfo` | id, ele_num, pre_num, variety, sex, birth, weight, house, hurdle, genes(A/B/C), scores, parents, images, state, belong, mon_age |
| `BasicObsoleteSheepinfo` | `basic_obsoletesheepinfo` | 淘汰记录 |
| `BasicBreederconditioninfo` | `basic_breederconditioninfo` | 繁育状况 |
| `BasicManuinfo` | `basic_manuinfo` | 产地/厂商信息 |
| `BasicManureinfo` | `basic_manureinfo` | 肥料记录 |
| `BasicMilkperformance` | `basic_milkperformance` | 产量指标 |
| `BasicProductivityinfo` | `basic_productivityinfo` | 生产力 |
| `BasicSkinperformance` | `basic_skinperformance` | 皮/产物性能 |
| `BasicSportsinfo` | `basic_sportsinfo` | 运动/活动记录 |
| `BasicCutinfo` | `basic_cutinfo` | 采收记录 |
| `BasicCapacity` | `basic_capacity` | 繁殖能力统计 |
| `BasicCapacityram` | `basic_capacityrams` | 个体能力 |
| `BasicGroupramcapacity` | `basic_groupramcapacity` | 群体能力 |
| `BasicMakescore` | `basic_makescore` | 评分记录 |

**colony 模块 — 草地分区**

| 模型类 | 表名 | 核心字段 |
|--------|------|----------|
| `ColonyHouseinfo` | `colony_houseinfo` | id, name, area, manager, status, pid（父区域，支持树形结构） |
| `ColonyDisinfectioninfo` | `colony_disinfectioninfo` | 消毒记录 |
| `ColonyMaintenanceinfo` | `colony_maintenanceinfo` | 维护记录 |
| `ColonyTransferinfo` | `colony_transferinfo` | 转移/搬迁记录 |

**d_health 模块 — 病虫害**

| 模型类 | 表名 | 核心字段 |
|--------|------|----------|
| `DHealthImmunizationinfo` | `d_health_immunizationinfo` | id, basic_id, vaccine_id, imm_date, next_date, belong |
| `DHealthDrugbathinfo` | `d_health_drugbathinfo` | 药浴/治疗记录 |
| `DHealthDiseaseinfo` | `d_health_diseaseinfo` | 疾病记录 |
| `DHealthDeathinfo` | `d_health_deathinfo` | 死亡记录 |
| `DHealthAbortioninfo` | `d_health_abortioninfo` | 流产/异常记录 |
| `DHealthNursinginfo` | `d_health_nursinginfo` | 护理/监测记录 |
| `DHealthQuarantineinfo` | `d_health_quarantineinfo` | 检疫记录 |

**e_breed 模块 — 生长监测**

| 模型类 | 表名 | 核心字段 |
|--------|------|----------|
| `EBreedRutinfo` | `e_breed_rutinfo` | id, basic_id, age, breeding, f_date, f_staff, belong |
| `EBreedBreedinginfo` | `e_breed_breedinginfo` | 繁殖记录 |
| `EBreedPregnantinfo` | `e_breed_pregnantinfo` | 孕期监测 |
| `EBreedLambinfo` | `e_breed_lambinfo` | 新生记录 |
| `EBreedWeaninginfo` | `e_breed_weaninginfo` | 断奶记录 |
| `EBreedPostnatalinfo` | `e_breed_postnatalinfo` | 产后记录 |
| `EBreedArtificialfeedinginfo` | `e_breed_artificialfeedinginfo` | 人工喂养 |
| `EBreedSemencollectinfo` | `e_breed_semencollectinfo` | 采集/样本 |

**supply 模块 — 供应商**

| 模型类 | 表名 | 核心字段 |
|--------|------|----------|
| `SupplyFSuppliersinfo` | `supply_f_suppliersinfo` | 饲料供应商 |
| `SupplyVSuppliersinfo` | `supply_v_suppliersinfo` | 疫苗供应商 |
| `SupplyCommodityinfo` | `supply_commodityinfo` | 商品目录 |
| `SupplyInsuranceinfo` | `supply_insuranceinfo` | 保险记录 |

**h_store 模块 — 物资**

| 模型类 | 表名 | 核心字段 |
|--------|------|----------|
| `HStoreFeedingin` | `h_store_feedingin` | 饲料入库 |
| `HStoreFeedingOut` | `h_store_feeding_out` | 饲料出库 |
| `HStoreInventory` | `h_store_inventory` | 库存 |
| `HStoreVaccineIn` | `h_store_vaccine_in` | 疫苗入库 |
| `HStoreVaccineOut` | `h_store_vaccine_out` | 疫苗出库 |

**g_slaughter 模块 — 损失评估**

| 模型类 | 表名 | 核心字段 |
|--------|------|----------|
| `GSlaughterSSalesinfo` | `g_slaughter_s_salesinfo` | 单笔销售 |
| `GSlaughterGSalesinfo` | `g_slaughter_g_salesinfo` | 批量销售 |
| `GSlaughterBinformationinfo` | `g_slaughter_binformationinfo` | 体测信息 |
| `GSlaughterSlaughtersegmentinfo` | `g_slaughter_slaughtersegmentinfo` | 分割信息 |
| `GSlaughterEconomicinfo` | `g_slaughter_economicinfo` | 经济数据 |

**analysis 模块 — 数据分析**

| 模型类 | 表名 | 核心字段 |
|--------|------|----------|
| `AnalysisDailyIncome` | `analysis_daily_income` | 日收入 |
| `AnalysisSheepAsset` | `analysis_daily_sheep_asset` | 资产分析 |
| `Analysisdailysheet` | `analysis_daily_sheet` | 日成本 |
| `Analysisdailystocksheet` | `analysis_daily_stock_sheet` | 库存成本 |

**其他**

| 模型类 | 表名 | 核心字段 |
|--------|------|----------|
| `AccountMyuser` | `account_myuser` | 用户账户（username, password, realname, jobrole, belong） |
| `WinformationImmunizationMessageinfo` | `w_information_immunizationMessageinfo` | 预警消息 |
| `ThresholdSetMessageinfo` | `threshold_setting` | 预警阈值配置 |

### 4.7 认证模块详解 — login_auth

**模型 (`login_auth/models.py`)：**

```python
class Testuser(db.Model):
    __tablename__ = 'testuser'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(100))  # 明文存储（未哈希）
    last_login = db.Column(db.DateTime)
```

**登录接口参数：**
- 请求：`POST /login`，`Content-Type: application/json`
- 请求体：`{"username": "string", "password": "string"}`
- 成功响应：`{"code": 200, "data": {"access_token": "xxx", "refresh_token": "xxx"}, "msg": "登录成功"}`
- 失败响应：`{"code": 400, "msg": "用户名或密码错误"}`

**密码验证方式：** 明文比较 `pwd == user.password`（注意：安全风险）

**Token 刷新接口：**
- 请求：`POST /refresh`，`Authorization: Bearer <refresh_token>`
- 成功响应：`{"code": 200, "data": "<new_access_token>", "msg": "刷新成功"}`

### 4.8 多租户模式

所有数据表都包含 `belong` 字段（Integer），当前硬编码过滤条件为 `belong == 0`，即单租户模式。如需扩展为多租户，需在 `create_app()` 中从 JWT 提取 `belong` 值并传入查询。

---

## 5. 前端架构详解

### 5.1 应用入口 — src/main.ts

```typescript
const app = createApp(App);

// 全局错误处理
app.config.errorHandler = errorHandler;

// 注册 Element Plus 图标组件
Object.keys(Icons).forEach(key => {
  app.component(key, Icons[key as keyof typeof Icons]);
});

// 注册插件
app.use(ElementPlus)    // UI 组件库
    .use(directives)   // 自定义指令
    .use(router)       // 路由
    .use(I18n)         // 国际化
    .use(pinia)        // 状态管理
    .mount("#app");     // 挂载到 #app
```

### 5.2 全局配置 — src/config/index.ts

```typescript
export const HOME_URL = "/home/index";     // 首页路由
export const LOGIN_URL = "/login";          // 登录路由
export const ROUTER_WHITE_LIST = [         // 路由白名单（无需认证）
  "/basic/basicinfo/detail"
];
```

### 5.3 路由系统

**静态路由 (`staticRouter.ts`)：**
- `/login` — 登录页（无需认证）
- `/layout` — 主布局（需认证，动态加载子路由）
- 403/404/500 错误页
- `/basic/basicinfo/detail` — 田块详情（白名单）
- `/test/chatbox` — AI 问答测试页

**动态路由 (`dynamicRouter.ts`)：**
1. 从静态 JSON 文件 `authMenuList.json` 加载菜单配置
2. 递归构建路由对象，设置 `component: () => import(...)` 动态导入
3. 通过 `router.addRoute()` 注入到 Vue Router
4. 在 `router.beforeEach` 中检查：无 token → 跳登录 / 有 token 但无菜单 → 加载动态路由

**路由守卫流程（`routers/index.ts`）：**
```
beforeEach(to, from, next)
  → NProgress.start()
  → 设置标题 document.title
  → to.path === LOGIN_URL?
    → 有 token: next(from.fullPath)（阻止跳回登录页）
    → 无 token: resetRouter() → next()（放行到登录页）
  → to.path 在白名单? → next()（放行）
  → 无 token? → next(LOGIN_URL)（跳转登录）
  → authStore.authMenuListGet.length === 0?
    → initDynamicRouter() → next({...to, replace: true})（重新加载）
  → setRouteName(to.name)
  → next()（正常放行）
afterEach() → NProgress.done()
```

### 5.4 状态管理（Pinia Stores）

#### useUserStore (`stores/modules/user.ts`)

| 字段 | 类型 | 说明 |
|------|------|------|
| `token` | `string` | JWT access_token |
| `refresh_token` | `string` | JWT refresh_token |
| `userInfo` | `{name, expire_date}` | 从 JWT payload 解码的用户信息 |

**持久化：** localStorage（pinia-plugin-persistedstate）

**关键方法：**
- `setToken(token)` — 设置 access_token
- `setRefreshToken(token)` — 设置 refresh_token
- `setUserInfo(info)` — 设置用户信息（从 JWT payload 解析 `{sub: username, exp: timestamp}`）

#### useAuthStore (`stores/modules/auth.ts`)

| 字段 | 类型 | 说明 |
|------|------|------|
| `authMenuList` | `Menu.MenuOptions[]` | 从 JSON 加载的菜单列表 |
| `authButtonList` | `{[key: string]: string[]}` | 按钮权限映射 |
| `routeName` | `string` | 当前路由名（用于按钮权限筛选） |

### 5.5 API 层 — Axios 封装

**核心文件：** `src/api/index.ts`

**请求拦截器：**
```
1. axiosCanceler.addPending(config)  — 取消重复请求
2. showFullScreenLoading()            — 显示全屏 loading
3. 检查 token 是否过期（compare expire_date with now）
   → 已过期：调用 getNewAccessToken() 刷新
4. 设置 Authorization: Bearer ${userStore.token}
```

**响应拦截器：**
```
1. axiosCanceler.removePending(config)  — 移除已完成的请求
2. tryHideFullScreenLoading()            — 隐藏全屏 loading
3. data.code === OVERDUE(401)?
   → 清除 token，跳转登录页
4. data.code !== SUCCESS(200)?
   → ElMessage.error(data.msg)，reject
5. 成功 → return data
```

**Token 刷新函数 `getNewAccessToken()`：**
```typescript
const getNewAccessToken = async () => {
  const userStore = useUserStore();
  await fetch(VITE_API_URL + "/refresh", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${userStore.refresh_token}`
    },
    body: JSON.stringify({})
  })
    .then(res => {
      if (res.status === 401) {
        // refresh_token 也过期，跳转登录
        userStore.setToken("");
        router.push(LOGIN_URL);
      }
      return res.json();
    })
    .then(data => {
      if (data.code === 200) {
        userStore.setToken(data.data);
        // 解析新 access_token 的 payload
        let payload = JSON.parse(atob(token.split(".")[1]));
        userStore.setUserInfo({ name: payload.sub, expire_date: payload.exp });
      }
    });
};
```

**API 模块前缀常量 (`servicePort.ts`)：**
```typescript
export const PORT1 = "/basic";          // 田块基本信息
export const PORT2 = "/hooks";          // (未使用)
export const PORT3 = "d_health";        // 病虫害管理
export const PORT4 = "/login";           // 登录认证
export const PORT5 = "/w_information";   // 预警信息
```

**HTTP 方法封装：**
```typescript
http.get<T>(url, params?, _object?)      // GET
http.post<T>(url, params?, _object?)      // POST
http.put<T>(url, params?, _object?)       // PUT
http.delete<T>(url, params?, _object?)   // DELETE
http.download(url, params?, _object?)     // POST + responseType: 'blob'
```

### 5.6 功能模块详解

每个前端模块遵循统一结构：
```
views/<module>/<feature>/
├── api/              # TypeScript API 调用函数
│   └── index.ts      # 使用 http.post/get 封装
├── hooks/            # Vue Composables
│   └── index.ts      # use<Feature>() composable
├── components/       # 子组件
│   └── *.vue
└── useProTable/
    └── index.vue     # 主页面（表格 + 搜索 + 分页）
```

#### API 调用示例（以 e_breed/rutinfo 为例）

```typescript
// src/views/e_breed/rutinfo/api/index.ts
import http from "@/api";
import { PORT1 } from "@/api/config/servicePort";

// 列表查询
export const getRutinfoList = (params: any) => {
  return http.post(`${PORT1}/e_breed/rutinfo`, params);
};

// 新增
export const addRutinfo = (params: any) => {
  return http.post(`${PORT1}/e_breed/rutinfo/add`, params);
};

// 编辑
export const editRutinfo = (params: any) => {
  return http.post(`${PORT1}/e_breed/rutinfo/edit`, params);
};

// 导出
export const exportRutinfo = (params: any) => {
  return http.download(`${PORT1}/e_breed/rutinfo/export`, params);
};
```

#### 前端模块清单

| 模块名 | 路径 | 功能 |
|--------|------|------|
| basic | `src/views/basic/` | 田块信息、运动、采收、繁育状况、产量、皮毛、肥料、产地 |
| colony | `src/views/colony/` | 区域管理、栏位管理、消毒记录、维护记录、转移记录 |
| d_health | `src/views/d_health/` | 免疫、药浴、检疫、护理、疾病、流产、死亡 |
| e_breed | `src/views/e_breed/` | 生长监测、繁殖、孕期、新生、断奶、产后、人工喂养、采集 |
| g_slaughter | `src/views/g_slaughter/` | 单笔销售、批量销售、体测、分割、经济数据 |
| h_store | `src/views/h_store/` | 饲料入库/出库、疫苗入库/出库、药品库存、饲料库存 |
| supply | `src/views/supply/` | 饲料供应商、疫苗供应商、商品目录、保险 |
| analysis | `src/views/analysis/` | 资产标准、资产信息、日收入、日资产、库存、日报、销售分析、数据可视化 |
| statistic | `src/views/statistic/` | 基本统计、淘汰统计、评分统计、系谱图 + DOCX 导出 |
| home | `src/views/home/` | 首页仪表盘、系谱图、年度报表、能力图表、数据统计 |
| w_information | `src/views/w_information/` | 免疫预警消息 |
| login | `src/views/login/` | 登录页 |

### 5.7 组件库

| 组件 | 路径 | 说明 |
|------|------|------|
| ProTable | `src/components/ProTable/` | 高级表格组件（搜索+分页+操作栏） |
| SearchForm | `src/components/SearchForm/` | 搜索表单组件 |
| SelectFilter | `src/components/SelectFilter/` | 筛选下拉组件 |
| TreeFilter | `src/components/TreeFilter/` | 树形筛选组件 |
| ImportExcel | `src/components/ImportExcel/` | Excel 导入组件 |
| Upload | `src/components/Upload/` | 图片上传（单张/多张） |
| WangEditor | `src/components/WangEditor/` | 富文本编辑器 |
| ECharts | `src/components/ECharts/` | ECharts 图表封装 |
| SvgIcon | `src/components/SvgIcon/` | SVG 图标 |
| Grid | `src/components/Grid/` | 栅格布局 |
| SwitchDark | `src/components/SwitchDark/` | 暗黑模式切换 |
| Loading | `src/components/Loading/` | 加载遮罩 |
| ErrorMessage | `src/components/ErrorMessage/` | 403/404/500 错误页 |

### 5.8 布局系统

| 布局 | 路径 | 说明 |
|------|------|------|
| LayoutClassic | `src/layouts/LayoutClassic/` | 经典布局（侧边栏+顶栏） |
| LayoutTransverse | `src/layouts/LayoutTransverse/` | 横向布局（顶部导航） |
| LayoutColumns | `src/layouts/LayoutColumns/` | 分栏布局 |
| LayoutVertical | `src/layouts/LayoutVertical/` | 垂直布局 |

布局组件包含：Header（顶部栏+面包屑+搜索+消息+头像）、Menu（侧边菜单）、Tabs（标签页）、Main（内容区）、Footer（底部）、ThemeDrawer（主题设置抽屉）。

---

## 6. 数据流全链路

### 6.1 登录流程

```
[浏览器]
  → 用户输入 username + password
  → loginApi({username, password})
  → POST /api/login
    → Nginx proxy → http://flask:5000/login

[Flask]
  → login_auth/login()
    → request.get_json() → {username, password}
    → Testuser.query.filter_by(username=name).first()
    → pwd == user.password  (明文比较)
    → create_access_token(identity=name)    → access_token (15min)
    → create_refresh_token(identity=name)   → refresh_token (30day)
    → user.last_login = datetime.now()
    → db.session.commit()
    → 返回 {code: 200, data: {access_token, refresh_token}}

[浏览器]
  → localStorage 存储 token + refresh_token
  → 解析 JWT payload: {sub: username, exp: timestamp}
  → router.push(HOME_URL)
  → initDynamicRouter() 加载菜单路由
```

### 6.2 数据查询流程（以田块列表为例）

```
[浏览器]
  → useProTable 组件初始化
  → getBasicinfoList({pageNum: 1, pageSize: 12, ...filters})
  → http.post("/basic/basicinfo", params)
  → Axios 请求拦截器:
    → 检查 token 过期 → 如过期先刷新
    → 设置 Authorization: Bearer <token>
    → showFullScreenLoading()

[Flask]
  → before_request 拦截器:
    → path 不在白名单 → verify_jwt_in_request()
    → POST JSON 数据 .strip() 所有字符串
  → basic/get_basicinfo()
    → 解析 pageNum, pageSize
    → 构建 search_params 过滤条件
    → BasicBasicinfo.query.filter(and_(*conditions)).filter(belong == 0)
    → .order_by(desc(BasicBasicinfo.id)).paginate(...)
    → json.dumps(info, cls=AlchemyEncoder) 序列化每条记录
    → 返回 {code: 200, data: {list, pageNum, pageSize, total}, msg: "成功"}

[浏览器]
  → Axios 响应拦截器:
    → data.code === 200 → return data
    → tryHideFullScreenLoading()
  → ProTable 渲染列表数据
```

### 6.3 Excel 导出流程（以免疫记录导出为例）

```
[浏览器]
  → 用户勾选要导出的记录
  → exportImmunizationinfo({selected_ids: [1, 3, 5]})
  → http.download("/d_health/immunizationinfo/export", params)
  → Axios 发送 POST，responseType: 'blob'

[Flask]
  → d_health/export_immunizationinfo()
    → selected_ids = request.json.get('selected_ids')
    → if selected_ids:
        query = DHealthImmunizationinfo.query.filter(id.in_(selected_ids))
    → query.outerjoin(BasicBasicinfo).outerjoin(SupplyCommodityinfo)
    → 构建列表数据，处理日期 .isoformat()
    → pd.DataFrame(data_list)
    → df.to_excel(output, index=False)
    → send_file(output, as_attachment=True, download_name='immunization_info.xlsx')

[浏览器]
  → 创建 Blob → URL.createObjectURL → <a> 标签触发下载
```

### 6.4 AI 问答流程

```
[浏览器]
  → ChatBubble 组件发送 {message, model_type}
  → http.post("/chatbox/chat", params) 或 fetch + EventSource

[Flask]
  → chatbox/chat()
    → ZhipuAI(api_key=ZHIPU_API_KEY)
    → client.chat.completions.create(
        model=MODEL_MAP.get(model_type, "glm-4-flash"),
        messages=[{"role": "user", "content": message}],
        stream=True
      )
    → 生成器逐块返回 → Response(generate(), content_type='text/event-stream')

[浏览器]
  → 逐块接收文本 → 渲染到聊天界面
```

---

## 7. 关键数据结构映射

### 请求/响应统一格式

**请求格式（POST JSON）：**
```json
{
  "pageNum": 1,
  "pageSize": 12,
  "field1": "value1",
  "field2": "value2"
}
```

**列表响应格式：**
```json
{
  "code": 200,
  "data": {
    "list": [...],
    "pageNum": 1,
    "pageSize": 12,
    "total": 100
  },
  "msg": "成功"
}
```

**新增/编辑响应格式：**
```json
{
  "code": 200,
  "msg": "添加成功" // 或 "编辑成功"
}
```

**错误响应格式：**
```json
{
  "code": 400,
  "msg": "错误信息"
}
```

### 前端 API 前缀与后端路由映射

| 前端常量 | 值 | 对应后端蓝图 |
|----------|---|-------------|
| `PORT1` | `/basic` | `basic` 蓝图 |
| `PORT2` | `/hooks` | （未使用） |
| `PORT3` | `d_health` | `d_health` 蓝图 |
| `PORT4` | `/login` | `login_auth` 蓝图 |
| `PORT5` | `/w_information` | `w_information` 蓝图 |

其余模块（e_breed, analysis, colony, supply, h_store, g_slaughter, statistic, chatbox）在各自的 API 文件中直接使用路径字符串调用。

---

## 8. 枚举值与配置映射

### basic 模块枚举

| 枚举名 | 选项 | 值 |
|--------|------|----|
| `color_type` | 浅绿/深绿/黄绿/混合色 | 0/1/2/3 |
| `gene_a_type` | 抗虫型(RR)/杂合型(Rr)/感虫型(rr)/未检测 | 0/1/2/3 |
| `gene_b_type` | 抗病型A/抗病型B/感病型/未检测 | 0/1/2/3 |
| `gene_c_type` | 耐旱型A/耐旱型B/普通型/未检测 | 0/1/2/3 |
| `purpose_type` | 粮食作物/经济作物/饲草作物/蔬菜作物/牧草/幼苗期作物 | 0/1/2/5/6/8 |
| `rank_type` | 重度受灾/中度受灾/轻度受灾/疑似受灾/未评级 | 0/1/2/3/9 |
| `sex_type` | 草本/木本 | 1/0 |
| `state_type` | 已淘汰/正常/已死亡/已出售 | -1/0/1/2 |

### JWT Token 结构

```
access_token payload: { "sub": "<username>", "exp": <timestamp>, "iat": <timestamp>, "type": "access" }
refresh_token payload: { "sub": "<username>", "exp": <timestamp>, "iat": <timestamp>, "type": "refresh" }
```

---

## 9. 安全与部署注意事项

| 项目 | 当前状态 | 建议 |
|------|---------|------|
| 数据库密码 | `sheep123` 硬编码 | 使用环境变量 |
| JWT 密钥 | `nihaoshijie` 硬编码 | 使用强随机密钥 |
| 密码存储 | 明文比较 | 使用 bcrypt/argon2 哈希 |
| CORS | 允许所有来源 | 限制为前端域名 |
| `.env.production` | API 指向 mock URL | 配置为实际生产地址 |
| AI API Key | 硬编码在源码 | 使用环境变量 |
| SQL 注入 | 使用 SQLAlchemy ORM（参数化查询） | 安全 |
| XSS | Vue 模板自动转义 | 安全 |