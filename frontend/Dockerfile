FROM node:18-alpine AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

COPY package.json package-lock.json ./
RUN  npm install

FROM node:18-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED 1
# If the backend is not running locally, it is important to uncomment and modify the following line
# ENV NEXT_PUBLIC_BACKEND_ENDPOINT http://x.x.x.x:8000

RUN npm run build:docker

FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
COPY --from=builder --chown=nextjs:nodejs  /app/.next/standalone ./

USER nextjs

EXPOSE 3000

ENV PORT 3000

CMD ["node", "server.js"]
