# setup.py

from setuptools import setup, find_packages
import codecs
import os 

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()



setup(
    name='alig_seq_dist',
    version='0.1',
    description="A package for computing the distance of aligned sequences inside FASTA file",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'pandas',
        'numpy',
        'biopython',
        'IPython',
    ],
    extras_requires={"dev": ["pytest>=7.0","twine>=4.0.2"],
    },
    author='IMSI2024',
    author_email='jcevall1@asu.edu',
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    url='https://github.com/jcevall1/alig_seq_dist',
)
