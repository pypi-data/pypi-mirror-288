from setuptools import setup, find_packages

setup(
    name='whistlingduck', 
    version='0.2',
    description='Whistling Duck is a Python library for data quality exploration and validation, designed for small to medium-sized datasets. It is written using DuckDB.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Subha Saha',
    author_email='whistlingducklib@gmail.com',
    url='https://github.com/thewhistlingducklib/whistlingduck',

    install_requires=[
        'duckdb>=0.10.2',
        'pydantic>=2.8.2'
    ],
)