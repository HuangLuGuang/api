# -*- coding: utf-8 -*-
# @createTime    : 2019/8/27 14:13
# @author  : Huanglg
# @fileName: views.py
# @email: luguang.huang@mabotech.com
from flask import current_app
from flask.json import jsonify

from . import auth_blue

@auth_blue.route('/test')
def test_auth():
    sql = "select name, employeeno, loginname, password, employeevaliddate, resourceid from employee"
    res = current_app.db.query(sql)
    return jsonify(res)
