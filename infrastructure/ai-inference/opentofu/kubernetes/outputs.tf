# Outputs from the Kubernetes cluster module
output "artifact_bucket_name" {
  description = "S3 bucket used to exchange bootstrap artifacts (join command)"
  value       = module.kubernetes.artifact_bucket_name
}

output "control_plane_private_ips" {
  description = "Private IP addresses of control plane instances"
  value       = module.kubernetes.control_plane_private_ips
}

output "worker_private_ips" {
  description = "Private IP addresses of worker instances"
  value       = module.kubernetes.worker_private_ips
}

output "control_plane_public_ips" {
  description = "Public IP addresses of control plane instances (if assigned)"
  value       = module.kubernetes.control_plane_public_ips
}

output "worker_public_ips" {
  description = "Public IP addresses of worker instances (if assigned)"
  value       = module.kubernetes.worker_public_ips
}

output "control_plane_subnet_ids" {
  description = "Subnet IDs of control plane instances"
  value       = data.aws_subnets.control_plane.ids
}

output "worker_subnet_ids" {
  description = "Subnet IDs of worker instances"
  value       = data.aws_subnets.worker.ids
}

output "cluster_name" {
  description = "Name of the Kubernetes cluster"
  value       = var.cluster_name
}

output "vpc_id" {
  description = "VPC ID where the cluster is deployed"
  value       = var.vpc_id
}

output "aws_region" {
  description = "AWS region where the cluster is deployed"
  value       = var.aws_region
}