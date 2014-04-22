from distutils.core import setup

setup(
    name='JobRunner',
    version='0.1.0',
    author='Eero Torri',
    author_email='et@torri.be',
    packages=['runner'],
    scripts=['bin/default','bin/couchrun'],
    #url='http://pypi.python.org/pypi/TowelStuff/',
    license='LICENSE.txt',
    description='Run commands and get their output reported to couchdb or mq.',
    long_description=open('README.txt').read(),
    install_requires=[
        "couchdb",
    ],
)
