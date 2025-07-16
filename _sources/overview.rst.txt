Product Overview
================

What is DICOM Store SCP for AWS HealthImaging?
-----------------------------------------------

DICOM Store SCP for AWS HealthImaging (StoreSCP) is a solution for healthcare institutions to securely and efficiently manage DICOM images from medical devices such as CT, MRI, and X-ray systems in the AWS cloud.

Problems This Solution Addresses
--------------------------------

**Challenges with Traditional PACS Systems:**

- High upfront hardware costs and maintenance expenses
- System aging and expensive upgrade cycles
- Complex data protection and disaster recovery requirements
- Storage capacity limitations and expansion costs
- IT staffing challenges and operational burden

**Solutions Provided by StoreSCP:**

- Dramatically reduce initial investment (no hardware required)
- Pay-as-you-go pricing model for cost optimization
- Data protection with AWS's highly reliable infrastructure
- Unlimited storage capacity with automatic scaling
- Reduced operational burden through managed services

Target Healthcare Organizations
-------------------------------

- **Small to Medium Hospitals**: Want to implement PACS with minimal initial investment
- **Large Hospitals**: Considering cloud migration of existing systems
- **Radiology Clinics**: Need cost-effective image management solutions
- **Telemedicine Providers**: Require flexible cloud-based access
- **Healthcare IT Vendors**: Want to offer cloud PACS solutions to customers

Prerequisites
-------------

- AWS Account
- Appropriate IAM permissions
- VPC (existing or new)
- NAT Gateway (for ECR access from private subnets)

Supported Regions
-----------------

Regions where AWS HealthImaging is supported:

- us-east-1 (N. Virginia)
- us-west-2 (Oregon)
- eu-west-1 (Ireland)
- ap-southeast-2 (Sydney)

Pricing
-------

AWS Service Costs
~~~~~~~~~~~~~~~~~

- ECS Fargate: Charged based on execution time
- AWS HealthImaging: Charged based on storage and API usage
- Lambda: Charged based on execution count and duration
- Other AWS Services: Standard pricing

For detailed cost estimates, use the `AWS Pricing Calculator <https://calculator.aws>`_.

Security Considerations
-----------------------

Data Protection
~~~~~~~~~~~~~~~

- Encryption at rest (S3, DynamoDB)
- Encryption in transit (TLS support)
- Communication isolation within VPC

Access Control
~~~~~~~~~~~~~~

- IAM role-based access control
- Network control with security groups

Compliance
~~~~~~~~~~

- HIPAA-ready design
- Security based on AWS Shared Responsibility Model

.. note::
   This solution is not a medical device. Do not use for medical diagnosis or treatment decisions.
