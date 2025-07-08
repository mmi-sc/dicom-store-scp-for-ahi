Troubleshooting Guide
======================

This guide provides solutions for common issues encountered when deploying and operating DICOM Store SCP for AWS HealthImaging.

Deployment Issues
-----------------

CloudFormation Stack Creation Failures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

VPC-Related Errors
^^^^^^^^^^^^^^^^^^^

**Error Messages:**

.. code-block:: text

   Invalid subnet ID: subnet-xxxxxxxxx does not exist
   Subnet subnet-xxxxxxxxx is not in the same VPC as subnet-yyyyyyyyy

**Causes and Solutions:**

- **Cause**: Non-existent subnet ID specified, or mixing subnets from different VPCs
- **Verification Method**:
  
  1. VPC Console → Subnets
  2. Verify specified subnet IDs exist
  3. Confirm all subnets belong to the same VPC

- **Solution**: Re-enter correct subnet IDs

Permission Errors
^^^^^^^^^^^^^^^^^

**Error Messages:**

.. code-block:: text

   User: arn:aws:iam::123456789012:user/username is not authorized to perform: cloudformation:CreateStack
   Access Denied when calling the CreateRole operation

**Causes and Solutions:**

- **Cause**: Insufficient IAM permissions
- **Verification Method**:
  
  1. IAM Console → Users → Select user
  2. Check permissions in "Permissions" tab

- **Solution**: Request administrator to add the following permissions:
  
  - CloudFormationFullAccess
  - ECSFullAccess
  - LambdaFullAccess
  - IAMFullAccess (for role creation)

Resource Limit Errors
^^^^^^^^^^^^^^^^^^^^^^

**Error Messages:**

.. code-block:: text

   The maximum number of VPCs has been reached
   Service limit exceeded for resource type 'AWS::ECS::Service'

**Causes and Solutions:**

- **Cause**: AWS account resource limits reached
- **Verification Method**: Check current usage in Service Quotas console
- **Solutions**:
  
  1. Delete unnecessary resources
  2. Request limit increase from AWS Support

Connection Issues
-----------------

DICOM Connection Timeout
~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptoms**: DICOM device connections fail with "Timeout" error

**Troubleshooting Steps:**

**Step 1: Network Connectivity Check**

.. code-block:: bash

   # Windows
   telnet PacsNLB-1234567890.elb.us-east-1.amazonaws.com 11112
   
   # Success: Black screen appears
   # Failure: Connection timeout or refused

**Step 2: Security Group Verification**

1. EC2 Console → Security Groups
2. Find the security group used by ECS service
3. Verify inbound rules allow traffic from client IP:

.. code-block:: text

   Type: Custom TCP
   Port: 11112
   Source: [Client IP or CIDR]

**Step 3: ECS Service Status Check**

1. ECS Console → Clusters → Select cluster
2. Services tab → Select service
3. Verify:
   
   - Service status: ACTIVE
   - Running count matches desired count
   - Tasks are in RUNNING state

**Step 4: Network Load Balancer Health Check**

1. EC2 Console → Load Balancers
2. Select the Network Load Balancer
3. Target Groups tab → Check target health
4. Verify targets are "healthy"

DICOM Association Rejected
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptoms**: Connection established but DICOM association rejected

**Common Causes and Solutions:**

**AE Title Mismatch:**

.. code-block:: text

   Error: Association rejected (Called AE Title not recognized)

- **Solution**: Verify Called AE Title matches server configuration
- **Check**: CloudFormation Outputs → DICOMAETitle value

**Unsupported SOP Class:**

.. code-block:: text

   Error: SOP Class not supported

- **Solution**: Check SupportedSOPClassUIDs parameter
- **Default**: Empty (accepts all SOP classes)
- **Custom**: Specify required SOP Class UIDs

**Network Configuration Issues:**

- **Check**: VPC routing tables
- **Verify**: NAT Gateway configuration for private subnets
- **Confirm**: Internet Gateway attached to VPC

Processing Issues
-----------------

Images Not Appearing in HealthImaging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptoms**: DICOM images successfully sent but not visible in AWS HealthImaging

**Troubleshooting Steps:**

**Step 1: Check Step Functions Execution**

1. Step Functions Console → State machines
2. Find the import workflow state machine
3. Check recent executions for failures

**Step 2: Review Lambda Function Logs**

1. CloudWatch Console → Log groups
2. Check logs for Lambda functions:
   
   - `/aws/lambda/start-import-job`
   - `/aws/lambda/check-import-status`
   - `/aws/lambda/trigger-state-machine`

**Step 3: Verify S3 Bucket Contents**

1. S3 Console → Find DICOM storage bucket
2. Verify DICOM files are present
3. Check object metadata and permissions

**Step 4: Check DynamoDB Job Status**

1. DynamoDB Console → Tables
2. Find the import job tracking table
3. Query for recent job entries
4. Check job status and error messages

Import Job Failures
~~~~~~~~~~~~~~~~~~~~

**Common Error Patterns:**

**Invalid DICOM Format:**

.. code-block:: text

   Error: Invalid DICOM file format

- **Cause**: Corrupted or non-DICOM file
- **Solution**: Verify file integrity at source
- **Prevention**: Implement client-side validation

**HealthImaging Service Limits:**

.. code-block:: text

   Error: Import job limit exceeded

- **Cause**: Too many concurrent import jobs
- **Solution**: Implement job queuing and throttling
- **Monitoring**: Set up CloudWatch alarms

**Insufficient Permissions:**

.. code-block:: text

   Error: Access denied to HealthImaging datastore

- **Cause**: IAM role lacks required permissions
- **Solution**: Update IAM role with HealthImaging permissions
- **Required Actions**:
  
  - medical-imaging:CreateImageSet
  - medical-imaging:GetImageSet
  - medical-imaging:StartDICOMImportJob

Performance Issues
------------------

Slow Image Processing
~~~~~~~~~~~~~~~~~~~~~

**Symptoms**: Long delays between image transmission and availability

**Performance Optimization:**

**ECS Task Scaling:**

1. ECS Console → Services → Update service
2. Increase desired count for more parallel processing
3. Adjust auto-scaling policies:

.. code-block:: text

   Scale out when: CPU > 70% or Memory > 80%
   Scale in when: CPU < 30% and Memory < 50%

**Lambda Function Optimization:**

1. Increase memory allocation (affects CPU)
2. Optimize code for better performance
3. Use provisioned concurrency for consistent performance

**S3 Performance:**

1. Use appropriate storage class
2. Enable transfer acceleration if needed
3. Optimize object naming for better performance

High Connection Latency
~~~~~~~~~~~~~~~~~~~~~~~

**Symptoms**: Slow DICOM connection establishment

**Network Optimization:**

**Load Balancer Configuration:**

1. Verify cross-zone load balancing is enabled
2. Check target group health check settings
3. Optimize health check intervals

**ECS Task Placement:**

1. Use placement strategies for optimal distribution
2. Consider task placement constraints
3. Monitor task distribution across AZs

**VPC Configuration:**

1. Verify optimal subnet placement
2. Check route table configurations
3. Monitor VPC Flow Logs for bottlenecks

Monitoring and Alerting
-----------------------

Setting Up Comprehensive Monitoring
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Essential CloudWatch Alarms:**

**ECS Service Health:**

.. code-block:: text

   Metric: CPUUtilization
   Threshold: > 80%
   Period: 5 minutes
   Evaluation: 2 consecutive periods

**Lambda Function Errors:**

.. code-block:: text

   Metric: Errors
   Threshold: > 0
   Period: 1 minute
   Evaluation: 1 period

**Step Functions Failures:**

.. code-block:: text

   Metric: ExecutionsFailed
   Threshold: > 0
   Period: 5 minutes
   Evaluation: 1 period

**Custom Metrics:**

Create custom metrics for business-specific monitoring:

- DICOM images processed per hour
- Average processing time
- Connection success rate
- Import job success rate

Log Analysis
~~~~~~~~~~~~

**Structured Logging:**

Implement structured logging for better analysis:

.. code-block:: json

   {
     "timestamp": "2024-01-01T12:00:00Z",
     "level": "INFO",
     "component": "dicom-scp",
     "message": "Image received",
     "metadata": {
       "ae_title": "CT01",
       "sop_instance_uid": "1.2.3.4.5",
       "file_size": 1024000
     }
   }

**Log Aggregation:**

Use CloudWatch Insights for log analysis:

.. code-block:: sql

   fields @timestamp, level, message, metadata.ae_title
   | filter level = "ERROR"
   | sort @timestamp desc
   | limit 100

Preventive Measures
-------------------

Regular Maintenance Tasks
~~~~~~~~~~~~~~~~~~~~~~~~~

**Weekly Tasks:**

1. Review CloudWatch alarms and metrics
2. Check ECS service health and scaling
3. Verify S3 bucket lifecycle policies
4. Monitor DynamoDB table performance

**Monthly Tasks:**

1. Review and optimize costs
2. Update security group rules if needed
3. Check for AWS service updates
4. Review and update documentation

**Quarterly Tasks:**

1. Disaster recovery testing
2. Security configuration review
3. Performance optimization review
4. Capacity planning assessment

Health Checks and Monitoring
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Automated Health Checks:**

Implement comprehensive health checks:

1. DICOM connectivity tests
2. End-to-end processing validation
3. Performance benchmarking
4. Security compliance checks

**Monitoring Dashboard:**

Create a comprehensive monitoring dashboard:

- Real-time connection status
- Processing queue depth
- Error rates and trends
- Performance metrics
- Cost tracking

Emergency Procedures
--------------------

Incident Response Plan
~~~~~~~~~~~~~~~~~~~~~~

**Severity Levels:**

**Critical (P1):**
- Complete service outage
- Data loss or corruption
- Security breach

**High (P2):**
- Partial service degradation
- Performance issues affecting users
- Failed deployments

**Medium (P3):**
- Minor functionality issues
- Non-critical errors
- Monitoring alerts

**Response Procedures:**

1. **Immediate Response** (within 15 minutes):
   
   - Acknowledge incident
   - Assess impact and severity
   - Initiate appropriate response team

2. **Investigation** (within 1 hour):
   
   - Identify root cause
   - Implement temporary workaround if possible
   - Communicate status to stakeholders

3. **Resolution** (timeline varies):
   
   - Implement permanent fix
   - Verify resolution
   - Update documentation

4. **Post-Incident Review**:
   
   - Conduct root cause analysis
   - Identify improvement opportunities
   - Update procedures and documentation

Contact Information
-------------------

**AWS Support:**
- Submit support cases through AWS Console
- Use appropriate support plan level

**AWS Marketplace Support:**
- Contact through AWS Marketplace
- Include detailed error messages and logs

**Documentation Updates:**
- Report documentation issues
- Suggest improvements and additions

.. note::
   Always include relevant log excerpts, error messages, and configuration details when requesting support.