from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='datafaser',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.1.2',
    description='Data combiner and converter',
    long_description=long_description,
    url='https://github.com/korpiq/python-datafaser',
    author='Kalle Hallivuori',
    author_email='korpiq@iki.fi',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Interpreters',
        'Topic :: Text Processing :: Markup',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='data conversion',
    packages=find_packages(exclude=('test', 'test.*')),

    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'jsonschema >= 2.5.1',
        'PyYAML >= 3.11',
        'jinja2 >= 2.6',
    ],

    # $ pip install -e .[dev,test]
    extras_require={
        'dev': [],
        'test': ['nose','nose-cov >= 1.6'],
    },
    tests_require=['nose'],
    setup_requires=['wheel'],

    package_data={
        'datafaser': ['data/*'],
    },

    entry_points={
        'console_scripts': [
            'datafaser=datafaser.main:main',
        ],
    },
    test_suite = 'nose.collector',
)

