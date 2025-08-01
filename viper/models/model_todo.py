from sqlalchemy import text

from viper.core.db import engine


def get_todos():
    sql_str = '''
        SELECT 
            id, name
        FROM 
            your_table
        WHERE 
            id < :max_id
    '''
    params = {'max_id': 10}

    with engine.connect() as conn:
        result = conn.execute(text(sql_str), params)
        # data is [] or [{'id': 1, 'name': 'a'}, {'id': 2, 'name': 'b'}]
        data = result.mappings().all()
    return data


def get_todo_by_id():
    sql_str = '''
        SELECT 
            id, name
        FROM 
            your_table
        WHERE 
            id < :max_id
        LIMIT 1
    '''
    params = {'id': 123}

    with engine.connect() as conn:
        result = conn.execute(text(sql_str), params)
        # data is None or {'id': 123, 'name': '张三'}
        data = result.mappings().first()
    return data
