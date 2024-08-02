from setuptools import find_packages, setup

with open('./README.md', 'r', encoding='utf-8') as fh:
  readme = fh.read()

setup(
  name='WdSql',
  version='0.0.4',
  description='Funciones basicas para bases de datos relacionales',
  long_description=readme,
  long_description_content_type='text/markdown',
  author='Pedro Jesús Pérez Hernández',
  author_email='pedrojesus.perez@welldex.mx',
  url='https://gitwell.gwldx.com:2443/python_libraries/wsql',
  install_requires=[
    'mysql-connector',
    'pyodbc',
    'wellog',
  ],
  license='MIT',
  packages=find_packages(),
  include_package_data=True,
  python_requires='>=3.8'
)