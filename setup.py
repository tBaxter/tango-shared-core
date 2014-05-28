# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('docs/requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='tango-shared-core',
    version='0.7.4',
    author=u'Tim Baxter',
    author_email='mail.baxter@gmail.com',
    description='Tango shared/core functionality.',
    long_description=open('README.md').read(),
    url='https://github.com/tBaxter/tango-shared-core',
    license='LICENSE',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    dependency_links = [
        'http://github.com/tBaxter/django-voting/tarball/master#egg=tango-voting',
    ]
)
