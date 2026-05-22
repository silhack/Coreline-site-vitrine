# ── Build stage ────────────────────────────────────────────
FROM node:22.3.0-alpine AS build

WORKDIR /app

COPY package*.json ./

# ✅ Install ALL deps (devDeps needed for the build)
RUN npm ci

COPY . .

RUN npm run build

# ── Production stage ───────────────────────────────────────
FROM nginx:1.27.0-alpine

# ✅ Non-root user setup & permission hardening
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    touch /var/run/nginx.pid && \
    chown nginx:nginx /var/run/nginx.pid

# Copy compiled assets from build stage
COPY --from=build /app/dist /usr/share/nginx/html

# ✅ SPA routing + cache headers (Make sure it uses port 8080!)
COPY nginx.conf /etc/nginx/conf.d/default.conf

USER nginx

# 💡 Port 8080 is mandatory for non-root users
EXPOSE 8080

# ✅ Healthcheck updated to monitor port 8080
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget -qO- http://localhost:8080/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
