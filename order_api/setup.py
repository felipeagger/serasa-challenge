from setuptools import find_packages, setup

__version__ = '1.0.0'
__description__ = 'Orders API'
__long_description__ = 'Micro-Service for Orders using Flask'
__author__ = 'Felipe Alves'

testing_extras = [
    'pytest',
    'pytest-cov',
]

setup(
    name='order_api',
    author=__author__,
    license='MIT',
    description=__description__,
    long_description=__long_description__,
    packages=find_packages(),
    include_package_data=True,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    extras_require={
        'testing': testing_extras,
    },
)