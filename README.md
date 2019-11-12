# WG-Gesucht Profile Upranking

WG-Gesucht allows users to publish a profile about themselves in case they are looking for a shared apartment. Other people offering a room can then search through the ever growing list of profiles to find a cool roomie. This application upranks the profile to the beginning of the list by simply updating the title.

### Setup

- Create wg-gesucht profile
- Create "env-file" from "env-file.template" and adapt user values accordingly
- Adapt `cron-job` file accordingly
- Execute `make run`

### Debug with Display Window

The following steps allow you to follow on what the driver is actually executing in the browser window in case something goes wrong.

- install python libraries locally
- set `debug_wg_gesucht="true"` in env-file
- `source env-file`
- `python upranking.py`

Note: This script will most likely break when the wg-gesucht website is updated.
