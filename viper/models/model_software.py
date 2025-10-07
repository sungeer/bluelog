from viper.models.model_base import BaseModel


class BlessModel(BaseModel):

    def get_blesses(self):
        sql_str = '''
            SELECT
                id, text, status, created_at, updated_at, is_deleted, version
            FROM
                blessing
            ORDER BY id DESC
        '''
        self.conn()
        self.execute(sql_str)
        blesses = self.cursor.fetchall()
        self.close()
        return blesses


    def get_bless_by_id(self, bless_id):
        sql_str = '''
            SELECT
                id, text, status, created_at, updated_at, is_deleted, version
            FROM
                blessing
            WHERE
                id = %s
        '''
        self.conn()
        self.execute(sql_str, (bless_id,))
        bless_info = self.cursor.fetchone()
        self.close()
        return bless_info


    def add_bless(self, text, created_at, updated_at):
        sql_str = '''
            INSERT INTO blessing (text, created_at, updated_at)
            VALUES (%s, %s, %s)
        '''
        self.conn()
        self.execute(sql_str, (text, created_at, updated_at))
        self.commit()
        lastrowid = self.cursor.lastrowid  # 自增主键id
        self.close()
        return lastrowid

    def update_bless(self, text, status, bless_id):
        sql_str = '''
            UPDATE
                blessing
            SET
                text = %s, status = %s
            WHERE
                id = %s
        '''
        self.conn()
        self.execute(sql_str, (text, status, bless_id))
        self.commit()
        rowcount = self.cursor.rowcount  # 更新成功，受影响行数
        self.close()
        return rowcount

    def delete_bless(self, bless_id):
        sql_str = '''
            DELETE FROM
                blessing
            WHERE
                id = %s
        '''
        self.conn()
        self.execute(sql_str, (bless_id,))
        self.commit()
        rowcount = self.cursor.rowcount  # 删除成功，受影响行数
        self.close()
        return rowcount
