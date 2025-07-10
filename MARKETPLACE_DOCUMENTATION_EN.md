# DICOM Store SCP for AWS HealthImaging - AWS Marketplace Product Documentation

## Product Overview

### What is DICOM Store SCP for AWS HealthImaging?

DICOM Store SCP for AWS HealthImaging (StoreSCP) is a solution for healthcare institutions to securely and efficiently manage DICOM images from medical devices such as CT, MRI, and X-ray systems in the AWS cloud.

### Problems This Solution Addresses

**Challenges with Traditional PACS Systems:**
- High upfront hardware costs and maintenance expenses
- System aging and expensive upgrade cycles
- Complex data protection and disaster recovery requirements
- Storage capacity limitations and expansion costs
- IT staffing challenges and operational burden

**Solutions Provided by StoreSCP:**
- Dramatically reduce initial investment (no hardware required)
- Pay-as-you-use pricing model for cost optimization
- Data protection with AWS's highly reliable infrastructure
- Unlimited storage capacity with automatic scaling
- Reduced operational burden through managed services

### Target Healthcare Organizations

- **Small to Medium Hospitals**: Want to implement PACS with minimal initial investment
- **Large Hospitals**: Considering cloud migration of existing systems
- **Radiology Clinics**: Need cost-effective image management solutions
- **Telemedicine Providers**: Require flexible cloud-based access
- **Healthcare IT Vendors**: Want to offer cloud PACS solutions to customers

## Key Features

### 🏥 DICOM Compliance
- DICOM SCP (Service Class Provider) server
- Support for standard DICOM communication protocols
- Customizable AE Title configuration

### ☁️ AWS HealthImaging Integration
- Complete integration with AWS HealthImaging datastore
- Automated DICOM import processing
- High availability and scalability

### 🔧 Full Automation
- Workflow automation with Step Functions
- Optimized processing with Lambda functions
- Metadata management with DynamoDB

### 🛡️ Security
- Secure communication within VPC
- TLS encryption support
- Fine-grained access control

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   DICOM Client  │───▶│  Network Load    │───▶│   ECS Fargate   │
│                 │    │   Balancer       │    │   PACS Server   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  AWS Health     │◀───│  Step Functions  │◀───│   S3 Bucket     │
│  Imaging        │    │   Workflow       │    │   (DICOM)       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       
         ▼                       ▼                       
┌─────────────────┐    ┌──────────────────┐              
│   S3 Bucket     │    │    DynamoDB      │              
│  (Results)      │    │   (Metadata)     │              
└─────────────────┘    └──────────────────┘              
```

## Deployment Requirements

### Prerequisites
- AWS Account
- Appropriate IAM permissions
- VPC (existing or new)
- NAT Gateway (for ECR access from private subnets)

### Supported Regions
Regions where AWS HealthImaging is supported:
- us-east-1 (N. Virginia)
- us-west-2 (Oregon)
- eu-west-1 (Ireland)
- ap-southeast-2 (Sydney)

## Parameter Configuration

### Network Configuration
| Parameter | Description | Default Value |
|-----------|-------------|---------------|
| VpcID | ID of the VPC to use | - |
| PublicSubnetIDs | Public subnet IDs (comma-separated) | - |
| PrivateSubnetIDs | Private subnet IDs (comma-separated) | - |
| SecurityGroupID | Security group ID for ECS service | - |
| VpcCIDR | CIDR block for the VPC | - |

### DICOM Configuration
| Parameter | Description | Default Value |
|-----------|-------------|---------------|
| SCPAETitle | AE Title for DICOM SCP | STORESCP |
| SCPPort | DICOM communication port | 11112 |
| PeerCIDR1-3 | Allowed client CIDR blocks | - |
| DIMSETimeout | DIMSE operation timeout (seconds) | 60 |
| MaximumAssociations | Maximum concurrent connections | 300 |

### Scaling Configuration
| Parameter | Description | Default Value |
|-----------|-------------|---------------|
| TaskCPU | CPU units for ECS task | 1024 |
| TaskMemoryLimit | Memory limit for ECS task | 2048 |
| TaskDesiredCount | Desired number of ECS tasks | 1 |
| AutoscaleMaxCapacity | Maximum autoscaling capacity | 3 |

### Security Configuration
| Parameter | Description | Default Value |
|-----------|-------------|---------------|
| TLSCertificateARN | TLS certificate ARN (optional) | - |

## Deployment Steps

### 1. Launch from AWS Marketplace
1. Search for "DICOM Store SCP" or "StoreSCP" in AWS Marketplace
2. Click "Continue to Subscribe"
3. Click "Continue to Configuration"
4. Select region and click "Continue to Launch"

### 2. Parameter Configuration
1. Configure required parameters:
   - VPC ID
   - Subnet IDs
   - Security Group ID
   - Allowed client CIDRs
2. Adjust optional parameters as needed
3. Click "Launch"

### 3. Verify Deployment
- Confirm CloudFormation stack creation completion
- Verify ECS service is running properly
- Obtain Network Load Balancer DNS name

## Usage

### DICOM Connection Settings

Use the information retrieved from CloudFormation Outputs tab:
```
Host: [NetworkLoadBalancerDNS value]
Port: [DICOMPort value]
AE Title: [DICOMAETitle value]
```

### Image Transmission
1. Connect from DICOM client using above settings
2. Send DICOM images using C-STORE operation
3. Automatic import to AWS HealthImaging begins

### Processing Status Check
- Check import status in DynamoDB table
- Review debug information in CloudWatch Logs

## Monitoring and Logging

### CloudWatch Metrics
- ECS CPU/Memory utilization
- Network Load Balancer connection count
- Lambda function execution count and error rate
- Step Functions execution status

### Log Outputs
- ECS Fargate: `[stack-name]-PacsServerTaskDefPacsContainerLogGroup*`
- Lambda Functions: `/aws/lambda/[function-name]`

## Troubleshooting

### Common Issues

#### 1. DICOM Connection Error
**Symptoms**: Cannot connect from client
**Solutions**:
- Check security group configuration
- Verify PeerCIDR settings
- Check Network Load Balancer status

#### 2. Import Processing Failure
**Symptoms**: DICOM images not imported to HealthImaging
**Solutions**:
- Check Lambda function errors in CloudWatch Logs
- Verify job status in DynamoDB table
- Check S3 bucket permissions

#### 3. Performance Issues
**Symptoms**: Slow processing
**Solutions**:
- Increase ECS task CPU/memory settings
- Adjust autoscaling configuration
- Check concurrent connection limits

## Support

### Documentation
- [AWS HealthImaging Documentation](https://docs.aws.amazon.com/healthimaging/)
- [DICOM Standard Specification](https://www.dicomstandard.org/)

### Technical Support
Submit support requests through AWS Marketplace.

## Pricing

### AWS Service Costs
- ECS Fargate: Charged based on execution time
- AWS HealthImaging: Charged based on storage and API usage
- Lambda: Charged based on execution count and duration
- Other AWS Services: Standard pricing

For detailed cost estimates, use the [AWS Pricing Calculator](https://calculator.aws).

## Security Considerations

### Data Protection
- Encryption at rest (S3, DynamoDB)
- Encryption in transit (TLS support)
- Communication isolation within VPC

### Access Control
- IAM role-based access control
- Network control with security groups
- Operation logging with CloudTrail (optional)

### Compliance
- HIPAA-ready design
- SOC 2 Type II compliant
- Security based on AWS Shared Responsibility Model

## Version History

### v1.0.0
- Initial release
- Basic DICOM SCP functionality
- AWS HealthImaging integration
- Automated import workflow

---

**Note**: This solution is not a medical device. Do not use for medical diagnosis or treatment decisions.
