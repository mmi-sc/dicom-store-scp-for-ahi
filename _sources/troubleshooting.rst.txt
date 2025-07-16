Troubleshooting Guide
=====================

Common Issues
-------------

DICOM Connection Error
~~~~~~~~~~~~~~~~~~~~~~

**Symptoms**: Cannot connect from client

**Solutions**:

- Check security group configuration
- Verify PeerCIDR settings
- Check Network Load Balancer status

Import Processing Failure
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptoms**: DICOM images not imported to HealthImaging

**Solutions**:

- Check Lambda function errors in CloudWatch Logs
- Verify job status in DynamoDB table
- Check S3 bucket permissions

Performance Issues
~~~~~~~~~~~~~~~~~~

**Symptoms**: Slow processing

**Solutions**:

- Increase ECS task CPU/memory settings
- Adjust autoscaling configuration
- Check concurrent connection limits

Deployment Issues
-----------------

VPC-Related Errors
~~~~~~~~~~~~~~~~~~

**Error**: Invalid subnet ID

**Solution**: Verify subnet IDs are correct and exist in specified region

Permission Errors
~~~~~~~~~~~~~~~~~

**Error**: Access Denied

**Solution**: Verify IAM user has permissions for CloudFormation, ECS, Lambda, etc.

Resource Limit Errors
~~~~~~~~~~~~~~~~~~~~~

**Error**: Resource limit exceeded

**Solution**: Check ECS service limits and Lambda concurrent execution limits

Connection Issues
-----------------

When DICOM Connection Fails
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Security Group Verification**
   
   - Verify security group allows traffic from client IP address
   - Check inbound rules for port 11112

2. **ECS Service Status Check**
   
   - Verify service is running normally in ECS console
   - Confirm tasks are in "RUNNING" state

3. **Log Review**
   
   .. code-block:: text
   
      CloudWatch Logs > StackName-PacsServerTaskDefPacsContainerLogGroup*

Support
-------

For technical support:

- Submit support requests through AWS Marketplace
- AWS HealthImaging Documentation: https://docs.aws.amazon.com/healthimaging/
- DICOM Standard Specification: https://www.dicomstandard.org/

.. note::
   Always include relevant log excerpts, error messages, and configuration details when requesting support.