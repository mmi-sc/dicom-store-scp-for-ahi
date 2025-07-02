DICOM Store SCP for AWS HealthImaging Documentation
====================================================

Welcome to the DICOM Store SCP for AWS HealthImaging documentation. This solution provides a fully serverless DICOM SCP (Service Class Provider) for efficiently receiving DICOM images and automatically importing them to AWS HealthImaging.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   overview
   marketplace
   deployment
   architecture
   troubleshooting

Key Features
------------

🏥 **DICOM Compliance**
   - DICOM SCP (Service Class Provider) server
   - Support for standard DICOM communication protocols
   - Customizable AE Title configuration

☁️ **AWS HealthImaging Integration**
   - Complete integration with AWS HealthImaging datastore
   - Automated DICOM import processing
   - High availability and scalability

🔧 **Full Automation**
   - Workflow automation with Step Functions
   - Optimized processing with Lambda functions
   - Metadata management with DynamoDB

🛡️ **Security**
   - Secure communication within VPC
   - TLS encryption support
   - Fine-grained access control

Quick Start
-----------

1. **Subscribe on AWS Marketplace**
   Search for "DICOM Store SCP" and subscribe to the product.

2. **Deploy with CloudFormation**
   Configure parameters and create the stack.

3. **Configure DICOM Clients**
   Use the provided endpoint information to connect your DICOM devices.

Support
-------

For technical support, please submit requests through AWS Marketplace.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`