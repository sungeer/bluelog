from viper.models.base_model import BaseModel
from viper.utils.decorators import sync_to_async_db


class UserModel(BaseModel):

    @sync_to_async_db
    def get_user_by_phone(self, phone_number):
        sql_str = '''
            SELECT
                id, name, phone, password_hash, is_admin, created_time
            FROM
                users
            WHERE
                phone = %s
        '''
        self.conn()
        self.execute(sql_str, (phone_number,))
        user_info = self.cursor.fetchone()
        self.close()
        return user_info

    @sync_to_async_db
    def get_user_by_id(self, user_id):
        sql_str = '''
            SELECT
                id, name, phone, is_admin, created_time
            FROM
                users
            WHERE
                id = %s
        '''
        self.conn()
        self.execute(sql_str, (user_id,))
        user_info = self.cursor.fetchone()
        self.close()
        return user_info
