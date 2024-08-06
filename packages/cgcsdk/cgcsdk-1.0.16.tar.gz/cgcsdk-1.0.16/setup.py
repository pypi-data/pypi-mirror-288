import os
from dotenv import load_dotenv
from setuptools import setup, find_packages

with open("README.md", "r", encoding="UTF-8") as fh:
    long_description = fh.read()

load_dotenv("./cgc/.env")
MAJOR_VERSION = int(os.getenv("MAJOR_VERSION"))
MINOR_VERSION = int(os.getenv("MINOR_VERSION"))
RELEASE = int(os.getenv("RELEASE"))

VERSION_STRING = f"{RELEASE}.{MAJOR_VERSION}.{MINOR_VERSION}"

setup(
    name="cgcsdk",
    version=VERSION_STRING,
    description="Comtegra GPU Cloud REST API client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.comtegra.pl/",
    project_urls={
        "Documentation": "https://docs.cgc.comtegra.cloud/",
        "GitHub": "https://git.comtegra.pl/",
        "Changelog": "https://git.comtegra.pl/foobar/foobar/blob/master/CHANGELOG.md",
    },
    author="Comtegra AI Team",
    author_email="ai@comtegra.pl",
    keywords=["cloud", "sdk", "orchestrator", "kubernetes", "jupyter-notebook"],
    license="BSD 2-clause",
    packages=find_packages(exclude=["cgc.tests.*, cgc.tests"]),
    package_data={"cgc": ["CHANGELOG.md", ".env", "tests/desired_responses/*"]},
    py_modules=["cgc/cgc"],
    install_requires=[
        "click",
        "python-dotenv",
        "tabulate",
        "pycryptodomex",
        "paramiko>=2.11",
        "statsd",
        "requests",
        "setuptools",
        "colorama",
        "psycopg2-binary",
    ],
    entry_points={
        "console_scripts": [
            "cgc = cgc.cgc:cli",
        ],
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
