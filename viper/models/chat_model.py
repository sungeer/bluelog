from viper.models.base_model import BaseModel
from viper.utils.decorators import sync_to_async_db


class ChatModel(BaseModel):

    @sync_to_async_db
    def add_chat(self, conversation_id, title, user_id):
        sql_str = '''
            INSERT INTO 
                chats 
                (conversation_id, title, user_id) 
            VALUES 
                (%s, %s, %s)
        '''
        values = (conversation_id, title, user_id)
        self.conn()
        self.execute(sql_str, values)
        self.commit()
        lastrowid = self.cursor.lastrowid
        self.close()
        return lastrowid

    @sync_to_async_db
    def get_chats(self, user_id):
        sql_str = '''
            SELECT
                id, conversation_id, title, created_time
            FROM
                chats
            WHERE
                user_id = %s
            LIMIT 100
        '''
        self.conn()
        self.execute(sql_str, (user_id,))
        chats = self.cursor.fetchall()
        self.close()
        return chats

    @sync_to_async_db
    def get_chat_by_conversation(self, conversation_id):
        sql_str = '''
            SELECT 
                id, conversation_id, title, created_time
            FROM 
                chats
            WHERE
                conversation_id = %s
        '''
        self.conn()
        self.execute(sql_str, (conversation_id,))
        chat_info = self.cursor.fetchone()
        self.close()
        return chat_info
