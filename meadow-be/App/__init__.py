# __init__.py：初始化文件，创建Flask应用
import datetime


from flask import Flask
from flask_jwt_extended import JWTManager

from App.login_auth.views import login_auth
from App.basic.views import basic
from App.field.views import field
from App.supply.views import supply
from App.h_store.views import h_store
from App.g_harvest.views import g_harvest
from App.pest_control.views import pest_control
from .analysis.views import analysis
from .propagation.views import propagation
from .exts import init_exts, db
from .statistic.view import Statistic
from .w_information.views import w_information
from .chatbox.views import chatbox

def create_app():
    app = Flask(__name__)
    # CORS(app, resources={r"/*": {"origins": "*"}})
    print(app.config)
    '''
    <Config {'DEBUG': True, 'TESTING': False, 'PROPAGATE_EXCEPTIONS': None, 'SECRET_KEY': None, 'PERMANENT_SESSION_LIFETIME': datetime.timedelta(days=31), 'USE_X_SENDFILE': False, 'SERVER_NAME': None, 'APPLICATION_ROOT': '/', 'SESSION_COOKIE_NAME': 'session', 'SESSION_COOKIE_DOMAIN': None, 'SESSION_COOKIE_PATH': None, 'SESSION_COOKIE_HTTPONLY': True, 'SESSION_COOKIE_SECURE': False, 'SESSION_COOKIE_SAMESITE': None, 'SESSION_REFRESH_EACH_REQUEST': True, 'MAX_CONTENT_LENGTH': None, 'SEND_FILE_MAX_AGE_DEFAULT': None, 'TRAP_BAD_REQUEST_ERRORS': None, 'TRAP_HTTP_EXCEPTIONS': False, 'EXPLAIN_TEMPLATE_LOADING': False, 'PREFERRED_URL_SCHEME': 'http', 'TEMPLATES_AUTO_RELOAD': None, 'MAX_COOKIE_SIZE': 4093}>

    '''
    app.config['SECRET_KEY'] = 'nihaoshijie'
    app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=30)

    # 注册蓝图
    app.register_blueprint(login_auth)      #登录
    app.register_blueprint(basic)       #草只基本信息
    app.register_blueprint(field)  #
    app.register_blueprint(supply)
    app.register_blueprint(h_store)
    app.register_blueprint(g_harvest)
    app.register_blueprint(pest_control)
    app.register_blueprint(propagation)
    app.register_blueprint(w_information)
    app.register_blueprint(Statistic)
    app.register_blueprint(analysis)
    app.register_blueprint(chatbox)

    # 配置数据库
    # db_uri = 'sqlite:///sqlite3.db'
    # db_uri = 'mysql+pymysql://root:dpfxzby$ztcxlbj$9264$@39.99.175.254:8055/grass_555'  # mysql链接
    # db_uri = 'mysql+pymysql://root:hscjtCemt2024$@182.92.207.3:3306/meadow_test' #mysql链接
    db_uri = 'mysql+pymysql://root:meadow123@mysql-db:3306/meadow_test' #mysql链接
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 配置jwt
    app.config['JWT_SECRET_KEY'] = 'nihaoshijie'
    # 设置普通JWT过期时间
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(minutes=15)
    # 设置刷新JWT过期时间
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = datetime.timedelta(days=30)
    jwt = JWTManager(app)

    # 初始化插件
    #建立数据库连接
    init_exts(app=app)

    return app
