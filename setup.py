'''
Created on Jun 28, 2010

@author: brianjinwright
'''
from setuptools import setup, find_packages
 
version = '0.1.0'
 
LONG_DESCRIPTION = """
=====================================
RestXL (python REST framework)
=====================================

This project exists to make it easier to create REST clients that are also
very easy to understand. 

The cores of this project are requests, url variables, headers, and RestXLers.
"""
 
setup(
    name='restxl',
    version=version,
    description="This project exists to make it easier to create REST clients that are also"
    "very easy to understand.",
    long_description=LONG_DESCRIPTION,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Environment :: Web Environment",
    ],
    keywords='rest,django,declarative,api,web',
    author='Brian Jinwright',
    author_email='restxl@ipoots.com',
    url='http://github.com/bjinwright/restxl',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)