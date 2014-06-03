from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
    name='ckanext-aggregator_theme',
    version=version,
    description="theme for civic.info",
    long_description='''
    ''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Hayden Waring',
    author_email='haydenwaring@gmail.com',
    url='',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.aggregator_theme'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points='''
        [ckan.plugins]
        # Add plugins here, e.g.
        aggregator_theme=ckanext.aggregator_theme.plugin:AggregatorThemeClass
    ''',
)
