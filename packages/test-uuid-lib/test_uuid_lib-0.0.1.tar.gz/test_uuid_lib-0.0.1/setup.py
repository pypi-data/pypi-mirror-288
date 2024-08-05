from setuptools import setup, find_packages
from pathlib import Path

setup(
    name="test_uuid_lib",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.whl'],
    },
)