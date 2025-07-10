# DICOM Store SCP for AWS HealthImaging Deployment Guide

## About This Guide

This guide is a comprehensive deployment manual for healthcare professionals who handle DICOM images and want to build a DICOM image reception system on AWS. Even AWS beginners can safely use this solution by following the detailed step-by-step instructions provided.

## What is DICOM Store SCP for AWS HealthImaging?

### Product Overview
DICOM Store SCP for AWS HealthImaging (StoreSCP) is a solution for securely managing medical DICOM images in the cloud.

**Key Features:**
- **DICOM Image Reception**: Receives medical images from CT, MRI, X-ray, and other devices using standard DICOM protocols
- **Automatic Cloud Storage**: Automatically stores received images in AWS HealthImaging for long-term preservation
- **Secure Communication**: Standard security features appropriate for medical data
- **Scalable**: Automatically adjusts system capacity based on hospital size

### Target Users
- Healthcare IT administrators
- Radiology system administrators
- Organizations considering DICOM image management system implementation
- Healthcare institutions considering cloud migration

## Pre-Deployment Preparation

### 1. AWS Environment Setup

#### AWS Account Creation
1. Access [AWS Official Website](https://aws.amazon.com/)
2. Click "Create AWS Account"
3. Set email address, password, and account name
4. Enter contact information and payment details
5. Complete phone verification

#### Required IAM Permissions
You need an IAM user or role with the following permissions:
- CloudFormation: Full access
- ECS: Full access
- Lambda: Full access
- S3: Full access
- VPC: Read permissions
- IAM: Role creation permissions

**Permission Setup Steps:**
1. AWS Management Console → IAM
2. "Users" → "Add user"
3. Select "Attach existing policies directly"
4. Choose policies corresponding to the above permissions

### 2. Understanding and Preparing Network Environment

#### What is VPC (Virtual Private Cloud)?
VPC is a virtual private network created on AWS. Think of it as recreating your hospital's internal network in the cloud.

#### Required Network Configuration

**Public Subnets (2 or more)**
- Purpose: Areas accessible from the internet
- Deployment: Network Load Balancer (receives external connections)
- Requirement: Deploy in different Availability Zones (AZ)

**Private Subnets (2 or more)**
- Purpose: Secure areas not directly accessible from outside
- Deployment: DICOM processing servers (actual image processing)
- Requirement: Deploy in different Availability Zones

**NAT Gateway (Required)**
- Purpose: Allows servers in private subnets to access the internet
- Why Required: DICOM processing servers need to download container images from ECR (Elastic Container Registry)
- Deployment: At least one NAT Gateway in one public subnet
- Critical: System will not start properly without NAT Gateway

**What are Availability Zones (AZ)?**
Physically separated locations of AWS data centers. For disaster recovery, we distribute across different AZs.

#### How to Check Network Settings
1. AWS Management Console → VPC
2. Check existing VPC ID in "VPC" menu
3. Check public/private subnet IDs in "Subnets" menu
4. Check "NAT Gateways" menu to verify at least one NAT Gateway is deployed in a public subnet
5. Check access control settings in "Security Groups"

**How to Create NAT Gateway if Missing:**
1. VPC Console → "NAT Gateways"
2. Click "Create NAT Gateway"
3. Select a public subnet and allocate an Elastic IP
4. Add route to NAT Gateway in private subnet route tables

### 3. Understanding Security Requirements

#### What are Security Groups?
Firewall functionality on AWS. Controls which IP addresses from within the VPC and from the internet (global IP addresses assigned to healthcare institutions) can access which ports.

#### Security Group Configuration for DICOM Communication

**VPC Internal Access Configuration Example:**
```
Type: Custom TCP
Port: 11112 (standard DICOM port)
Source: 10.0.0.0/16 (VPC internal IP address range)
Description: VPC internal DICOM SCP connection
```
*Automatically configured by specifying the VpcCIDR parameter.

**Internet Access Configuration Example:**
```
Type: Custom TCP
Port: 11112 (standard DICOM port)
Source: 203.0.113.0/24 (hospital's global IP address range)
Description: Internet DICOM SCP connection
```
*Configured by specifying PeerCIDR1/PeerCIDR2/PeerCIDR3 parameters.

#### TLS Certificate (Optional)
**What is TLS Certificate**: Digital certificate for encrypting communications
**When Required**: When conducting DICOM communication over the internet
**How to Obtain**: Available free through AWS Certificate Manager (ACM)

## Deployment Steps

### Step 1: Subscribe on AWS Marketplace

1. **Access AWS Marketplace**
   - Log in to AWS Management Console
   - Navigate to AWS Marketplace

2. **Search for StoreSCP**
   - Enter "DICOM Store SCP" or "StoreSCP" in the search bar
   - Select the corresponding product

3. **Subscribe**
   - Click "Continue to Subscribe"
   - Review and accept terms by clicking "Accept Terms"
   - Wait for subscription processing to complete

### Step 2: Configuration and Deployment

1. **Navigate to Configuration**
   - Click "Continue to Configuration"

2. **Basic Configuration**
   - **Region**: Select deployment region
   - **Version**: Select latest version
   - Click "Continue to Launch"

3. **Launch Configuration**
   - **Action**: Select "Launch CloudFormation"
   - Click "Launch"

### Step 3: CloudFormation Parameter Configuration

#### Required Parameters

**Network Configuration**

| Parameter | Description | Example | How to Check |
|-----------|-------------|---------|---------------|
| VpcID | ID of the VPC to use | vpc-xxxxxxxxx | VPC Console → "VPCs" |
| PublicSubnetIDs | Public subnet IDs (comma-separated) | subnet-xxxxxxxx,subnet-yyyyyyyy | VPC Console → "Subnets" |
| PrivateSubnetIDs | Private subnet IDs (comma-separated) | subnet-aaaaaaaa,subnet-bbbbbbbb | VPC Console → "Subnets" |
| AvailabilityZones | Availability zones (comma-separated) | us-east-1a,us-east-1b | Check subnet details |
| SecurityGroupID | Security group ID | sg-xxxxxxxxx | EC2 Console → "Security Groups" |
| VpcCIDR | VPC IP address range | 10.0.0.0/16 | Check VPC details |

**DICOM Configuration**

| Parameter | Description | Example | Recommended Value |
|-----------|-------------|---------|-------------------|
| SCPAETitle | DICOM device identifier | MYHOSPITAL | Hospital abbreviation (max 16 chars) |
| SCPPort | DICOM communication port | 11112 | Keep default value |
| PeerCIDR1 | Allowed IP address range 1 | 203.0.113.0/24 | Hospital's global IP range |
| PeerCIDR2 | Allowed IP address range 2 | "" | Additional IP range (optional) |
| PeerCIDR3 | Allowed IP address range 3 | "" | Additional IP range (optional) |
| RequireCalledAETitle | Enable AE Title verification | false | Usually false |
| RequireCallingAETitle | Allowed client AE Titles | "" | Set when restricting to specific devices |

#### Optional Parameters

**Performance Configuration**

| Parameter | Description | Default Value | Recommended Value |
|-----------|-------------|---------------|-------------------|
| TaskCPU | CPU units for ECS task | 1024 | 2048 |
| TaskMemoryLimit | Memory limit for ECS task (MiB) | 2048 | 4096 |
| TaskDesiredCount | Desired number of ECS tasks | 1 | 2 |
| AutoscaleMaxCapacity | Maximum capacity for autoscaling | 3 | 5 |

**Security Configuration**

| Parameter | Description | Default Value | Example |
|-----------|-------------|---------------|----------|
| TLSCertificateARN | TLS certificate ARN (optional) | "" | arn:aws:acm:us-east-1:123456789012:certificate/xxxxxxxx |

**Advanced DICOM Configuration**

| Parameter | Description | Default Value | Recommended Value |
|-----------|-------------|---------------|-------------------|
| DIMSETimeout | DIMSE timeout in seconds | 60 | 60 |
| MaximumAssociations | Maximum concurrent associations | 300 | 300 |
| NetworkTimeout | Network timeout in seconds | 90 | 90 |
| SupportedSOPClassUIDs | Supported SOP Class UIDs (comma-separated) | "" | Set when restricting to specific UIDs |

### Step 4: Execute Deployment

1. **Parameter Verification**
   - Confirm all required parameters are correctly configured

2. **CloudFormation Stack Creation**
   - Click "Create stack"
   - Monitor stack creation progress

3. **Deployment Completion Verification**
   - Confirm stack status becomes "CREATE_COMPLETE"
   - Typically takes 10-15 minutes to complete

## Post-Deployment Configuration

### 1. Retrieve Endpoint Information

**From CloudFormation Outputs Tab**

After deployment completion, retrieve connection information using these steps:

1. AWS Management Console → CloudFormation
2. Select your created stack
3. Click the **Outputs** tab
4. Note the following information:

```
NetworkLoadBalancerDNS: PacsNLB-1234567890.elb.us-east-1.amazonaws.com
DICOMPort: 11112
DICOMAETitle: STORESCP
```

### 2. DICOM Client Configuration

**Connection Settings Example**
```
Host: PacsNLB-1234567890.elb.us-east-1.amazonaws.com
Port: 11112
Called AE Title: STORESCP  # Use DICOMAETitle from CloudFormation Outputs
Calling AE Title: WORKSTATION1
```

### 3. Connection Testing

**DICOM Echo Test**
```bash
# Example using dcmtk
echoscu -aec STORESCP -aet WORKSTATION1 PacsNLB-1234567890.elb.us-east-1.amazonaws.com 11112
```

## Monitoring Setup

### 1. CloudWatch Dashboard Creation

**Key Metrics**
- ECS CPU utilization
- ECS Memory utilization
- NLB Active connection count
- Lambda execution count and error rate

### 2. Alarm Configuration

**Recommended Alarms**
```
- ECS CPU utilization > 80%
- ECS Memory utilization > 80%
- Lambda error rate > 5%
- HealthImaging import errors
```

## Security Configuration

### 1. Security Group Configuration

**Inbound Rules Example**
```
# VPC Internal Access
Type: Custom TCP
Port: 11112
Source: 10.0.0.0/16 (VPC CIDR)
Description: VPC internal DICOM SCP access

# Internet Access
Type: Custom TCP
Port: 11112
Source: 203.0.113.0/24 (Hospital's global IP CIDR)
Description: Internet DICOM SCP access
```

### 2. TLS Configuration (Optional)

**ACM Certificate Preparation**
1. Create certificate in AWS Certificate Manager
2. Complete domain validation
3. Set certificate ARN in parameters

## Troubleshooting

### Deployment Errors

**Common Errors and Solutions**

1. **VPC-related Errors**
   ```
   Error: Invalid subnet ID
   Solution: Verify subnet IDs are correct and exist in specified region
   ```

2. **Permission Errors**
   ```
   Error: Access Denied
   Solution: Verify IAM user has permissions for CloudFormation, ECS, Lambda, etc.
   ```

3. **Resource Limit Errors**
   ```
   Error: Resource limit exceeded
   Solution: Check ECS service limits and Lambda concurrent execution limits
   ```

### Connection Errors

**When DICOM Connection Fails**

1. **Security Group Verification**
   - Verify security group allows traffic from client IP address
   - Check inbound rules for port 11112

2. **ECS Service Status Check**
   - Verify service is running normally in ECS console
   - Confirm tasks are in "RUNNING" state

3. **Log Review**
   ```
   CloudWatch Logs > StackName-PacsServerTaskDefPacsContainerLogGroup*
   ```
   
   *StackName is the CloudFormation stack name specified during creation

## Scaling Configuration

### Auto Scaling

**CPU-based Target Tracking**
```
Target Value: CPU Utilization 50%
Min Capacity: 1
Max Capacity: AutoscaleMaxCapacity parameter (default 3, recommended 5)
Scale In/Out Cooldown: 60 seconds
```

**How to Verify**
```
AWS Management Console → ECS → Clusters → [cluster-name] → Services → [service-name] → Auto Scaling tab
```

## Data Protection Features

### Implemented Protection Features

**S3 Buckets**
- Encryption at rest (S3 managed encryption)
- SSL/TLS communication enforcement
- Public access blocking

**DynamoDB**
- Point-in-time recovery enabled
- Encryption at rest

**AWS HealthImaging**
- Automatic backup by AWS managed service
- High availability architecture

## Operational Best Practices

### 1. Regular Maintenance
- Monthly CloudWatch Logs review
- Quarterly security configuration review
- Annual data recovery testing

### 2. Performance Optimization
- Regular metrics analysis
- Scaling configuration adjustments as needed
- Cost optimization implementation

### 3. Security
- Regular security group reviews
- Access log auditing
- Vulnerability scanning

---

Following this guide will enable you to deploy and operate DICOM Store SCP for AWS HealthImaging safely and efficiently.