Deployment Guide
================

About This Guide
----------------

This guide is a comprehensive deployment manual for healthcare professionals who handle DICOM images and want to build a DICOM image reception system on AWS. Even AWS beginners can safely use this solution by following the detailed step-by-step instructions provided.

What is DICOM Store SCP for AWS HealthImaging?
-----------------------------------------------

Product Overview
~~~~~~~~~~~~~~~~

DICOM Store SCP for AWS HealthImaging (StoreSCP) is a solution for securely managing medical DICOM images in the cloud.

**Key Features:**

- **DICOM Image Reception**: Receives medical images from CT, MRI, X-ray, and other devices using standard DICOM protocols
- **Automatic Cloud Storage**: Automatically stores received images in AWS HealthImaging for long-term preservation
- **Secure Communication**: Standard security features appropriate for medical data
- **Scalable**: Automatically adjusts system capacity based on hospital size

Target Users
~~~~~~~~~~~~

- Healthcare IT administrators
- Radiology system administrators
- Organizations considering DICOM image management system implementation
- Healthcare institutions considering cloud migration

Pre-Deployment Preparation
--------------------------

AWS Environment Setup
~~~~~~~~~~~~~~~~~~~~~

AWS Account Creation
^^^^^^^^^^^^^^^^^^^^

1. Access `AWS Official Website <https://aws.amazon.com/>`_
2. Click "Create AWS Account"
3. Set email address, password, and account name
4. Enter contact information and payment details
5. Complete phone verification

Required IAM Permissions
^^^^^^^^^^^^^^^^^^^^^^^^

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

Network Environment Preparation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Understanding VPC (Virtual Private Cloud)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

VPC is a virtual private network created on AWS. Think of it as recreating your hospital's internal network in the cloud.

Required Network Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

How to Check Network Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. AWS Management Console → VPC
2. Check existing VPC ID in "VPC" menu
3. Check public/private subnet IDs in "Subnets" menu
4. Check "NAT Gateways" menu to verify at least one NAT Gateway is deployed in a public subnet
5. Check access control settings in "Security Groups"

Security Requirements
~~~~~~~~~~~~~~~~~~~~~

Understanding Security Groups
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Firewall functionality on AWS. Controls which IP addresses from within the VPC and from the internet can access which ports.

Security Group Configuration for DICOM Communication
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**VPC Internal Access Configuration Example:**

.. code-block:: text

   Type: Custom TCP
   Port: 11112 (standard DICOM port)
   Source: 10.0.0.0/16 (VPC internal IP address range)
   Description: VPC internal DICOM SCP connection

**Internet Access Configuration Example:**

.. code-block:: text

   Type: Custom TCP
   Port: 11112 (standard DICOM port)
   Source: 203.0.113.0/24 (hospital's global IP address range)
   Description: Internet DICOM SCP connection

TLS Certificate (Optional)
^^^^^^^^^^^^^^^^^^^^^^^^^^

- **What is TLS Certificate**: Digital certificate for encrypting communications
- **When Required**: When conducting DICOM communication over the internet
- **How to Obtain**: Available free through AWS Certificate Manager (ACM)

Detailed Deployment Steps
-------------------------

Step 1: Subscribe on AWS Marketplace
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

Step 2: Configuration and Deployment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Navigate to Configuration**
   
   - Click "Continue to Configuration"

2. **Basic Configuration**
   
   - **Region**: Select deployment region
   - **Version**: Select latest version
   - Click "Continue to Launch"

3. **Launch Configuration**
   
   - **Action**: Select "Launch CloudFormation"
   - Click "Launch"

Step 3: CloudFormation Parameter Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Required Parameters
^^^^^^^^^^^^^^^^^^^

**Network Configuration**

.. list-table::
   :header-rows: 1

   * - Parameter
     - Description
     - Example
     - How to Check
   * - VpcID
     - ID of the VPC to use
     - vpc-xxxxxxxxx
     - VPC Console → "VPCs"
   * - PublicSubnetIDs
     - Public subnet IDs (comma-separated)
     - subnet-xxxxxxxx,subnet-yyyyyyyy
     - VPC Console → "Subnets"
   * - PrivateSubnetIDs
     - Private subnet IDs (comma-separated)
     - subnet-aaaaaaaa,subnet-bbbbbbbb
     - VPC Console → "Subnets"
   * - SecurityGroupID
     - Security group ID
     - sg-xxxxxxxxx
     - EC2 Console → "Security Groups"
   * - VpcCIDR
     - VPC IP address range
     - 10.0.0.0/16
     - Check VPC details

**DICOM Configuration**

.. list-table::
   :header-rows: 1

   * - Parameter
     - Description
     - Example
     - Recommended Value
   * - SCPAETitle
     - DICOM device identifier
     - MYHOSPITAL
     - Hospital abbreviation (max 16 chars)
   * - SCPPort
     - DICOM communication port
     - 11112
     - Keep default value
   * - PeerCIDR1
     - Allowed IP address range 1
     - 203.0.113.0/24
     - Hospital's global IP range
   * - PeerCIDR2
     - Allowed IP address range 2
     - ""
     - Additional IP range (optional)
   * - PeerCIDR3
     - Allowed IP address range 3
     - ""
     - Additional IP range (optional)

Step 4: Execute Deployment
~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Parameter Verification**
   
   - Confirm all required parameters are correctly configured

2. **CloudFormation Stack Creation**
   
   - Click "Create stack"
   - Monitor stack creation progress

3. **Deployment Completion Verification**
   
   - Confirm stack status becomes "CREATE_COMPLETE"
   - Typically takes 10-15 minutes to complete

Post-Deployment Configuration
-----------------------------

Retrieve Connection Information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After deployment completion, retrieve connection information using these steps:

1. AWS Management Console → CloudFormation
2. Select your created stack
3. Click the **Outputs** tab
4. Note the following information:

.. code-block:: text

   NetworkLoadBalancerDNS: PacsNLB-1234567890.elb.us-east-1.amazonaws.com
   DICOMPort: 11112
   DICOMAETitle: STORESCP

DICOM Device Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Connection Settings Example**

.. code-block:: text

   Host: PacsNLB-1234567890.elb.us-east-1.amazonaws.com
   Port: 11112
   Called AE Title: STORESCP
   Calling AE Title: WORKSTATION1

Connection Testing
~~~~~~~~~~~~~~~~~~

**DICOM Echo Test**

.. code-block:: bash

   # Example using dcmtk
   echoscu -aec STORESCP -aet WORKSTATION1 PacsNLB-1234567890.elb.us-east-1.amazonaws.com 11112

Device-Specific Configuration Guide
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**GE Equipment:**

1. Service → Network → DICOM Settings
2. Enter the above parameters
3. Connection Test to verify connectivity

**Siemens Equipment:**

1. System → Network → DICOM Configuration
2. Create New Destination
3. Configure the above parameters

**Philips Equipment:**

1. Setup → System → Network → DICOM
2. Add Destination
3. Enter connection information