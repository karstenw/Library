## Nodebox Library folder ##



## Things that are new ##

`twyg` - The twyg library needs at least NodeBox 1.9.23.



The contents of this repo go into the ```~/Library/Application Support/Nodebox/``` folder. As of 2017-05-20 and NodeBox v1.9.17+ the library folder can be anywhere.

These are modules that could be made to work with my [Nodebox fork](https://github.com/karstenw/nodebox-pyobjc).

The module ```ants``` runs.

The module ```beziereditor``` runs.

The module ```boids``` runs.

The module ```colors``` has been patched for zipfile support. The [patch](https://github.com/shoebot/shoebot/commit/b2b9c43b28acb9312ca2a0557cc8728fc49a47bb) came from the [shoebot](https://github.com/shoebot/shoebot) project. You'll need at least Nodebox version 1.9.17.

The module ```coreimage``` runs mostly.

The module ```cornu``` runs.

The module ```database``` runs but should not be used. Use linguistics.pattern.db

The module ```en``` has been removed. Use linguistics and adapt your scripts.

The module ```explode``` runs.

The module ```fatpath``` runs.

The module ```flowerewolf``` is in adaption.

The module ```graph``` runs mostly.

The module ```graphbrowser``` runs mostly.

The module ```grid``` runs.

The module ```ìsight``` has been rewritten to use the newer [imagesnap](http://iharder.net/imagesnap) tool which makes it possible to take sequences of images very quickly.

The module ```lsys```has been written from scratch. Why? Because lindemayer systems are fun. Included are a lot of demos from "Algorithmic Beauty of Plants" and "Lindenmayer Systems, Fractals, and Plants".

The module ```lsystem``` runs.

The module ```noise``` has been adapted and the _noise.so file has been compiled for x86\_64

The module ```perception``` has been removed; may come back.

The module ```photobot``` has been adapted to use [Pillow](https://github.com/python-pillow/Pillow), the PIL successor. You'll need at least Nodebox version 1.9.12.

The module ```pixie``` runs.

The module ```quicktime``` runs on Intel. Can't run on newer Macs with M-*

The module ```supershape``` has been adapted and the cSuperformula.so file has been compiled for x86_64

The module ```svg``` runs.

The module ```web``` has been removed. Use linguistics.pattern.web; [docs](https://www.nodebox.net/code/index.php/Web.html)

The module ```wikipedia``` has been removed. Use linguistics.pattern.wikipedia

The module ```wordnet``` removed. Use linguistics.pattern.text.wordnet; [docs](https://www.nodebox.net/code/index.php/WordNet.html)



## Things that do not work ##

1. ```boostgraph```: Missing source files for shared libs.

1. ```cutout```: No demo files, no docs.

1. ```geometry```: Has been integrated into the app.

1. ```google```: Needs a licence key which I do not have and wont apply for.

1. ```purenode, tuio and wiinode```: Need devices which I do not have.


