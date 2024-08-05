# coding: utf-8

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='tinymoss',
    version='0.0.1',
    description='Tiny Moss for python3', 
    author='xuwh',  
    author_email='xuwhdev@gmail.com',
    url='https://',
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
)