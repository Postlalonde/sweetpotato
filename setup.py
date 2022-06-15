from os import path
from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="sweetpotato",
    url="https://github.com/greysonlalonde/sweetpotato",
    download_url="https://github.com/greysonlalonde/sweetpotato/v0.1-alpha.tar.gz",
    author="Greyson R. LaLonde",
    author_email="greyson.r.lalonde@gmail.com",
    packages=find_packages(),
    install_requires=[],
    version="v0.1-alpha",
    license="MIT",
    description="React-native development for python users",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
)