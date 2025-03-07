# Use node to build the Vue app
FROM node:18 as build-stage

WORKDIR /app

# Copy package files separately to leverage caching
COPY package.json package-lock.json ./
RUN npm install

# Copy the rest of the application
COPY . .

# Ensure Vue CLI is installed before building
RUN npm install --save-dev @vue/cli-service  
RUN npm install --save-dev vue-template-compiler


# Build the Vue app
RUN npm run build

# Use nginx to serve the static files
FROM nginx:alpine as production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html

# Cloud Run requires the app to listen on PORT=8080
ENV PORT=8080
EXPOSE 8080


CMD ["nginx", "-g", "daemon off;"]
