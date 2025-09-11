module "gpt_oss_20b" {
  source = "../../"

  ami_id               = data.aws_ami.ai_inference.id
  instance_type        = "g6.xlarge"
  vpc_id               = data.aws_vpc.default.id
  subnet_id            = data.aws_subnets.default.ids[0]
  iam_instance_profile = data.aws_iam_instance_profile.ai_inference_profile.name
  key_name             = "gpt_oss_20b_key"

  allowed_ip_addresses = var.allowed_ip_addresses
  hugging_face_token   = var.hugging_face_token
  model                = "openai/gpt-oss-20b"
  vllm_timeout         = 600
  vllm_version         = "v0.10.1"
}
