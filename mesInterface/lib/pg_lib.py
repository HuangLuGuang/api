# -*- coding: utf-8 -*-
# @createTime    : 2019/8/26 21:16
# @author  : Huanglg
# @fileName: pg_lib.py
# @email: luguang.huang@mabotech.com
# -*- coding: UTF-8 -*-
import psycopg2
import traceback
from logging import getLogger

log = getLogger('pg_lib')


def try_except(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            log.error(traceback.print_exc())
            raise

    return wrapper


class PG_LIB(object):
    def __init__(self, host, db, user, pwd, port):
        self.host = host
        self.db = db
        self.user = user
        self.pwd = pwd
        self.port = port
        self._conn = self._connect()
        self._cursor = self._conn.cursor()

    @try_except
    def _connect(self):
        return psycopg2.connect(
            database=self.db,
            user=self.user,
            password=self.pwd,
            host=self.host,
            port=self.port)

    @try_except
    def select(self, sqlCode):
        self._cursor.execute(sqlCode)
        return self._cursor.fetchall()

    def insert(self, sqlCode):
        self.common(sqlCode)

    def update(self, sqlCode):
        self.common(sqlCode)

    def delete(self, sqlCode):
        self.common(sqlCode)

    def close(self):
        self._cursor.close()
        self._conn.close()

    def insertAndGetField(self, sql_code, field):
        """
        插入数据，并返回当前 field
        :param sql_code:
        :param field:
        :return:
        """
        try:
            self.cursor.execute(sql_code + " RETURNING " + field)
        except Exception as e:
            print(e)
            self.conn.rollback()
            self.cursor.execute(sql_code + " RETURNING " + field)
        self.conn.commit()

        return self.cursor.fetchone()

    def common(self, sqlCode):
        try:
            self._cursor.execute(sqlCode)
        except Exception as e:
            print(e)
            self._conn.rollback()
            self._cursor.execute(sqlCode)
        self._conn.commit()

    def __del__(self):
        print("最后一步，关闭数据库")
        self.close()


if __name__ == '__main__':
    pg = PG_LIB(host="huanglg.top",
      db="flxuser1",
      user="postgres",
      pwd="postgres",
      port="5433")
    sql = "select * from employee"
    res = pg.select(sql)
    print(res)
