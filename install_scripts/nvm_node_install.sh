#!/bin/bash
# A script to install nvm and node version 10.24.0 

# Define Directories
APIDIR=/tracker-api
UIDIR=/tracker-ui

# Define Versions
INSTALL_NODE_VER=10.24.0
INSTALL_NVM_VER=0.35.3

echo "==> Ensuring .bashrc exists and is writable"
touch ~/.bashrc

echo "==> INstalling node version manager (NVM). Version $INSTALL_NVM_VER"
# Removes nvm if already installed
rm -rf ~/.nvm
# Unset exported variable
export NVM_DIR

# Install NVM
curl -o- https://raw.githubusercontent.com/creationix/nvm/v$INSTALL_NVM_VER/install.sh | bash
# Make nvm command available to terminal
source ~/.nvm/nvm.sh

echo "==> Installing node js version $INSTALL_NODE_VER"
nvm install $INSTALL_NODE_VER

# Will make node 10.24.0 default for system
echo "==> Make this version system default"
nvm alias default $INSTALL_NODE_VER
nvm use default

# Allows user to use nvm without reopening terminal
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion


