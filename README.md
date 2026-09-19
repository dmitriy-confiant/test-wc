# test-wc

Dummy **workerclient** repository, used as a sandbox for cross-repo automation
experiments.

## What this repo is

This is a throwaway stand-in for a worker client: the component that embeds a
CEF (Chromium Embedded Framework) client and runs the shared `cajs` scripts that
are handed to it by the puppet-master side.

Nothing here is production code. The contents exist so that automation — sync
workflows, agents, CI experiments — has a realistic shape to act on.

## Layout

```
cef_client/
  cajs/
    cajs.js               shared CEF-side script
    patch_js_objects.js   shared JS object patching helpers
server.py                 minimal stdlib HTTP server
LICENSE
README.md
```

## Running the server

Start the server with:

```
python3 server.py
```

Endpoints:

- `GET /ping` — health check for this service.
- `GET /call-pm` — proxies the puppet-master's `GET /api/ping` and returns its JSON.

## HTTP server

`server.py` is a small HTTP server built on the Python standard library — no
external dependencies. Run it with:

```
python3 server.py
```

It listens on `127.0.0.1:8000` by default. Endpoints:

| Endpoint | Response |
| --- | --- |
| `GET /ping` | `{"service": "test-wc", "status": "ok"}` |
| `GET /call-pm` | the JSON returned by the puppet-master's `GET /api/ping` |

`/call-pm` calls `test-pm` at `http://localhost:3000` by default — the port its
Next.js app is expected to use. `test-pm` does not serve `/api/ping` yet — adding
it is the sibling ticket CC-13, which has no merged pull request — so `/call-pm`
currently returns a 502 error body.

Configuration is read from the environment:

| Variable | Default | Meaning |
| --- | --- | --- |
| `HOST` | `127.0.0.1` | interface this server binds to |
| `PORT` | `8000` | port this server listens on |
| `PM_BASE_URL` | `http://localhost:3000` | puppet-master base URL (`http`/`https` only) |
| `PM_TIMEOUT` | `5` | seconds to wait for the puppet-master |

## Related repositories

| Repo | Role | Link |
| --- | --- | --- |
| `test-pm` | puppet-master | https://github.com/dmitriy-confiant/test-pm |
| `test-wc` | workerclient (this repo) | https://github.com/dmitriy-confiant/test-wc |

The puppet-master repository,
[dmitriy-confiant/test-pm](https://github.com/dmitriy-confiant/test-pm), owns the
canonical copies of the `cajs` scripts under `cef/cajs/`. Changes made there are
propagated into this repository's `cef_client/cajs/` directory by the sync
workflows that live on the puppet-master side.

Practically, that means:

- Edit `cajs.js` / `patch_js_objects.js` in **test-pm**, not here.
- Expect incoming automated pull requests against `cef_client/cajs/` in this
  repo when the puppet-master copies change.

## Working on this repo

There is no build, no dependency manifest, and no test suite. Clone it, edit the
files, open a pull request.
