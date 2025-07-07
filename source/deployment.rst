Deployment Guide
================

This comprehensive deployment guide provides detailed instructions for healthcare professionals to build a DICOM image reception system on AWS.

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
- Why Required: DICOM processing servers need to download container images from ECR
- Deployment: At least one NAT Gateway in one public subnet
- Critical: System will not start properly without NAT Gateway

**Availability Zones (AZ)**

Physically separated locations of AWS data centers. For disaster recovery, we distribute across different AZs.

How to Check Network Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. AWS Management Console → VPC
2. Check existing VPC ID in "VPC" menu
3. Check public/private subnet IDs in "Subnets" menu
4. Check "NAT Gateways" menu to verify at least one NAT Gateway is deployed
5. Check access control settings in "Security Groups"

**How to Create NAT Gateway if Missing:**

1. VPC Console → "NAT Gateways"
2. Click "Create NAT Gateway"
3. Select a public subnet and allocate an Elastic IP
4. Add route to NAT Gateway in private subnet route tables

Security Requirements
~~~~~~~~~~~~~~~~~~~~~

Understanding Security Groups
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Firewall functionality on AWS. Controls which IP addresses from within the VPC and from the internet can access which ports.

Security Group Configuration for DICOM Communication
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**VPC Internal Access Configuration:**

.. code-block:: text

   Type: Custom TCP
   Port: 11112 (standard DICOM port)
   Source: 10.0.0.0/16 (VPC internal IP address range)
   Description: VPC internal DICOM SCP connection

*Automatically configured by specifying the VpcCIDR parameter.*

**Internet Access Configuration:**

.. code-block:: text

   Type: Custom TCP
   Port: 11112 (standard DICOM port)
   Source: 203.0.113.0/24 (hospital's global IP address range)
   Description: Internet DICOM SCP connection

*Configured by specifying PeerCIDR1/PeerCIDR2/PeerCIDR3 parameters.*

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

CloudFormation automatically creates and configures AWS resources. Complex system configurations can be built at once.

**Required Parameters - Network Configuration**

.. list-table::
   :header-rows: 1
   :widths: 20 30 30 20

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
   * - AvailabilityZones
     - Availability zones (comma-separated)
     - us-east-1a,us-east-1b
     - Check subnet details
   * - SecurityGroupID
     - Security group ID
     - sg-xxxxxxxxx
     - EC2 Console → "Security Groups"
   * - VpcCIDR
     - VPC IP address range
     - 10.0.0.0/16
     - Check VPC details

**Required Parameters - DICOM Configuration**

.. list-table::
   :header-rows: 1
   :widths: 20 30 30 20

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
   * - RequireCalledAETitle
     - Enable AE Title verification
     - false
     - Usually false
   * - RequireCallingAETitle
     - Allowed client AE Titles
     - ""
     - Set when restricting to specific devices

.. note::
   **AE Title (Application Entity Title)** is a name to identify DICOM devices. Each device (CT, MRI, etc.) in the hospital has a unique identifier.

**Optional Parameters - Performance Configuration**

.. list-table::
   :header-rows: 1
   :widths: 20 30 20 30

   * - Parameter
     - Description
     - Default Value
     - Recommended Value
   * - TaskCPU
     - CPU units for ECS task
     - 1024
     - 2048
   * - TaskMemoryLimit
     - Memory limit for ECS task (MiB)
     - 2048
     - 4096
   * - TaskDesiredCount
     - Desired number of ECS tasks
     - 1
     - 2
   * - AutoscaleMaxCapacity
     - Maximum capacity for autoscaling
     - 3
     - 5

**Optional Parameters - Security Configuration**

.. list-table::
   :header-rows: 1
   :widths: 20 30 20 30

   * - Parameter
     - Description
     - Default Value
     - Example
   * - TLSCertificateARN
     - TLS certificate ARN (optional)
     - ""
     - arn:aws:acm:us-east-1:123456789012:certificate/xxxxxxxx

**Optional Parameters - Advanced DICOM Configuration**

.. list-table::
   :header-rows: 1
   :widths: 20 30 20 30

   * - Parameter
     - Description
     - Default Value
     - Recommended Value
   * - DIMSETimeout
     - DIMSE timeout in seconds
     - 60
     - 60
   * - MaximumAssociations
     - Maximum concurrent associations
     - 300
     - 300
   * - NetworkTimeout
     - Network timeout in seconds
     - 90
     - 90
   * - SupportedSOPClassUIDs
     - Supported SOP Class UIDs (comma-separated)
     - ""
     - Set when restricting to specific UIDs

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

**Detailed Steps to Retrieve Connection Information**

**Step 1: Access CloudFormation Console**

1. Log in to AWS Management Console
2. Select "CloudFormation" from services list
3. Confirm the region is correct (same as deployment region)

**Step 2: Verify Stack**

1. Find your created stack name in the stack list
   
   - Stack name example: "StoreSCP-Stack-20241201"
   - Confirm status is "CREATE_COMPLETE"

2. Click the stack name to open details

**Step 3: Retrieve Connection Information**

1. Click the **"Outputs"** tab
2. Note or copy the following important information:

.. list-table::
   :header-rows: 1
   :widths: 30 40 30

   * - Item
     - Description
     - Usage
   * - NetworkLoadBalancerDNS
     - Server address for connection
     - DICOM device connection settings
   * - DICOMPort
     - Connection port number
     - DICOM device connection settings
   * - DICOMAETitle
     - Server's AE Title
     - DICOM device connection settings

**Example:**

.. code-block:: text

   NetworkLoadBalancerDNS: storescp-nlb-1234567890.elb.us-east-1.amazonaws.com
   DICOMPort: 11112
   DICOMAETitle: STORESCP

DICOM Device Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~

**What are DICOM Devices?**

CT, MRI, X-ray, ultrasound diagnostic equipment, and other devices that generate and transmit medical images.

**Connection Configuration Steps**

**General DICOM Device Settings:**

.. list-table::
   :header-rows: 1
   :widths: 30 40 30

   * - Setting Item
     - Description
     - Setting Value
   * - Host/Server Address
     - Connection destination server address
     - NetworkLoadBalancerDNS from CloudFormation Outputs
   * - Port
     - Connection port
     - DICOMPort from CloudFormation Outputs (usually 11112)
   * - Called AE Title
     - Destination AE Title
     - DICOMAETitle from CloudFormation Outputs
   * - Calling AE Title
     - Source device AE Title
     - Device-specific name (e.g., CT01, MRI01)

**Configuration Example:**

.. code-block:: text

   Host: storescp-nlb-1234567890.elb.us-east-1.amazonaws.com
   Port: 11112
   Called AE Title: STORESCP
   Calling AE Title: CT01  # Source device identifier

Device-Specific Configuration Guide
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**For GE Equipment:**

1. Service → Network → DICOM Settings
2. Enter the above parameters
3. Verify connection with Connection Test

**For Siemens Equipment:**

1. System → Network → DICOM Configuration
2. Create New Destination
3. Configure the above parameters

**For Philips Equipment:**

1. Setup → System → Network → DICOM
2. Add Destination
3. Enter connection information

Connection Testing
~~~~~~~~~~~~~~~~~~

**Importance of Connection Testing**

Verify that DICOM connection works properly before sending actual medical images.

**Test Method 1: DICOM Echo Test from Device**

**Steps:**

1. Access DICOM device management screen
2. Open Network/DICOM settings screen
3. Execute "Connection Test" or "Echo Test"
4. Confirm "Success" or "OK" is displayed

**Test Method 2: Using DCMTK Tools (For Technical Staff)**

**What is DCMTK**: Free tool for testing DICOM communication

**Installation Method (Windows):**

1. Download from `DCMTK Official Site <https://dicom.offis.de/dcmtk.php.en>`_
2. Execute from command prompt after installation

**Test Command Examples:**

.. code-block:: bash

   # Basic Echo Test
   echoscu -aec STORESCP -aet TESTCLIENT storescp-nlb-1234567890.elb.us-east-1.amazonaws.com 11112

   # Detailed Log Test
   echoscu -v -aec STORESCP -aet TESTCLIENT storescp-nlb-1234567890.elb.us-east-1.amazonaws.com 11112

**Success Display Example:**

.. code-block:: text

   I: Association Request Acknowledged (Max Send PDV: 16372)
   I: Echo Response: 0000H (Success)
   I: Releasing Association

**Test Method 3: Actual Image Transmission Test**

**Precautions:**

- Use anonymized test images
- Do not use actual images containing patient information

**Steps:**

1. Select small test image on DICOM device
2. Set destination to configured StoreSCP
3. Execute transmission
4. Verify image is properly saved in AWS HealthImaging