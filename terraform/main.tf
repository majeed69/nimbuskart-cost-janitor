locals {
  common_tags = {
    Project     = var.project
    Environment = var.environment
    Owner       = var.owner
    ManagedBy   = "terraform"
  }
}

module "network" {
  source = "./modules/network"

  project             = var.project
  environment         = var.environment
  vpc_cidr            = var.vpc_cidr
  public_subnet_cidrs = var.public_subnet_cidrs
  availability_zones  = var.availability_zones
  common_tags         = local.common_tags
}

resource "aws_security_group" "web" {
  name        = "${var.project}-${var.environment}-web-sg"
  description = "Web security group"
  vpc_id      = module.network.vpc_id

  ingress {
    description = "HTTP"

    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS"

    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH"

    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.ssh_allowed_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(
    local.common_tags,
    {
      Name = "${var.project}-${var.environment}-web-sg"
    }
  )
}

resource "aws_instance" "web" {
  count = 2

  ami                    = "ami-12345678"
  instance_type          = "t3.micro"
  subnet_id              = module.network.public_subnet_ids[count.index]
  vpc_security_group_ids = [aws_security_group.web.id]

  tags = merge(
    local.common_tags,
    {
      Name = "${var.project}-${var.environment}-web-${count.index + 1}"
      Tier = "web"
    }
  )
}

resource "aws_s3_bucket" "logs" {
  bucket = "${var.project}-${var.environment}-logs"

  tags = merge(
    local.common_tags,
    {
      Name = "${var.project}-${var.environment}-logs"
    }
  )
}

resource "aws_s3_bucket_versioning" "logs" {
  bucket = aws_s3_bucket.logs.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_ebs_volume" "orphan" {
  availability_zone = "us-east-1a"
  size              = 8

  tags = merge(
    local.common_tags,
    {
      Name = "${var.project}-${var.environment}-orphan-volume"
    }
  )
}
