import os
from setuptools import setup
from io import open

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, "simplgmail", '__version__.py'), 'r', encoding='utf-8') as f:
    exec(f.read(), about)

with open('README.rst', 'r', encoding='utf-8') as f:
    readme = f.read()

with open('HISTORY.rst', 'r', encoding='utf-8') as f:
    history = f.read()

setup(name=about["__title__"],
      version=about["__version__"],
      description=about["__description__"],
      long_description=readme + '\n\n' + history,
      url=about["__url__"],
      download_url="https://github.com/liamcryan/simplgmail/archive/{}.tar.gz".format(about["__version__"]),
      license=about["__license__"],
      author=about["__author__"],
      author_email=about["__author_email__"],
      packages=[about["__title__"]],
      install_requires=["selenium"],
      keywords="simple gmail automatic app password two step authentication",
      classifiers=["Development Status :: 2 - Pre-Alpha",
                   "Intended Audience :: Developers",
                   "Programming Language :: Python",
                   "Programming Language :: Python :: 3.5"]
      )
