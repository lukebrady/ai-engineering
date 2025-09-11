module "gemma_3_27b" {
  source = "../../../"

  ami_id               = data.aws_ami.ai_inference.id
  instance_type        = "g6.12xlarge"
  vpc_id               = data.aws_vpc.default.id
  subnet_id            = data.aws_subnets.default.ids[0]
  iam_instance_profile = data.aws_iam_instance_profile.ai_inference_profile.name
  key_name             = "gemma_3_27b_key"

  allowed_ip_addresses = var.allowed_ip_addresses
  hugging_face_token   = var.hugging_face_token
  model                = "google/gemma-3-27b-it"
  vllm_args            = "--tensor-parallel-size=4" # 4 GPUs
  vllm_timeout         = 900
  vllm_version         = "latest"
}
