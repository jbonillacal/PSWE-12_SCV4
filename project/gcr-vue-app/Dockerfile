# Use node to build the Vue app
FROM node:18 as build-stage

WORKDIR /app

# Copy package files separately to optimize caching
COPY package.json package-lock.json ./
RUN npm install

# Copy the rest of the application files
COPY . .  

# Build the Vue app
RUN npm run build

# Use nginx to serve the static files
FROM nginx:alpine as production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
