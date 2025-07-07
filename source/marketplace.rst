AWS Marketplace Deployment
==========================

This guide covers deployment from AWS Marketplace and basic configuration.

Deployment Steps
----------------

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

Parameter Configuration
-----------------------

Network Configuration
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 35 25 15

   * - Parameter
     - Description
     - Example
     - Required
   * - VpcID
     - ID of the VPC to use
     - vpc-xxxxxxxxx
     - Yes
   * - PublicSubnetIDs
     - Public subnet IDs (comma-separated)
     - subnet-xxxxxxxx,subnet-yyyyyyyy
     - Yes
   * - PrivateSubnetIDs
     - Private subnet IDs (comma-separated)
     - subnet-aaaaaaaa,subnet-bbbbbbbb
     - Yes
   * - SecurityGroupID
     - Security group ID for ECS service
     - sg-xxxxxxxxx
     - Yes
   * - VpcCIDR
     - CIDR block for the VPC
     - 10.0.0.0/16
     - No

DICOM Configuration
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 35 25 15

   * - Parameter
     - Description
     - Default Value
     - Required
   * - SCPAETitle
     - AE Title for DICOM SCP
     - STORESCP
     - No
   * - SCPPort
     - DICOM communication port
     - 11112
     - No
   * - PeerCIDR1
     - Allowed client CIDR block 1
     - 
     - Yes
   * - PeerCIDR2
     - Allowed client CIDR block 2
     - 
     - No
   * - PeerCIDR3
     - Allowed client CIDR block 3
     - 
     - No

Performance Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 35 20 20

   * - Parameter
     - Description
     - Default Value
     - Recommended
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

Security Configuration
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 45 30

   * - Parameter
     - Description
     - Example
   * - TLSCertificateARN
     - TLS certificate ARN (optional)
     - arn:aws:acm:us-east-1:123456789012:certificate/xxxxxxxx

Post-Deployment Configuration
-----------------------------

Retrieve Connection Information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After deployment completion, retrieve connection information from CloudFormation Outputs:

1. AWS Management Console → CloudFormation
2. Select your created stack
3. Click the **Outputs** tab
4. Note the following information:

.. code-block:: text

   NetworkLoadBalancerDNS: cloudpacs-nlb-xxxxxxxxx.elb.us-east-1.amazonaws.com
   DICOMPort: 11112
   DICOMAETitle: STORESCP

DICOM Client Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~

Configure your DICOM clients with the retrieved information:

.. code-block:: text

   Host: cloudpacs-nlb-xxxxxxxxx.elb.us-east-1.amazonaws.com
   Port: 11112
   Called AE Title: STORESCP
   Calling AE Title: WORKSTATION1

Connection Testing
~~~~~~~~~~~~~~~~~~

Test the connection using DICOM tools:

.. code-block:: bash

   # Example using dcmtk
   echoscu -aec STORESCP -aet WORKSTATION1 cloudpacs-nlb-xxxxxxxxx.elb.us-east-1.amazonaws.com 11112

Usage
-----

Image Transmission
~~~~~~~~~~~~~~~~~~

1. Connect from DICOM client using the configuration above
2. Send DICOM images using C-STORE operation
3. Automatic import to AWS HealthImaging begins

Processing Status Check
~~~~~~~~~~~~~~~~~~~~~~~

- Check import status in DynamoDB table
- Review debug information in CloudWatch Logs

Monitoring
----------

CloudWatch Metrics
~~~~~~~~~~~~~~~~~~~

Key metrics to monitor:

- ECS CPU utilization
- ECS Memory utilization
- NLB Active connection count
- Lambda execution count and error rate

Recommended Alarms
~~~~~~~~~~~~~~~~~~

.. code-block:: text

   - ECS CPU utilization > 80%
   - ECS Memory utilization > 80%
   - Lambda error rate > 5%
   - HealthImaging import errors