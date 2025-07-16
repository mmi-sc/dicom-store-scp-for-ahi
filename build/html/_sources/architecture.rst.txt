Architecture Overview
=====================

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

- **Purpose**: Load balancing and health checking for DICOM communication
- **Features**:
  
  - Layer 4 (TCP) load balancing
  - High availability and scalability
  - TLS termination support (optional)

- **Configuration**:
  
  - Target: ECS Fargate tasks
  - Health Check: TCP connection verification
  - Sticky Sessions: Disabled

ECS Fargate PACS Server
~~~~~~~~~~~~~~~~~~~~~~~

- **Purpose**: Execution environment for DICOM SCP server
- **Features**:
  
  - Serverless container execution
  - Auto-scaling support
  - Managed infrastructure

- **Configuration**:
  
  - CPU: Configurable via TASK_CPU parameter
  - Memory: Configurable via TASK_MEMORY_LIMIT_MIB parameter
  - Network Mode: awsvpc

S3 Storage Buckets
~~~~~~~~~~~~~~~~~~

**DICOM Files Bucket**

- **Purpose**: Temporary storage for received DICOM files
- **Features**:
  
  - Encryption: AES-256 (S3 managed)
  - Public access: Blocked
  - SSL enforcement: Enabled

**Results Bucket**

- **Purpose**: Storage for HealthImaging output results
- **Features**:
  
  - Processing result metadata
  - Conversion logs

AWS HealthImaging
~~~~~~~~~~~~~~~~~

- **Purpose**: Long-term storage and management of medical images
- **Features**:
  
  - DICOM standard compliant
  - High availability and durability
  - API-based access

- **Configuration**:
  
  - Encryption: AWS managed encryption
  - Access Control: IAM

DynamoDB Metadata Store
~~~~~~~~~~~~~~~~~~~~~~~

- **Purpose**: Import job metadata management
- **Table Design**:

.. code-block:: text

   Table: DicomImportJobTable
   ├── PK: jobId (String)
   ├── jobStatus (String)
   ├── submittedAt (String)
   ├── inputS3Uri (String)
   ├── outputS3Uri (String)
   ├── datastoreId (String)
   ├── dataAccessRoleArn (String)
   ├── studyDate (String)
   ├── studyInstanceUID (String)
   ├── seriesInstanceUID (String)
   ├── sopInstanceUID (String)
   ├── endedAt (String)
   └── message (String)

Lambda Functions
~~~~~~~~~~~~~~~~

**Trigger Import Function**

- **Trigger**: S3 PUT event
- **Processing**:
  
  - DICOM file validation
  - Metadata extraction
  - Step Functions execution start

**Start Import Job Function**

- **Processing**:
  
  - HealthImaging Import Job creation
  - Job information recording in DynamoDB
  - Job ID return

**Check Status Function**

- **Processing**:
  
  - Import Job status check
  - DynamoDB update
  - Completion/error determination

Step Functions Workflow
~~~~~~~~~~~~~~~~~~~~~~~

- **Purpose**: DICOM import process orchestration
- **Workflow States**:
  
  - TriggerImport → StartImportJob → WaitForCompletion → CheckStatus → IsComplete

Data Flow
---------

DICOM Image Reception Flow
~~~~~~~~~~~~~~~~~~~~~~~~~~

1. DICOM Client → NLB (TCP:11112)
2. NLB → ECS Fargate Task
3. ECS → DICOM Protocol Processing
4. ECS → S3 Bucket (DICOM Files)
5. S3 Event → Lambda (Trigger Import)

Import Processing Flow
~~~~~~~~~~~~~~~~~~~~~~

1. Lambda (Trigger) → Step Functions
2. Step Functions → Lambda (Start Import Job)
3. Lambda → HealthImaging API
4. HealthImaging → Processing
5. Lambda (Check Status) → Status Polling
6. HealthImaging → S3 (Results)
7. DynamoDB ← Status Updates

Error Handling and Recovery
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Error Detection → CloudWatch Logs
2. DynamoDB → Error Status Update
3. Step Functions → Retry Logic

Security Architecture
---------------------

Network Security
~~~~~~~~~~~~~~~~

- **VPC Isolation**: Public/Private subnet separation
- **Security Groups**: Principle of least privilege
- **NACLs**: Subnet-level control
- **TLS Encryption**: DICOM communication encryption (optional)

Data Security
~~~~~~~~~~~~~

- **Encryption**:
  
  - S3: AES-256 (SSE-S3)
  - DynamoDB: Default encryption
  - HealthImaging: AWS managed encryption

- **Access Logs**: VPC Flow Logs
- **Auditing**: CloudWatch

Scalability and Performance
---------------------------

Auto Scaling
~~~~~~~~~~~~

- **ECS Auto Scaling**: CPU utilization-based (target: 50%)
- **Lambda**: Automatic scaling (configurable concurrent execution limits)
- **DynamoDB**: On-demand capacity (PAY_PER_REQUEST)

High Availability Design
~~~~~~~~~~~~~~~~~~~~~~~~

- **Multi-AZ**: Distribution across multiple Availability Zones
- **Health Checks**: Automatic failover with NLB
- **Data Protection**: S3 encryption and access controls

Performance Optimization
~~~~~~~~~~~~~~~~~~~~~~~~

**Latency Optimization**

- **NLB**: Low latency with Layer 4 load balancing and cross-zone load balancing
- **ECS Tasks**: Distributed across private subnets in multiple AZs
- **Lambda**: Automatic scaling with configurable memory

**Throughput Optimization**

- **ECS Auto Scaling**: 60-second cooldown for scale-in/scale-out
- **S3**: Standard performance (transfer acceleration disabled)
- **DynamoDB**: On-demand capacity for variable workloads

**Cost Optimization**

- **S3 Lifecycle**: Configurable retention policies
- **ECS Fargate**: Pay-per-use pricing model
- **DynamoDB**: On-demand billing for unpredictable traffic

Monitoring and Observability
-----------------------------

CloudWatch Integration
~~~~~~~~~~~~~~~~~~~~~~

- **Metrics**:
  
  - ECS: CPU/Memory utilization
  - NLB: Connection count, response time
  - Lambda: Execution count, error rate, execution time
  - Step Functions: Execution status

- **Logs**:
  
  - ECS: Application logs
  - Lambda: Execution logs
  - VPC: Flow logs
