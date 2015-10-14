# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('docs/requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='tango-shared-core',
    version='0.16.0',
    author=u'Tim Baxter',
    author_email='mail.baxter@gmail.com',
    description='Tango shared/core functionality.',
    long_description=open('README.md').read(),
    url='https://github.com/tBaxter/tango-shared-core',
    license='MIT',
    packages=find_packages(),
    zip_safe=False,
    install_requires=required,
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
)
