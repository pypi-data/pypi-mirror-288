import os

from setuptools import setup, find_packages

cscript = 'datamanwithvan=datamanwithvan.datamanwithvan:datamanwithvan_entry'

setup(
    name='datamanwithvan',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        # Add your dependencies here
        "hdfs",
        "impyla",
        "azure-storage-file-datalake",
        "dynaconf",
        "SQLAlchemy",
        "pyodbc",
        "dask",
        "boto3"
    ],
    entry_points={
        'console_scripts': [
            # Add command line scripts here
            cscript,
        ],
    },
    author='Evangelos Papakirykou',
    author_email='vpapakir@gmail.com',
    description="A distributed, parallel data"
                "replication engine that caters to various "
                "source/target system combinations "
                "and complex corporate environments.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/vpapakir/datamanwithvan',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
