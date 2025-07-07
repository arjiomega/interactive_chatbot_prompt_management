provider "aws" {
  region = "us-east-1"
}

variable "key_pair_name" {
  description = "Name of the existing EC2 Key Pair"
  type        = string
}

variable "my_ip" {
    description = "My IP"
    type = string
}

variable "OPENAI_API_KEY" {
  description = "Your OPEN AI API KEY"
  type = string
}

resource "aws_security_group" "sg" {
  name        = "allow_ssh_ping"
  description = "Allow SSH and ICMP"

  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = [var.my_ip]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "free_tier_ec2" {
  ami                    = "ami-020cba7c55df1f615"
  instance_type          = "t2.micro"
  key_name               = var.key_pair_name
  associate_public_ip_address = true

  vpc_security_group_ids = [aws_security_group.sg.id]

  user_data = templatefile("${path.module}/ec2_bootstrap.sh", {
    OPENAI_API_KEY = var.OPENAI_API_KEY
  })


  tags = {
    Name = "FreeTier-Instance"
  }
}

output "public_ip" {
  value = aws_instance.free_tier_ec2.public_ip
}