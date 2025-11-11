# Build stage
FROM node:24-alpine AS build
WORKDIR /app
COPY frontend/package*.json ./
COPY frontend/ ./
# Use npm ci when a lockfile is present for reproducible installs; otherwise fall
# back to npm install so builds don't fail on systems that haven't committed
# package-lock.json (common on some projects).
RUN if [ -f package-lock.json ] || [ -f npm-shrinkwrap.json ]; then \
			npm ci; \
		else \
			npm install --no-audit --no-fund; \
		fi
RUN npm run build

# Production stage: serve with nginx
FROM nginx:stable-alpine
COPY --from=build /app/dist /usr/share/nginx/html
# Simple nginx config: rely on default, ensure SPA fallback
RUN rm /etc/nginx/conf.d/default.conf
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
