Security Responsibility
=======================

This product follows a shared responsibility model similar to AWS services. Understanding the division of responsibilities between the vendor and the customer is essential for enterprise security review and compliance discussions.

DICOM Store SCP for AWS HealthImaging is a customer-managed deployment that operates entirely within the customer's AWS account. The vendor, Man Machine Interface, Inc., does not access the customer's AWS account, environments, or customer data at any time.

Vendor Responsibilities
-----------------------

The vendor is responsible for:

- **Product Development**: Providing the container image and deployment templates that implement the DICOM Store SCP functionality.
- **Secure Design**: Designing the software with security considerations and reasonable default configurations.
- **Software Updates**: Providing software updates that may include security fixes for supported releases.
- **Documentation**: Publishing product documentation, deployment guidance, and architectural best practices.

The vendor's responsibility ends at the delivery of the software artifacts and documentation. The vendor does not operate, monitor, or maintain the deployed infrastructure.

Customer Responsibilities
-------------------------

The customer is responsible for:

- **Infrastructure Operation**: Operating and maintaining all infrastructure components within their AWS account
- **IAM Management**: Managing IAM roles, policies, and permissions for all deployed resources
- **Network Configuration**: Configuring VPC, subnets, security groups, and network access control lists
- **Encryption Settings**: Configuring encryption at rest and in transit according to their security requirements
- **Logging and Monitoring**: Enabling, configuring, and reviewing CloudWatch logs, VPC Flow Logs, and other monitoring tools
- **Data Governance**: Governing DICOM data, metadata, patient information, and retention policies
- **Compliance Validation**: Validating compliance with applicable legal, regulatory, and organizational requirements
- **Security Review**: Reviewing deployment settings, security configurations, and access controls before production use
- **Operational Security**: Managing security incidents, patching, updates, and ongoing security operations

The customer retains full control over the deployment, configuration, and operation of the solution within their AWS environment.

Customer Security Review
-------------------------

Customers remain responsible for conducting their own security review of the deployment. This includes:

- Evaluating the solution against internal security policies and standards
- Assessing compliance with applicable regulations such as HIPAA, GDPR, or other healthcare data protection requirements
- Reviewing IAM permissions and ensuring least privilege access
- Validating network configurations and access controls
- Testing security controls in non-production environments before production deployment

The vendor provides documentation and architectural guidance to support these reviews, but the final security posture and compliance determination rest with the customer.

.. note::
   This product does not include vendor access to customer environments or customer data. All operations, monitoring, and data governance are performed by the customer within their own AWS account.
