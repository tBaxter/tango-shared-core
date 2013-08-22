# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='tango-shared-core',
    version='0.2',
    author=u'Tim Baxter',
    author_email='mail.baxter@gmail.com',
    packages=['tango_shared'],
    url='https://github.com/tBaxter/tango-shared-core',
    license='LICENSE',
    description='Tango shared/core functionality.',
    long_description=open('README.txt').read(),
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True
)
