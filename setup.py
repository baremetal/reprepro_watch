#!/usr/bin/env python 

from distutils.core import setup 

setup(name = 'reprepro_watch', 
      version = '0.1', 
      description = "An inotify-based tool to rebuild an APT repository",
      author = "Roberto Aguilar", 
      author_email = "roberto.c.aguilar@gmail.com", 
      packages = ['reprepro'], 
      long_description=open('README.md').read(),
      # http://stackoverflow.com/questions/3472430/how-can-i-make-setuptools-install-a-package-thats-not-on-pypi
      dependency_links = ["http://github.com/rca/clint.git@c56d059fe6d9909a088f70f3df8d44810e5a9e75#egg=clint-dev"],
      install_requires= [
          "clint",
          "nose==1.2.1",
          "pyinotify==0.8.9",
          "sh==1.07",
          "supervisor==3.0a8",
      ],
      scripts=['scripts/reprepro_watch'],
      url='http://github.com/rca/reprepro_watch',
      license='LICENSE.txt'
)
