reprepro_watch
==============

An inotify-based tool to rebuild an APT repository.

`reprepro_watch` was inspired by the Debian administration article [Setting up your own APT repository with upload support](http://www.debian-administration.org/articles/286).  It uses inotify instead of a cron job to detect when packages are uploaded to the `incoming` directory.

Basic Installation
------------------

The system should have `virtualenv`, `supervisord`, `gnupg2`, and `gnupg-agent` installed beforehand.

Clone the repository in the `/srv` directory.

In `/srv/reprepro_watch`, create a virtualenv, install requirements, and install reprepro_watch:

```
virtualenv venv
venv/bin/pip install -r requirements.txt
venv/bin/python setup.py install
```

Finally, copy the Upstart init script and start the watcher:

```
sudo cp /srv/reprepro_watch/etc/init/reprepro_watch.conf /etc/init
sudo start reprepro_watch
```

Assumptions
-----------

Currently this assumes there is a user named `ubuntu` on the system.

It also assumes the APT repository was created in `/srv/apt_repository`.
