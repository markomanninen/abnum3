try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import os

# python setup.py sdist upload
# pip install --no-cache-dir --upgrade abnum

version = 'v0.1.9'

name = 'abnum'

def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname), encoding="utf8").read()
    except:
        print("Could not read/open file: %s" % os.path.join(os.path.dirname(__file__), fname))
        return ''

setup(
  name = name,
  packages = [name],
  package_dir = {name: name},
  package_data = {
    name: ['*.py']
  },
  install_requires = ["remarkuple", "romanize3", "IPython", "pandas"],
  version = version,
  description = 'Abnum - Alphabetic numerals package including various letter value substituting systems from ancient times to modern artificial ones',
  long_description = read('README'),
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
    "Programming Language :: Python",
    "Topic :: Software Development :: Libraries",
  ]
)
