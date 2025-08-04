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

This solution is designed for deployment in **us-east-1 (N. Virginia)** via AWS Marketplace.

.. note::
   While AWS HealthImaging is available in multiple regions (us-west-2, eu-west-1, ap-southeast-2),
   this AWS Marketplace solution currently supports us-east-1 only due to container image hosting limitations.

Pricing
-------

AWS Service Components and Costs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following table details all AWS components deployed by this solution and their associated costs:

**Primary Cost Components**

.. list-table::
   :header-rows: 1
   :widths: 25 15 20 40

   * - Service
     - Quantity
     - Billing Model
     - Description
   * - **ECS Fargate**
     - 1-3 tasks
     - CPU/Memory hours
     - DICOM SCP server (1024 CPU, 2048MB default)
   * - **Network Load Balancer**
     - 1 instance
     - Hourly + data processing
     - Internet-facing load balancer
   * - **AWS HealthImaging**
     - 1 datastore
     - Storage + API calls
     - Medical image storage and management
   * - **S3 Storage**
     - 3 buckets
     - Storage volume
     - DICOM files, access logs, import results
   * - **DynamoDB**
     - 1 table
     - On-demand requests
     - Import job metadata (PAY_PER_REQUEST)

**Supporting Components**

.. list-table::
   :header-rows: 1
   :widths: 25 15 20 40

   * - Service
     - Quantity
     - Billing Model
     - Description
   * - **Lambda Functions**
     - 3 functions
     - Execution count/duration
     - Import workflow automation
   * - **Step Functions**
     - 1 state machine
     - State transitions
     - Workflow orchestration
   * - **SQS Queues**
     - 3 queues
     - Message count
     - Event processing and error handling
   * - **CloudWatch Logs**
     - Multiple log groups
     - Log storage volume
     - Application and system logs

Cost Estimation Examples
~~~~~~~~~~~~~~~~~~~~~~~~

**Small Hospital (100-500 images/month)**

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Component
     - Monthly Cost (USD)
     - Notes
   * - ECS Fargate (1 task)
     - $30-40
     - 1024 CPU, 2048MB, 24/7 operation
   * - Network Load Balancer
     - $16-20
     - Base hourly rate + minimal data processing
   * - AWS HealthImaging
     - $5-15
     - Storage + API calls for 100-500 images
   * - S3 Storage
     - $2-5
     - DICOM files and logs
   * - Other Services
     - $5-10
     - Lambda, DynamoDB, SQS, CloudWatch
   * - **Total Estimate**
     - **$60-90**
     - Varies based on actual usage

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
