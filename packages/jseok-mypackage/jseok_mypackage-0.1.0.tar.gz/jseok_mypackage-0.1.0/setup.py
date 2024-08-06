# setup.py
from setuptools import setup, find_packages
setup(
    name="jseok_mypackage",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="julim",
    author_email="whizkid00@gmail.com",
    description="A simple example package",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/koesnuj/python_study",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
