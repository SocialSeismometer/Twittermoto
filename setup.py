# https://python-packaging.readthedocs.io
from setuptools import setup

setup(name                 = 'Twittermoto',
      version              = '0.1',
      description          = 'Earthquake detection using twitter data.',
      url                  = 'https://github.com/twittermoto/twittermoto.git',
      author               = 'Jaime Liew',
      author_email         = 'jaimeliew1@gmail.com',
      license              = 'MIT',
      packages             = ['twittermoto'],
      install_requires     = ['pandas', 'numpy', 'importlib', 'click', 'tweepy'],
      zip_safe             = False,
      include_package_date = True,
      #entry_points         = {
    #    'console_scripts': ['twittermoto=twittermoto.cli:cli']},
)
