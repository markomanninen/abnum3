try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import os

#python setup.py sdist upload

version = 'v0.1.1'

name = 'abnum3'

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), encoding="utf8").read()

setup(
  name = name,
  packages = [name],
  package_dir = {name: name},
  package_data = {
    name: ['*.py']
  },
  install_requires = [],
  version = version,
  description = 'Abnum 3 - Alphabetic numerals package including various letter value substituting systems from ancient times to modern artificial ones',
  long_description = read('README.md'),
  author = 'Marko Manninen',
  author_email = 'elonmedia@gmail.com',

  url = 'https://github.com/markomanninen/%s' % name,
  download_url = 'https://github.com/markomanninen/%s/archive/%s.tar.gz' % (name, version),
  keywords = ['python', 'jupyter notebook', 'ancient greek', 'isopsephy', 'text analysis'],
  platforms = ['any'],

  classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Lisp",
    "Topic :: Software Development :: Libraries",
  ]
)
