from setuptools import setup, find_packages
from os import path

working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='DataPrep_Kit_khater',
    version='18.12.99',
    url='https://github.com/Mahmoud-Khater/ElectroPi/blob/main/dataprep_kit.ipynb',
    author='Khater',
    author_email='mahmoudgamalkhater@gmail.com',
    description='This package aims to be a comprehensive toolkit for preprocessing datasets.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['pandas','numpy'],
)