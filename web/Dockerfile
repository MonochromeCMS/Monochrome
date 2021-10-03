# build stage
FROM node:lts-slim as build-stage
WORKDIR /app
COPY package.json ./
COPY yarn.lock ./
RUN yarn

ARG VUE_APP_DOMAIN_NAME=localhost
ARG VUE_APP_PROTOCOL=http
ARG VUE_APP_TITLE=Monochrome
ARG VUE_APP_DESCRIPTION

COPY . .
RUN yarn build

# production stage
FROM caddy:2-alpine as final-stage
COPY ./Caddyfile /etc/caddy/Caddyfile
WORKDIR /srv
COPY --from=build-stage /app/dist .
RUN mkdir /srv/media
