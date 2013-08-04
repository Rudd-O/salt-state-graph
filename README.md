A tool for visualising the dependency graph of a
[Salt](https://github.com/saltstack/salt) highstate.

The utility ingests the YAML representing the Salt highstate (or sls state) for
a single minion and produces a program written in DOT.

An example: http://i.imgur.com/wETR0WG.png

Each node is a state. Edges are dependency relationships:

* `require`
* `require_in`
* `watch`
* `watch_in`

requires are blue; watches are red.

Installation
============

* pydot
* dot

dot
---

Most operating systems have a package for it, usually as part of GraphViz.

**Debian**:

	apt-get install graphviz

**Arch**:

	pacman -S graphviz

**OSX with homebrew**:

	brew install graphviz


pydot
-----

The maintainer's version doesn't work in
Python2.7+; we're working on getting PyPi access, in the meantime use [this
fork](https://github.com/nlhepler/pydot):


i.e.:

```bash
$ git clone https://github.com/nlhepler/pydot.git
$ cd pydot
$ python setup.py install
```

Usage
====

Example:

```bash
# Run a show_highstate for a single minion and clean up the output
$ salt-call state.show_highstate | sed -r "s/    ----------//g" > ~/highstate

# Run salt-state-graph with the recorded highstate as stdin
$ python salt-state-graph.py < ~/highstate > ~/highstate.dot
```

Now you can use the [`dot`](http://en.wikipedia.org/wiki/DOT_%28graph_description_language%29) utility to compile this into a graph:

```bash
$ dot -Tpng < ~/highstate.dot -o highstate.png
```

```bash
$ dot -Tsvg < ~/highstate.dot -o highstate.svg
```
