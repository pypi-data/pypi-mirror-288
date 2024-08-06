""" Setup file for the ModelHub SDK. """
from setuptools import setup, find_packages

# Detailed description of the project
long_description = """
# ModelHub SDK

The ModelHub SDK is a comprehensive toolkit designed to streamline the creation, management, and deployment of machine learning pipelines. It integrates seamlessly with ModelHub, a robust platform for developing and deploying machine learning models. This SDK provides an intuitive API for interacting with various ModelHub components, including MLflow for experiment tracking and pipeline orchestration.

## Key Features

- **Modular Architecture**: Organized into well-defined modules for core functionalities, client implementations, models, and utilities.
- **MLflow Integration**: Simplifies interaction with MLflow for tracking experiments, logging metrics, and managing model artifacts.
- **Pipeline Management**: Tools for creating, updating, and submitting machine learning pipelines efficiently.
- **Utility Functions**: Includes helper functions for common tasks such as logging setup and file encoding.
- **Extensibility**: Designed to be easily extendable for future enhancements and additional features.

## Installation

To install the ModelHub SDK, run:
pip install autonomize-model-sdk

"""

setup(
    name="autonomize-model-sdk",
    version="0.1.0",
    long_description=long_description,
    description="SDK for creating and managing machine learning pipelines.",
    author="Jagveer Singh",
    author_email="jagveer@autonomize.ai",
    url="https://github.com/autonomize-ai/autonomize-model-sdk.git",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "pyyaml",
        "jinja2",
        "kubernetes",
        "requests",
        "aiohttp",
        "mlflow",
        "azure-storage-blob",
        "azure-identity",
        "graphviz",
        "IPython",
        "pydantic",
        "networkx",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
