from io import open
from setuptools import setup

with open('README.md', encoding='utf-8')as f:
    long_description = f.read()


long_description = '''This library is not that useful. Perhaps someday it will become great.'''

setup(
    name = "index_cmd",
        version = "0.1.1",
    authoers="сорока алексей" ,
    authoers_email="no",

descirpton = "It's empty here!!!",

    packages = ['index_cmd'],
    install_requires=['aiohttp', 'aiofiles'],

   classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)