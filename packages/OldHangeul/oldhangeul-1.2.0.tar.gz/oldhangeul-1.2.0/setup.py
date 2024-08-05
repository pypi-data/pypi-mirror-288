from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(name='OldHangeul', 

version='1.2.0',

description='Program with functions for manipulation of old Korean script, including Unicode normalization and jamo separation.',

long_description = long_description,

long_description_content_type='text/markdown',

author='go00od',

author_email='go00od@naver.com',

url='https://github.com/go00ood/OldHangeul',

py_modules=['old_hangeul'], 

python_requires='>=3',

packages=find_packages(exclude=[]),

package_data={'OldHangeul': ['data/*.pickle']},

)