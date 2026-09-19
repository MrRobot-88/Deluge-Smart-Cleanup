# Deluge Smart Cleanup

Safe, conservative torrent cleanup for **Deluge**, with documentation for **Gluetun** and an optional tested **AutoRemovePlus** workflow.

This project complements:
- https://github.com/MrRobot-88/Sonarr-Smart-Optimizer
- https://github.com/MrRobot-88/Radarr-Smart-Optimizer

## What this project is for

There are two different cleanup jobs:

1. **Completed torrents / seeding retention** — AutoRemovePlus can keep completed torrents for a configured seed time and then remove the torrent and its download data.
2. **Dead or stuck incomplete torrents** — `deluge-smart-cleanup.py` tracks incomplete torrents over time and can remove torrents that remain inactive for a configured number of days.

They are deliberately separate. The smart-cleanup script does **not** replace AutoRemovePlus.

## Setup used during development

The setup this project was developed around was:

`Prowlarr -> Sonarr/Radarr -> Deluge -> Gluetun`

Prowlarr and Gluetun are **not required** by the cleanup script. Sonarr/Radarr can use any supported indexer setup. Gluetun is simply the VPN/network layer used for Deluge in the tested setup.

## Safety

- Smart Cleanup is **DRY RUN by default**.
- Actual removal requires `--live`.
- Default inactivity threshold is **11 days**.
- Only incomplete torrents below 100% are candidates for stuck cleanup.
- A torrent showing download/upload activity resets its inactivity timer.
- State is stored locally so inactivity is measured across runs.
- Completed torrents are left to AutoRemovePlus rather than being deleted by Smart Cleanup.
- Configuration is via environment variables; no API keys, NAS paths or tracker names are built in.

Always run dry mode and inspect the output before enabling live deletion.

## Smart Cleanup

Requirements: Python 3.8+ and Deluge Web API enabled/reachable.

Example:

```bash
export DELUGE_URL="http://127.0.0.1:8112"
export DELUGE_PASSWORD="your-web-password"
python3 deluge-smart-cleanup.py
```

After checking dry-run output:

```bash
python3 deluge-smart-cleanup.py --live
```

Configuration:

| Variable | Default | Meaning |
| --- | --- | --- |
| `DELUGE_URL` | `http://127.0.0.1:8112` | Deluge Web URL |
| `DELUGE_PASSWORD` | required | Deluge Web password |
| `DELUGE_CLEANUP_STATE` | beside script | State JSON location |
| `DELUGE_INACTIVE_DAYS` | `11` | Inactivity before an incomplete torrent qualifies |
| `DELUGE_ACTIVITY_BPS` | `1024` | Download/upload rate considered activity |
| `DELUGE_REMOVE_DATA` | `true` | Also delete download data in live mode |

### Scheduling

Run it periodically, for example once per day. Keep the password in a protected file or environment rather than putting it in a public script.

## AutoRemovePlus

The tested setup uses **AutoRemovePlus 2.0.0 for Python 3.12**. AutoRemovePlus is third-party GPLv3 software; it is not authored by this project.

The tested retention rule was **264 hours = 11 days** of seed time for the Sonarr/Radarr download labels. Your tracker rules may require a different minimum, so configure the value for your own tracker before enabling removal.

AutoRemovePlus can remove both the torrent and its downloaded data after its configured rule is satisfied. Verify its settings carefully.

See `AUTOREMOVEPLUS.md` for attribution and notes about the tested build.

## Deluge + Gluetun

When using Gluetun, route Deluge through Gluetun's network namespace and expose Deluge's required ports through Gluetun. This keeps VPN networking separate from cleanup policy.

This repository intentionally does not contain VPN credentials, provider-specific secrets or a copy/paste compose file pretending to fit every Docker/NAS environment.

## License

The original code in this repository is MIT licensed.

AutoRemovePlus is a separate third-party project licensed under GPLv3. Its license and attribution must be preserved independently.
