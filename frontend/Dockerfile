FROM node:22-alpine AS build

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:1.27-alpine

ENV PORT=80 \
    SITE1_HOSTPORT=site1:8001 \
    SITE2_HOSTPORT=site2:8002 \
    SITE3_HOSTPORT=site3:8003 \
    SITE4_HOSTPORT=site4:8004 \
    SITE5_HOSTPORT=site5:8005 \
    TRACKER_HOSTPORT=tracker:8007

COPY nginx.conf.template /etc/nginx/templates/default.conf.template
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
