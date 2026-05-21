# NimbusKart Cost Janitor

Cloud Cost Optimization & Infrastructure Automation Project built using Terraform, Python, Docker, LocalStack, and GitHub Actions.

---

# Project Overview

NimbusKart Cost Janitor is a DevOps-focused cloud governance project that simulates AWS infrastructure locally using LocalStack and automatically detects stale cloud resources such as:

* Stopped EC2 instances
* Unattached (orphan) EBS volumes

The project provisions infrastructure using Terraform modules and performs automated cloud scanning using Python and boto3.

It also supports:

* Dry-run cleanup mode
* JSON & Markdown report generation
* CI/CD automation using GitHub Actions
* Local AWS simulation using Docker + LocalStack

---

# Tech Stack

## Infrastructure & Cloud

* Terraform
* AWS Concepts (EC2, VPC, Subnets, Security Groups, S3, EBS)
* LocalStack
* Docker

## Automation

* Python
* boto3
* Rich (terminal formatting)

## DevOps & CI/CD

* Git
* GitHub
* GitHub Actions

---

# Features

## Infrastructure as Code

* Reusable Terraform modules
* VPC provisioning
* Public subnets
* Internet Gateway
* Route tables
* Security groups
* EC2 instances
* S3 bucket
* Orphan EBS volume simulation

## Cost Janitor Automation

* Detects stopped EC2 instances
* Detects unattached EBS volumes
* Generates JSON reports
* Generates Markdown reports
* Safe dry-run cleanup mode

## CI/CD Automation

GitHub Actions workflow automatically:

* Validates Terraform
* Starts LocalStack
* Applies infrastructure
* Runs janitor automation
* Uploads generated reports as artifacts

---

# Project Structure

```bash
nimbuskart-cost-janitor/
│
├── .github/
│   └── workflows/
│       └── cost-janitor.yml
│
├── janitor/
│   ├── janitor.py
│   ├── constants.py
│   ├── requirements.txt
│   └── tests/
│
├── terraform/
│   ├── main.tf
│   ├── provider.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── modules/
│       └── network/
│           ├── main.tf
│           ├── variables.tf
│           └── outputs.tf
│
├── docs/
├── samples/
├── README.md
├── DESIGN.md
└── SUBMISSION.md
```

---

# Infrastructure Provisioned

Terraform provisions the following resources locally using LocalStack:

* 1 VPC
* 2 Public Subnets
* 1 Internet Gateway
* Route Tables
* Security Group
* 2 EC2 Instances
* 1 S3 Bucket
* 1 Orphan EBS Volume

---

# How It Works

## Step 1 — Provision Infrastructure

Terraform creates AWS-like infrastructure locally using LocalStack.

## Step 2 — Simulate Stale Resources

One EC2 instance is manually stopped to simulate unused infrastructure.

## Step 3 — Run Cost Janitor

The Python automation scans infrastructure using boto3 and identifies:

* stopped EC2 instances
* unattached EBS volumes

## Step 4 — Generate Reports

The janitor generates:

* report.json
* report.md

## Step 5 — Safe Cleanup Simulation

Dry-run mode previews cleanup actions without deleting resources.

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone https://github.com/majeed69/nimbuskart-cost-janitor.git
cd nimbuskart-cost-janitor
```

---

## 2. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r janitor/requirements.txt
```

---

## 4. Install Terraform

Verify installation:

```bash
terraform --version
```

---

## 5. Install Docker

Verify installation:

```bash
docker --version
```

---

## 6. Start LocalStack

```bash
docker run -d \
-p 4566:4566 \
--name localstack \
localstack/localstack:3.0
```

Verify health:

```bash
curl http://localhost:4566/_localstack/health
```

---

# Terraform Usage

## Initialize Terraform

```bash
cd terraform
terraform init
```

## Validate Terraform

```bash
terraform validate
```

## Apply Infrastructure

```bash
terraform apply -auto-approve
```

---

# Running the Janitor

## Activate Virtual Environment

```bash
source .venv/bin/activate
```

## Run in Dry-Run Mode

```bash
cd janitor
python janitor.py --dry-run
```

---

# Example Output

## Detected Resources

* Stopped EC2 Instances
* Orphan EBS Volumes

## Generated Reports

* report.json
* report.md

---

# GitHub Actions Workflow

The workflow automatically:

1. Starts LocalStack
2. Initializes Terraform
3. Validates infrastructure
4. Applies Terraform configuration
5. Runs janitor automation
6. Uploads generated reports

Workflow file:

```bash
.github/workflows/cost-janitor.yml
```

---

# Engineering Decisions

## Why LocalStack?

Using LocalStack allows safe local AWS simulation without creating real AWS resources or incurring cloud costs.

## Why Dry-Run Mode?

Dry-run mode prevents accidental resource deletion and simulates cleanup actions safely.

## Why Terraform Modules?

Reusable modules improve scalability, maintainability, and infrastructure organization.

## Why GitHub Actions?

CI/CD automation validates infrastructure and ensures repeatable execution.

---

# Challenges Faced

During development, multiple real-world DevOps issues were encountered and resolved:

* LocalStack Community Edition compatibility issues
* Terraform provider initialization issues
* Git large file push failures
* Terraform state management mistakes
* Docker container debugging
* AWS CLI credential configuration
* GitHub Actions workflow permission issues

These debugging experiences significantly improved understanding of real DevOps workflows.

---

# Future Improvements

Possible future enhancements:

* Elastic IP detection
* Age-based stale resource filtering
* Slack/Discord notifications
* CSV report export
* Unit testing
* Docker Compose setup
* Automated scheduling
* CloudWatch metrics integration

---

 and portfolio purposes.
