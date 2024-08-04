# CloudOrchestrator

CloudOrchestrator is a CLI tool to manage AWS resources such as EC2, RDS, Route53, Lambda, ECR, S3, Docker, SNS, IAM, CloudWatch, DynamoDB, SSM, and ELB.

## Installation

```bash
pip install boto3
pip install paramiko
pip install .
```

## Usage

### Initialize the Config
```bash
CloudOrchestrator initialize
```

### Add AWS Account
```bash
CloudOrchestrator add-account
```

### EC2
```bash
CloudOrchestrator ec2 start <instance_name>
CloudOrchestrator ec2 stop <instance_name>
CloudOrchestrator ec2 ssh <instance_name> <command>
```

### ECR
```bash
CloudOrchestrator ecr-ls
CloudOrchestrator ecr-create <repository_name>
CloudOrchestrator ecr-delete <repository_name>
CloudOrchestrator ecr-describe <repository_name>
CloudOrchestrator ecr-uri <repository_name>
```

### S3
```bash
CloudOrchestrator s3-ls
CloudOrchestrator s3-create <bucket_name>
CloudOrchestrator s3-delete <bucket_name>
```

### RDS
```bash
CloudOrchestrator rds start <db_instance_identifier>
CloudOrchestrator rds stop <db_instance_identifier>
CloudOrchestrator rds-ls
```

### Docker
```bash
CloudOrchestrator docker ls
CloudOrchestrator docker ps
CloudOrchestrator docker stop <container_id>
CloudOrchestrator docker sh <container_id>
CloudOrchestrator docker run <port1> <port2> <image_name>
```

### SNS
```bash
CloudOrchestrator sns list
CloudOrchestrator sns create <topic_name>
CloudOrchestrator sns delete <topic_arn>
```

### IAM
```bash
CloudOrchestrator iam list
CloudOrchestrator iam create <user_name>
CloudOrchestrator iam delete <user_name>
```

### CloudWatch
```bash
CloudOrchestrator cloudwatch list
CloudOrchestrator cloudwatch put <namespace> <metric_name> <value>
```

### DynamoDB
```bash
CloudOrchestrator dynamodb list
CloudOrchestrator dynamodb create <table_name> <key_schema> <attribute_definitions> <provisioned_throughput>
CloudOrchestrator dynamodb delete <table_name>
```

### SSM
```bash
CloudOrchestrator ssm list
CloudOrchestrator ssm get <name>
CloudOrchestrator ssm put <name> <value> <type>
```

### ELB
```bash
CloudOrchestrator elb list
CloudOrchestrator elb create <load_balancer_name> <listeners> <availability_zones>
CloudOrchestrator elb delete <load_balancer_name>
```

### Deploy
```bash
CloudOrchestrator deploy <profile_name> <resource_name> <folder_path>
```

### Tag
```bash
CloudOrchestrator <tag_keyword> ls
```