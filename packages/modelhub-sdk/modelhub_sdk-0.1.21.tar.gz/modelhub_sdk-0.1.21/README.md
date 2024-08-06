# ModelHub SDK

ModelHub SDK for managing ML pipelines using FastAPI and Argo Workflows.

## Installation

Install the SDK using pip:

```sh
pip install modelhub
```

## Usage 

```sh
from modelhub.client import ModelHub
from modelhub.pipelines import Pipelines

# Initialize the ModelHub client
modelhub = ModelHub(base_url="http://localhost:3000")

pipeline = Pipelines(modelhub)
created_pipeline = pipeline.create_or_update_pipeline("config/pipeline.yaml")
print("Pipeline created/updated with ID:", created_pipeline["pipeline_id"])

# Submit the pipeline for execution
pipeline_id = created_pipeline["pipeline_id"]
pipeline.submit(pipeline_id)
```

## Contributing

### How to Push an Update to PyPI

To push an updated version of the ModelHub SDK to PyPI, follow these steps:

	1.	Update setup.py: Ensure that your setup.py file is updated with the new version number.

  ```
  from setuptools import setup, find_packages

  setup(
      name='modelhub',
      version='1.1.0',  # Update this version
      description='ModelHub SDK for interacting with the ModelHub API',
      packages=find_packages(),
      install_requires=[
          'requests',
          'mlflow',
          'python-dotenv'
      ],
      entry_points={
          'console_scripts': [
              'modelhub=modelhub.cli:main',
          ],
      },
  )
  ```
  2.	Build your distribution: Use setuptools and wheel to build your package.
  ```
  pip install setuptools wheel
  python setup.py sdist bdist_wheel
  ```
  3.	Upload your package to PyPI: Use twine to upload your package to PyPI.
  ```
  pip install twine
  twine upload dist/*
  ```