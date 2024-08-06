from distutils.core import setup
# import setuptools

packages = ['mdbsql']
setup(name='mdbsql',
      version='0.0.1',
      author='xigua, ',
      author_email="2587125111@qq.com",
      long_description='''
      mongodb/mysql 数据库更新, 移除冗余数据。
      ''',
      packages=packages,
      package_dir={'requests': 'requests'},
      license="MIT",
      python_requires='>=3.6',
      )
