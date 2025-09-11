module "qwen3_0_6b" {
  source = "../../../"

  ami_id               = data.aws_ami.ai_inference.id
  vpc_id               = data.aws_vpc.default.id
  subnet_id            = data.aws_subnets.default.ids[0]
  iam_instance_profile = data.aws_iam_instance_profile.ai_inference_profile.name
  key_name             = "qwen3_0_6b_key"

  allowed_ip_addresses = var.allowed_ip_addresses
  hugging_face_token   = var.hugging_face_token
  model                = "Qwen/Qwen3-0.6B"
  vllm_timeout         = 360
  vllm_version         = "latest"
}
