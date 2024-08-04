from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='pylibupdator',
    version='0.2.0',
    author='Dark Angel',
    author_email='jrayvon@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'pylibupdate=pythonlibupdate.pylibupdator:main',
        ],
    },
    description='A tool to check for newer versions of installed Python packages',
    long_description=long_description,
    long_description_content_type="text/markdown",
)