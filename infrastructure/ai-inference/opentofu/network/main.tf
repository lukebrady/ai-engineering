module "vpc" {
  source = "git::https://github.com/lukebrady/tf-modules.git//networking/vpc?ref=feat/tf-module"

  cidr_block = "10.0.0.0/16"
}

module "dmz" {
  source = "git::https://github.com/lukebrady/tf-modules.git//networking/dmz-subnet?ref=feat/tf-module"

  for_each = var.availability_zones

  availability_zone = each.value
  cidr_block        = cidrsubnet(module.vpc.cidr_block, 3, index(tolist(var.availability_zones), each.value))
  igw_id            = module.vpc.igw_id
  vpc_id            = module.vpc.vpc_id
}

module "nat" {
  source = "git::https://github.com/lukebrady/tf-modules.git//networking/nat-instance-subnet?ref=feat/tf-module"

  for_each = var.availability_zones

  availability_zone = each.value
  cidr_block        = cidrsubnet(module.vpc.cidr_block, 3, index(tolist(var.availability_zones), each.value) + length(var.availability_zones))
  nat_subnet_id     = module.dmz[each.value].subnet_id
  vpc_id            = module.vpc.vpc_id
}

module "vpn" {
  source = "git::https://github.com/lukebrady/tf-modules.git//networking/vpn/openvpn?ref=feat/tf-module"

  allowed_ip_addresses = var.allowed_ip_addresses
  route_table_ids      = toset([for subnet in module.nat : subnet.route_table_id])
  subnet_id            = module.dmz[tolist(var.availability_zones)[0]].subnet_id
  vpc_id               = module.vpc.vpc_id
}
