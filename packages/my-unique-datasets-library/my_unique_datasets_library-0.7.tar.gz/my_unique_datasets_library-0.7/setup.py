# setup.py

from setuptools import setup, find_packages

setup(
    name='my_unique_datasets_library',  # Make sure this is unique
    version='0.7',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pandas',
    ],
    description='A library that provides predefined datasets.',
    author='ravishankar',
    author_email='your.email@example.com',
    keywords=['datasets', 'iris', 'data science'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package_data={
        'my_datasets': ['/home/ravi/Desktop/datasets/my_datasets/data/Iris.csv','/home/ravi/Desktop/datasets/my_datasets/data/flight_data_2018_2024.csv'],
    },
)

