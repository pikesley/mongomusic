Mongo Music
===========

Indexes your (properly tagged) mp3s/oggs in Mongo. Probably useful for something.

* `sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10`
* `echo "deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen" >> /etc/apt/sources.list`
* `apt-get update`
* `apt-get install mongodb-10gen python-setuptools python-yaml python-tagpy`
* `easy_install pymongo`

edit _config/config.yaml_ to taste, then

`./store_my_music.py -h`
