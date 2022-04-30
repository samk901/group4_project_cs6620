#!/bin/bash
#A script to install, compile and run API and UI applications

# Install and run API application
echo "==> Installing npm in API"
cd /home/ec2-user/group4_project_cs6620/tracker-api/
npm install

echo "==> Starting API application"
npm start

