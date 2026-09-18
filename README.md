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
LICENSE
README.md
```

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
