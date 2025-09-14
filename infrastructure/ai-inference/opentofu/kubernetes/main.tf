# Kubernetes cluster module
module "kubernetes" {
  source = "git::https://github.com/lukebrady/tf-modules.git//kubernetes/cluster?ref=feat/tf-module"

  # Required variables
  cluster_name             = var.cluster_name
  vpc_id                   = var.vpc_id
  control_plane_subnet_ids = data.aws_subnets.control_plane.ids
  worker_subnet_ids        = data.aws_subnets.worker.ids
  region                   = var.aws_region

  # Optional customizations
  control_plane_count         = var.control_plane_count
  worker_count                = var.worker_count
  control_plane_instance_type = var.control_plane_instance_type
  worker_instance_type        = var.worker_instance_type
  associate_public_ip         = var.associate_public_ip

  # Security settings
  ssh_ingress_cidrs      = var.ssh_ingress_cidrs
  api_ingress_cidrs      = var.api_ingress_cidrs
  nodeport_ingress_cidrs = var.nodeport_ingress_cidrs

  # S3 configuration
  create_artifact_bucket = var.create_artifact_bucket
  artifact_bucket_name   = var.artifact_bucket_name

  # Tags
  tags = merge(var.default_tags, var.additional_tags)
}