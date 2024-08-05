from setuptools import setup
import os

with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='config-server-client-python',
      version='1.0.1',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Jayant Reddy',
      url='https://github.com/jayantreddy181198/config-server-client-python',
      description='Streamline configuration management by fetching and updating configurations from a Spring Cloud Config Server in Python.',
      packages=['src'],
      author_email='jayantreddy181198@gmail.com',
      zip_safe=False)
