from setuptools import setup, find_packages
import os, sys
#import setuptools 
#from numpy.distutils.core import setup, Extention 

with open("README.md", "r") as fh:
     long_description = fh.read()


if sys.version_info >= (3,7):
    install_requires_py_ver=[
    "numpy>=1.21",
    "scipy>=1.2.1",
    "matplotlib==3.3.1",
    "formlayout==1.2.0",
    "PyQt5>=5.15.4",
    "pathos>=0.2.5"]
else:
    install_requires_py_ver=[
    "numpy>=1.16.6",
    "scipy>=1.2.1",
    "matplotlib==3.2.1",
    "formlayout==1.2.0",
    "PyQt5==5.9.2",
    "pathos>=0.2.5"]


setup(
name='DetExCal',  
version='0.04',
scripts=['scripts/DetExCal'],
author="Trifon Trifonov",
author_email="trifonov@mpia.de",
description="This is a simple exposure time calculator for CCD and CMOS detectors with a GUI interface: 'DetExCal'",
long_description=long_description,
long_description_content_type="text/markdown",
url="https://github.com/3fon3fonov/DetExCal",
#packages=['exostriker'],
packages=find_packages(),
include_package_data = True,
classifiers=[
 "Programming Language :: Python :: 3",
 "License :: MIT License",
 "Operating System :: OS Independent",
],
install_requires=install_requires_py_ver,
extras_requires={
            'pexpect>=4.8.0':['pexpect']},    

license="MIT"
 )
 
