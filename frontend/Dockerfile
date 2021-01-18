# Write your own dockerfile
FROM node

WORKDIR /code
COPY package.json .

RUN npm install

COPY . .

ENTRYPOINT ["npm", "start"]