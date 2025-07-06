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

resource "aws_security_group" "sg" {
  name        = "allow_ssh_ping"
  description = "Allow SSH and ICMP"

  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = [var.my_ip]
  }
}

resource "aws_instance" "free_tier_ec2" {
  ami                    = "ami-020cba7c55df1f615"
  instance_type          = "t2.micro"
  key_name               = var.key_pair_name
  associate_public_ip_address = true

  vpc_security_group_ids = [aws_security_group.sg.id]

  user_data = <<-EOF
            #!/bin/bash
            # Install dependencies
            yum update -y
            yum install -y git python3

            # Set up a virtual environment
            python3 -m venv /home/ec2-user/appenv
            source /home/ec2-user/appenv/bin/activate

            # Clone your Streamlit repo
            cd /home/ec2-user
            git clone https://github.com/yourusername/your-streamlit-repo.git
            cd your-streamlit-repo

            # Install requirements if present
            if [ -f requirements.txt ]; then
            pip install -r requirements.txt
            fi

            # Run Streamlit app in the background, listening on port 8501
            streamlit run app.py --server.port 8501 --server.enableCORS false \
            &> /home/ec2-user/streamlit.log &
            EOF


  tags = {
    Name = "FreeTier-Instance"
  }
}

output "public_ip" {
  value = aws_instance.free_tier_ec2.public_ip
}