# Developer notes — Noe Buddy Beacon

## Development summary

**Current goal:** Refuse stale cached iOS fixes before generating an ostensibly current emergency check-in. Pythonista documents `get_location()` as the **most recently obtained** position, including its own `timestamp`; this is not necessarily a newly acquired fix. The deliverable is a conservative sensor-time check at ingestion, preserving the existing packet and Shortcuts interface. Target: next unreleased maintenance patch.

**Integration:** Earlier finite-reading/diagnostic repair [PR #1](https://github.com/levelinglucy/Free-open-source-codes-for-ai-users/pull/1) was merged at `0c9a18f`. The freshness correction is being developed on `noe/portfolio-beacon-fresh-fix`; treat it as **proposed only** until the new PR's GitHub merge status is observed.

**Validation:** Four new device-free location-polling regression methods were added. The original implementation failed the new test suite on Python 3.11/3.12, [test-first CI run 42391217213](https://github.com/levelinglucy/Free-open-source-codes-for-ai-users/actions/runs/42391217213). The final implementation candidate and its exact CI result are authoritative in the new PR; no device or Shortcuts integration test is claimed. Prior `safe_float` milestone had five passing synthetic checks at its [merged-main CI](https://github.com/levelinglucy/Free-open-source-codes-for-ai-users/actions/runs/42381807855).

**Publication:** No verified GitHub release/tag for this maintenance correction. The original file's “Public Release Tutorial Build 1.1” header is historical, not proof of publication.

**Meaningful changes:** `fresh_location` compares the timestamp actually provided by iOS against sampling time; absent, non-finite, over-30-second-old or over-5-second-future fixes are not accepted. Existing numeric and position checks still apply. Refusal produces a failure reply instead of presenting an old position with a new collection timestamp. Original raw fix timestamp and on-device file layout stay intact.

**Next selected steps:** (1) Observe CI on the final changed revision, then merge only if all required checks and protections allow it. (2) Consider separate privacy-minimizing log-history controls after explicit compatibility examination. (3) Seek trusted iPhone/Shortcuts confirmation only when independently available; do not rely on Dylan for routine tests.

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

**Privacy and safety:** The existing defaults retain timestamped plain-text location logs and clipboard output for tutorial compatibility; these are potentially sensitive. Documented clearly in the README and at the source settings. Do not silently alter existing on-device data or claim privacy certification.

## Test commands

```sh
python -m py_compile Noe_Buddy_Beacon.py
python -m unittest discover -s tests -v
```

The workflow runs these commands on CPython 3.11 and 3.12. It imports the source without invoking `main()` and uses disposable numeric fixtures.

## History and roadmap

The original script is a public tutorial build; the earlier authorial intent and practical device success cannot be reconstructed from the available repository alone. Historical files are preserved. The maintenance roadmap is to retain a trustworthy core message, improve deliberate data minimization in a separately scoped change, and establish honest platform-compatibility evidence when available. Avoid broad refactors or release claims without additional evidence.
