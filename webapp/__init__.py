from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import DebugConfig

app = Flask(__name__)

app.config.from_object(DebugConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)  # 用户登录状态管理模块
login_manager.login_view = 'login'  # 注册登录处理的视图函数

from webapp import routes
from webapp import api
from webapp import models
