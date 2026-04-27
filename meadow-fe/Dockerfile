FROM m.daocloud.io/docker.io/library/node:23.6.0-alpine AS builder

WORKDIR /vue-app

COPY package.json pnpm-lock.yaml ./
RUN npm install --registry=https://registry.npmmirror.com -g pnpm
RUN pnpm install --registry=https://registry.npmmirror.com --frozen-lockfile

COPY . .
RUN pnpm build:dev

FROM m.daocloud.io/docker.io/library/nginx:1.27.3-alpine

WORKDIR /vue-app
COPY --from=builder /vue-app/dist /vue-app
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
