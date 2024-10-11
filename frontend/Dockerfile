FROM node:16-alpine as build

WORKDIR /app

COPY package*.json ./

RUN npm add global @vue/cli
RUN npm install

COPY . .

ENTRYPOINT ["npm", "run", "serve", "--", "--host", "0.0.0.0", "--port", "8080"]
