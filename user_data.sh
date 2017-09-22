#!/bin/bash -v
echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
export DEBIAN_FRONTEND=noninteractive 
sudo apt update -y
sudo apt install git ansible -y
git clone https://github.com/TachyonProject/ansible-django-stack
cd ~/ansible-django-stack & ansible-playbook -vvvv -i inventory.ini ansible/playbooks/playbook-install-python2.yml
cd ~/ansible-django-stack & ansible-playbook -vvvv -i ansible/inventory.ini ansible/playbooks/playbook-all.yml
