# Utiliser Node.js 18 LTS Alpine pour une image plus légère
FROM node:18-alpine

# Définir le répertoire de travail
WORKDIR /app

# Variables d'environnement pour le développement React
ENV NODE_ENV=development \
    CHOKIDAR_USEPOLLING=true \
    WATCHPACK_POLLING=true

# Installer les dépendances système si nécessaires
RUN apk add --no-cache git

# Copier package.json et package-lock.json (si existe)
COPY package*.json ./

# Installer les dépendances Node.js
# Utiliser npm ci si package-lock.json existe, sinon npm install
RUN if [ -f package-lock.json ]; then npm ci; else npm install; fi

# Copier le reste du code source
COPY . .

# Exposer le port 3000
EXPOSE 3000

# Commande par défaut pour démarrer React
CMD ["npm", "start"]