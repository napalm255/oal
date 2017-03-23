#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup module."""

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'click==6.6',
    'ipaddress==1.0.17',
    'requests==2.11.1',
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='oal',
    version='0.4.0',
    description="Office 365 Address Lists",
    long_description=readme + '\n\n' + history,
    author="Brad Gibson",
    author_email='napalm255@gmail.com',
    url='https://github.com/napalm255/oal',
    packages=[
        'oal',
    ],
    package_dir={'oal':
                 'oal'},
    entry_points={
        'console_scripts': [
            'oal=oal.__main__:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="BSD license",
    zip_safe=False,
    keywords='oal',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
