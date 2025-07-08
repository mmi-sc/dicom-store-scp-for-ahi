Architecture Overview
======================

This section provides a detailed overview of the DICOM Store SCP for AWS HealthImaging architecture, including system components, data flow, and design principles.

System Architecture
-------------------

High-Level Architecture Diagram
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

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

Core Components
---------------

Network Load Balancer (NLB)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:**
- Provides a stable endpoint for DICOM clients
- Distributes incoming DICOM connections across ECS tasks
- Handles high-throughput, low-latency connections

**Key Features:**
- Layer 4 (TCP) load balancing
- Static IP addresses
- High availability across multiple AZs
- Health checks for backend services

**Configuration:**
- Listens on port 11112 (configurable)
- Routes traffic to ECS Fargate tasks
- Supports both public and internal load balancers

ECS Fargate PACS Server
~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:**
- Runs the DICOM SCP server application
- Receives and processes DICOM images
- Stores images temporarily in S3 for processing

**Key Features:**
- Serverless container execution
- Auto-scaling based on CPU utilization target tracking
- No infrastructure management required
- Integrated with AWS CloudWatch for monitoring

**Container Specifications:**
- Base image: Custom DICOM SCP application
- CPU: 1024-4096 units (configurable via TaskCPU parameter)
- Memory: 2048-8192 MiB (configurable via TaskMemoryLimit parameter)
- Network: VPC with private subnets

**DICOM SCP Capabilities:**
- C-STORE SCP implementation
- Configurable AE Title
- Support for multiple SOP Classes
- Association management
- DIMSE timeout handling

S3 Storage Buckets
~~~~~~~~~~~~~~~~~~

**DICOM Storage Bucket:**
- Temporary storage for received DICOM files
- Triggers Step Functions workflow on object creation
- Lifecycle policies for automatic cleanup
- Server-side encryption enabled

**Results Storage Bucket:**
- Stores processing results and metadata
- Long-term retention for audit purposes
- Cross-region replication (optional)
- Versioning enabled for data protection

Step Functions Workflow
~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:**
- Orchestrates the DICOM import process
- Manages error handling and retries
- Provides visibility into processing status

**Workflow Steps:**

1. **Trigger**: S3 object creation event
2. **Validation**: Verify DICOM file integrity
3. **Import Job**: Create AWS HealthImaging import job
4. **Monitor**: Track import job progress
5. **Completion**: Update metadata and cleanup

**Error Handling:**
- Automatic retries with exponential backoff
- Dead letter queue for failed imports
- CloudWatch alarms for monitoring failures

Lambda Functions
~~~~~~~~~~~~~~~~

**Start Import Job Function:**
- Creates AWS HealthImaging import jobs
- Validates DICOM file format
- Updates DynamoDB with job metadata

**Check Import Status Function:**
- Monitors import job progress
- Handles job completion and failures
- Triggers cleanup processes

**Trigger State Machine Function:**
- Initiates Step Functions workflow
- Processes S3 event notifications
- Manages workflow parameters

AWS HealthImaging
~~~~~~~~~~~~~~~~~

**Purpose:**
- Long-term storage and management of medical images
- DICOM-native cloud storage service
- Optimized for medical imaging workflows

**Key Features:**
- Petabyte-scale storage
- Sub-second image retrieval
- Built-in DICOM metadata extraction
- Integration with medical imaging applications

**Data Organization:**
- Datastores for logical grouping
- Image sets for related images
- Automatic metadata indexing
- Version control for image updates

DynamoDB Metadata Store
~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:**
- Tracks import job status and metadata
- Provides fast lookup for processing status
- Stores audit trail information

**Table Structure:**
- Partition key: Job ID
- Sort key: Timestamp
- Attributes: Status, metadata, error information
- Global secondary indexes for queries

**Data Patterns:**
- Job tracking and status updates
- Error logging and debugging
- Performance metrics collection
- Audit trail maintenance

Data Flow
---------

DICOM Image Reception Flow
~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Client Connection:**
   - DICOM client establishes connection to NLB endpoint
   - NLB routes connection to available ECS task
   - ECS task accepts DICOM association

2. **Image Transmission:**
   - Client sends DICOM images via C-STORE operations
   - ECS task validates and stores images in S3
   - S3 object creation triggers Step Functions workflow

3. **Processing Workflow:**
   - Step Functions initiates import job creation
   - Lambda function creates AWS HealthImaging import job
   - Import job processes DICOM files asynchronously

4. **Status Monitoring:**
   - Lambda function monitors import job progress
   - DynamoDB stores job status and metadata
   - CloudWatch provides monitoring and alerting

5. **Completion:**
   - Import job completes successfully
   - Images available in AWS HealthImaging
   - Temporary S3 objects cleaned up

Error Handling and Recovery
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Connection Failures:**
- NLB health checks detect unhealthy tasks
- Auto-scaling creates replacement tasks
- Client connections automatically retry

**Processing Failures:**
- Step Functions retry failed operations
- Dead letter queue captures persistent failures
- CloudWatch alarms notify administrators

**Data Integrity:**
- DICOM file validation before processing
- Checksums verify data integrity
- Audit logs track all operations

Security Architecture
---------------------

Network Security
~~~~~~~~~~~~~~~~

**VPC Isolation:**
- All components deployed within VPC
- Private subnets for compute resources
- Public subnets only for load balancer

**Security Groups:**
- Restrictive inbound rules
- Principle of least privilege
- Separate groups for each component

**Network ACLs:**
- Additional layer of network security
- Subnet-level traffic control
- Default deny with explicit allows

Data Security
~~~~~~~~~~~~~

**Encryption at Rest:**
- S3 buckets with SSE-S3 encryption
- DynamoDB encryption enabled
- EBS volumes encrypted

**Encryption in Transit:**
- TLS support for DICOM connections
- HTTPS for all API communications
- VPC endpoints for AWS service access

**Access Control:**
- IAM roles with minimal permissions
- Service-linked roles for AWS services
- No long-term credentials stored

Monitoring and Observability
----------------------------

CloudWatch Integration
~~~~~~~~~~~~~~~~~~~~~~

**Metrics:**
- ECS task CPU and memory utilization
- NLB connection counts and latency
- Lambda function duration and errors
- Step Functions execution metrics

**Logs:**
- ECS task logs for DICOM operations
- Lambda function execution logs
- Step Functions workflow logs
- VPC Flow Logs for network analysis

**Alarms:**
- High CPU/memory utilization
- Failed import jobs
- Connection failures
- Processing delays

Distributed Tracing
~~~~~~~~~~~~~~~~~~~

**AWS X-Ray Integration:**
- End-to-end request tracing
- Performance bottleneck identification
- Error root cause analysis
- Service map visualization

Scalability and Performance
---------------------------

Auto Scaling
~~~~~~~~~~~~

**ECS Service Auto Scaling:**
- CPU-based target tracking scaling policy

**Scaling Metrics:**
- Target CPU utilization: 50%
- Scale-out cooldown: 60 seconds
- Scale-in cooldown: 60 seconds
- Min capacity: 1
- Max capacity: AutoscaleMaxCapacity parameter (default 3, recommended 5)

Performance Optimization
~~~~~~~~~~~~~~~~~~~~~~~~

**Connection Handling:**
- Connection pooling and reuse
- Optimized TCP settings
- Keep-alive configurations
- Timeout management

**Processing Efficiency:**
- Parallel processing of multiple images
- Batch operations where possible
- Efficient memory management
- Optimized I/O operations

Disaster Recovery
-----------------

High Availability Design
~~~~~~~~~~~~~~~~~~~~~~~~

**Multi-AZ Deployment:**
- ECS tasks distributed across AZs
- NLB with cross-zone load balancing
- S3 cross-region replication (optional)
- DynamoDB global tables (optional)

**Backup and Recovery:**
- Automated S3 backups
- DynamoDB point-in-time recovery
- CloudFormation stack recreation
- Infrastructure as Code approach

**Recovery Procedures:**
- RTO (Recovery Time Objective): < 1 hour
- RPO (Recovery Point Objective): < 15 minutes
- Automated failover mechanisms
- Manual recovery procedures documented

Cost Optimization
-----------------

Resource Optimization
~~~~~~~~~~~~~~~~~~~~~

**Right-Sizing:**
- ECS task sizing based on workload
- S3 storage class optimization
- Lambda memory allocation tuning
- DynamoDB capacity planning

**Cost Monitoring:**
- AWS Cost Explorer integration
- Resource tagging for cost allocation
- Budget alerts and notifications
- Regular cost optimization reviews

**Reserved Capacity:**
- ECS Savings Plans for predictable workloads
- S3 storage class transitions
- DynamoDB reserved capacity
- Long-term cost planning