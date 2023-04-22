try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

long_description = """
Module for controlling droids built and purchased at the Droid Depot in Disney's Galaxys Edge over Bleutooth
"""

setup(
    name='pydroid',
    description="Module for controlling droids built and purchased at the Droid Depot in Disney's Galaxys Edge",
    long_description=long_description,
    license='MIT',
    version='1.0.0',
    author='Jordan Maxwell',
    maintainer='Jordan Maxwell',
    url='https://github.com/thetestgame/pydroid',
    packages=['droid'],
    classifiers=[
        'Programming Language :: Python :: 3',
    ])