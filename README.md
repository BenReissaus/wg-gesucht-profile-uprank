# WG-Gesucht Profile Upranking

WG-Gesucht allows users to publish a profile about themselves in case they are looking for a shared apartment. Other people offering a room can then search through the ever growing list of profiles to find a cool roomie. This application upranks the profile to the beginning of the list by simply updating the title once an hour.

### How to run

- Create wg-gesucht profile and get your application id.
- Create `env-file` from `env-file.template` and adapt user values accordingly.
- Create `cron-job` from `cron-job.template` and adapt cron job interval accordingly.
- Execute `make run` which builds the docker image and runs the docker container.
- Check docker logs with `docker logs -f wg-gesucht`.

### Debug with display window on host system

The following steps allow you to follow on what the driver is actually executing in the browser window in case something goes wrong.

- Execute on host in virtual environment: `pip install -r requirements.txt`.
- Set `debug_wg_gesucht="true"` in `env-file`.
- Execute `source env-file`.
- Execute `python upranking.py`.

Note: This application will most likely break when the wg-gesucht website is updated.
