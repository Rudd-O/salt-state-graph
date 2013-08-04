"""
salt-state-graph

A tool that ingests the YAML representing the Salt highstate (or sls state) for
a single minion and produces a program written in DOT.

The tool is useful for visualising the dependency graph of a Salt highstate.
"""
from pydot import Dot, Node, Edge
import yaml
import sys


def find(obj, find_key):
    """
    Takes a list and a set.

    Recursively traverses the list to find objects with keys in the key set.

    Returns a list of all matching objects.
    """
    def inner(obj, find_key):
        results = []

        if not hasattr(obj, '__iter__'):
            # not a sequence type - return nothing
            return results

        if isinstance(obj, dict):
            # a dict - check each key
            for key, prop in obj.iteritems():
                if key == find_key:
                    results.extend(prop)
                else:
                    results.extend(inner(prop, find_key))
        else:
            # a list / tuple / set  - check each item
            for i in obj:
                results.extend(inner(i, find_key))

        return results

    final = []
    for i in obj:
        r = inner(i, find_key)
        if len(r) > 0:
            final.extend(r)

    return final


def make_node_name(state_type, state_label):
    return "{0} - {1}".format(state_type.upper(), state_label)


def find_edges(states, relname):
    deps = find(states, relname)
    for dep in deps:
        for dep_type, dep_name in dep.iteritems():
            yield make_node_name(dep_type, dep_name)


def main(input):
    state_obj = yaml.load(input)
    graph = Dot("states", graph_type='digraph')

    rules = {
        'require': {'color': 'blue'},
        'require_in': {'color': 'blue', 'reverse': True},
        'watch': {'color': 'red'},
        'watch_in': {'color': 'red', 'reverse': True},
    }

    for top_key, props in state_obj.iteritems():
        # Add a node for each state type embedded in this state
        # keys starting with underscores are not candidates

        if top_key == '__extend__':
            continue

        for top_key_type, states in props.iteritems():
            if top_key_type[:2] == '__':
                continue

            node_name = make_node_name(top_key_type, top_key)
            graph.add_node(Node(node_name))

            for edge_type, ruleset in rules.iteritems():
                for relname in find_edges(states, edge_type):
                    if 'reverse' in ruleset and ruleset['reverse']:
                        graph.add_edge(Edge(
                            node_name, relname, color=ruleset['color']))
                    else:
                        graph.add_edge(Edge(
                            relname, node_name, color=ruleset['color']))

    graph.write('/dev/stdout')

if __name__ == '__main__':
    main(sys.stdin)
