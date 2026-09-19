# AutoRemovePlus notes

The Deluge setup used while developing this project ran **AutoRemovePlus 2.0.0** built for **Python 3.12**. The existing AutoRemovePlus `.egg` was broken/incompatible with the newer Deluge environment used during testing; that compatibility issue was fixed and the resulting build was verified to load and work with that Deluge version.

AutoRemovePlus is third-party software. **MrRobot-88 does not claim authorship of AutoRemovePlus; the contribution here is the compatibility fix/build for the newer Deluge environment and testing that it works.** Metadata in the tested plugin identifies:

- Name: AutoRemovePlus
- Version: 2.0.0
- Author: Ervin Toth
- Homepage: http://github.com/tote94
- License: GPLv3

The tested configuration used a seed-time rule of **264 hours (11 days)** for the download labels used by Sonarr and Radarr, with removal of downloaded data enabled after the rule was satisfied.

That is an example, **not a universal recommendation**. Private trackers have different seeding requirements.

## Why the binary .egg is not committed here yet

The locally tested Python 3.12 build was inspected before publication. Because it is a modified/rebuilt third-party GPLv3 package, this repository does not publish that binary until its corresponding source, modification history, license text and reproducible build instructions are packaged together correctly.

This avoids distributing an opaque binary without the source/attribution material expected for a GPL release.

The Smart Cleanup script does not require AutoRemovePlus.
