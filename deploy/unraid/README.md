# Codey on Unraid with Cloudflare Tunnel

Repository: **https://github.com/mehhyin/codey**

Image: **ghcr.io/mehhyin/codey:latest**

WebUI: **https://codey.john.shiksha**

Container port: **8765/tcp**

Codey uses one hostname and one port for the app, account API and browser Python packages. There is no second runtime hostname. Python runs in a browser worker; no learner code runs in the container or on Unraid.

## Publish an image

The repository root is the `codey` directory containing `Dockerfile` and `package.json`. Include all source files and `.github/workflows/container-release.yml` when pushing to GitHub.

1. In **Actions → Container release → Run workflow**, leave **publish** unchecked for a build-only check.
2. Publish a GitHub release from a commit containing these changes with a Docker-compatible tag such as **v3.0.0**. Do not reuse the existing older v1/v2 tags.
3. The workflow builds for `linux/amd64`, runs all 173 reference solutions, account/proxy tests and a container smoke test. It publishes only after these checks pass.
4. Stable releases publish their exact tag, `latest` and a SHA tag to **ghcr.io/mehhyin/codey**. Prereleases publish the exact tag and SHA without changing `latest`. Manual publishing creates only a SHA tag.
5. Configure the package visibility in GitHub. A **public container package** is simplest for Unraid pulls; new GHCR packages can be private even when the source repository is public. The workflow does not change visibility.

The workflow uses GitHub's automatic `GITHUB_TOKEN` with `packages: write`; no Docker Hub credentials are needed. For a private package, authenticate Unraid to GHCR using a GitHub personal access token (classic) with `read:packages` and package access. Do not put registry credentials in the template or repository.

References: [GitHub image publishing](https://docs.github.com/en/actions/tutorials/publish-packages/publish-docker-images), [GHCR permissions and visibility](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry).

## Install the template

1. Copy **codey.xml** to `/boot/config/plugins/dockerMan/templates-user/my-codey.xml` on Unraid.
2. Open **Docker → Add Container** and select **codey**.
3. Repository is already set to `ghcr.io/mehhyin/codey:latest`. Use a fixed release tag if you prefer controlled upgrades.
4. Keep the container port **8765**. Choose a free host port; the default is also **8765**.
5. Keep **App data** mapped to `/mnt/user/appdata/codey` → `/data`.
6. Public app URL and WebUI are already set to `https://codey.john.shiksha`.
7. Enter Google and/or GitHub OAuth credentials if available. Leave both values empty for an unused provider. Guest practice works without OAuth.
8. Apply. The container should become healthy before you configure the tunnel.

The image runs as **UID 99 / GID 100** with no privileged mode or Docker socket mount. Appdata must be writable by that user/group. If necessary, adjust ownership of that specific appdata folder on Unraid. PUID/PGID variables are not used by this image.

## Configure your existing Cloudflare Tunnel

Add one published application route to your existing tunnel:

| Field | Value |
| --- | --- |
| Public hostname | `codey.john.shiksha` |
| Service type | HTTP |
| Service URL | `UNRAID-LAN-IP:8765` |
| HTTP Host Header | `codey.john.shiksha` |

If you mapped a different **host** port, use it in Service URL. If `cloudflared` and Codey share a user-defined Docker network, the service can instead be `http://codey:8765`. Do not use `localhost` inside a separate tunnel container; that refers to the tunnel container itself.

Set the Host header override under the route's additional HTTP settings. Codey validates the configured public Host and does not trust arbitrary `X-Forwarded-Host` headers. Cloudflare provides HTTPS externally while connecting to the container over HTTP. No certificate installation inside Codey, router port forwarding, second DNS name or second port is required.

Send **all paths** through this route, including `/api/*` and `/python/*`. Do not add redirects, transform paths, override Content-Security-Policy, or serve uploaded content beneath `/python/`. Avoid interactive challenges or a separate Access login on worker assets; those return HTML where Python expects packages. Do not cache account/API responses. If you add a custom Cloudflare cache rule, bypass `/api/*`; the app emits `Cache-Control: no-store`.

Open **https://codey.john.shiksha**, not a plain HTTP LAN URL. Browser secure-context APIs and remote OAuth require HTTPS. Cloudflare Tunnel configuration reference: [HTTP Host Header setting](https://developers.cloudflare.com/tunnel/configuration/).

## OAuth values

Google:

- Authorized JavaScript origin: `https://codey.john.shiksha`
- Redirect URI: `https://codey.john.shiksha/api/auth/callback/google`

GitHub:

- Homepage URL: `https://codey.john.shiksha`
- Authorization callback URL: `https://codey.john.shiksha/api/auth/callback/github`

Enter the provider client IDs and secrets in the Unraid template. Restart the container after edits. While Google is in testing, add your account as a test user. See the main README for provider registration steps.

## Persistence and backups

Everything durable lives in `/data`:

- `codey.sqlite` plus WAL/SHM companions: accounts, drafts, progress and submission history.
- `auth-secret`: generated once if the optional secret override is blank. Keep it across upgrades.
- `backups/`: consistent database snapshots.

Create a database backup without stopping Codey:

```sh
docker exec codey node scripts/container-entrypoint.mjs backup
```

Protect a copy of `auth-secret` alongside your backups. If using a secret override, back up that value securely. Masked XML values are still stored in Unraid configuration files; keep exports containing credentials private.

To migrate from the local app, stop it and copy `data/codey.sqlite` into Unraid appdata. Copy any WAL/SHM companions that remain after shutdown. Set the same `BETTER_AUTH_SECRET` from the local `.env` as the template override, or save it as `auth-secret` readable by UID 99. Sign in again at the new domain. If migrating an older Pyroom database, copy it as `codey.sqlite`; its schema and exercise IDs are compatible.

Guest progress belongs to the original browser address. Import it into an account locally before copying the database. The new Unraid domain cannot access local-browser storage from `127.0.0.1`.

Keep one active container per database, and use local Unraid appdata storage rather than SMB/NFS for SQLite. Never mount appdata over `/app` or `.runtime`; packages are already inside the image.

## Updates and limits

Before updating, create a backup. Pull the new image and recreate the container with the same appdata mapping and configuration. Migrations run at startup. To roll back after a schema change, stop the container and restore the database backup that matches the old image tag.

Browser Python uses a dedicated worker with a policy restricting network access to the bundled `/python/` path. Nested workers are blocked. Session cookies are HttpOnly, and workers have no DOM or localStorage access. It is not a separate-origin sandbox: do not add sensitive IndexedDB/OPFS data under this origin without reviewing worker access. Flask previews use an opaque sandboxed iframe with learner scripts and network requests disabled. Practice completions are browser-reported, not independently verified exam results.

The development PC has no Docker engine. The local build and application tests can be checked here; the actual Linux image build, container persistence smoke test and installation run in GitHub Actions or on Unraid. A workflow file alone does not mean an image has been published.
