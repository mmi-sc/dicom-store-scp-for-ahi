Security and Architecture Guide
===============================

This guide provides an overview of the security design and architectural controls implemented in DICOM Store SCP for AWS HealthImaging. It is intended for architecture and security reviewers, compliance teams, and technical decision-makers evaluating the solution.

The information presented here summarizes security-relevant aspects of the architecture. This guide does not replace the customer's own security review, risk assessment, or compliance validation processes.

Architecture Components
-----------------------

The solution is built on the following AWS services:

**Compute and Networking**

- **Amazon ECS Fargate**: Serverless container execution environment for the DICOM Store SCP server
- **Amazon VPC**: Network isolation with public and private subnets
- **Network Load Balancer**: Layer 4 load balancing for DICOM traffic with optional TLS termination

**Storage and Data Management**

- **Amazon S3**: Object storage for received DICOM files and processing results
- **AWS HealthImaging**: DICOM-compliant medical image storage and management service
- **Amazon DynamoDB**: Metadata storage for import job tracking and status management

**Orchestration and Processing**

- **AWS Lambda**: Serverless functions for workflow automation and event processing
- **AWS Step Functions**: State machine orchestration for DICOM import workflows

**Security and Monitoring**

- **AWS IAM**: Role-based access control for all service interactions
- **Amazon CloudWatch**: Logging and monitoring for operational visibility
- **VPC Flow Logs**: Network traffic visibility and analysis

Key Security Considerations
----------------------------

**Customer-Managed Deployment**

The solution is deployed entirely within the customer's AWS account. The vendor does not have access to the customer's environment, infrastructure, or data. All operational control and data governance remain with the customer.

**Network Isolation**

All components operate within the customer's VPC. Network traffic is controlled through security groups, network ACLs, and subnet routing. DICOM clients connect through a Network Load Balancer, and internal communication occurs within the VPC.

**IAM-Based Access Control**

All interactions between AWS services use IAM roles with least privilege permissions. The solution does not use long-term credentials or access keys. Customers can review and modify IAM policies to meet their security requirements.

**Encryption in Transit**

- DICOM communication can be encrypted using TLS at the Network Load Balancer
- Communication between AWS services uses AWS-managed encryption
- Customers configure TLS policies and certificate management

**Encryption at Rest**

- S3 buckets use server-side encryption with AWS-managed keys (SSE-S3)
- DynamoDB tables use default encryption
- AWS HealthImaging uses AWS-managed encryption
- Customers can configure customer-managed keys (CMK) where supported

**Separation of Environments**

The vendor and customer environments are completely separated. The vendor provides the container image and deployment templates but does not access customer data, logs, or infrastructure. No telemetry or usage data is collected by the vendor.

**Logging and Operational Visibility**

CloudWatch Logs, VPC Flow Logs, and service-level logging provide visibility into system operations. Customers configure log retention, analysis, and alerting according to their operational and compliance requirements.

Recommended Customer Controls
------------------------------

Customers should implement the following controls as part of their deployment and operational practices:

**Network Security**

- Review and configure security groups to allow DICOM traffic only from trusted sources
- Restrict inbound access using CIDR blocks or security group references
- Enable VPC Flow Logs for network traffic analysis
- Consider using AWS PrivateLink or VPC endpoints for service communication

**Access Management**

- Apply least privilege IAM policies to all roles
- Review IAM permissions before production deployment
- Use IAM policy conditions to restrict access based on source IP, time, or other factors
- Enable CloudTrail for API activity logging and auditing

**Encryption**

- Enable TLS for DICOM communication at the Network Load Balancer
- Review encryption settings for S3, DynamoDB, and AWS HealthImaging
- Consider using customer-managed keys (CMK) for additional control over encryption keys
- Validate that encryption meets organizational and regulatory requirements

**Monitoring and Logging**

- Enable CloudWatch Logs for all Lambda functions and ECS tasks
- Configure log retention policies according to compliance requirements
- Set up CloudWatch alarms for operational and security events
- Review logs regularly for anomalies or security incidents

**Configuration Validation**

- Review all CloudFormation parameters before deployment
- Test the deployment in a non-production environment first
- Validate security group rules, IAM policies, and network configurations
- Document configuration decisions and deviations from defaults

**Operational Security**

- Establish procedures for monitoring import job status and errors
- Define incident response processes for security events
- Plan for regular review of IAM permissions and network configurations
- Keep deployment templates and container images up to date with vendor releases

Compliance and Regulatory Considerations
-----------------------------------------

This solution is designed with healthcare data security in mind and follows AWS best practices for HIPAA-eligible services. However, customers are responsible for:

- Determining applicability of regulations such as HIPAA, GDPR, or other data protection laws
- Configuring the solution to meet specific compliance requirements
- Conducting compliance assessments and audits
- Maintaining documentation for regulatory review
- Implementing additional controls as required by their compliance framework

The vendor does not make claims about compliance certifications or regulatory approval. Customers must validate compliance based on their own requirements and risk assessments.

.. note::
   This guide provides architectural and security information to support customer review processes. It does not constitute security advice, legal guidance, or compliance certification. Customers are responsible for their own security review, risk assessment, and compliance validation.
