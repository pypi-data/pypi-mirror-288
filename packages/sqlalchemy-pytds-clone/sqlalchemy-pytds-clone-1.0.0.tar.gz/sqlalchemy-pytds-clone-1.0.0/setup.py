import sys
import os
import re

if sys.version_info < (2, 6):
    raise Exception("SQLAlchemy TDS requires Python 2.6 or higher.")

from setuptools import setup

v = open(os.path.join(os.path.dirname(__file__), 'sqlalchemy_pytds', '__init__.py'))
VERSION = re.compile(r".*__version__ = '(.*?)'", re.S).match(v.read()).group(1)
v.close()

readme = os.path.join(os.path.dirname(__file__), 'README.rst')
requires = [
    'pytds-clone',
    'SQLAlchemy >= 2.0',
]

setup(name='sqlalchemy-pytds-clone',
      version=VERSION,
      description="sqlalchemy-pytds-clone",
      long_description=open(readme).read(),
      long_description_content_type='text/x-rst',
      license='MIT',
      platforms=["any"],
      packages=['sqlalchemy_pytds'],
      classifiers=[
      ],
      install_requires = requires,
      include_package_data=True,
      tests_require=['nose >= 0.11'],
      test_suite="nose.collector",
      entry_points={
         'sqlalchemy.dialects': [
              'mssql.pytds = sqlalchemy_pytds.dialect:MSDialect_pytds',
              ]
        }
)
