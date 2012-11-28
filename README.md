reprepro_watch
================

An inotify-based tool to rebuild an APT repository.

`reprepro_watch` was inspired by the Debian administration article [Setting up your own APT repository with upload support](http://www.debian-administration.org/articles/286).  It uses inotify instead of a cron job to detect when packages are uploaded to the `incoming` directory.

Basic Installation
------------------

The system should have `virtualenv`, `supervisord`, `gnupg2`, and `gnupg-agent` installed beforehand.

Clone the repository at /srv/reprepro

In /srv/reprepro, create a virtualenv, install requirements, and install reprepro_watch:

```
virtualenv venv
venv/bin/pip install -r requirements.txt
venv/bin/python setup.py install
```

Manually create the following directories:

```
mkdir -p /var/run/reprepro_watch /var/log/reprepro_watch
chown ubuntu.ubuntu /var/run/reprepro_watch /var/log/reprepro_watch
```

Assumptions
-----------

Currently this assumes there is a user named `ubuntu` on the system.  It also
assumes the project is extracted at `/srv/reprepro_watch` and that the APT
repository was created in `/srv/apt_repository`.
