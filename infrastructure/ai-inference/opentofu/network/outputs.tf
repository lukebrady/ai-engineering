output "vpn_public_ip" {
  description = "Public IP address of the VPN"
  value       = module.vpn.public_ip
}
