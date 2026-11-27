variable "project_name" {
  description = "Name of the healthcare SRE project"
  type        = string
}

variable "environment" {
  description = "Deployment environment"
  type        = string
}

variable "github_repository" {
  description = "GitHub owner and repository allowed to assume the role"
  type        = string
}

variable "github_branch" {
  description = "Git branch allowed to assume the role"
  type        = string
}

variable "ecr_repository_arns" {
  description = "ECR repository ARNs GitHub Actions can publish to"
  type        = list(string)

  validation {
    condition     = length(var.ecr_repository_arns) > 0
    error_message = "At least one ECR repository ARN must be provided."
  }
}
