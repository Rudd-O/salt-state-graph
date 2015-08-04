# salt-state-graph

This is a tool for visualising the runtime dependency graph of a
[Salt](https://github.com/saltstack/salt) highstate.

It takes the json output of `state.show_highstate` or `state.show_sls` from
Salt and produces a program written in
[dot](http://www.graphviz.org/doc/info/lang.html), which is a tool from
Graphviz for defining an acyclic graph.

States are nodes and dependencies are edges. `require` and `require_in` are blue; `watch` and `watch_in` are red.

Some examples, with the dot programs rendered as png:

http://i.imgur.com/wETR0WG.png

http://i.imgur.com/LJ6ckzr.png

## Usage

The tool expects the JSON output of `show_highstate` or `show_sls` over stdin.
It outputs `dot` code representing the dependency graph. The dot code defines a
single digraph called "states".

For example, if you have a salt master running:

	salt 'minion1' state.show_highstate --out json | salt_state_graph

You can write the dot output to a file, or pipe it further into the `dot` tool
from GraphViz. In this example, we produce a png called `output.png`:

	salt 'minion*' state.show_highstate --out json \
	| salt_state_graph \
	| dot -Tpng -o output.png

The tool currently only supports rendering the output from one minion. If you
give it output with two minions, it'll report an error.

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

## TODO

* support backends aside from dot (e.g. JSON to feed into D3)
* add more tests
* add `pydot` as a proper dependency once it's updated in pypi

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
