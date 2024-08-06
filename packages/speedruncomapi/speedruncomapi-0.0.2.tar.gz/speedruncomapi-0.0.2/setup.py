from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'A python api wrapper for Speedrun.com'

# Setting up
setup(
    name="speedruncomapi",
    version=VERSION,
    author="Sallie Lay",
    author_email="<mail@neuralnine.com>",
    description=DESCRIPTION,
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