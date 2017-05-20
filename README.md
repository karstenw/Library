## Nodebox Library folder ##

The contents of this repo go into the ```~/Library/Application Support/Nodebox/``` folder.

These are modules that could be made to work with my [Nodebox fork](https://github.com/karstenw/nodebox-pyobjc).


The module ```ìsight``` has been rewritten to use the newer [imagesnap](http://iharder.net/imagesnap) tool which makes it possible to take sequences of images very quickly.

The module ```photobot``` has been adapted. It now uses the PIL successor [Pillow](https://github.com/python-pillow/Pillow). You'll need at least Nodebox version 1.9.12.

The module ```lsys```has been written from scratch. Why? Because lindemayer systems are fun. Included are a lot of demos from "Algorithmic Beauty of Plants" and "Lindenmayer Systems, Fractals, and Plants".

The module ```colors``` has been patched for zipfile support. The [patch](https://github.com/shoebot/shoebot/commit/b2b9c43b28acb9312ca2a0557cc8728fc49a47bb) came from the [shoebot](https://github.com/shoebot/shoebot) project. 