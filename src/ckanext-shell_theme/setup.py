from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
    name='ckanext-shell_theme',
    version=version,
    description="ckan shell theme",
    long_description='''
    ''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Luke Chisholm',
    author_email='luke.chisholm6@gmail.com',
    url='http://opengovgear.com/',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.shell_theme'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points='''
        [ckan.plugins]
	shell_theme=ckanext.shell_theme.plugin:ShellThemePlugin
        # Add plugins here, e.g.
        # myplugin=ckanext.shell_theme.plugin:PluginClass
    ''',
)
