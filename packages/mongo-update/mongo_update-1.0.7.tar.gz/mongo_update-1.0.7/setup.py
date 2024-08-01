from distutils.core import setup
# import setuptools

packages = ['mongo_update']
setup(name='mongo_update',
      version='1.0.7',
      author='xigua, ',
      author_email="2587125111@qq.com",
      long_description='''
      mongodb数据更新。
      ''',
      packages=packages,
      package_dir={'requests': 'requests'},
      license="MIT",
      python_requires='>=2.7',
      )
