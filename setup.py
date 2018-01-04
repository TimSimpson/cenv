#!/usr/bin/env python
import setuptools

setuptools.setup(
    name='cenv',
    version='1.1.0',
    description='A manager for CGet environments',
    author='Tim Simpson',
    license='MIT',
    packages=setuptools.find_packages(exclude=['docs', 'test*']),
    install_requires=[
        'six',
        'typing>=3.6.2'
    ],
    entry_points={
        'console_scripts': [
            'cenv = cenv.cli:main'
        ]
    }
)
