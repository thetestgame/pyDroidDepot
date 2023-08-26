try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from pathlib import Path
repository_directory = Path(__file__).parent
long_description = (repository_directory / "README.md").read_text()

setup(
    name='pyDroidDepot',
    description="Module for controlling droids built and purchased at the Droid Depot in Disney's Galaxys Edge",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    version='1.0.3',
    author='Jordan Maxwell',
    maintainer='Jordan Maxwell',
    url='https://github.com/thetestgame/pyDroidDepot',
    packages=['droiddepot'],
    classifiers=[
        'Programming Language :: Python :: 3',
    ])