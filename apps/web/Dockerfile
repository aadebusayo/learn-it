FROM node:22.21.1-alpine3.22 AS deps
WORKDIR /app
RUN corepack enable
COPY package.json pnpm-workspace.yaml ./
COPY apps/web/package.json apps/web/package.json
COPY packages/shared/package.json packages/shared/package.json
RUN pnpm install --frozen-lockfile=false

FROM deps AS runner
WORKDIR /app
COPY . .
EXPOSE 3000
CMD ["pnpm", "--filter", "@learn-it/web", "dev"]
