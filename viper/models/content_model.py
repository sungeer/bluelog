from viper.models.base_model import BaseModel
from viper.utils.decorators import sync_to_async_db


class ContentModel(BaseModel):

    @sync_to_async_db
    def add_content(self, message_id, content):
        sql_str = '''
            INSERT INTO 
                contents 
                (message_id, content) 
            VALUES 
                (%s, %s)
        '''
        self.conn()
        self.execute(sql_str, (message_id, content))
        self.commit()
        last_row_id = self.cursor.lastrowid
        self.close()
        return last_row_id
