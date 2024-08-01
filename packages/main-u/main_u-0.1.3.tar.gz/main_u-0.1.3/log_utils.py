#!/usr/bin/env python
# coding=utf-8
import logging

class LoggingUtils:
    def __init__(self, log_name='app', log_level=logging.INFO):
        self.log_file = log_name + '.log'
        self.log_level = log_level

        # 设置日志格式
        self.formatter = logging.Formatter(f'%(asctime)s - {log_name} - %(levelname)s - %(message)s')

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

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)

    def debug(self, message):
        self.logger.debug(message)


if __name__ == '__main__':
    log = LoggingUtils('app', log_level=logging.INFO)
    # 使用示例
    log.info("这是一条信息日志1234")
    log.error("这是一条错误日志12")