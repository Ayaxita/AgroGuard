# exts.py:插件管理
# 扩展的第三方插件

# 1.导入第三方插件
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

import logging

# 2.初始化

db = SQLAlchemy()  # ORM
migrate = Migrate()  # 数据迁移

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)


# 3.和app对象绑定

def init_exts(app):
    db.init_app(app=app)  #将db对象(ORM映射)与app进行了关联
    migrate.init_app(app=app, db=db)  #
    CORS(app, supports_credentials=True)
    # CORS(app, supports_credentials=True)
