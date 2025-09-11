output "public_ip" {
  description = "Public IP address of the AI inference server"
  value       = module.qwen3_0_6b.public_ip
}
