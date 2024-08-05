from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.1.1'
DESCRIPTION = 'APIFixer is a Python class that automatically starts an API server, checks its routes, generates documentation based on the OpenAI API, and tests API endpoints to fix bugs and improve API performance.'

# Setting up
setup(
    name="APIFixer",
    version=VERSION,
    author="Bohdan Terskow",
    author_email="bohdanterskow@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    url='https://github.com/gods-created/APIFixer',
    packages=find_packages(),
    install_requires=['loguru', 'openai', 'requests', 'uvicorn'],
    keywords=['python', 'logs', 'api', 'fastapi', 'docs', 'ai', 'openai'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)