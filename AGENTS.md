# Repository Guidelines

## Project Structure & Module Organization

This repository is a Home Assistant custom integration. All runtime code lives in `custom_components/daily_islamic_hadith/`. `__init__.py` registers the integration, `config_flow.py` handles setup and options, `sensor.py` fetches and exposes the daily Hadith sensor, and `const.py` contains shared identifiers and values. Keep service definitions in `services.yaml` and Home Assistant metadata in `manifest.json`. `hacs.json` supports HACS distribution; `README.md` is the user-facing installation and usage guide. No test or asset directories are currently committed.

## Build, Test, and Development Commands

There is no project-specific build script or pinned development dependency file. Validate changes in a Home Assistant development environment after copying or symlinking `custom_components/daily_islamic_hadith/` into its `custom_components/` directory. At minimum, check syntax before submitting:

```sh
python3 -m compileall custom_components/daily_islamic_hadith
```

Restart Home Assistant, add the integration through **Settings → Devices & Services**, and exercise the `daily_islamic_hadith.fetch_new_hadith` service. Do not add an unverified command to this guide; document any new test tooling with its configuration.

## Coding Style & Naming Conventions

Use Python with four-space indentation and standard `snake_case` for functions, variables, and module files; classes use `PascalCase`. Follow Home Assistant async conventions: name coroutines `async_*`, await I/O, and obtain HTTP sessions through Home Assistant helpers. Keep integration-wide values in `const.py`, use relative imports within the package, and log through a module-level `_LOGGER`. Preserve the existing service key and domain naming pattern, for example `daily_islamic_hadith.fetch_new_hadith`.

## Testing Guidelines

No automated test framework or coverage threshold is configured yet. For behavior changes, add focused pytest tests under `tests/` when introducing the required Home Assistant test setup. Name files `test_<module>.py` and test functions `test_<behavior>`. Manually verify both Arabic and English configuration flows, scheduled refresh behavior, API-error handling, and sensor attributes.

## Commit & Pull Request Guidelines

Recent commits use short, imperative subjects such as `Add Fetch New Hadith Service` and `Fix Frequent Polling For Daily Hadith Fetching`. Keep each commit scoped to one change. Pull requests should summarize the behavior change, identify any Home Assistant or HACS metadata impact, link related issues when available, and include screenshots or service-output examples for user-visible changes. Confirm the integration can load before requesting review.
