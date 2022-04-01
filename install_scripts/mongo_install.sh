#!/bin/bash
# A script to install and start mongodb

# Define Directories
APIDIR=/tracker-api
UIDIR=/tracker-ui

# Define Versions if needed


# Move Repo File to yum repo
echo "==> Moving mongo-org-5.0.repo to /etc.yum.repos.d/ to allow for yum install"
sudo cp mongo-org-5.0.repo /etc/yum.repos.d/

# Install mongodb
echo "==> Installing latest stable version of MongoDB"
sudo yum install -y mongodb-org

# Start mongod process
echo "==> Starting mongod process"
sudo systemctl start mongod

# Show MongoDB Process is running
echo "==> Showing mongodb porcess should see it active"
sudo systemctl status mongod


