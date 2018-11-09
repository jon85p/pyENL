#!/usr/bin/env python3

from setuptools import setup

from pip.req import parse_requirements
from distutils.core import Extension

# requirements = parse_requirements('requirements.txt', session=False)
#
# requires = []
# for item in requirements:
#     # we want to handle package names and also repo urls
#     if getattr(item, 'url', None):  # older pip has url
#         links.append(str(item.url))
#     if getattr(item, 'link', None):  # newer pip has link
#         links.append(str(item.link))
#     if item.req:
#         requires.append(str(item.req))

setup(name='pyENL',
      version='0.1a',
      license='MIT',
      description='Engineering nonlinear system equations solver',
      author='Jhon Valencia',
      author_email='jhonvalencia314@gmail.com',
      url='https://jon85p.github.io/pyENL/',
      # install_requires=requires,
      entry_points={'console_scripts': [
          'pyENL-cli=entrada:main', 'pyENL=pyENL.main']},
      )
