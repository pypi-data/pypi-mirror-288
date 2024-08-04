from setuptools import setup, find_packages
import os

def find_pyc_files(directory):
    pyc_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.pyc'):
                pyc_files.append(os.path.join(root, file))
    return pyc_files

setup(
    name='safibase',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='Insolify',
    author_email='dev@insolify.com',
    description='A Python library for Safibase.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/insolify/safibase',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
