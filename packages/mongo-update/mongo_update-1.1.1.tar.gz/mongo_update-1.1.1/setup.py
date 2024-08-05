from distutils.core import setup
# import setuptools

packages = ['mongo_update']
setup(name='mongo_update',
      version='1.1.1',
      author='xigua, ',
      author_email="2587125111@qq.com",
      long_description='''
      mongodb 数据更新, 移除冗余数据。
      ''',
      packages=packages,
      package_dir={'requests': 'requests'},
      license="MIT",
      python_requires='>=3.6',
      )
