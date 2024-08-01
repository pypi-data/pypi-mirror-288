from distutils.core import  setup
import setuptools
packages = ['yoltv8']# 唯一的包名，自己取名
setup(name='malaria',
	version='1.0.2',
	author='czc',
    packages=packages,
    package_dir={'requests': 'requests'},)
