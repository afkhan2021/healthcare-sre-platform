variable "project_name" {
  description = "Name of the healthcare SRE project"
  type        = string
  default     = "healthcare-sre-platform"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "AWS deployment region"
  type        = string
  default     = "ca-central-1"
}
variable "kubernetes_version" {
  description = "Kubernetes version for the EKS cluster"
  type        = string
  default     = "1.37"
}

variable "eks_instance_types" {
  description = "EC2 instance types for EKS worker nodes"
  type        = list(string)
  default     = ["t3.medium"]
}
variable "cluster_endpoint_public_access_cidrs" {
  description = "Public IP ranges allowed to access the EKS Kubernetes API"
  type        = list(string)
  default     = ["142.112.164.125/32"]
}