# setup.py

from setuptools import setup, find_packages

setup(
    name='firmpriori',
    version='0.1.1',
    author='SeabirdShore',
    author_email='3220105728@zju.edu.cn',
    description='A simple package that prints hello',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/hello_package',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
