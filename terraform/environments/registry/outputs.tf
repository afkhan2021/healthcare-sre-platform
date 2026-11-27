output "repository_urls" {
  description = "ECR repository URLs for container publishing"
  value       = module.ecr.repository_urls
}

output "repository_arns" {
  description = "ECR repository ARNs for IAM policy configuration"
  value       = module.ecr.repository_arns
}

output "github_actions_role_arn" {
  description = "IAM role ARN for GitHub Actions OIDC authentication"
  value       = module.github_oidc.github_actions_role_arn
}
