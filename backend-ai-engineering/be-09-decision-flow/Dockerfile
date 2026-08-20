FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY be-09-decision-flow/package*.json ./
RUN npm ci

# Copy application code
COPY be-09-decision-flow/src ./src
COPY be-09-decision-flow/public ./public
COPY be-09-decision-flow/next.config.js ./
COPY be-09-decision-flow/tsconfig.json ./
COPY be-09-decision-flow/tailwind.config.ts ./
COPY be-09-decision-flow/postcss.config.js ./

# Build the application
RUN npm run build

# Expose port
EXPOSE 3009

# Default command
CMD ["npm", "start"]