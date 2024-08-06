
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="coingecko_exporter",  
    version="0.1.9",
    description="A package to export bulk data from the CoinGecko API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Matt Maximo",
    author_email="matt@pioneerdigital.org",
    url="https://github.com/MattMaximo/coingecko_exporter",
    packages=find_packages(),
    install_requires=[
        "httpx",
        "pandas",
        "duckdb",
        "aiolimiter",
        "httpx",
        "pyarrow",
        "fastparquet",
        "boto3",

    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["coingecko", "crypto", "data", "api", "exporter"],
    python_requires='>=3.6',
)