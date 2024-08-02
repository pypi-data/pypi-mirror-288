#!/usr/bin/env python
# coding=utf-8
import logging

class LogUtils:
    def __init__(self, log_file='app', log_level=logging.INFO):
        self.log_file = log_file
        self.log_level = log_level

        # 设置日志格式
        self.formatter = logging.Formatter(f'%(asctime)s - {log_file.split(".")[0]} - %(levelname)s - %(message)s')

        # 配置日志处理器
        self.file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        self.file_handler.setFormatter(self.formatter)

        # 配置控制台日志处理器
        self.console_handler = logging.StreamHandler()
        self.console_handler.setFormatter(self.formatter)

        # 获取根日志记录器并添加处理器
        self.logger = logging.getLogger()
        self.logger.setLevel(self.log_level)
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.console_handler)

    def get_logger(self):
        return self.logger

