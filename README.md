# engage-project

A very simple face based authorization system.



Steps to run in your system

1) Clone this repository.
2) Run ```pip install -r requirements.txt``` in your shell to get all the dependencies
3) Run   ```python app.py``` to deploy the project

Please note: Your local host is assumed to be 127.0.0.1 on port 5000 so if it is anything else than this, things might not work properly..

Update:
Added the sign up page.

While signing up, please use the photo with single face. And make sure the photo is clear

After sign-up, server needs to be restarted. This is because all the reference images are loaded during the time of server initialization itself.
