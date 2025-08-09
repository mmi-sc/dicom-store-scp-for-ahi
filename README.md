# DICOM Store SCP for AWS HealthImaging Documentation

[![AWS MARKETPLACE](https://img.shields.io/badge/AWS%20MARKETPLACE-v1.0.0-orange?style=for-the-badge&logo=amazon-aws)](https://aws.amazon.com/marketplace/pp/prodview-a5gbqrjog5eww)

This repository contains comprehensive documentation for DICOM Store SCP for AWS HealthImaging, a fully serverless PACS solution built on AWS.

## Product Overview

DICOM Store SCP for AWS HealthImaging (StoreSCP) is a solution for healthcare institutions to securely and efficiently manage DICOM images from medical devices such as CT, MRI, and X-ray systems in the AWS cloud.

### Key Features

- **DICOM SCP Server**: Fully compliant DICOM Service Class Provider
- **AWS HealthImaging Integration**: Seamless integration with AWS HealthImaging datastore
- **Serverless Architecture**: Built on AWS Lambda, ECS Fargate, and Step Functions
- **Auto Scaling**: Automatic scaling based on workload
- **Security**: VPC isolation, encryption at rest and in transit

### Target Healthcare Organizations

- **Small to Medium Hospitals**: Want to implement PACS with minimal initial investment
- **Large Hospitals**: Considering cloud migration of existing systems
- **Radiology Clinics**: Need cost-effective image management solutions
- **Telemedicine Providers**: Require flexible cloud-based access
- **Healthcare IT Vendors**: Want to offer cloud PACS solutions to customers

## Pre-Deployment Preparation

### Prerequisites

- AWS Account with appropriate IAM permissions
- VPC with public and private subnets
- NAT Gateway (for ECR access from private subnets)
- Security Groups configured for DICOM communication

### Supported Regions

Regions where AWS HealthImaging is supported:

- us-east-1 (N. Virginia)
- us-west-2 (Oregon)
- eu-west-1 (Ireland)
- ap-southeast-2 (Sydney)

## Deployment Steps

### Quick Deployment via AWS Marketplace

1. **Subscribe on AWS Marketplace**
   - Search for "DICOM Store SCP" in AWS Marketplace
   - Click "Continue to Subscribe" and accept terms

2. **Configure Parameters**
   - Set VPC and subnet configurations
   - Configure DICOM settings (AE Title, allowed CIDRs)
   - Adjust performance parameters as needed

3. **Deploy via CloudFormation**
   - Launch CloudFormation stack
   - Monitor deployment progress (typically 10-15 minutes)
   - Retrieve connection information from Outputs tab

## Documentation Structure

### Architecture and Design
- [Architecture Overview (English)](ARCHITECTURE_OVERVIEW_EN.md)
- [Architecture Overview (Japanese)](ARCHITECTURE_OVERVIEW.md)

### Deployment Guides
- [Deployment Guide (English)](DEPLOYMENT_GUIDE_EN.md)
- [Deployment Guide (Japanese)](DEPLOYMENT_GUIDE.md)

### AWS Marketplace
- [Marketplace Documentation (English)](MARKETPLACE_DOCUMENTATION_EN.md)
- [Marketplace Documentation (Japanese)](MARKETPLACE_DOCUMENTATION.md)

### API Documentation
- [Sphinx Documentation](docs/build/html/index.html) - Comprehensive technical documentation

## Quick Start

After deployment, configure your DICOM devices with:

```
Host: [NetworkLoadBalancerDNS from CloudFormation Outputs]
Port: 11112
AE Title: STORESCP (or your configured value)
```

## Support

- **AWS HealthImaging Documentation**: https://docs.aws.amazon.com/healthimaging/
- **DICOM Standard**: https://www.dicomstandard.org/
- **Technical Support**: Submit requests through AWS Marketplace

## Security Notice

This solution is designed for healthcare environments and includes:

- HIPAA-ready architecture
- Encryption at rest and in transit
- VPC isolation and security groups
- Audit logging capabilities

**Important**: This solution is not a medical device. Do not use for medical diagnosis or treatment decisions.

## Version History

- **v1.0.0**: Initial release with basic DICOM SCP functionality and AWS HealthImaging integration