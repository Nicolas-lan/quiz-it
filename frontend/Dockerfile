FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

# Installation des dépendances
RUN npm install

COPY public/ ./public/
COPY src/ ./src/
COPY tailwind.config.js ./
COPY postcss.config.js ./

EXPOSE 3000

CMD ["npm", "start"] 