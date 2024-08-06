from setuptools import setup, find_packages

VERSION = '1.0.2'

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(name='fuelai-python-sdk',
      version=VERSION,
      description='Fuel AI Python SDK',
      author='Fuel AI',
      author_email='technology@fuelhq.ai',
      url='https://github.com/FuelHQ-Public/fuelai-python',
      license='MIT',
      long_description=long_description,
      long_description_content_type='text/markdown',
      python_requires='>=3.6',
      packages=find_packages(exclude=['tests', 'tests.*']),
      install_requires=requirements,
      tests_require=['pytest >= 6.0.0'])
