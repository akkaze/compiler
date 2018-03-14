from distutils.core import setup
from setuptools import find_packages
setup(
    name='compiler',
    version='1.0',
    author='ankun.zheng',
    author_email='zhengankun@163.com',
    packages=find_packages(),#['compiler', 'compiler.frontend', 'compiler.ast', 'compiler.utils', 'compiler.parser', 'compiler.entity', 'compiler.type'],
    description='',
    long_description='',
)
