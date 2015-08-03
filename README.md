# salt-state-graph

This is a tool for visualising the runtime dependency graph of a
[Salt](https://github.com/saltstack/salt) highstate.

It takes the json output of `state.show_highstate` or `state.show_sls` from
Salt and produces a program written in
[dot](http://www.graphviz.org/doc/info/lang.html), which is a tool from
Graphviz for defining an acyclic graph.  

Some examples, with the dot programs rendered as png:

http://i.imgur.com/wETR0WG.png
http://i.imgur.com/LJ6ckzr.png

## Usage

The tool expects the JSON output of `show_highstate` or `show_sls` over stdin.
It outputs `dot` code representing the dependency graph. The dot code defines a
single digraph called "states".

For example, if you have a salt master running:

	salt 'minion*' state.show_highstate --out json | salt_state_graph

You can write the dot output to a file, or pipe it further into the `dot` tool
from GraphViz. In this example, we produce a png called `output.png`:

	salt 'minion*' state.show_highstate --out json \
	| salt_state_graph \
	| dot -Tpng -o output.png


## Installation

Install directly from PyPi:

	pip install salt_state_graph

Or clone this repository and use `setup.py`:

	python setup.py install

Unfortunately, the version of the `pydot` package in PyPi doesn't work in
Python 2.7+. We're working on getting this up to date. In the meantime, please
use this fork to install the `pydot` package first:

https://github.com/nlhepler/pydot


## dot

Most operating systems have a package for it, usually as part of GraphViz.

**Debian / Ubuntu**:

	apt-get install graphviz

**OSX with homebrew**:

	brew install graphviz


pydot
-----


Usage
====

Example:

```bash
# Run a show_highstate for a single minion and get the output as YAML
$ salt-call state.show_highstate --out yaml > ~/highstate

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

## Running tests

The test runner is [tox](https://tox.readthedocs.org/en/latest/). Run it from
the root of the project. It will run tests for a number of different Python
versions, as well as Flake8:

	$ tox -l
	py27
	py34
	pypy
	flake8

This will run all of the tests in python 2.7, 3.4 and pypy.
