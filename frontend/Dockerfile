# etap build
FROM node:20-alpine AS builder

ARG VITE_BACKEND_API_HOST
ENV VITE_BACKEND_API_HOST=${VITE_BACKEND_API_HOST}

WORKDIR /app

COPY frontend/hermes/package.json frontend/hermes/package-lock.json* ./
RUN npm install

COPY frontend/hermes/ ./
RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
