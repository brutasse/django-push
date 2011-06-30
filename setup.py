# -*- coding: utf-8 -*-
import os
from distutils.core import setup
from setuptools import find_packages

def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()

setup(
    name='django-push',
    version='0.4',
    author='Bruno Renié',
    author_email='bruno@renie.fr',
    url='http://github.com/brutasse/django-push',
    license='BSD',
    description='PubSubHubbub (PuSH) support for Django',
    long_description=read('README.rst'),
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'feedparser'
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
    ],
)
