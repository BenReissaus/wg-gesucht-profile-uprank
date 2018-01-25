# WG-Gesucht Profile Upranking 

WG-Gesucht allows users to publish a profile about themselves in case they are looking for a shared apartment. Other people offering a room can then search through the ever growing list of profiles to find a cool roomie. The python script in this repository upranks the profile to the beginning of the list by simply updating the title. 

### Setup

- Create WG-Gesucht Profile
- Checkout repository
- Install Python requirements
- Download Google ChromeDriver
- Set values in `config.yml` accordingly
- Create Cron job to call script repeatedly (1x / h shouldn't draw too much attention ;)

Note: This script will most likely break when the website is updated. 
