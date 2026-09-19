# AutoRemovePlus

This repository includes a tested **AutoRemovePlus 2.0.0 build for Python 3.12**.

The existing `.egg` was incompatible with the newer Deluge environment used during testing. That compatibility issue was fixed, and the resulting build was tested successfully.

## Credit and license

AutoRemovePlus is third-party software. **MrRobot-88 does not claim authorship of AutoRemovePlus.** The contribution here is the compatibility fix/build and testing it with the newer Deluge environment.

Original plugin metadata:

- **Author:** Ervin Toth
- **Homepage:** http://github.com/tote94
- **License:** GPLv3

The tested `.egg` and its corresponding source are included under `autoremoveplus/`.

## Tested setup

Our setup used a seed-time rule of **264 hours (11 days)** and removed the downloaded data after the rule was satisfied.

That is an example, not a universal setting. Check the seeding rules of your own tracker before enabling automatic removal.

AutoRemovePlus handles completed torrents. The Smart Cleanup script handles long-inactive **incomplete** torrents, so either can also be used without the other.
