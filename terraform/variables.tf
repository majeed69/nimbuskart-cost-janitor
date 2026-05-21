variable "project" {
  type    = string
  default = "nimbuskart"
}

variable "environment" {
  type    = string
  default = "staging"
}

variable "region" {
  type    = string
  default = "us-east-1"
}

variable "owner" {
  type    = string
  default = "majid"
}

variable "vpc_cidr" {
  type    = string
  default = "10.20.0.0/16"
}

variable "public_subnet_cidrs" {
  type = list(string)

  default = [
    "10.20.1.0/24",
    "10.20.2.0/24"
  ]
}

variable "availability_zones" {
  type = list(string)

  default = [
    "us-east-1a",
    "us-east-1b"
  ]
}

variable "ssh_allowed_cidr" {
  type    = string
  default = "0.0.0.0/0"
}
