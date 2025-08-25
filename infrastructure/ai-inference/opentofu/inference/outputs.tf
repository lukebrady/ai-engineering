# Outputs for AI Inference Server

output "instance_id" {
  description = "ID of the AI inference server instance"
  value       = aws_instance.ai_inference_server.id
}

output "public_ip" {
  description = "Public IP address of the AI inference server"
  value       = var.create_eip ? aws_eip.ai_inference[0].public_ip : aws_instance.ai_inference_server.public_ip
}

output "private_ip" {
  description = "Private IP address of the AI inference server"
  value       = aws_instance.ai_inference_server.private_ip
}

output "instance_arn" {
  description = "ARN of the AI inference server instance"
  value       = aws_instance.ai_inference_server.arn
}

output "ami_id" {
  description = "ID of the AMI used for the instance"
  value       = data.aws_ami.ai_inference.id
}

output "ami_name" {
  description = "Name of the AMI used for the instance"
  value       = data.aws_ami.ai_inference.name
}

output "ssh_key_name" {
  description = "Name of the SSH key pair used for the instance"
  value       = aws_key_pair.ai_inference_key.key_name
}

output "ssh_private_key_file" {
  description = "Path to the private SSH key file"
  value       = local_file.private_key.filename
  sensitive   = true
}
