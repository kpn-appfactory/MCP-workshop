#!/bin/bash

# This script is tested on Ubuntu 24.04 LTS in an WSL2 environment

# Update OS & install docker
sudo apt update
sudo apt upgrade
sudo apt install docker.io -y

# Give current user access to docker
sudo usermod -aG docker $(whoami)

# Install K3S
curl -sfL https://get.k3s.io | sh -

# Allow all users to access Kubernetes (k3s)
sudo chmod +r /etc/rancher/k3s/k3s.yaml

# Configure bash completion and alias for kubectl
LINE='source <(kubectl completion bash)'
grep "${LINE}" ~/.bashrc > /dev/null
if [ ${?} -gt 0 ]
then
    echo "${LINE}" >> ~/.bashrc
    echo 'alias k=kubectl' >> ~/.bashrc
    echo 'complete -o default -F __start_kubectl k' >> ~/.bashrc
fi

# Install k9s
wget https://github.com/derailed/k9s/releases/download/v0.32.7/k9s_linux_amd64.deb -O /tmp/k9s_linux_amd64.deb && sudo apt install /tmp/k9s_linux_amd64.deb && rm /tmp/k9s_linux_amd64.deb

# Link to kube config for k9s
ln -fs /etc/rancher/k3s/k3s.yaml ~/.kube/config

echo
echo "!!! Please logout and login again to make use of new group membership !!!"
