# Deluge Smart Cleanup

A small, safety-first cleanup tool for **Deluge**. It handles torrents that get stuck before finishing and can be used alongside **AutoRemovePlus** for completed torrents.

Works with a normal Deluge setup. **Gluetun, Sonarr, Radarr and Prowlarr are optional.**

Related projects:
- https://github.com/MrRobot-88/Sonarr-Smart-Optimizer
- https://github.com/MrRobot-88/Radarr-Smart-Optimizer

## What does it do?

There are two cleanup jobs:

- **Stuck incomplete torrents:** `deluge-smart-cleanup.py` remembers torrent activity between runs. If an incomplete torrent stays inactive for the configured number of days, it becomes eligible for removal.
- **Completed torrents:** AutoRemovePlus can keep them seeding for a set time and remove them afterward.

Keeping these jobs separate makes the behavior easier to understand and safer to control.

## Safety first

Smart Cleanup starts in **dry-run mode**. It only shows what it *would* remove.

Nothing is removed unless you run it with `--live`.

By default:
- inactivity must last **11 days**
- only torrents below **100%** are considered
- download or upload activity resets the timer
- completed torrents are ignored by Smart Cleanup
- state is saved locally between runs

Always check the dry-run output before enabling live deletion.

## Quick start

Requirements: **Python 3.8+** and a reachable **Deluge Web API**.

Set your Deluge address and password:

```bash
export DELUGE_URL="http://127.0.0.1:8112"
export DELUGE_PASSWORD="your-web-password"
python3 deluge-smart-cleanup.py
```

That is a dry run. If the results look correct:

```bash
python3 deluge-smart-cleanup.py --live
```

### Settings

| Variable | Default | What it does |
| --- | --- | --- |
| `DELUGE_URL` | `http://127.0.0.1:8112` | Deluge Web address |
| `DELUGE_PASSWORD` | required | Deluge Web password |
| `DELUGE_CLEANUP_STATE` | beside script | Where cleanup state is saved |
| `DELUGE_INACTIVE_DAYS` | `11` | Days an incomplete torrent may stay inactive |
| `DELUGE_ACTIVITY_BPS` | `1024` | Transfer rate treated as activity |
| `DELUGE_REMOVE_DATA` | `true` | Delete downloaded data as well in live mode |

Run the script periodically, such as once per day. Keep real passwords and other credentials out of scripts you publish or share.

## AutoRemovePlus

This repository also includes a tested **AutoRemovePlus 2.0.0 Python 3.12** build.

The older `.egg` was incompatible with the newer Deluge environment used during testing. That compatibility problem was fixed and the resulting build was tested successfully.

AutoRemovePlus is **third-party GPLv3 software** and is not authored by this project. See `AUTOREMOVEPLUS.md` for attribution and build notes.

Our tested setup used **11 days (264 hours)** of seed time before completed downloads were removed. This is only an example: use the seeding requirements of your own tracker.

## Gluetun

If Deluge runs through **Gluetun**, keep Deluge in Gluetun's network namespace and expose the ports Deluge needs through Gluetun.

Smart Cleanup does not manage your VPN and does not contain VPN credentials or provider-specific configuration.

A typical setup can look like:

`Prowlarr → Sonarr/Radarr → Deluge → Gluetun`

Only Deluge is required by the cleanup script.

## License

The Smart Cleanup code is **MIT licensed**.

AutoRemovePlus is separate third-party software licensed under **GPLv3**. Its original attribution and license remain separate.
