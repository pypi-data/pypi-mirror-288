from setuptools import setup, find_packages

setup(
    name='durationsense',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'durationsense=durationsense.main:main',
        ],
    },
)
