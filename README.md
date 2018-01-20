# genmagyartvm3u
This is a really simple application written in Django that generates an M3U file of Hungarian TV feed from https://www.mediaklikk.hu. The resulting URL can be played using Kodi's PVR IPTV add-on.

# Heroku Support
The project has been optimized to run in Heroku. Heroku provides a free service to run Django applications. Download and install Heroku. After Heroku has been installed, open a command prompt (or shell) and execute the following commands:

git clone https://github.com/t3knoid/genmagyartvm3u.git.
cd genmagyartvm3u
heroku create
heroku buildpacks:set heroku:/python
heroku config:set DISABLE_COLLECTSTATIC=1
git push heroku master
heroku ps:scale web=1
