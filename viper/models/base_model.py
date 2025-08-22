from viper.utils.db_util import create_dbconn


class BaseModel:

    def __init__(self):
        self.cursor = None
        self._conn = None

    def conn(self):
        if not self.cursor:
            self._conn = create_dbconn()
            self.cursor = self._conn.cursor()

    def rollback(self):
        self._conn.rollback()

    def commit(self):
        try:
            self._conn.commit()
        except Exception:
            self.rollback()
            raise

    def begin(self):
        self._conn.begin()

    def close(self):
        try:
            if self.cursor:
                self.cursor.execute('UNLOCK TABLES;')
                self.cursor.close()
            if self._conn:
                self._conn.close()
        finally:
            self.cursor = None
            self._conn = None

    def execute(self, sql_str, values=None):
        try:
            self.cursor.execute(sql_str, values)
        except Exception:
            self.rollback()
            self.close()
            raise

    def executemany(self, sql_str, values=None):
        try:
            self.cursor.executemany(sql_str, values)
        except Exception:
            self.rollback()
            self.close()
            raise
