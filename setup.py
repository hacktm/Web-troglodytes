from setuptools import setup, find_packages


setup(
    name='Photodrop',
    url='git@github.com:hacktm/web-troglodytes',
    version='0.1',
    install_requires=[
        'pillow',
        'boto',
        'ExifRead == 1.4.2',
        'Django <1.7',
        'django-storages',
        'django-tastypie',
    ],
    test_requires=[
        'mock',
    ]
    # entry_points={
    #     'console_scripts': [''],
    # }
)
