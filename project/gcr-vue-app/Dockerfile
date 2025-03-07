# Use node to build the Vue app
FROM node:18 as build-stage

WORKDIR /app

COPY gcr-vue-app/package.json gcr-vue-app/package-lock.json ./
RUN npm install

COPY gcr-vue-app ./
RUN npm run build

# Use nginx to serve the static files
FROM nginx:alpine as production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
