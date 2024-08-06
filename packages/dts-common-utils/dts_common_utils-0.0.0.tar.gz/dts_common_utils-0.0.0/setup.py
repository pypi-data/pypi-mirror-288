import os
from setuptools import setup, find_packages

version = os.getenv("VERSION", "0.0.0")

setup(
    name="dts_common_utils",
    version=version,
    packages=find_packages("src"),
    package_dir={"": "src"},
)
