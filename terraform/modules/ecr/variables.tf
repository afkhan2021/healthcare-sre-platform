variable "project_name" {
  description = "Name of the healthcare SRE project"
  type        = string
}

variable "environment" {
  description = "Deployment environment"
  type        = string
}

variable "repository_names" {
  description = "Container repository names to create"
  type        = set(string)

  validation {
    condition     = length(var.repository_names) > 0
    error_message = "At least one ECR repository name must be provided."
  }
}
