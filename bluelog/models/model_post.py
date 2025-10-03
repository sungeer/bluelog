from bluelog.models.model_base import BaseModel


class PostModel(BaseModel):

    def get_posts(self):
        sql_str = '''
            SELECT
                p.id, title, body, created, author_id, username
            FROM
                post p
                LEFT JOIN user u ON p.author_id = u.id
            ORDER BY created DESC
        '''
        self.conn()
        self.execute(sql_str)
        posts = self.cursor.fetchall()
        self.close()
        return posts


    def get_post_by_id(self, post_id):
        sql_str = '''
            SELECT
                p.id, title, body, created, author_id, username
            FROM
                post p
                LEFT JOIN user u ON p.author_id = u.id
            WHERE
                p.id = %s
        '''
        self.conn()
        self.execute(sql_str, (post_id,))
        post = self.cursor.fetchone()
        self.close()
        return post


    def add_post(self, title, body, author_id, created_at):
        sql_str = '''
            INSERT INTO
                post
                (title, body, author_id, created_at)
            VALUES (%s, %s, %s, %s)
        '''
        self.conn()
        self.execute(sql_str, (title, body, author_id, created_at))
        self.commit()
        lastrowid = self.cursor.lastrowid  # 自增主键id
        self.close()
        return lastrowid

    def update_post(self, title, body, post_id):
        sql_str = '''
            UPDATE
                post
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

    def delete_post(self, post_id):
        sql_str = '''
            DELETE FROM
                post
            WHERE
                id = %s
        '''
        self.conn()
        self.execute(sql_str, (post_id,))
        self.commit()
        rowcount = self.cursor.rowcount  # 删除成功，受影响行数
        self.close()
        return rowcount
