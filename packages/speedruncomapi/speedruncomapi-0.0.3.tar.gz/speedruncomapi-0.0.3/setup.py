from setuptools import setup, find_packages
from pathlib import Path

VERSION = '0.0.3'
DESCRIPTION = 'A Python API wrapper for Speedrun.com'

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="speedruncomapi",
    version=VERSION,
    author="Sallie Lay",
    author_email="mail@neuralnine.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'wrapper', 'api', 'speedrun'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
