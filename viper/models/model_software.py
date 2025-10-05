from viper.models.model_base import BaseModel


class SoftwareModel(BaseModel):

    def get_softwares(self):
        sql_str = '''
            SELECT
                p.id, title, body, created, author_id, username
            FROM
                softwares
            ORDER BY created DESC
        '''
        self.conn()
        self.execute(sql_str)
        posts = self.cursor.fetchall()
        self.close()
        return posts


    def get_software_by_id(self, post_id):
        sql_str = '''
            SELECT
                p.id, title, body, created, author_id, username
            FROM
                softwares
            WHERE
                p.id = %s
        '''
        self.conn()
        self.execute(sql_str, (post_id,))
        post = self.cursor.fetchone()
        self.close()
        return post


    def add_software(self, title, body, author_id, created_at):
        sql_str = '''
            INSERT INTO
                softwares
                (title, body, author_id, created_at)
            VALUES (%s, %s, %s, %s)
        '''
        self.conn()
        self.execute(sql_str, (title, body, author_id, created_at))
        self.commit()
        lastrowid = self.cursor.lastrowid  # 自增主键id
        self.close()
        return lastrowid

    def update_software(self, title, body, post_id):
        sql_str = '''
            UPDATE
                softwares
            SET
                title = %s, body = %s
            WHERE
                id = %s
        '''
        self.conn()
        self.execute(sql_str, (title, body, post_id))
        self.commit()
        rowcount = self.cursor.rowcount  # 更新成功，受影响行数
        self.close()
        return rowcount

    def delete_software(self, post_id):
        sql_str = '''
            DELETE FROM
                softwares
            WHERE
                id = %s
        '''
        self.conn()
        self.execute(sql_str, (post_id,))
        self.commit()
        rowcount = self.cursor.rowcount  # 删除成功，受影响行数
        self.close()
        return rowcount
