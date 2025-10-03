from bluelog.models.model_base import BaseModel


class AuthModel(BaseModel):

    def get_user_by_id(self, user_id):
        sql_str = '''
            SELECT
                id, username, password
            FROM
                user
            WHERE
                id = %s
        '''
        self.conn()
        self.execute(sql_str, (user_id,))
        user = self.cursor.fetchone()
        self.close()
        return user

    def exists_by_username(self, username):
        sql_str = '''
            SELECT EXISTS(
                SELECT 1 FROM user WHERE username = %s
            ) AS is_exist
        '''
        self.conn()
        self.execute(sql_str, (username,))
        user = self.cursor.fetchone()
        self.close()
        is_exist = user['is_exist']
        return bool(is_exist)

    def add_user(self, username, password, created_at):
        sql_str = '''
            INSERT INTO
                user
                (username, password， created_at)
            VALUES (%s, %s, %s)
        '''
        self.conn()
        self.execute(sql_str, (username, password, created_at))
        self.commit()
        lastrowid = self.cursor.lastrowid  # 自增主键id
        self.close()
        return lastrowid

    def get_user_by_username(self, username):
        sql_str = '''
            SELECT
                id, username, password
            FROM
                user
            WHERE
                username = %s
        '''
        self.conn()
        self.execute(sql_str, (username,))
        user = self.cursor.fetchone()
        self.close()
        return user
