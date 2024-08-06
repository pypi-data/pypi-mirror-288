# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 11:19:46 2024

@author: 90545
"""

# setup.py

from setuptools import setup, find_packages

setup(
    name="my_similarity_package",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'nltk'
    ],
    setup_requires=['wheel'],
    description='A package for calculating cosine similarity between sentences',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    #url='https://github.com/yourusername/my_similarity_package',  # GitHub veya başka bir repo URL'si
    author='Your Name',
    author_email='your.email@example.com',
    license='MIT',
)
