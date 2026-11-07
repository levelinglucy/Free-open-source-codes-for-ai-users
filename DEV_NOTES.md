# Developer notes — Noe Buddy Beacon

## Development summary

**Current goal:** Make beacon local-storage opt-outs truthful without breaking the default check-in and Shortcuts interface. On the previous source, `SAVE_LOCAL_FILES = False` still created an exception traceback file, while plaintext/JSON history accumulated without a latest-only option. Target: next unreleased privacy-maintenance patch. Support target remains Pythonista 3 / iOS (unverified) and tested CPython 3.11/3.12.

**Integration:** Sensor repairs [PR #1](https://github.com/levelinglucy/Free-open-source-codes-for-ai-users/pull/1) and [PR #2](https://github.com/levelinglucy/Free-open-source-codes-for-ai-users/pull/2) are merged; current baseline main `53bce316`. Privacy controls are being developed on `noe/portfolio-beacon-private-logs`; proposed until explicitly merged. Existing user data is not migrated or deleted.

**Validation:** Five new synthetic privacy tests include failure-path no-write, latest-only history, opt-in diagnostics and legacy history compatibility; the original source failed 3/14 checks per Python 3.11/3.12 at [test-first CI 42405585205](https://github.com/levelinglucy/Free-open-source-codes-for-ai-users/actions/runs/42405585205). Exact repaired-source validation and integration state belong in the new PR, not inferred here. Earlier stale-fix and numeric tests remain in the same suite. No iPhone, real location, clipboard or Shortcuts integration tests are claimed.

**Publication:** No verified GitHub release/tag for this maintenance correction. The original file's “Public Release Tutorial Build 1.1” header is historical, not proof of publication.

**Meaningful proposed change:** `SAVE_LOCAL_FILES` governs all writes, even traceback capture. `SAVE_TIMESTAMPED_HISTORY` defaults to True for existing tutorial behaviour but may be set False to retain only latest reports. New `SAVE_ERROR_TRACEBACK` defaults to False, with explicit opt-in while local saving is enabled. Clipboard and Shortcuts output are unaffected, and existing files are never removed. Earlier sensor freshness and numeric repairs stay intact.

**Next selected steps:** (1) Validate the exact proposed privacy change on CPython 3.11/3.12 and review its diff. (2) Merge a low-risk PR only if checks, branch status and protections allow. (3) Revisit real Pythonista behaviour only with suitable evidence; do not ask Dylan to operate routine tests.

## Acceptance criteria and scope

- A cached location older than 30 seconds, a missing/non-finite timestamp, or a timestamp more than 5 seconds in the future must not produce a normal check-in.
- A fresh reading (including small positive clock skew) remains eligible; old and new samples are not combined.
- Real `timestamp` values supplied by iOS remain in the raw sample; collection time must not masquerade as a location-fix time.
- Retain the former finite-coordinate/accuracy and truthful-error-message tests.
- Complete device-free tests on CPython 3.11/3.12. Do not change the packet structure, local-file layout or recipient/Shortcuts behaviour as part of this fix.

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

## Test commands

```sh
python -m py_compile Noe_Buddy_Beacon.py
python -m unittest discover -s tests -v
```

The workflow runs these commands on CPython 3.11 and 3.12. It imports the source without invoking `main()` and uses disposable numeric fixtures.

## History and roadmap

The original script is a public tutorial build; the earlier authorial intent and practical device success cannot be reconstructed from the available repository alone. Historical files are preserved. The maintenance roadmap is to retain a trustworthy core message, improve deliberate data minimization in a separately scoped change, and establish honest platform-compatibility evidence when available. Avoid broad refactors or release claims without additional evidence.
