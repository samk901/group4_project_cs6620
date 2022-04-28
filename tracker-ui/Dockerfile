# Pull the Node Image from Docker Hub
FROM node:14-slim

# Setting Working Directory
COPY group4_project_cs6620/tracker-ui/package.json package.json
COPY group4_project_cs6620/tracker-ui tracker-ui

WORKDIR tracker-ui
RUN npm install
EXPOSE 3000
RUN npm update
RUN npm run compile
CMD ["npm", "start" ]
