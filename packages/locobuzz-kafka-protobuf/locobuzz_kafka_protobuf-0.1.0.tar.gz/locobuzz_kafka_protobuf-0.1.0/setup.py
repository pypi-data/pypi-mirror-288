import os

from Cython.Build import cythonize
from setuptools import setup, find_packages

with open('README.md', 'r') as file:
    content = file.read()


def find_python_files(directory):
    return [os.path.join(root, file)
            for root, dirs, files in os.walk(directory)
            for file in files
            if file.endswith('.py') and not file.startswith('__init__')]


setup(
    name="locobuzz_kafka_protobuf",
    version='0.1.0',
    packages=find_packages(),
    ext_modules=cythonize(find_python_files("locobuzz_kafka_protobuf")),
    install_requires=[
        'Cython',
        'confluent_kafka',
        'protobuf'
    ],
    author="Shweta Singh",
    author_email="shweta.singh@locobuzz.com",
    description="uses of protocol buffer for kafka",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/my_package",
    test_suite='tests',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'protobuf_kafka=protobuf_kafka.__main__:main'
        ]
    },
)
