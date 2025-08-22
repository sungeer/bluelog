from functools import wraps

from viper.utils.pools import run_in_thread_pool_db


def async_run_in_thread_pool_db(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        return await run_in_thread_pool_db(func, *args, **kwargs)

    return wrapper


class AsyncMethodsMeta(type):

    def __new__(cls, name, bases, dct):
        for attr_name, attr_value in dct.items():
            if callable(attr_value) and not attr_name.startswith('__'):
                dct[attr_name] = async_run_in_thread_pool_db(attr_value)  # 为同步方法添加装饰器
        return super().__new__(cls, name, bases, dct)


if __name__ == '__main__':
    class ParentClass(metaclass=AsyncMethodsMeta):  # class ParentClass: pass

        @staticmethod
        def common_method():
            print('父类方法运行')


    class ChildClass(ParentClass):  # class ChildClass(ParentClass, metaclass=AsyncMethodsMeta): pass

        @staticmethod
        def custom_sync_method(x, y):
            print(f'在子类中运行同步方法: {x} + {y} = {x + y}')
            return x + y
