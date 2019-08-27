# -*- coding: utf-8 -*-
# @createTime    : 2019/8/26 21:02
# @author  : Huanglg
# @fileName: __init__.py.py
# @email: luguang.huang@mabotech.com
import logging
from logging.handlers import RotatingFileHandler
from mesInterface.lib.pgwrap.db import connection
from flask import Flask
from flask_session import Session
from .config import Config,config_dict
from redis import StrictRedis
from flask_wtf import CSRFProtect,csrf


def setup_log(config_name):
    """配置日志"""

    # 设置日志的记录等级
    logging.basicConfig(level=config_dict[config_name].LOG_LEVEL)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


# 实例化redis对象 decode_response=True 默认直接编码
redis_store = StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT,decode_responses=True)

# 定义工厂函数
def create_app(config_name):
    app = Flask(__name__)
    # 配置项目日志
    setup_log(config_name)
    app.config.from_object(config_dict[config_name])
    # Session(app)
    CSRFProtect(app)
    db = create_conn(config_name)
    app.db = db
    # 每次请求之后都设置一个csrf_token
    @app.after_request
    def after_request(response):
        csrf_token = csrf.generate_csrf()
        response.set_cookie('csrf_token',csrf_token)
        return response
    from .modules.auth import auth_blue
    app.register_blueprint(auth_blue)
    return app

def create_conn(config_name):
    db_info = config_dict[config_name].DB_INFO
    db = connection(db_info)
    return db
