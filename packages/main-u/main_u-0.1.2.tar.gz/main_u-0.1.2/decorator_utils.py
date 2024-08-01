#!/usr/bin/env python
# coding=utf-8
import datetime, time
from functools import wraps
from log_utils import LoggingUtils

class DecoratorFactory(object):
    """
    装饰器工具工厂类，用于注册和获取不同类型的装饰器工具
    """
    def __init__(self):
        """
        构造函数，初始化一个空字典用于存储装饰器工具
        """
        self._decorator_map = {}  # 将 _decorate_utils 更名为 _decorator_map ，更清晰地表明是一个映射（字典）

    def register_decorator(self, name: str, decorator: object):
        """
        用于向工厂注册装饰器工具的方法

        参数:
        - name (str): 装饰器工具的名称
        - decorator_utils: 装饰器工具对象
        """
        self._decorator_map[name] = decorator

    def get_decorator(self, name: str):
        """
        根据名称获取已注册的装饰器工具

        参数:
        - name (str): 要获取的装饰器工具的名称

        返回:
        - 对应的装饰器工具对象，如果不存在则返回 None
        """
        return self._decorator_map.get(name)


def default_decorator(func):
    """
    默认装饰器，用于演示如何使用装饰器工厂

    参数:
    - func: 要装饰的函数

    返回:
    - 装饰后的函数
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"This is a default decorator.")
        return func(*args, **kwargs)

    return wrapper


def logger_decorator(func):
    """
    日志装饰器，用于记录函数的调用信息

    参数:
    - func: 要装饰的函数

    返回:
    - 装饰后的函数
    """
    time_str = datetime.datetime.now().strftime("%Y%m%d")
    logger = LoggingUtils(log_file=f"{time_str}.log")

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"============================={func.__name__}===================================")
        if args:
            logger.info(f"Args: {args}")
        if kwargs:
            logger.info(f"Kwargs: {kwargs}")
        return func(*args, **kwargs)

    return wrapper

def time_decorator(func):
    """
    计时装饰器，用于记录函数的执行时间

    参数:
    - func: 要装饰的函数

    返回:
    - 装饰后的函数
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        print(f"cost time: {end_time - start_time} seconds")

    return wrapper


# 创建装饰器工具工厂实例
decorator_factory = DecoratorFactory()

# 向工厂注册名为 'default' 的装饰器工具
decorator_factory.register_decorator('default', default_decorator)
decorator_factory.register_decorator('log', logger_decorator)
decorator_factory.register_decorator('timer', time_decorator)

# 获取装饰器工具
decorator = decorator_factory.get_decorator('default')
log_decorator = decorator_factory.get_decorator('log')
timer_decorator = decorator_factory.get_decorator('timer')



if __name__ == '__main__':

    # 使用装饰器工具装饰一个函数
    @log_decorator
    def hello(name):
        print("Hello, World!", name)

    hello('Alice')  
