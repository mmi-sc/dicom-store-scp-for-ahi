DICOM Store SCP for AWS HealthImaging Documentation
==================================================

CloudPacs is a fully serverless PACS (Picture Archiving and Communication System) deployment powered by AWS CDK. It includes a DICOM SCP server, HealthImaging Datastore, Import Job automation, and supporting infrastructure components such as Lambda, DynamoDB, and Step Functions.

Quick Start
-----------

1. **Create Python Virtual Environment**

   .. code-block:: bash

      python -m venv .venv
      source .venv/bin/activate  # Windows: .venv\Scripts\activate.bat

2. **Install Dependencies**

   .. code-block:: bash

      pip install -r requirements.txt

3. **Set Up Environment Variables**

   .. code-block:: bash

      cp .env.template .env
      # Edit .env as needed

4. **Bootstrap CDK (first-time only)**

   .. code-block:: bash

      cdk bootstrap

5. **Deploy Stack**

   .. code-block:: bash

      cdk deploy

Key Features
------------

- **DICOM SCP Server**: Fully compliant DICOM Service Class Provider
- **AWS HealthImaging Integration**: Seamless integration with AWS HealthImaging datastore
- **Serverless Architecture**: Built on AWS Lambda, ECS Fargate, and Step Functions
- **Auto Scaling**: Automatic scaling based on workload
- **Security**: VPC isolation, encryption at rest and in transit

Contents:
---------

.. toctree::
   :maxdepth: 2

   overview
   architecture
   deployment
   marketplace
   troubleshooting

Support
-------

For technical support and questions:

- AWS HealthImaging Documentation: https://docs.aws.amazon.com/healthimaging/
- DICOM Standard Specification: https://www.dicomstandard.org/

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`