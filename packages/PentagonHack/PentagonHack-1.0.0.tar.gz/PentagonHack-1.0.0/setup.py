from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
	name='PentagonHack',
	version='1.0.0',
	author='ALhorm',
	author_email='gladkoam@gmail.com',
	description='Library for hacking the Pentagon.',
	long_description=readme(),
	long_description_content_type='text/markdown',
	packages=find_packages(),
	install_requires=['rich>=13.0.0'],
	classifiers=[
	    'Programming Language :: Python :: 3.11',
	    'License :: OSI Approved :: MIT License',
	    'Operating System :: OS Independent'
  	],
  	keywords='hack hacking pentagon python',
  	python_requires='>=3.7.0'
)
