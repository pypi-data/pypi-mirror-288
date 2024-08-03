
from distutils.core import setup
from setuptools import find_packages

with open("README.MD", "r") as f:
  long_description = f.read()

setup(name='package_sample',
      version='0.0.2',
      description='A small example package',
      long_description=long_description,
      author='glsite.com',
      author_email='admin@glsite.com',
      url='',
      install_requires=[],
      license='MIT License',
      packages=["package_sample"],
      platforms=["Windows-x86_64"],
      python_requires='>=3.7',
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Programming Language :: Python :: 3.12',
          'Programming Language :: Python :: 3.13',
          'Topic :: Software Development :: Libraries'
      ],
      )

