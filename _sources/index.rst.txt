DICOM Store SCP for AWS HealthImaging Documentation
===================================================

.. image:: https://img.shields.io/badge/AWS%20MARKETPLACE-v1.0.0-orange?style=for-the-badge&logo=amazon-aws
   :target: https://aws.amazon.com/marketplace/pp/prodview-a5gbqrjog5eww
   :alt: AWS MARKETPLACE

DICOM Store SCP for AWS HealthImaging (StoreSCP) is a fully serverless PACS (Picture Archiving and Communication System) deployment powered by AWS CloudFormation. It includes a DICOM Store SCP server, HealthImaging Datastore, Import Job automation, and supporting infrastructure components such as Lambda, DynamoDB, and Step Functions.

Key Features
------------

- **DICOM Store SCP Server**: Fully compliant DICOM Store Service Class Provider
- **AWS HealthImaging Integration**: Seamless integration with AWS HealthImaging datastore
- **Serverless Architecture**: Built on AWS Lambda, ECS Fargate, and Step Functions
- **Auto Scaling**: Automatic scaling based on workload
- **Security**: VPC isolation, encryption at rest and in transit

Contents:
---------

.. toctree::
   :maxdepth: 2

   overview
   deployment
   architecture
   troubleshooting

Support
-------

For technical support and questions:

- AWS HealthImaging Documentation: https://docs.aws.amazon.com/healthimaging/
- DICOM Standard Specification: https://www.dicomstandard.org/

.. note::
   This product is not a medical device.

   It is designed to help healthcare institutions manage medical imaging data efficiently and enhance the quality of patient care. However, it is not intended to replace professional medical advice, diagnosis, or treatment.
