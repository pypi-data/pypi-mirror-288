from setuptools import setup, find_packages
from os.path import dirname, join

dir = dirname(__file__)
with open(join(dir, 'README.md'), 'r') as readme:
    long_description = readme.read()

setup(
    name='retroyaml',
    version='0.0.2',
    license='MIT',
    license_files = ('LICENSE',),
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="retrontology",
    author_email='retrontology@gmail.com',
    package_dir={'': 'src'},
    url='https://github.com/retrontology/retroyaml',
    keywords='yaml dict',
    install_requires=['pyyaml'],
)