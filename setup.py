# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()

setup(
    name = 'django-push',
    version = '0.1',
    url = 'http://github.com/brutasse/django-push',
    license = 'BSD',
    description = 'PubSubHubbub (PuSH) support for Django',
    long_description = read('README.rst'),

    author = 'Bruno Renié',
    author_email = 'bruno@renie.fr',

    packages = find_packages('src'),
    package_dir = {'': 'src'},

    install_requires = ['setuptools'],

    classifiers = [
        ## FIXME
    ],
)
