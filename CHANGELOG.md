# Changelog

## Unreleased — safety checks for the public beacon

- Reject `NaN` and infinite sensor values before they reach location validation, weighted coordinates or numeric presentation, preventing misleading non-finite check-in results.
- Replace the failure reply's unconditional “no valid location fix” claim with wording that also covers processing errors; successful messages and the existing storage format remain unchanged.
- Add five device-free, synthetic regression tests and Python 3.11/3.12 GitHub Actions validation, plus setup, privacy and limitations guidance in README and developer notes.

This remains an untagged maintenance candidate; see [PR #1](https://github.com/levelinglucy/Free-open-source-codes-for-ai-users/pull/1) for integration and exact validation evidence. The historical “Tutorial Build 1.1” label is not a verified release tag.
