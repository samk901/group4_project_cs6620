#!/bin/bash
#A script to install, compile and run API and UI applications

# Install and run API application
echo "==> Installing npm in API"
cd /home/ec2-user/group4_project_cs6620/tracker-api/
npm install

echo "==> Starting API application"
npm start

# Install and run UI Application
echo "===> Installing npm in UI"
cd /home/ec2-user/group4_project_cs6620/tracker-ui/
npm install

echo "==> Compiling Webpack files for production"
npm run compile

echo "==> Starting UI Application"
npm start


