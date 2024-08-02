#!/usr/bin/env python
# coding=utf-8
""""
for example:
    from decorator_utils import DecoratorUtils, LogUtils

    logger = LogUtils().get_logger()
    decorator = DecoratorUtils(logger)
    @decorator.logger_decorator
    def func():
        pass
        
    >>>
    2024-08-02 10:39:13,382 - app - INFO - Kwargs: {'url': 'www.baidu.com', 'name': 'test'
    2024-08-02 10:39:13,382 - app - INFO - Args: ('afghhf', 'fghfghfgh')
"""
import time
from functools import wraps
from log_utils import LogUtils


class DecoratorUtils:
    """
    日志工具类，用于记录函数的输入输出和执行时间
    """
    def __init__(self, logger: LogUtils):
        self.logger = logger

    def logger_decorator(self, func):
        """
        日志装饰器，用于记录函数的调用信息

        参数:
        - func: 要装饰的函数

        返回:
        - 装饰后的函数
        """
        try:
            @wraps(func)
            def wrapper(*args, **kwargs):
                if args:
                    self.logger.info(f"Args: {args}")
                if kwargs:
                    self.logger.info(f"Kwargs: {kwargs}")
                return func(*args, **kwargs)

            return wrapper
        except Exception as e:
            self.logger.error(f"Error occurred in {func.__name__}: {str(e)}")
            raise e
        
    def time_decorator(self, func):
        """
        计时装饰器，用于记录函数的执行时间

        参数:
        - func: 要装饰的函数

        返回:
        - 装饰后的函数
        """
        try:
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()
                print(f"cost time: {end_time - start_time} seconds")
                return result
            
            return wrapper
        except Exception as e:
            raise e
