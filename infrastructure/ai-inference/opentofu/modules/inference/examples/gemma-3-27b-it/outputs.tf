output "public_ip" {
  description = "Public IP address of the AI inference server"
  value       = module.gemma_3_27b.public_ip
}
