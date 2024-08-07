from setuptools import setup, find_packages

setup(
    name='vnd_arxml_shortname',
    version='0.0.3',
    packages=find_packages(),
    install_requires=[],
    author='HJANSS16',
    author_email='HJANNS16@volvocars.com',
    description='Library for parsing and changing the names of arxml files',
    url='https://github.com/volvo-cars/vnd_arxml_shortname',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)