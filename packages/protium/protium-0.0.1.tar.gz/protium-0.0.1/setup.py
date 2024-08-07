# mypackage/setup.py

from setuptools import setup, find_packages

setup(
    name="protium",
    version="0.0.1",
    author="Haohui",
    author_email="harveyquery@gmail.com",
    description="A simple example package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Mile-Away/PROTIUM",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
