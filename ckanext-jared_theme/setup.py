from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
    name='ckanext-jared_theme',
    version=version,
    description="Jared's attempt at a simple theme",
    long_description='''
    ''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Jared Brown',
    author_email='jaredbrown79@gmail.com',
    url='www.opengovgear.com',
    license='Affero',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.jared_theme'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points='''
        [ckan.plugins]
        # Add plugins here, e.g.
        jared_theme=ckanext.jared_theme.plugin:JaredThemePlugin
    ''',
)
