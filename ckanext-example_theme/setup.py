from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(
    name='ckanext-example_theme',
    version=version,
    description="The example theme extension from CKAN theming tutorial",
    long_description='''
    ''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Jared Brown',
    author_email='jaredbrown79@gmail.com',
    url='www.opengovgear.com',
    license='GNU Affero GPL',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.example_theme'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points='''
        [ckan.plugins]
        # Add plugins here, e.g.
        # myplugin=ckanext.example_theme.plugin:PluginClass
    ''',
)
