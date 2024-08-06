#!/usr/bin/env python
from setuptools import find_packages, setup


setup(
    name='ogialibs',
    version="0.1.1",
    description=(
        "Common Python methods for OGIA"
        ),
    long_description='README.md',
    packages=find_packages(exclude=['sandbox*', 'tests*']),
    include_package_data=True,
    install_requires=[
        'geopandas>=0.13',
        'pyarrow',
    ],
)
