from setuptools import setup, find_packages

setup(
    name='cohesion_measuring',
    version='0.1',
    description='A Python library for calculating SCOM cohesion value for a microservice',
    author='Bianca Kasper',
    packages=find_packages(),
    long_description=open("readme.md").read(),
    long_description_content_type="text/markdown"
)
