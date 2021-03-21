# pull the base image
FROM node:alpine

# set the working direction
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# install app dependencies
COPY ./app/package.json ./

COPY ./app/package-lock.json ./

RUN npm install

# add app
COPY ./app ./

# start app
CMD ["npm", "start"]
