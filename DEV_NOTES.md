# Developer notes — Noe Buddy Beacon

## Development summary

**Current goal:** Preserve complete previously saved latest message/packet files if serialization or file replacement fails. Target: unreleased atomic-per-file integrity repair. Intended platform: Pythonista 3/iOS (not device-validated); CI targets CPython 3.11/3.12.

**Integration:** Baseline main `3d501ba` includes merged PRs #1–5 (finite sensor values, cached-fix checks, privacy controls, neutral replies and collision-safe archived history). The latest-file change is [PR #6](https://github.com/levelinglucy/Free-open-source-codes-for-ai-users/pull/6); use the PR's actual state for integration, not a branch note as a claim of merge.

**Validation:** [Test-first branch CI 42529945672](https://github.com/levelinglucy/Free-open-source-codes-for-ai-users/actions/runs/42529945672) reproduced three failures (22 tests total) on each Python 3.11/3.12. [Candidate CI 42530106583](https://github.com/levelinglucy/Free-open-source-codes-for-ai-users/actions/runs/42530106583) passed 22/22 synthetic tests and compilation on each version at `2c5ae7e`. PR #6 owns subsequent exact-revision validation evidence; branch checks alone cannot establish a merged-main result.

**Publication:** No verified GitHub release/tag for these maintenance changes; the historical script's “Public Release Tutorial Build 1.1” label is not publication evidence.

**Latest meaningful change:** Serialize packet before touching any destination; stage each new `latest_*` file in the same folder and replace its filename only after the staged file is closed. Clean staged files on caught failures; preserve the previous complete file if replacement fails. The public Shortcuts message, default privacy switches, timestamped history naming and packet schema are unchanged.

**Next selected steps:** (1) Confirm integration and exact merged-main checks via PR #6; (2) separately evaluate whether stale successful latest JSON should be explicitly marked when a later failure-only message is saved, without deleting historical records; (3) seek real-device/Shortcuts evidence only if it materially changes platform support.

## Acceptance criteria and scope

- When `os.replace` fails, each affected `latest_*` destination retains the exact previous complete file, with failed staging files cleaned up.
- Unsupported packet objects fail *before* the previous latest message or packet is modified. Both synthetic and normal updates stay readable.
- Successful message and JSON saves preserve their existing filenames, JSON formatting, Shortcuts output and archive naming; local-saving privacy switches work as before.
- Candidate and merged-main compilation and all 22 synthetic tests pass on CPython 3.11 and 3.12.

**Limitations:** Latest message and packet are *two separate replaces*, not a transaction. A failure after publishing the message may leave a previous packet, and a failed check-in with `packet=None` intentionally does not erase a prior successful JSON packet; consumers must not mistake it for a same-check-in record. Crashes may leave a staging file and no directory `fsync` is performed; no power-loss, concurrent-writer, guaranteed disk durability or device-portability claim is justified. Archived pairs remain susceptible to partial writes on interruption. Pythonista runtime, iOS Shortcuts and actual SMS delivery have not been tested.

## Design decision — stage latest files before replacement

**Verified predecessor:** `save_outputs()` used `open("w")` on both latest outputs, immediately truncating the existing complete report. Failure-injection CI confirmed that an unsupported JSON packet could leave the message replaced and JSON truncated; tests also exercised both replacement failure points, unavailable to the predecessor because it never used atomic rename.

**Alternatives:** Keep direct truncating writes (simple but loses prior data on errors), introduce a transactional bundle/manifest (safer cross-file semantics but breaks compatibility), or stage each file beside its target and `os.replace` after successful serialization and close (**chosen**). It is a bounded, compatible correctness improvement without changing on-disk filenames.

**Trade-off:** A temporary file consumes extra short-lived space. Individual-file publication is atomic on supported local filesystem semantics, but two files can represent different runs if the second replace fails, and the previous JSON persists after a failure-only message. We avoid automatic deletion of older personal reports. `os.replace` availability and filesystem behaviour on Pythonista/iOS remain unverified. Stage-only residues after a process crash are not automatically purged. Revisit a transactional latest-pair format if real consumers need an inseparable pair and a migration path exists.

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
