# etap build
FROM node:20-alpine AS builder

ARG VITE_BACKEND_API_URL
ENV VITE_BACKEND_API_URL=${VITE_BACKEND_API_URL}

WORKDIR /app

COPY frontend/hermes/package.json frontend/hermes/package-lock.json* ./
RUN npm install

COPY frontend/hermes/ ./
RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
