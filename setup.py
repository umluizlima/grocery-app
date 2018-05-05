from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='grocery-app',
    version='0.0.1',
    description='A simple grocery list',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/umluizlima/grocery-app',
    author='Luiz Lima',
    author_email='umluizlima@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'gunicorn',
    ],
)
