# Build stage
FROM node:18-alpine AS build
WORKDIR /app
COPY frontend/package*.json ./
COPY frontend/ ./
RUN npm ci
# Ensure Vite can find the entry `index.html` when it's stored under `public/` in the repo.
# Move public/index.html to project root so Vite/Rollup can resolve it during the container build.
RUN if [ -f public/index.html ]; then cp public/index.html ./index.html; fi
RUN npm run build

# Production stage: serve with nginx
FROM nginx:stable-alpine
COPY --from=build /app/dist /usr/share/nginx/html
# Simple nginx config: rely on default, ensure SPA fallback
RUN rm /etc/nginx/conf.d/default.conf
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
