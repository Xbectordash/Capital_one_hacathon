# Use official Node.js image as a parent image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json ./
COPY package-lock.json ./

# Install dependencies
RUN npm install --production

# Copy the rest of the application code
COPY . .

# Expose port (adjust as needed)
EXPOSE 3000

# Start the application (adjust if entry point is different)

CMD ["node", "src/index.js"]