try:
  from setuptools import setup, find_packages
except ImportError:
  from distutils.core import setup


setup(name='Repeat Finder',
  version='1.0',
  description='It downloads your top Spotify tracks!',
  author='Farooq Ansari',
  author_email='farooq73a@gmail.com',
  packages = find_packages(),       
  install_requires = ['youtube_dl','spotipy','pydub'],
  )