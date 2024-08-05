from io import open
from setuptools import setup

# KiryxaTech (c) 2024

version = "0.1"

with open('README.md', encoding='utf-8') as f:
    long_discription = f.read()

setup(
    name="exnums",
    version=version,

    author="KiryxaTech",
    author_email="kiryxatech@gmail.com",

    description=("Exnums are libraries for expanding the user's capabilities in Python"),
    long_description=long_discription,
    long_description_content_type="text/markdown",

    url="https://github.com/KiryxaTechDev/exnums",
    download_url=f"https://github.com/KiryxaTechDev/exnums/archive/refs/tags/{version}.zip",

    packages=['exnums'],

    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12"
    ]
)