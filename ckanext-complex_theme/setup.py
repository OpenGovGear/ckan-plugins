from setuptools import setup, find_packages
import sys, os

version = '0.1'
#adding some bs to prove mike wrong
setup(
    name='ckanext-complex_theme',
    version=version,
    description="complex theme",
    long_description='''
    ''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='OpenGov Gear',
    author_email='luke.chisholm@gmail.com',
    url='opengovgear.com',
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
	complex_theme=ckanext.complex_theme.plugin:ComplexThemePlugin
        # Add plugins here, e.g.
        # myplugin=ckanext.complex_theme.plugin:PluginClass
    ''',
)
