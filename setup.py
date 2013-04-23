#!/usr/bin/env python

from distutils.core import setup

externalRequirements = [
	'path.py (>=3.0)',
]

setup(name = "odwcore",
      version = "1.0.0",
      description = 'Manifest system',
      author = 'ODW',
      author_email = 'td@odw.com.cn',
      url = '',
      long_description = open('README.md').read(),
      
      # as per: http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers = [
        "Development Status :: 4 - Beta",
        "Natural Language :: Chinese (Simplified)",
        "Operating System :: Microsoft :: Windows",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
      ],
       
      package_dir = {
        'odwcore': 'src/odwcore',
      },
        
      packages = [
      	'odwcore',
        'odwcore.system',
        'odwcore.system.user',
      ],

      requires = externalRequirements,

)
