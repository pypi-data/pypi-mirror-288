from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="uzbekistanweather",
    version="0.0.1",
    description="bu worldweather kutubxonasi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Sino Farmonov",
    author_email="farmonovsino4@gmail.com",
    packages=find_packages(),
    requires=[
        "requests",
        "beautifulsoup4",
    ],
)