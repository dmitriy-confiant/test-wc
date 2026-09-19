# AGENTS.md

Guidance for AI agents working in this repository.

## Purpose

`test-wc` is a dummy **workerclient** repository — a sandbox for cross-repo
automation experiments. It is the counterpart to the **puppet-master** repo,
[dmitriy-confiant/test-pm](https://github.com/dmitriy-confiant/test-pm), which
holds the canonical `cajs` scripts this repo mirrors.

Nothing here is production code. The files exist to give automation — sync
workflows, agents, CI experiments — a realistic shape to act on.

## Structure

```
cef_client/cajs/    mirrored CEF-side scripts (cajs.js, patch_js_objects.js)
server.py           minimal stdlib HTTP server
```

`README.md` carries the full file tree under **Layout**, the server's endpoints
and configuration under **HTTP server**, and the state of the tooling under
**Working on this repo**. Read them there — they are not duplicated here.

## Working conventions

- **Read `README.md` first.** It is the source of truth for repo layout, for the
  server's behaviour, and for the current state of the sync pipeline. Point at
  it rather than restating its details here or in new files, so the two cannot
  drift apart.
- **Edit `cajs` scripts in `test-pm`, not here.** `cef_client/cajs/` holds
  mirrored copies; the canonical ones live in the puppet-master repo. Expect
  incoming automated pull requests against this directory.
- **Do not assume mirroring happened.** Sync is driven from the `test-pm` side
  and is not reliably working end to end. Check `test-pm` before treating a
  `cajs` file here as current.
- **The `cajs` scripts are injected into a CEF page, not run under Node.** They
  are IIFEs that lean on browser globals (`window`, `document`) and the
  host-provided `cajsNoodle` object. There are no imports and no module system —
  keep it that way.
- **`server.py` is standard-library only.** It has no dependency manifest and
  should not grow one.
- **Verify before you describe.** Confirm what the code actually does before
  writing anything that asserts behaviour.
- **Verification:** there is no build and no test suite. "Verify" means
  re-reading the diff and confirming edited files still parse —
  `python3 -m py_compile server.py` and `node --check` on a `cajs` file are
  available. Say plainly what you ran rather than implying a test run happened.
- **Cross-repo changes:** if a change needs matching edits in `test-pm`, open a
  separate PR there and cross-link the two.
- **Branch and PR.** Never commit to `main` directly; open a pull request.

## Related repositories

See the **Related repositories** section of `README.md`.
