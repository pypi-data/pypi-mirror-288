# ModelHub SDK

The ModelHub SDK is a comprehensive toolkit designed to streamline the creation, management, and deployment of machine learning pipelines. It integrates seamlessly with ModelHub, a robust platform for developing and deploying machine learning models, and supports FastAPI and Argo Workflows for workflow orchestration.

## Installation

Install the SDK using pip:

```sh
pip install autonomize-model-sdk
```

## Usage
```sh
from modelhub.clients import PipelineManager

# Initialize the ModelHub client
pipeline_manager = PipelineManager(base_url=os.getenv("MODELHUB_BASE_URL"))

pipeline = pipeline_manager.start_pipeline("pipeline_config.yaml")

logger.info("Pipeline started: %s", pipeline)
```

## Contributing

### How to Push an Update to PyPI

To push an updated version of the ModelHub SDK to PyPI, follow these steps:

	1.	Update setup.py: Ensure that your setup.py file is updated with the new version number.
        from setuptools import setup, find_packages

        setup(
            name='autonomize-model-sdk',
            version='1.1.0',  # Update this version
            description='SDK for ModelHub to create and manage machine learning pipelines',
            author='Jagveer Singh',
            author_email='jagveer@autonomize.ai',
            url='https://github.com/autonomize-ai/autonomize-model-sdk.git',
            packages=find_packages(),
            install_requires=[
                'pandas',
                'pyyaml',
                'jinja2',
                'kubernetes',
                'requests',
                'aiohttp',
                'mlflow',
                'azure-storage-blob',
                'azure-identity',
                'graphviz',
                'IPython',
                'pydantic',
                'networkx',
            ],
            classifiers=[
                'Programming Language :: Python :: 3',
                'License :: OSI Approved :: MIT License',
                'Operating System :: OS Independent',
            ],
            python_requires='>=3.9',
        )

    2.	Build your distribution: Use setuptools and wheel to build your package.
        
        pip install setuptools wheel
        python setup.py sdist bdist_wheel
    
    3.	Upload your package to PyPI: Use twine to upload your package to PyPI.

        pip install twine
        twine upload dist/*


