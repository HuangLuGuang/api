# -*- coding: utf-8 -*-
# @createTime    : 2019/8/27 14:20
# @author  : Huanglg
# @fileName: manage.py
# @email: luguang.huang@mabotech.com
from mesInterface import create_app


app = create_app('development')

if __name__ == '__main__':
    app.run(debug=True)
    print(app.url_map)
    app.run()
