import math
import re

import MySQLdb
from MySQLdb.cursors import DictCursor
from dbutils.pooled_db import PooledDB

from viper.core import settings

dbpool = PooledDB(
    creator=MySQLdb,
    maxcached=5,
    host=settings.CONF.get_conf('DATABASE', 'HOST'),
    port=settings.CONF.get_int_conf('DATABASE', 'PORT'),
    db=settings.CONF.get_conf('DATABASE', 'NAME'),
    user=settings.CONF.get_conf('DATABASE', 'USER'),
    passwd=settings.CONF.get_sec_conf('DATABASE', 'PASSWD'),
    charset='utf8mb4',
    cursorclass=DictCursor
)


def create_dbconn():
    conn = dbpool.connection()  # 从连接池中获取一个连接
    return conn


class DBConnection:
    def __init__(self):
        self.dbconn = None
        self.cursor = None

    def commit(self):
        self.dbconn.commit()

    def __enter__(self):
        if not self.dbconn:
            self.dbconn = create_dbconn()
        if not self.cursor:
            self.cursor = self.dbconn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self.cursor:
                self.cursor.execute('UNLOCK TABLES;')
                self.cursor.close()
            if self.dbconn:
                self.dbconn.close()
        finally:
            self.dbconn = None
            self.cursor = None


class Common:

    @staticmethod
    def parse_limit_str(page_info=None):
        if page_info is None:
            page_info = {}
        page = int(page_info.get('page', 1))
        page_size = int(page_info.get('rows', 20))
        limit_str = ' LIMIT %s, %s ' % ((page - 1) * page_size, page_size)
        return limit_str

    @staticmethod
    def parse_update_str(table, p_key, p_id, update_dict):
        sql_str = ' UPDATE %s SET ' % (table,)
        temp_str = []
        sql_values = []
        for key, value in update_dict.items():
            temp_str.append(key + ' = %s ')
            sql_values.append(value)
        sql_str += ', '.join(r for r in temp_str) + ' WHERE ' + p_key + ' = %s '
        sql_values.append(p_id)
        return sql_str, sql_values

    @staticmethod
    def parse_where_str(filter_fields, request_data):
        if not isinstance(filter_fields, tuple) and not isinstance(filter_fields, list):
            filter_fields = (filter_fields,)
        where_str = ' WHERE 1 = %s '
        where_values = [1]
        for key in filter_fields:
            value = request_data.get(key)
            if value:
                where_str += ' AND ' + key + ' = %s '
                where_values.append(value)
        if not where_values:
            where_values = None
        return where_str, where_values

    @staticmethod
    def parse_where_like_str(filter_fields, request_data):
        if not isinstance(filter_fields, tuple) and not isinstance(filter_fields, list):
            filter_fields = (filter_fields,)
        where_str = ' WHERE 1 = %s '
        where_values = [1]
        for key in filter_fields:
            value = request_data.get(key)
            if value:
                where_str += ' AND ' + key + ' LIKE %s '
                where_values.append('%%%%%s%%%%' % value)
        if not where_values:
            where_values = None
        return where_str, where_values

    @staticmethod
    def parse_count_str(sql_str, truncate=False):
        if truncate:
            if 'GROUP BY' in sql_str:
                sql_str = 'SELECT COUNT(*) total FROM (%s) AS TEMP' % sql_str
            else:
                sql_str = re.sub(r'SELECT[\s\S]*?FROM', 'SELECT COUNT(*) total FROM', sql_str, count=1)
        if 'ORDER BY' in sql_str:
            sql_str = sql_str[:sql_str.find('ORDER BY')]
        if 'LIMIT' in sql_str:
            sql_str = sql_str[:sql_str.find('LIMIT')]
        return sql_str

    @staticmethod
    def get_page_info(total, page=1, per_page=20):
        pages = math.ceil(total / per_page)
        next_num = page + 1 if page < pages else None
        has_next = page < pages
        prev_num = page - 1 if page > 1 else None
        has_prev = page > 1
        page_info = {
            'page': page,
            'per_page': per_page,  # 每页显示的记录数
            'pages': pages,  # 总页数
            'total': total,
            'next_num': next_num,
            'has_next': has_next,
            'prev_num': prev_num,
            'has_prev': has_prev
        }
        return page_info
