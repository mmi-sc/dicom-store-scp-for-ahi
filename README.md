# DICOM Store SCP for AWS HealthImaging

[![AWS MARKETPLACE](https://img.shields.io/badge/AWS%20MARKETPLACE-v1.0.0-orange?style=for-the-badge&logo=amazon-aws)](https://aws.amazon.com/marketplace/pp/prodview-a5gbqrjog5eww)

DICOM Store SCP for AWS HealthImaging is a serverless DICOM ingestion solution designed to run entirely within a customer's AWS account. It enables healthcare organizations to receive DICOM images using standard DICOM C-STORE operations and automatically import them into AWS HealthImaging.

The solution uses AWS managed services such as Amazon ECS Fargate, AWS Step Functions, AWS Lambda, Amazon S3, and Amazon DynamoDB to implement scalable DICOM ingestion workflows.

This project is designed to help healthcare organizations manage medical imaging data efficiently within AWS environments.

---

## Key Features

- Serverless architecture based on Amazon ECS Fargate
- Automated DICOM ingestion workflows
- Native integration with AWS HealthImaging
- Deployment within the customer's AWS account and VPC
- Support for standard DICOM C-STORE operations
- Integration with AWS managed services for orchestration and storage

---

## Architecture Overview

The system uses AWS managed services to provide a scalable architecture for receiving and processing DICOM data.

Core components include:

- Amazon ECS Fargate (DICOM Store SCP service)
- Network Load Balancer
- Amazon S3 for temporary DICOM storage
- AWS Step Functions for workflow orchestration
- AWS Lambda for processing tasks
- Amazon DynamoDB for job tracking
- AWS HealthImaging datastore for medical imaging storage

A detailed architecture description is available in the documentation site.

---

## Deployment

The solution is deployed using AWS CloudFormation.

Typical deployment flow:

1. Prepare AWS HealthImaging datastore
2. Deploy the CloudFormation stack
3. Configure AE Titles and networking
4. Connect DICOM modalities or PACS systems
5. Start ingesting DICOM images into AWS HealthImaging

Detailed deployment instructions are available in the documentation.

---

## Security Responsibility

This solution follows a shared responsibility model similar to AWS services.

Vendor responsibilities include:

- Providing the software container image
- Providing deployment templates
- Publishing documentation and architecture guidance

Customer responsibilities include:

- Operating infrastructure within their AWS account
- Managing IAM policies and network configuration
- Configuring encryption, monitoring, and logging
- Managing regulatory and organizational compliance requirements

The vendor does not operate or manage customer AWS environments.

---

## Network Communication

The software operates entirely within the customer's AWS account and VPC.

DICOM data is received through the standard DICOM C-STORE protocol and processed using AWS services configured by the customer.

The software does not transmit customer data outside the customer's AWS account except when interacting with AWS services configured by the customer.

---

## Support Policy

Community support is provided through the GitHub repository.

Users may submit questions or report issues through the GitHub issues page.

The vendor does not operate or manage customer AWS environments. Customers are responsible for operating and maintaining their own infrastructure.

---

## Documentation

Full documentation is available at:

https://www.mmi-sc.co.jp/dicom-store-scp-for-ahi/

Documentation includes:

- Product Overview
- Deployment Guide
- Architecture Overview
- Security Responsibility
- Network Communication
- Security and Architecture Guide
- Support Policy
- Troubleshooting Guide

---

## Security Notice

This project is designed to support secure healthcare workloads on AWS. Security, availability, and regulatory compliance depend on the customer's AWS configuration and operational practices.

---

## License

See LICENSE file for details.

---

## Contributing

Contributions and issue reports are welcome through GitHub.

---

## Disclaimer

This software is not a medical device and is not intended for diagnostic use.
