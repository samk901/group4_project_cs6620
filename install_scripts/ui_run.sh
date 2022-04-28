# Install and run UI Application
echo "===> Installing npm in UI"
cd /home/ec2-user/group4_project_cs6620/tracker-ui/
npm install

echo "==> Compiling Webpack files for production"
npm run compile

echo "==> Starting UI Application"
npm start


