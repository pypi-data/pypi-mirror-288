"""
Setup file for user_utils package
"""
from setuptools import setup, find_packages

setup(
    name='user-vpetrov',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'pydantic',
        'sqlalchemy',
        'alembic',
        'python-dateutil'
    ]
)