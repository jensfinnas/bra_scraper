# encoding: utf-8

from setuptools import setup



setup(name='bra_scraper',
      version='0.1.7',
      description=u'An interface for fetching statistical data from BRÅ. This is not an official service!',
      url='https://github.com/jensfinnas/bra_scraper',
      author='Jens Finnäs',
      author_email='jens.finnas@gmail.com',
      license='MIT',
      packages=['bra_scraper'],
      include_package_data=True,
      install_requires=[
            "requests==2.20.0",
            "wsgiref==0.1.2"
      ],
      zip_safe=False)
