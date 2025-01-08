#!/bin/bash

# This script is tested on Ubuntu 24.04 LTS in an WSL2 environment

# Update OS & install docker
sudo apt update
sudo apt upgrade
sudo apt install jq docker.io -y

# Give current user access to docker
sudo usermod -aG docker $(whoami)

# Install K3S
export K3S_KUBECONFIG_MODE="644"
curl -sfL https://get.k3s.io | sh -

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
LASTEST_K9S_VERSION=$(curl -s https://api.github.com/repos/derailed/k9s/releases/latest | jq -r .tag_name)
wget https://github.com/derailed/k9s/releases/download/${LASTEST_K9S_VERSION}/k9s_linux_amd64.deb -O /tmp/k9s_linux_amd64.deb && sudo apt install /tmp/k9s_linux_amd64.deb && rm /tmp/k9s_linux_amd64.deb

# Link to kube config for k9s
ln -fs /etc/rancher/k3s/k3s.yaml ~/.kube/config

echo
echo "!!! Please logout and login again to make use of new group membership !!!"

# Install Helm
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
rm get_helm.sh
