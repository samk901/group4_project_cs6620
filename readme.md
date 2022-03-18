## Getting Started

Install the following

1- Install npm\
2- Install mongo\
3- Downgrade node to 10.24.0\

## Tracker-api

-- Navigate to tracker-api directory\
-- In one terminal start mongo\

```console
mongo
```

-- In another terminal start the api application

```console
npm start
```

Application should connect to mongodb (will need at actually set this up)\
Application should start on port 3000\
You can see the graphql UI at "localhost:3000/graphql"\
Once we set up mongo you will be able to test the api through the gui

## Tracker-ui

-- In a new terminal navigate to tracker-ui directory\
-- Make sure that the tracker-api is up and running\
-- Compile the source code\

```console
npm run compile
```

-- Start the application locally

```console
npm run start
```

Application should start on port 8000\
You should be able to see the barebones website at "localhost:8000"\

### Current Issues

-- Will need to enable Google Authentication in order to interact with the CRUD operations\
-- Setup new MongoDB Atlas account and run the mongo scripts to put in dummy data\
