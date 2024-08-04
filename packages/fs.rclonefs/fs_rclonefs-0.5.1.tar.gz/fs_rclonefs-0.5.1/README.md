# Access rclone from a pyfilesystem interface

__version__ = 0.5.1



## About

This gives you a `pyfilesystem` object with an `rclone` remote for a backend. So any backend you can use with rclone, you can use with pyfilesystem. (You need to configure rclone separately.)


### Usage

This assumes you've run the external program `rclone config` and configured a remote called `dropbox:`.

    >>> from fs.rclonefs import RcloneFS
    >>> my_remote = RcloneFS('dropbox:')
    >>> my_remote.listdir('/')

More examples:

    >>> my_remote.getinfo('/that file over there.mp4')
    >>> my_remote.remove('/that file over there.mp4')
    >>> my_remote.getinfo('/some folder', namespaces=['details'])

Use the 'storage' namespace to get directory sizes.

    >>> my_remote.getinfo('/gigantor', namespaces=['storage'])

The `removetree()` method uses rclone's `purge` command -- which should make quick work of directories and their contents -- really quick work if the rclone backend supports the purge command (like Dropbox does).

(The pyfilesystem default `removetree()` does a path walk and removes every item individually which causes a lot of calls to the rclone backend and takes a long time to complete large trees, tying up rclone for several minutes.)

### USE AT YOUR OWN RISK

Things might not work as expected. Like any other household product, you should test it on a small out-of-the-way place first before dumping it all over everything.

I went ahead and ran the pyfilesystem tests on my personal dropbox...

The simple stuff, listed below, works.

### Status

Working:
- getinfo()
- listdir()
- isdir()/isfile()
- exists()
- remove()
- removedir()
- removetree()
- writetext()
- readtext()

TODO:
- URI opener
- address pyfilesystem unittest failures
- make copy methods efficient between reclone remotes
  (Currently we rely on a TempFS to cache files,
  which is in addition to whatever caching is being
  done by rclone already, so we're looking at multiple
  copies being made if we use two pyfilesystem instances
  and try to copy between them.)

## Dependencies

#### Automatically installed: pyfilesystem 2.4.12

The Mac-Daddy of all file system abstractions -- along side rclone -- and FUSE. But _absolutely_ number one of the number ones.

Installed automagically with fs-rclone if'n y'all don't already have it.

#### You need to install: rclone v1.67.0

Control a wide variety of cloud storage with this puppy.

[github.com/rclone/rclone](https://github.com/rclone/rclone)
[Install rclone on your own.](https://rclone.org/install/)

__version_used_by_this_project__ = _rclone-v1.67.0-linux-amd64_


## Tools

The `Rclone` object class controls `rclone` on your system.

    >>>from fs.rclonefs import Rclone
    >>>rclone = Rclone()
    >>>rclone.list_files('myremote:')



## Changelog

0.5.1 Fixed relative import issue that prevented module from loading.

0.5.0 Implement `openbin()` and internal file handles to support `writetext()` and `readtext()` methods. Implement `upload()` and `download()` methods also. Add unittest `tests.py` -- (in src folder, not tests folder).

0.4.0 Add `remove()`, `removedir()`, `removetree()`. Add `Rclone` class. Add `storage` namespace for getinfo(). Fix datetime format in getinfo.

0.3.1 Fixed `fs` namespace packaging.

0.3.0 Add `getinfo()`, `listdir()`, `isdir()`. Add `makepy` tool. Add `Devnotes.ipynb`.

0.2.0 Fix project name for pyfilesystem style. Add src RcloneFS.ipynb and opener.ipynb.

0.1.2 Update README

0.1.0 Add dependencies to `pyproject.toml`. Add `SoftBOM` (software bill of materials). Delete test code.

0.0.1 fix bug in example::add_one

0.0.0 configure package files
