from os import path

import setuptools

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="bitdata",
    version="0.1.0",
    description="Tools for analyzing data on Bitcoin and Lightning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BITPoliTO/bitcoin-data-analysis",
    author="BitPolito",
    author_email="info.bitpolito@protonmail.com",
    license="MIT",
    packages=setuptools.find_namespace_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    include_package_data=True,
)
