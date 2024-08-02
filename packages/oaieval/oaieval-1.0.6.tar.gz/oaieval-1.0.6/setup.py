from setuptools import setup, find_packages
import os
import codecs

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

setup(
    name="oaieval",
    version="1.0.6",
    author="OpenAI",
    author_email="adam@openai.com",
    description="Test package for OpenAI evaluation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'oaieval=oaieval.main:main',  # 'oaieval' is the command, 'oaieval.main:main' specifies the function
        ],
    },
    keywords=['openai', 'evaluation', 'test'],
)
