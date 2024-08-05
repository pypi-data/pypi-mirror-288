# setup.py

from setuptools import setup, find_packages

setup(
    name="binaexperts",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author="Mohammad Javad Rahimi",
    author_email="manre80@gmail.com",
    description="SDK for Bina Experts to access BinaExperts' datasets and conduct ML projects",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
