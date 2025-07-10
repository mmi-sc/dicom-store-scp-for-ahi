AWS Marketplace Deployment
===========================

Deployment Steps
----------------

1. Launch from AWS Marketplace
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Search for "DICOM Store SCP" or "StoreSCP" in AWS Marketplace
2. Click "Continue to Subscribe"
3. Click "Continue to Configuration"
4. Select region and click "Continue to Launch"

2. Parameter Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Configure required parameters:
   
   - VPC ID
   - Subnet IDs
   - Security Group ID
   - Allowed client CIDRs

2. Adjust optional parameters as needed
3. Click "Launch"

3. Verify Deployment
~~~~~~~~~~~~~~~~~~~~

- Confirm CloudFormation stack creation completion
- Verify ECS service is running properly
- Obtain Network Load Balancer DNS name

Parameter Configuration
-----------------------

Network Configuration
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Parameter
     - Description
     - Default Value
   * - VpcID
     - ID of the VPC to use
     - \-
   * - PublicSubnetIDs
     - Public subnet IDs (comma-separated)
     - \-
   * - PrivateSubnetIDs
     - Private subnet IDs (comma-separated)
     - \-
   * - SecurityGroupID
     - Security group ID for ECS service
     - \-
   * - VpcCIDR
     - CIDR block for the VPC
     - \-

DICOM Configuration
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Parameter
     - Description
     - Default Value
   * - SCPAETitle
     - AE Title for DICOM SCP
     - STORESCP
   * - SCPPort
     - DICOM communication port
     - 11112
   * - PeerCIDR1-3
     - Allowed client CIDR blocks
     - \-
   * - DIMSETimeout
     - DIMSE operation timeout (seconds)
     - 60
   * - MaximumAssociations
     - Maximum concurrent connections
     - 300

Performance Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Parameter
     - Description
     - Default Value
   * - TaskCPU
     - CPU units for ECS task
     - 1024
   * - TaskMemoryLimit
     - Memory limit for ECS task
     - 2048
   * - TaskDesiredCount
     - Desired number of ECS tasks
     - 1
   * - AutoscaleMaxCapacity
     - Maximum autoscaling capacity
     - 3

Security Configuration
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Parameter
     - Description
     - Default Value
   * - TLSCertificateARN
     - TLS certificate ARN (optional)
     - \-

Usage
-----

DICOM Client Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the information retrieved from CloudFormation Outputs tab:

.. code-block:: text

   Host: [NetworkLoadBalancerDNS value]
   Port: [DICOMPort value]
   AE Title: [DICOMAETitle value]

Image Transmission
~~~~~~~~~~~~~~~~~~

1. Connect from DICOM client using above settings
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

- ECS CPU/Memory utilization
- Network Load Balancer connection count
- Lambda function execution count and error rate
- Step Functions execution status

Recommended Alarms
~~~~~~~~~~~~~~~~~~

.. code-block:: text

   - ECS CPU utilization > 80%
   - ECS Memory utilization > 80%
   - Lambda error rate > 5%
   - HealthImaging import errors

Post-Deployment Configuration
-----------------------------

Retrieve Connection Information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After deployment completion:

1. AWS Management Console → CloudFormation
2. Select your created stack
3. Click the **Outputs** tab
4. Note the connection information

Connection Testing
~~~~~~~~~~~~~~~~~~

**DICOM Echo Test**

.. code-block:: bash

   echoscu -aec STORESCP -aet WORKSTATION1 [NLB-DNS] 11112