FROM node:24-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install react-router-dom
RUN npm install

COPY . .

EXPOSE 8080

CMD ["npm", "run", "dev", "--", "--host", "--port", "8080"]