# encoding: utf-8

from setuptools import setup

# Get current version
with open("VERSION.txt") as f:
    version = f.read().strip()


setup(name='bra_scraper',
      version=version,
      description=u'An interface for fetching statistical data from BRÅ. This is not an official service!',
      url='https://github.com/jensfinnas/bra_scraper',
      author='Jens Finnäs',
      author_email='jens.finnas@gmail.com',
      license='MIT',
      packages=['bra_scraper'],
      include_package_data=True,
      install_requires=[
            "lxml>=4.6.2",
            "python-dateutil>=2.8.1",
            "requests>=2.11.1",
      ],
      zip_safe=False)
