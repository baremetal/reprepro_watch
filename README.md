reprepro_watch
==============

An inotify-based tool to rebuild an APT repository.

`reprepro_watch` was inspired by the Debian administration article [Setting up
your own APT repository with upload support](http://www.debian-administration.org/articles/286).  It uses inotify
instead of a cron job to detect when packages are uploaded to the `incoming`
directory.


Basic Installation
------------------

The system should have `dupload`, `reprepro`, `virtualenv`, `supervisord`, `gnupg2`, and
`gnupg-agent` installed beforehand.

Clone the repository in the `/srv` directory.

In `/srv/reprepro_watch`, create a virtualenv, install requirements, and
install reprepro_watch:

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


APT repository installation
---------------------------

Create the APT repository at `/srv/apt_repository`:

sudo mkdir -p /srv/apt_repository/conf
sudo mkdir -p /srv/apt_repository/incoming

Then create the `conf/distributions` file, for example:

```
Origin: Baremetal Industries
Label: Baremetal
Codename: lucid
Version: 3.1
Architectures: i386 amd64 source
Components: main non-free contrib
Description: Baremetal package repository for stable release code
```

Note: if you want packages to be automatically signed, add the `SignWith` parameter:

```
SignWith: <key_id>
```
Note that the i386 architecture is required otherwise `apt-get update` will
complain.  In order for signing to work unattended with a key that contains a
passphrase, the passphrase can be fed to the agent that the init script starts
up using the `scripts/preset_passphrase` script:

```
scripts/preset_passphrase <key_id>
```

Configure dupload
-----------------

[Dupload](http://packages.debian.org/search?keywords=dupload) is a standard tool
used to publish Debian packages.  Configure it by adding the following entry to
`/etc/dupload.conf`:

```
$cfg{'your_repo_alias'} = {
    fqdn => "<hostname>",
    login => "ubuntu",
    method => "scpb",

    incoming => "/srv/apt_repository/incoming",

    # The dinstall on ftp-master sends emails itself
    dinstall_runs => 1,
};
```

If this is the default location you will be uploading packages to, uncomment
the $default_host variable and set it to your entry's name; `your_repo_alias`
in the example above:

```
$default_host = "your_repo_alias";
```


Adding Packages with dupload
----------------------------

Add packages using the `dupload` tool.  After building a debian package point
`dupload` to the changes file and it will take care of the rest:

```
dupload --to your_repo_alias /path/to/package.changes
```

When the packages are uploaded, `reprepro_watch` will detect the upload and add
the packages to the repository.  Behind the scenes, it is running the command:

```
reprepro -Vb . include <distro_name> incoming/package.changes
```

Removing Packages
-----------------

Packages can be removed by running the command:

```
reprepro -Vb . remove <distro_name> <package_name>
```


Assumptions
-----------

Currently this assumes there is a user named `ubuntu` on the system.

It also assumes the APT repository was created in `/srv/apt_repository`.
