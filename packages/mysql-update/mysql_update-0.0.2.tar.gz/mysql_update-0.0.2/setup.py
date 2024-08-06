from distutils.core import setup
# import setuptools

packages = ['mysql_update']
setup(name='mysql_update',
      version='0.0.2',
      author='xigua, ',
      author_email="2587125111@qq.com",
      long_description='''
      mysql 数据更新, 移除冗余数据。
      ''',
      packages=packages,
      package_dir={'requests': 'requests'},
      license="MIT",
      python_requires='>=3.6',
      )
