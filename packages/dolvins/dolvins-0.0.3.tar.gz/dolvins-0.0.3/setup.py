from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.3'
DESCRIPTION = "Dolvin's Math and Stats Library"
LONG_DESCRIPTION = 'Mathematical, statistical, and probabilitic tools for Distribution Analysis, Linear Algebra, Calculus, Probability, and more'

# Setting up
setup(
    name="dolvins",
    version=VERSION,
    author="Landon Dolvin",
    author_email="landondolvin@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['psutil', 'numpy', 'pandas', 'tqdm', 'scipy'],
    keywords=['python', 'distributions', 'probability', 'linear algebra', 'statistics', 'mathematics'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)