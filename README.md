# test-wc

Dummy workerclient repo used to exercise the CEF client's injected JavaScript
and the automation that keeps it in sync with the puppet-master repo.

## Overview

The scripts under `cef_client/cajs/` are the JavaScript snippets injected into
pages loaded by the CEF client. Each one is a self-executing function that runs
in the page context: `cajs.js` decides whether injection should happen at all,
and `patch_js_objects.js` wraps browser APIs so suspicious usage is reported
back through the `cajsNoodle` runtime.

Changes to these files are mirrored automatically. When a pull request touches a
file in `cef_client/cajs/`, the `Sync Files to Puppet-Master` workflow copies it
into `dmitriy-confiant/test-pm` under `cef/cajs/` and opens (or updates) a
matching `[AUTO-SYNC]` pull request there.

## Structure

```
.github/workflows/sync.yml    CI workflow that syncs changed cajs files to test-pm
cef_client/cajs/
  cajs.js
  patch_js_objects.js
```

| File | Purpose |
| --- | --- |
| `cef_client/cajs/cajs.js` | Aborts injection by throwing when the current `document.URL` starts with `chrome-devtools://`, so the scripts never run inside DevTools. |
| `cef_client/cajs/patch_js_objects.js` | Patches `window.setTimeout` to inspect each callback and report `ENCODED_STRINGS` (hex/unicode escapes) and `LONG_TIMEOUT` (roughly 90s–599s) signals to `cajsNoodle` before returning the original result. |
