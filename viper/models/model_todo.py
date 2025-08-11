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
        data = [dict(r) for r in result.mappings()]
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
    params = {'max_id': 123}

    with engine.connect() as conn:
        result = conn.execute(text(sql_str), params)
        row = result.mappings().first()
        # data is None or {'id': 123, 'name': '张三'}
        data = None if row is None else dict(row)
    return data


def add_todo():
    sql_str = '''
        INSERT INTO your_table (name, age)
        VALUES (:name, :age)
    '''
    params = {'name': '张三', 'age': 20}

    with engine.begin() as conn:
        result = conn.execute(text(sql_str), params)
        # rowcount = result.rowcount  # 插入成功，受影响行数
        inserted_id = result.lastrowid  # 自增主键id
    return inserted_id


def add_todos():
    sql_str = '''
        INSERT INTO your_table (name, age)
        VALUES (:name, :age)
    '''
    data = [
        {'name': '张三', 'age': 20},
        {'name': '李四', 'age': 22},
        {'name': '王五', 'age': 25},
    ]

    with engine.begin() as conn:
        result = conn.execute(text(sql_str), data)
        rowcount = result.rowcount  # 插入成功，受影响行数
    return rowcount


def del_todo():
    sql_str = '''
        DELETE FROM your_table
        WHERE id=:id
    '''
    params = {'id': 5}

    with engine.begin() as conn:
        result = conn.execute(text(sql_str), params)
        rowcount = result.rowcount  # 删除成功，受影响行数
    return rowcount


def update_todo():
    sql_str = '''
        UPDATE your_table
        SET name=:name, age=:age
        WHERE id=:id
    '''
    params = {'name': '李四', 'age': 22, 'id': 3}

    with engine.begin() as conn:
        result = conn.execute(text(sql_str), params)
        rowcount = result.rowcount  # 更新成功，受影响行数
    return rowcount
