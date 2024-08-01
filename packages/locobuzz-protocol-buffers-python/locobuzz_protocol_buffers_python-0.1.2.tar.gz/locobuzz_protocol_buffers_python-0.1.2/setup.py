import os

from Cython.Build import cythonize
from setuptools import setup, find_packages


def find_python_files(directory):
    return [os.path.join(root, file)
            for root, dirs, files in os.walk(directory)
            for file in files
            if file.endswith('.py') and not file.startswith('__init__')]


setup(
    name='locobuzz_protocol_buffers_python',
    version='0.1.2',
    packages=find_packages(),
    ext_modules=cythonize(find_python_files("locobuzz_protocol_buffer_python")),
    install_requires=[
        'Cython',
        'grpcio',
        'grpcio-tools',
        'protobuf'
    ],
    author='Sheikh Muhammed Shoaib',
    author_email='shoaib.sheikh@locobuzz.com',
    description='This package helps in to build the protocol buffers',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/LocoBuzz-Solutions-Pvt-Ltd/locobuzz_python_configuration',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
