# setup.py
from setuptools import setup, find_packages

setup(
    name='my_middleware',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Flask>=2.0.0'
    ],
    description='A Flask middleware package to perform pre-checks before request execution.',
    author='Vishwaranjan Kumar',
    author_email='vishwaranjan.kumar@infoobjects.com',
    url='https://github.com/vishwaranjankumar2000/my_middleware',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
