# syntax=docker/dockerfile:1
FROM node:24-trixie-slim AS build
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends python3 ca-certificates && rm -rf /var/lib/apt/lists/*
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm npm ci
COPY . .
RUN npm run runtime:setup && npm run build && npm test && npm run test:runner
RUN npm prune --omit=dev

FROM node:24-trixie-slim AS runtime
WORKDIR /app
ENV NODE_ENV=production HOST=0.0.0.0 PORT=8765 \
    DATABASE_PATH=/data/codey.sqlite BACKUP_DIR=/data/backups \
    CODEY_SECRET_FILE=/data/auth-secret CODEY_CONTROL_DIR=/tmp/codey-control
COPY --from=build /app/package.json /app/package-lock.json ./
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/build ./build
COPY --from=build /app/.generated ./.generated
COPY --from=build /app/.runtime/pyodide ./.runtime/pyodide
COPY --from=build /app/runner ./runner
COPY scripts/container-entrypoint.mjs scripts/container-healthcheck.mjs ./scripts/
RUN mkdir -p /data && chown 99:100 /data
USER 99:100
VOLUME ["/data"]
EXPOSE 8765
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 CMD ["node", "scripts/container-healthcheck.mjs"]
ENTRYPOINT ["node", "scripts/container-entrypoint.mjs"]
