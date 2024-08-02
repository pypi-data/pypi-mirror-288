# -*- coding:utf-8 -*-
from setuptools import setup, find_packages
from pySingleFile import __version__

with open("readme.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="pySingleFile",
    version=__version__,
    author="ordar",
    author_email="w666q@qq.com",
    description="Python Implementation of SingleFile",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="BSD",
    keywords="SingleFile",
    url="https://github.com/MrWQ/pySingleFile",
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'lxml',
        'requests',
        'cssselect',
        'DownloadKit>=2.0.0',
        'websocket-client',
        'click',
        'tldextract',
        'psutil'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
        ],
    },
)
