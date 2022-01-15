import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='mconv',
    version='1.0.4',
    description='A convert system for playing speed of audio and video files by ffmpeg',
    long_description=README,
    author='Peyman Najafi',
    url='https://github.com/peynaj/mediaConvertor',
    packages=find_packages(),
    include_package_data=True,
    scripts=['commands/mconv'],
    install_requires=[],
    classifiers=[
    ],
)
