variable "project_name" {
  description = "Name of the healthcare SRE project"
  type        = string
  default     = "healthcare-sre-platform"
}

variable "environment" {
  description = "Registry environment"
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "AWS region for container repositories"
  type        = string
  default     = "ca-central-1"
}

variable "repository_names" {
  description = "ECR repositories for the healthcare platform"
  type        = set(string)

  default = [
    "healthcare-sre-api",
    "healthcare-incident-receiver"
  ]
}

variable "github_repository" {
  description = "GitHub owner and repository allowed to publish images"
  type        = string
  default     = "afkhan2021/healthcare-sre-platform"
}

variable "github_branch" {
  description = "Git branch allowed to assume the AWS publishing role"
  type        = string
  default     = "main"
}
