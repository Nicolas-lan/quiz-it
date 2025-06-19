FROM node:18-alpine

# Installation des dépendances système
RUN apk add --no-cache git python3 make g++ bash

# Installation de Claude Code
RUN npm install -g @anthropic-ai/claude-code

# Configuration du répertoire de travail
WORKDIR /workspace

# Point d'entrée direct avec node pour éviter les problèmes de shebang
ENTRYPOINT ["node", "/usr/local/lib/node_modules/@anthropic-ai/claude-code/cli.js"]