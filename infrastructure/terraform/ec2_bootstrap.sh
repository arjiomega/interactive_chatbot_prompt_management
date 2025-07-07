#!/bin/bash
exec > /var/log/user-data.log 2>&1
set -x

# Wait for networking
until ping -c1 github.com; do sleep 3; done

# Update and install dependencies
export DEBIAN_FRONTEND=noninteractive
apt-get clean
apt-get update -y
apt-get install -y software-properties-common
apt-get install -y git python3 python3-venv pip

# Setup project
cd /home/ubuntu
git clone https://github.com/arjiomega/interactive_chatbot_prompt_management.git || exit 1
cd interactive_chatbot_prompt_management

echo "OPENAI_API_KEY=${OPENAI_API_KEY}" >> .env

python3 -m venv venv
source venv/bin/activate
pip install -e .

# Start the app
nohup streamlit-start > streamlit.log 2>&1 &
