#!/usr/bin/env python
# coding=utf-8
'''
Author: waton
Date: 2024-08-01 09:32:15
LastEditTime: 2024-08-02 09:59:32
FilePath: \my_plugin\setup.py
Description:6
'''

#!/usr/bin/env python
# coding=utf-8

from setuptools import setup

setup(
    name='main_u',
    version='0.1.6',
    author='linshenghua',
    author_email='780141734@qq.com',
    install_requires=['pymysql', 'sshtunnel==0.4.0', 'PyYAML==6.0.1', 'xlrd==1.2.0', 'xlwt==1.3.0'],
    description=
    """
    some moudles for python user
    for example: file_utils: import file_utils or from file_utils import *
    """,
    py_modules=['file_utils', 'db_utils', 'log_utils', 'decorator_utils'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)