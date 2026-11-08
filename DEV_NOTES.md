# Developer notes — Noe Buddy Beacon

## Development summary

**Current goal:** Prevent repeated beacon check-ins within the same second from overwriting earlier timestamped local reports. Target: small unreleased history-integrity correction. Intended platform: Pythonista 3/iOS (unverified); automated validation targets CPython 3.11/3.12.

**Integration:** Earlier sensor, privacy and message repairs [PRs #1–4](https://github.com/levelinglucy/Free-open-source-codes-for-ai-users/pulls?q=is%3Apr+is%3Amerged) are merged. Baseline main for this change: `4c58d558`. Collision-safe archive writing is proposed on `noe/portfolio-beacon-history-collisions`, not yet integrated as of this branch's documentation. Existing latest-file, message, recipient, location and permission logic is unchanged.

**Validation:** A test-first [CI run 42524965803](https://github.com/levelinglucy/Free-open-source-codes-for-ai-users/actions/runs/42524965803) reproduced both failures on each of Python 3.11/3.12: two saves in one second collapsed into one archived report; an earlier archive pair was overwritten. Exact candidate validation belongs in this branch's PR; the two preceding runs alone do not validate the repair.

**Publication:** No observed GitHub release/tag for these maintenance changes; the source's historical “Public Release Tutorial Build 1.1” label does not prove a published release.

**Latest meaningful change:** New history entries use the original second-resolution names when available, appending an integer suffix only on collision. Exclusive creation prevents replacement of pre-existing archive entries, and paired text/JSON files share the chosen stem. An interrupted write can still leave a partial new entry, and the existing `latest_*` files are still overwritten in place; this patch is **not** a crash-safe or power-loss guarantee.

**Next selected steps:** (1) Validate exact candidate and inspect both Python-version logs; (2) merge only when current and permitted by required checks; (3) later assess latest-file crash safety or real-device behaviour if independent evidence warrants it.

## Acceptance criteria and scope

- Two writes in the same wall-clock second must each retain their own archived text, and (when available) JSON, using one matching stem per run.
- A pre-existing archived text/JSON pair must never be truncated or replaced by a new report. Keep the existing archive naming style for the first run and use suffixes only when needed.
- Preserve `SAVE_LOCAL_FILES = False` (no file creation), `SAVE_TIMESTAMPED_HISTORY = False` (latest only), and Shortcuts print/clipboard behaviour.
- Keep prior freshness, finite-reading and neutral-message safety tests passing, with 18/18 synthetic checks on each CPython 3.11/3.12 candidate. Do not change the location packet schema or recipient handling.

The source targets Pythonista 3 / iOS as a **design intention**. Actual location timestamp semantics in a running device, permission prompts, background Shortcuts execution, recipient delivery, clock changes, rescue-radius accuracy, and message confidentiality remain unverified. A fresh timestamp does not guarantee physical accuracy; it only excludes obviously stale provider samples.

## Design decision — cached location time

**Verified predecessor behaviour:** `collect_locations()` previously checked latitude, longitude and horizontal accuracy but did not inspect the sensor's `timestamp`. It stamped the time of polling in `_captured_unix_time` and later used the packet creation time in its message. This can make an old cached iOS position appear current. Pythonista's [documented `get_location()` contract](https://omz-software.com/pythonista/docs-3.4/py3/ios/location.html) says it returns the last-obtained position, including a `timestamp`, not necessarily a new update.

**Alternatives:** Trust returned coordinates and warn only, use an unbounded wait for a new location, or bound source-age at each poll. Selected: reject missing/invalid and over-30-second-old fixes, tolerate up to 5 seconds of future clock skew, and continue the existing bounded polling for new samples. If none qualifies, fail closed with a recoverable error message. These thresholds are conservative policy choices, not a validated rescue specification; change them only after meaningful iOS evidence.

**Trade-offs:** Users may receive a failure message indoors or when iOS supplies no new fix, rather than a potentially useful last-known position. The failure message never represents stale data as current; a future separate last-known-position mode would need conspicuous source-time labeling and explicit user choice. No packet schema or existing on-disk files are migrated.

## Design decision — finite-reading boundary

**Problem:** Python's `float()` accepts strings and numeric values representing `NaN` or infinities. The earlier `safe_float` treated these as valid, while `valid_location` used comparisons that don't reject `NaN`. A non-finite horizontal accuracy could therefore pass validation and spoil weighted position calculations or reported uncertainty.

**Options:** Reject malformed values individually at every call site, or reject them once at the shared normalization helper. We chose the shared helper using `math.isfinite()`, with `safe_round` reusing it. This is a small, local and testable change, but it does not prove real sensor freshness or statistical confidence.

**Diagnostic correction:** Previously every uncaught `main()` exception generated text saying the phone could not obtain a valid location. The replacement explicitly allows a processing failure. A more detailed stage-coded diagnostic can be reconsidered if actual device logs show it would aid troubleshooting without leaking sensitive internals.

**Privacy and safety:** Timestamped plain-text history and clipboard output remain enabled by default for tutorial compatibility. New opt-outs let the user disable dated history or all local files independently of clipboard output. Detailed tracebacks are opt-in because failures can contain sensitive context. Existing saved records are not deleted; no privacy certification is implied.

## Design decision — privacy controls and error paths

**Confirmed predecessor:** normal output respected `SAVE_LOCAL_FILES = False`, but the `main()` exception handler unconditionally called `ensure_save_folder()` and wrote `latest_error_traceback.txt`. This violates the user's selected no-local-save setting. Normal output also wrote unlimited timestamped reports without offering a latest-only mode; tracebacks contained detailed exception context by default.

**Options:** disable all saving by default (would break existing tutorial workflows), silently delete older files (would risk data loss), or provide explicit independent controls. **Decision:** keep legacy success-path defaults, make the master local-file switch authoritative even on errors, add a latest-only option while retaining history by default, and require opt-in for traceback files. The Shortcuts print and clipboard paths are unchanged. Previously saved files are preserved, not cleansed. Manual removal remains the user's choice.

**Acceptance:** synthetic tests must establish no folder on failures when saving is off; the latest-only mode must save only latest files; legacy history remains possible; tracebacks require both explicit opt-in and local saving. No real-device validation or automatic encryption/retention claim is made.

## Design decision — preserve history during timestamp collisions

**Verified predecessor:** `save_outputs()` opened `buddy_beacon_YYYYMMDD_HHMMSS.txt` (and matching JSON) using write/truncate mode. Two calls within one second reused exactly the same paths, destroying the earlier report; both failures were reproduced with synthetic local fixtures, not real device data.

**Options:** append to one file (breaks per-run layout), switch to microsecond timestamps (makes collisions less likely, not impossible), or retain the naming contract and use exclusive creation with bounded suffix retries (**chosen**). The selected design preserves earlier archives without renaming or removing them and keeps paired files on a common stem. An existing JSON sibling prevents reuse of an orphaned stem.

**Trade-offs:** Up to 1,000 name candidates are attempted per timestamp second. Individual new files can still be partial after an interrupted write; latest files still use non-atomic overwrite, and pairs are not transactionally committed. Ordinary file I/O errors remain non-fatal to sending the Shortcuts output, so a missing archive is possible. This is archive collision prevention, **not** durable or atomic saving. Consider staged atomic latest-file replacement separately if device/filesystem evidence justifies it.

## Test commands

```sh
python -m py_compile Noe_Buddy_Beacon.py
python -m unittest discover -s tests -v
```

The workflow runs these commands on CPython 3.11 and 3.12. It imports the source without invoking `main()` and uses disposable numeric fixtures.

## History and roadmap

The original script is a public tutorial build; the earlier authorial intent and practical device success cannot be reconstructed from the available repository alone. Historical files are preserved. The maintenance roadmap is to retain a trustworthy core message, improve deliberate data minimization in a separately scoped change, and establish honest platform-compatibility evidence when available. Avoid broad refactors or release claims without additional evidence.
