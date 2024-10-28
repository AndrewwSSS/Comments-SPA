FROM node:16-alpine

WORKDIR /app

COPY package*.json ./

RUN npm add global @vue/cli \
    && npm install

COPY . .

ENTRYPOINT ["npm", "run", "serve", "--", "--host", "0.0.0.0", "--port", "8080"]
