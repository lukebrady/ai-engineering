# IAM role for Packer build and inference server
resource "aws_iam_role" "ai_inference_role" {
  name = "ai-inference-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name = "ai-inference-role"
  }
}

# Attach the AmazonSSMManagedInstanceCore policy to the role
resource "aws_iam_role_policy_attachment" "ssm_managed_instance_core" {
  role       = aws_iam_role.ai_inference_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

# Attach S3 read-only access for downloading NVIDIA drivers and other resources
resource "aws_iam_role_policy_attachment" "s3_read_only" {
  role       = aws_iam_role.ai_inference_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
}

# IAM instance profile for the EC2 instance
resource "aws_iam_instance_profile" "ai_inference_profile" {
  name = "ai-inference-profile"
  role = aws_iam_role.ai_inference_role.name

  tags = {
    Name = "ai-inference-profile"
  }
}

resource "aws_ssm_parameter" "ai_inference_profile" {
  name  = "ai-inference-profile"
  type  = "String"
  value = aws_iam_instance_profile.ai_inference_profile.name
}
