# Stage 1: Build the application
FROM node:20 AS builder

WORKDIR /usr/src/app

# Copy package.json and package-lock.json to leverage Docker cache
COPY package*.json ./
RUN npm install

# Copy the rest of the application source code
COPY . .

# Compile TypeScript to JavaScript
RUN npm run build

# Stage 2: Create the production image
FROM node:20-slim

# Set the environment to production
ENV NODE_ENV=production
ENV PORT=3000

WORKDIR /usr/src/app

# Copy package files from the context
COPY package*.json ./

# Install only production dependencies
RUN npm install --omit=dev

# Copy the compiled code from the builder stage
COPY --from=builder /usr/src/app/dist ./dist

# Expose the port the app runs on
EXPOSE ${PORT}

# The command to run the application
CMD ["node", "dist/main.js"]