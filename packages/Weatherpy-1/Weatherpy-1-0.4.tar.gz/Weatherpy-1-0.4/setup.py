from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.4'
DESCRIPTION = 'Python Wrapper For Weather API'
LONG_DESCRIPTION = 'A package that allows you to get the weather of any city in the world with a simple python function and it also gives you the future forecast of the city'

# Setting up
setup(
    name="Weatherpy-1",
    version=VERSION,
    author="Deep Shah",
    author_email="dpshah2307@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'weather', 'weather api', 'weather forecast', 'weatherpy'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)