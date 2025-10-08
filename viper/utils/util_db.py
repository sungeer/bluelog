import math
import re


def parse_limit_str(page_info=None):
    if page_info is None:
        page_info = {}
    page = int(page_info.get('page', 1))
    page_size = int(page_info.get('rows', 20))
    limit_str = ' LIMIT %s, %s ' % ((page - 1) * page_size, page_size)
    return limit_str


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


def parse_where_str(filter_fields, request_data):
    if not isinstance(filter_fields, (tuple, list)):
        filter_fields = (filter_fields,)
    where_str = ' WHERE 1 = %s '
    where_values = [1]
    for key in filter_fields:
        value = request_data.get(key)
        if value:
            where_str += ' AND ' + key + ' = %s '
            where_values.append(value)
    return where_str, where_values


def parse_where_like_str(filter_fields, request_data):
    if not isinstance(filter_fields, (tuple, list)):
        filter_fields = (filter_fields,)
    where_str = ' WHERE 1 = %s '
    where_values = [1]
    for key in filter_fields:
        value = request_data.get(key)
        if value:
            where_str += ' AND ' + key + ' LIKE %s '
            where_values.append('%%%%%s%%%%' % value)
    return where_str, where_values


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
