Network Communication
=====================

This page provides transparency on network traffic flows and data movement within the DICOM Store SCP for AWS HealthImaging deployment. Understanding these communication patterns is essential for security review and network architecture planning.

Deployment Scope
----------------

The software operates entirely within the customer's AWS account and VPC. All processing, storage, and data movement occur within AWS services configured and managed by the customer.

DICOM data is received through standard DICOM C-STORE communication from medical imaging devices or DICOM clients. Once received, all processing occurs within the customer's AWS environment using services such as ECS Fargate, S3, Lambda, Step Functions, DynamoDB, and AWS HealthImaging.

Data Transmission Boundaries
-----------------------------

The software does not transmit customer data outside the customer's AWS account except when interacting with AWS services configured by the customer. Specifically:

- DICOM images and metadata remain within the customer's AWS account
- Processing occurs entirely within the customer's VPC and AWS services
- No data is sent to the vendor or any third-party services
- No telemetry, analytics, or usage tracking data is collected by the vendor

Customers retain full control over network paths, security groups, TLS settings, and VPC configuration. All network communication is governed by the customer's AWS networking and security policies.

Typical Communication Path
--------------------------

The following describes the standard end-to-end flow for DICOM image ingestion and processing:

1. **DICOM Client or Modality**: Medical imaging device or PACS system initiates a DICOM C-STORE operation to send images

2. **Network Load Balancer**: Receives inbound TCP connections on port 11112 (configurable) and distributes traffic to available ECS tasks

3. **ECS Fargate Store SCP**: Processes DICOM protocol communication, validates incoming data, and stores received DICOM objects

4. **S3 Bucket**: Stores received DICOM objects temporarily for processing

5. **Lambda and Step Functions**: Orchestrate the import workflow, including metadata extraction and job management

6. **AWS HealthImaging Datastore**: Stores medical images in a DICOM-compliant format for long-term access

7. **DynamoDB**: Tracks import job status, metadata, and processing results

All communication between these components occurs within the customer's AWS account using AWS service endpoints and VPC networking.

Operational Notes
-----------------

**Inbound Access Control**

- DICOM clients connect to the Network Load Balancer on a configurable port (default: 11112)
- Access is controlled by security groups and network ACLs configured by the customer
- Customers should restrict inbound access to trusted source IP ranges or CIDR blocks

**TLS Configuration**

- TLS encryption for DICOM communication is supported and can be configured at the Network Load Balancer
- Customers are responsible for certificate management and TLS policy configuration
- Encryption in transit between AWS services uses AWS-managed encryption

**AWS Service Endpoints**

- ECS Fargate tasks communicate with AWS services using VPC endpoints or NAT Gateway
- S3, Lambda, Step Functions, DynamoDB, and AWS HealthImaging are accessed via AWS service endpoints
- All service communication remains within the AWS network

**Logging and Monitoring**

- VPC Flow Logs provide visibility into network traffic patterns
- CloudWatch Logs capture application and service logs
- Network Load Balancer access logs can be enabled for connection tracking
- Customers configure and manage all logging and monitoring settings

.. note::
   No customer data, telemetry, or usage information is transmitted to the vendor. All data remains within the customer's AWS account and is subject to the customer's data governance policies.
