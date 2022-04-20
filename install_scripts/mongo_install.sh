#!/bin/bash
# A script to install and start mongodb

# Define Directories
APIDIR=/tracker-api
UIDIR=/tracker-ui

# Define Versions if needed


# Move Repo File to yum repo
echo "==> Moving mongo-org-5.0.repo to /etc.yum.repos.d/ to allow for yum install"
sudo cp mongodb-org-5.0.repo /etc/yum.repos.d/

# Install mongodb
echo "==> Installing latest stable version of MongoDB"
sudo yum install -y mongodb-org

# Start mongod process
echo "==> Starting mongod process"
sudo systemctl start mongod

# Show MongoDB Process is running
echo "==> Showing mongodb porcess should see it active"
sudo systemctl status mongod

# Execute Mongo Script to initialize database
echo "==> Running init.mongo.js...Expect to see 2 issues inserted"
mongo issuetracker /home/ec2-user/group4_project_cs6620/tracker-api/scripts/init.mongo.js

# Execute Mongo Script to generate database data
echo "==> Running generate_data.mongo.js...Expect to see issue count of 102"
mongo issuetracker /home/ec2-user/group4_project_cs6620/tracker-api/scripts/generate_data.mongo.js





