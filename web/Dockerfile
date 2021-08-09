# build stage
FROM node:lts-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# production stage
FROM caddy:2-alpine as final-stage
COPY ./Caddyfile /etc/caddy/Caddyfile
WORKDIR /srv
COPY --from=build-stage /app/dist .
RUN mkdir /srv/media
