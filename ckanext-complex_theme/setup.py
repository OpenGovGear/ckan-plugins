from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
    name='ckanext-complex_theme',
    version=version,
    description="complex theme",
    long_description='''
    ''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='mike',
    author_email='',
    url='',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.complex_theme'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points='''
        [ckan.plugins]
        # Add plugins here, e.g.
        complex_theme=ckanext.complex_theme.plugin:ComplexThemePlugin
    ''',
)
