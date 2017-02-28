from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='python-adventure-game',
    version='0.1.1',
    description='A simple text-based adventure game engine.',
    long_description=long_description,
    url='https://github.com/allanburleson/python-adventure-game',
    author='Allan Burleson',
    author_email='burleson.a@icloud.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Education :: Testing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='game text text-based adventure interactive-fiction',
    packages=find_packages(exclude='tests'),
    package_data={
        'pag': ['dictionary/*.txt']
    }
)
