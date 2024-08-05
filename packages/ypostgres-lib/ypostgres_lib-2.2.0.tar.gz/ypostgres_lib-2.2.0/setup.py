from setuptools import setup, find_packages

setup(
    name='ypostgres_lib',
    version='2.2.0',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here if any
    ],
    author='yactouat',
    author_email='yactouat@yactouat.com',
    description='helper functions for when I need talk to Postgres',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yactouat/ypostgres_lib',
    license='MIT',
)
