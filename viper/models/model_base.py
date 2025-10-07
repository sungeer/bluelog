from contextlib import suppress

from viper.cores.core_db import get_db_conn


class BaseModel:

    def __init__(self):
        self.cursor = None
        self._conn = None

    def conn(self, with_begin=False):
        self._conn = get_db_conn()
        if with_begin:
            self._conn.begin()
        self.cursor = self._conn.cursor()

    def commit(self):
        try:
            self._conn.commit()
        except (Exception,):
            with suppress(Exception):
                self._conn and self._conn.rollback()
            raise

    def close(self):
        with suppress(Exception):
            self.cursor and self.cursor.close()
        self.cursor = None
        with suppress(Exception):
            self._conn and self._conn.close()  # 归还到连接池
        self._conn = None

    def execute(self, sql_str, values=None):
        try:
            self.cursor.execute(sql_str, values)
        except (Exception,):
            with suppress(Exception):
                self._conn and self._conn.rollback()
            self.close()
            raise

    def executemany(self, sql_str, values=None):
        try:
            self.cursor.executemany(sql_str, values)
        except (Exception,):
            with suppress(Exception):
                self._conn and self._conn.rollback()
            self.close()
            raise
