"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name="motus-api",  # Required
    version="0.0.1",  # Required
    description="Python library implementing the Motus API",  # Optional
    url="https://github.com/sensorgnome-org/python-motus-api",  # Optional
    author="Sensorgnome-org",  # Optional
    author_email="dfloer@birdscanada.com",  # Optional
    classifiers=[  # Optional
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    # keywords="api motus",  # Optional
    packages=find_packages(exclude=["contrib", "docs", "tests"]),  # Required
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*, !=3.7.*, <4",
    install_requires=[
        "certifi==2020.4.5.2",
        "chardet==3.0.4",
        "idna==2.9",
        "requests==2.24.0",
        "urllib3==1.25.9",
    ],  # Optional
    extras_require={"dev": []},  # Optional
)
