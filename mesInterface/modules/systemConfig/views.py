# -*- coding: utf-8 -*-
# @createTime    : 2019/8/30 10:05
# @author  : Huanglg
# @fileName: views.py
# @email: luguang.huang@mabotech.com
import json
import traceback

from flask import current_app, request, make_response, abort
from flask.json import jsonify

from . import system_config_blue


@system_config_blue.route('/menu_item')
def test_auth():
    def get_children_menu_item(parentid):
        c_menu_item_base_sql = """select MI.ID, MI.NAME,TT.MEDIUM MENU_DESC,TTT.MEDIUM MENU_TYPE,MI.SHOWDESKTOP,MI.SHOWMOBILE,MI.PARENTID,
MI.REDIRECTURL, '' IMAGE_URL,MI.ACTIVE, MI.LASTUPDATEON, MI.LASTUPDATEDBY from MENU_ITEM MI
LEFT JOIN text_translation TT ON TT.TEXTID=MI.TEXTID AND TT.LANGUAGEID=2052
LEFT JOIN MENU_ITEM_TYPE MIT ON MIT.ID = MI.TYPE
LEFT JOIN TEXT_TRANSLATION TTT ON MIT.TEXTID = TTT.TEXTID AND TTT.LANGUAGEID=2052
where MI.PARENTID={}"""
        c_menu_item_sql = c_menu_item_base_sql.format(parentid)
        return current_app.db.query(c_menu_item_sql)

    p_menu_item_sql = """select MI.ID, MI.NAME,TT.MEDIUM MENU_DESC,TTT.MEDIUM MENU_TYPE,MI.SHOWDESKTOP,MI.SHOWMOBILE,MI.PARENTID,
MI.REDIRECTURL, '' IMAGE_URL,MI.ACTIVE, MI.LASTUPDATEON, MI.LASTUPDATEDBY from MENU_ITEM MI
LEFT JOIN text_translation TT ON TT.TEXTID=MI.TEXTID AND TT.LANGUAGEID=2052
LEFT JOIN MENU_ITEM_TYPE MIT ON MIT.ID = MI.TYPE
LEFT JOIN TEXT_TRANSLATION TTT ON MIT.TEXTID = TTT.TEXTID AND TTT.LANGUAGEID=2052
where MI.PARENTID is null"""

    p_menu_items = current_app.db.query(p_menu_item_sql)

    for p_menu_item in p_menu_items:
        p_menu_item['children'] = get_children_menu_item(p_menu_item['id'])

    return jsonify(p_menu_items)


@system_config_blue.route('/menu_list')
def menu_list():

    menu_list_sql = """select MI.ID, MI.NAME,TT.MEDIUM MENU_DESC,TTT.MEDIUM MENU_TYPE,MI.SHOWDESKTOP,MI.SHOWMOBILE,MI.PARENTID,
MI.REDIRECTURL, '' IMAGE_URL,MI.ACTIVE, MI.LASTUPDATEON, MI.LASTUPDATEDBY from MENU_ITEM MI
LEFT JOIN text_translation TT ON TT.TEXTID=MI.TEXTID AND TT.LANGUAGEID=2052
LEFT JOIN MENU_ITEM_TYPE MIT ON MIT.ID = MI.TYPE
LEFT JOIN TEXT_TRANSLATION TTT ON MIT.TEXTID = TTT.TEXTID AND TTT.LANGUAGEID=2052"""

    menu_list = current_app.db.query(menu_list_sql)

    return jsonify(menu_list)


@system_config_blue.route('/menu_tree')
def menu_tree():

    menu_list_sql = """select get_menu_item();"""

    menu_list = current_app.db.query(menu_list_sql)[0]['get_menu_item']

    # 拿到所有的id和menu的映射
    id_map_menu = {}
    for menu in menu_list:
        id = menu['id']
        id_map_menu[id] = menu

    arr = []

    for menu in menu_list:
        # 找到父节点加入到父节点的children
        parentid = menu['parentid']
        if parentid:
            parent = id_map_menu[parentid]
            parent_children = parent.get('children', [])
            if parent_children == []:
                parent['children'] = []
            parent['children'].append(menu)
        else:
            arr.append(menu)

    return jsonify(arr)


@system_config_blue.route('/delete_menu', methods=['POST', 'DELETE'])
def delete_ment():
    result = 0
    try:
        req_data = request.get_data(as_text=True)
        dict_data = json.loads(req_data)
        id = dict_data.get('id')
        base_sql = """DELETE from  menu_item  where id ={}"""
        sql = base_sql.format(id)
    except Exception as e:
        current_app.logger.error(traceback.format_exc())

    try:
        result = current_app.db.execute(sql)
    except Exception as e:
        current_app.logger.errorresult = traceback.format_exc()
    return jsonify({"result": result})


@system_config_blue.route('/get_menu_item', methods=['POST', 'GET'])
def get_menu_item():

    sql = "select get_menu_item();"
    result = current_app.db.query(sql)
    print(result[0]['get_menu_item'])
    return jsonify(result[0]['get_menu_item'])

@system_config_blue.route('/insert_menu', methods=['POST'])
def insert_menu():

    data = request.get_data(as_text=True)
    result = None
    try:
        json_data = json.loads(data)
        name = json_data['name']
        parentid = json_data['parentid']
        if parentid is None:
            parentid = 'null'
    except Exception as e:
        current_app.logger.error(traceback.format_exc())

    try:
        sql = "select insertMenu('{name}', {parentid});".format(name=name, parentid=parentid)
        print(sql)
        result = current_app.db.execute(sql)
    except Exception as e:
        current_app.logger.errorresult = traceback.format_exc()
    return jsonify({'result': result})


