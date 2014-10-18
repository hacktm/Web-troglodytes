from setuptools import setup, find_packages


setup(
    name='Photodrop',
    url='git@github.com:hacktm/web-troglodytes',
    version='0.1',
    install_requires=[
        'Django <1.7',
        'ExifRead == 1.4.2',
    ],
    entry_points={
        'console_scripts': [],
    }
)
