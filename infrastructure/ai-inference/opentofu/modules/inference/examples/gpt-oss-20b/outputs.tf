output "public_ip" {
  description = "Public IP address of the AI inference server"
  value       = module.gpt_oss_20b.public_ip
}
