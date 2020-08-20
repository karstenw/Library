## Nodebox Library folder ##

## Things that are new ##

`twyg` - The twyg library needs at least NodeBox 1.9.23.



The contents of this repo go into the ```~/Library/Application Support/Nodebox/``` folder. As of 2017-05-20 and NodeBox v1.9.17+ the library folder can be anywhere.

These are modules that could be made to work with my [Nodebox fork](https://github.com/karstenw/nodebox-pyobjc).

The module ```ants``` runs unchanged.

The module ```beziereditor``` runs unchanged.

The module ```boids``` runs unchanged.

The module ```colors``` has been patched for zipfile support. The [patch](https://github.com/shoebot/shoebot/commit/b2b9c43b28acb9312ca2a0557cc8728fc49a47bb) came from the [shoebot](https://github.com/shoebot/shoebot) project. You'll need at least Nodebox version 1.9.17.

The module ```coreimage``` has been adapted. The "perspectivetile" crash has been fixed.

The module ```cornu``` runs unchanged.

The module ```database``` has been adapted. Now uses the Python built-in sqlite3 library.

The module ```en``` runs unchanged.

The module ```explode``` runs unchanged.

The module ```fatpath``` runs unchanged.

The module ```flowerewolf``` runs unchanged.

The module ```graph``` runs unchanged.

The module ```graphbrowser``` runs unchanged.

The module ```grid``` runs unchanged.

The module ```ìsight``` has been rewritten to use the newer [imagesnap](http://iharder.net/imagesnap) tool which makes it possible to take sequences of images very quickly.

The module ```lsys```has been written from scratch. Why? Because lindemayer systems are fun. Included are a lot of demos from "Algorithmic Beauty of Plants" and "Lindenmayer Systems, Fractals, and Plants".

The module ```lsystem``` runs unchanged.

The module ```noise``` has been adapted and the _noise.so file has been compiled for i386/x86_64

The module ```perception``` runs unchanged.

The module ```photobot``` has been adapted to use [Pillow](https://github.com/python-pillow/Pillow), the PIL successor. You'll need at least Nodebox version 1.9.12.

The module ```pixie``` runs unchanged.

The module ```quicktime``` runs unchanged.

The module ```supershape``` has been adapted and the cSuperformula.so file has been compiled for i386/x86_64

The module ```svg``` runs unchanged.

The module ```web``` runs somehow. Many of the interfaced services have ceased to exist.

The module ```wikipedia``` runs unchanged.

The module ```wordnet``` runs unchanged.



## Things that do not work ##

1. ```boostgraph```: Missing source files for shared libs.

1. ```cutout```: No demo files, no docs.

1. ```geometry```: Has been integrated into the app.

1. ```google```: Needs a licence key which I do not have and wont apply for.

1. ```purenode, tuio and wiinode```: Need devices which I do not have.


