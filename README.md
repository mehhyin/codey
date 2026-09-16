# Codey

A local Python learning platform with 173 exercises, guided projects, Google/GitHub sign-in through Better Auth, and account progress stored in SQLite. The existing interface and blank editors are preserved.

For a container deployment, see **[Unraid setup](deploy/unraid/README.md)** and **[Unraid XML template](deploy/unraid/codey.xml)**. GitHub Actions builds and publishes release images to GHCR; the container uses persistent appdata and one HTTPS domain through Cloudflare Tunnel. The instructions below describe the original local Windows setup.

## Open it later

Double-click **Start Codey.cmd**, then use **http://127.0.0.1:8765** in your browser. Bookmark that exact address. Double-click **Stop Codey.cmd** when finished; closing the browser alone leaves the server running.

This computer is set up for guest practice. Add OAuth credentials below to enable account sign-in. No Docker, Go, Next.js, paid API or deployment is required.

## First-time setup on another computer

Install Node.js **24.15 or newer** and Python **3.12 or newer**. Python is only used to export the authored curriculum at build time; learner code runs in the browser. Open a terminal in this folder:

```sh
npm ci
npm run setup
npm run runtime:setup
npm run build
npm start
```

`setup` creates `.env` with a random authentication secret without overwriting an existing file. `runtime:setup` downloads Python and its learning libraries into `.runtime/pyodide`, verifying package checksums. Installation requires internet access. Lessons run locally afterwards; signing in with Google/GitHub requires internet access. The first Run after opening a lesson may take a few seconds to load the Python libraries.

If the curriculum export cannot find Python, set `CODEY_PYTHON` to the full Python executable path in your environment. On this computer, the existing bundled Python is detected automatically. `npm.cmd` can be used on Windows if PowerShell blocks `npm.ps1`.

After changing curriculum or interface source, run `npm run build`, restart Codey and refresh the page. Do not start the legacy `server.py` alongside the new server.

## Google and GitHub sign-in

Edit **.env locally**. Never put credentials into chat or commit the file. Configure either provider or both; leave an unused provider's two values empty. Restart Codey after editing.

### Google

1. In Google Cloud Console, create/select a project and configure its Google Auth Platform branding, audience and contact details. While the app is in testing, add your Google account as a test user.
2. Create an OAuth client with application type **Web application**.
3. Add the authorized JavaScript origin `http://127.0.0.1:8765` and authorized redirect URI `http://127.0.0.1:8765/api/auth/callback/google`.
4. Set `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` in `.env`.

Reference: [Better Auth Google setup](https://www.better-auth.com/docs/authentication/google).

### GitHub

1. In GitHub Settings → Developer settings → OAuth Apps, register an OAuth application.
2. Set Homepage URL to `http://127.0.0.1:8765` and Authorization callback URL to `http://127.0.0.1:8765/api/auth/callback/github`.
3. Generate its client secret and set `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` in `.env`.

Reference: [Better Auth GitHub setup](https://www.better-auth.com/docs/authentication/github).

Keep `BETTER_AUTH_URL` and every registered callback identical, including hostname and port. If your provider requires `localhost`, set `BETTER_AUTH_URL=http://localhost:8765` and use that hostname consistently in the provider settings and browser. Guest browser storage belongs to the original address; import it there before switching addresses. Keep `BETTER_AUTH_SECRET` stable across restarts.

After restart, the configured sign-in button becomes active. The provider authenticates you; Codey stores its user, account and session records in SQLite. Password registration is disabled in the normal app. Account linking is disabled: use the same provider to return to the same account. Live Google/GitHub authorization cannot be verified until real credentials are configured.

## Where your progress lives

When signed in, **data/codey.sqlite** stores:

- Better Auth users, provider accounts and sessions.
- Every exercise's main and companion-file drafts, with revision checks.
- Completion, revealed hints, solution reveals and the last exercise opened.
- Submitted code snapshots, check results and submission history.

All account routes derive the user ID from the session. Another account cannot read your drafts or attempts. Drafts autosave after a short pause; wait for **Saved to your account** before closing. A temporary browser recovery copy holds pending drafts, hints and submissions if a save fails. Network failures retry; conflicting edits from another tab require choosing which draft to keep. Recovery data is scoped to the signed-in account. Use a separate browser profile on a shared computer: browser recovery storage is not encrypted against someone using that same profile.

Guests continue using `codey.workspace.v1` in browser local storage. Guest work survives the upgrade at the same browser/address. Codey falls back to the old `pyroom.workspace.v1` key on first use and writes to `codey.workspace.v1`; old recovery data remains readable too. The old key is retained as a fallback. After signing in, choose **Import browser progress** to import it once. Existing account drafts take priority; hints and completions merge. The original guest copy is retained. Account imports are labelled as imported practice results internally.

Different browsers and private windows have separate guest storage. SQLite account progress remains available after signing into the same account from another browser on this computer.

### Backup and restore

Run `npm run backup` to make a consistent SQLite snapshot in **backups/**, including changes in the WAL. It works while Codey is running. Protect backups because they include account data and sessions. Back up `.env` separately in a secure location.

To restore, stop Codey, preserve the existing database together with any `-wal`/`-shm` companions in another folder, then copy the chosen backup to the configured `DATABASE_PATH`. Start Codey again. Do not replace a database while its server is running.

## Learn

Pick any lesson; all modules are available immediately. Each exercise and companion file starts blank. Required inputs and debugging examples appear in the instructions. Variables, functions and filenames in questions are rendered as inline code.

- **Run code** executes your Python; **Submit answer** checks it and records a practice submission when signed in.
- **Ctrl+Enter** runs; **Ctrl+Shift+Enter** submits. Tab inserts four spaces, and Enter preserves indentation.
- Reveal hints one at a time. Worked solutions require a separate confirmation and do not automatically complete an exercise.
- **History** shows your latest 30 submissions for the current exercise, including their code.
- Charts and declared exports appear under **Output files** and can be downloaded. Attempt files live in browser memory and reset for every run.

| Track | Modules | Exercises | Topics |
| --- | ---: | ---: | --- |
| Foundations | 9 | 118 | Python essentials, control flow, collections, functions, files, analysis, pandas, automation and web concepts |
| Intermediate | 10 | 55 | Mixed review, NumPy, Matplotlib, deeper pandas, Excel, SQLite, APIs, reliable programs, Flask and independent projects |

There is no advanced track yet. The curriculum is original, with progression informed by public [DataCamp](https://www.datacamp.com/courses/intro-to-python-for-data-science) and [Dataquest](https://www.dataquest.io/path/data-analyst/) curriculum outlines.

## Browser Python and web projects

Pyodide runs Python 3.14 in a fresh Web Worker served under `/python/` on the same origin. NumPy, pandas, Matplotlib, openpyxl, SQLite and Flask are available. No learner Python runs on the host or in the Node server. Host files and the account database are not mounted into Python. A content-security policy restricts worker requests to the static `/python/` path and blocks nested workers. That path has no account API, filesystem proxy, uploads or redirects. Workers cannot access the DOM or localStorage; account session cookies are HttpOnly. This is browser-based isolation, not a separate-origin security boundary. Session cookies are HttpOnly; the main app also checks origin and request headers for writes.

The local Node process listens on **8765**. Containers configure `HOST=0.0.0.0` and `PORT=8765`; `BETTER_AUTH_URL` sets the public browser address. The app, API and bundled Python files use this one port. Remote deployments require HTTPS. The Unraid template is configured for **https://codey.john.shiksha**.

Exercises have 8-second or 20-second execution limits after runtime initialization; infinite loops terminate the worker. Output is capped at 24,000 characters. Exports are limited to 2 MB per file and 6 MB total. Very large allocations can still exhaust a browser tab's memory. `input()` is not an interactive prompt here.

API exercises use an offline `urllib` adapter with practice responses, pagination, HTTP errors and retries. They teach the request/response workflow without outbound network access.

**Preview app** runs Flask through its test client. HTML forms and local links work inside the Output files panel. Learner JavaScript, external links and network requests are disabled. Define `app`; do not call `app.run()`. Preview databases survive form submissions within that preview and reset on another run, exercise change or page reload. This teaches Flask routing, validation, templates and SQL; it does not start a listening web server.

Checks run in the learner's browser, so stored completions are **personal practice results**, not independently verified exam scores. Users can inspect or modify browser-side checks. This is the deliberate tradeoff for a Docker-free local platform.

## Architecture and development

One Node.js process runs Hono, Better Auth, SQLite, the built Vite interface and the static Python assets. Better Auth's TypeScript integration is the reason this build uses Node instead of a single Go binary.

- `web/`: interface source and account/runtime clients.
- `server/`: Hono routes, authentication, migrations, account persistence and backup utility.
- `runner/`: browser Python execution, offline API fixture and Flask preview transport.
- `course*.py`, `intermediate*.py`: original curriculum, checks and worked solutions.
- `scripts/`: environment setup, curriculum export and runtime downloads.
- `build/`, `.generated/`, `.runtime/`: generated, ignored files.
- `server.py`, `worker.py`, `project_preview.py`, `dist/`: retained legacy implementation for reference; not served by the new launcher.

Better Auth migrations and versioned application migrations run automatically at startup. SQLite uses foreign keys, WAL and a busy timeout. Back up before future schema upgrades. `.env`, databases, backups, runtime packages and dependencies are excluded from Git.

```sh
npm run build
npm run typecheck
npm test
npm run test:runner
```

The account integration tests create real Better Auth sessions in disposable databases. Password sign-up is enabled only inside the test factory, never by the normal server entry point. Runtime tests execute all 173 reference solutions using the installed WebAssembly Python, including the Flask form workflow.

## Troubleshooting

- Cannot connect: run Start Codey.cmd, then refresh the exact configured address.
- Sign-in buttons disabled: configure that provider's two `.env` values and restart.
- OAuth redirect mismatch: check the exact hostname, port and callback path above.
- Python cannot load: run `npm run runtime:setup`; check that `/python/pyodide/runtime.json` is reachable through the same hostname.
- Endless program: the worker will stop at its time limit. Correct the loop and run again.
- Save conflict: use the banner to keep your local draft or use the account draft.
- Save failure: keep the tab open. Pending work retries when the connection returns.
- Startup error: see `.runtime/server-error.log` and `.runtime/server.log`.
