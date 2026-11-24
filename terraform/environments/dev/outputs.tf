output "vpc_id" {
  description = "Healthcare SRE VPC ID"
  value       = aws_vpc.main.id
}

output "availability_zones" {
  value = local.availability_zones
}

output "public_subnet_ids" {
  value = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  value = aws_subnet.private[*].id
}

output "eks_cluster_role_arn" {
  description = "IAM role ARN for the EKS control plane"
  value       = module.iam.eks_cluster_role_arn
}

output "eks_node_role_arn" {
  description = "IAM role ARN for EKS worker nodes"
  value       = module.iam.eks_node_role_arn
}

output "eks_cluster_name" {
  description = "EKS cluster name"
  value       = module.eks.cluster_name
}

output "eks_cluster_endpoint" {
  description = "EKS Kubernetes API endpoint"
  value       = module.eks.cluster_endpoint
}
output "eks_node_group_name" {
  description = "EKS managed node group name"
  value       = module.eks.node_group_name
}

output "eks_node_group_status" {
  description = "EKS managed node group status"
  value       = module.eks.node_group_status
}