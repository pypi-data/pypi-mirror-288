from setuptools import setup
from codecs import open
from os import path
package_name = "cututil"
root_dir = path.abspath(path.dirname(__file__))


def _requirements():
    return [name.rstrip() for name in open(path.join(root_dir, 'requirements.txt')).readlines()]


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()
setup(
    name=package_name,
    version='0.0.5',
    description='Redesigned the cut command to be more convenient.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ntk01/command-util',
    author='ntk01',
    author_email='n.taku.law@gmail.com',
    license='MIT',
    keywords='python,cut,command,utility',
    packages=[package_name],
    install_requires=_requirements(),
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
