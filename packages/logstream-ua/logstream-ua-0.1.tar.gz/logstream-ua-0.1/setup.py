from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1'
DESCRIPTION = 'Logger Tool'

# Setting up
setup(
    name="logstream-ua",
    version=VERSION,
    author="Bohdan Terskow",
    author_email="bohdanterskow@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    url='https://github.com/gods-created/logstream-ua',
    packages=find_packages(),
    install_requires=['loguru'],
    keywords=['python', 'logs', 'loguru', 'log', 'logstream', 'error', 'debug', 'info', 'fatal', 'warning'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
