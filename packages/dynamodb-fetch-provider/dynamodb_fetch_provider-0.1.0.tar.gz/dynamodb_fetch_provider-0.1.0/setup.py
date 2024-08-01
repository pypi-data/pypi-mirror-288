from setuptools import setup, find_packages

setup(
    name='dynamodb-fetch-provider',
    version='0.1.0',
    description='Custom Fetch Provider for DynamoDB',
    packages=find_packages(),
    install_requires=[
        'boto3',
        'opal-common',
        'cachetools',
        'pydantic',
        'flask'
    ],
)
