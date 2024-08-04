from setuptools import setup, find_packages

setup(
    name="sellgate",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
    ],
    author="Sellgate",
    author_email="support@sellgate.io",
    description="A Python SDK for the Sellgate API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sellgate/python-sdk",
)