# WG-Gesucht Profile Upranking

WG-Gesucht allows users to publish a profile about themselves in case they are looking for a shared apartment. Other people offering a room can then search through the ever growing list of profiles to find a cool roomie. This application upranks the profile to the beginning of the list by simply updating the title once an hour.

### Setup

- Create wg-gesucht profile.
- Create `env-file` from `env-file.template` and adapt user values accordingly.
- Execute `make run` which builds the docker image and runs the docker container.

### Debug with Display Window

The following steps allow you to follow on what the driver is actually executing in the browser window in case something goes wrong.

- Install python libraries locally.
- Set `debug_wg_gesucht="true"` in `env-file`.
- Execute `source env-file`.
- Execute `python upranking.py`.

Note: This script will most likely break when the wg-gesucht website is updated.
