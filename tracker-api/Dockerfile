# Pull Node image from Docker Hub
FROM node:14-slim

##Setting Working Directory
#WORKDIR /usr/app

# Copying only package.json
COPY group4_project_cs6620/tracker-api tracker-api
#COPY group4_project_cs6620/tracker-api/package.json ./

WORKDIR tracker-api

# Install Dependencies
RUN npm install

# Copy rest of the code to container
COPY . .
EXPOSE 3080

# Run the API on Nodemon
CMD ["npm", "start"]