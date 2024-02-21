FROM node:latest AS build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
RUN rm -rf node_modules  # Remove unnecessary dependencies
RUN npm install --production  # Install production dependencies only

# Stage 2: Serve the built Vue.js application using Nginx
FROM nginx:latest
COPY nginx.conf /etc/nginx/nginx.conf
COPY cors.conf /etc/nginx/cors.conf
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
