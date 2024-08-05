# -*- coding: UTF-8 -*-
from setuptools import setup, find_packages

print(find_packages())
# 项目名称
NAME = "vbpip"
# 项目版本
VERSION = "0.0.1"
# 项目作者
AUTHOR = "PyDa5"
# 作者邮箱
AUTHOR_EMAIL = "1174446068@qq.com"
# 项目描述
DESCRIPTION = "基于pypi，类比pip，实现简单的vb包管理功能。"
# 项目的长描述，可以从 README 文件读取
with open('README.md', 'r', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()
# 项目的许可证
LICENSE = "MIT"
# 项目的分类
setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license=LICENSE,
    package_data={
        'vbpip': ['vbpip.py'],
    },
    entry_points={
        # 可以在此处指定命令行工具，会在scripts文件夹生成exe
        'console_scripts': [
            'vb = vbpip:main'
        ]
    },
)