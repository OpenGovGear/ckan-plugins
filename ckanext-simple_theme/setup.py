from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
    name='ckanext-simple_theme',
    version=version,
    description="simple ckan theme",
    long_description='''
    ''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='opengov gear',
    author_email='luke.chisholm6@gmail.com',
    url='opengovgear.com',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.simple_theme'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points='''
        [ckan.plugins]
	simple_theme=ckanext.simple_theme.plugin:SimpleThemePlugin
        # Add plugins here, e.g.
        # myplugin=ckanext.simple_theme.plugin:PluginClass
    ''',
)
