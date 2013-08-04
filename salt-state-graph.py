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
    Takes a list and a set.  Returns a list of all matching objects.

    Uses find_inner to recursively traverse the data structure, finding objects
    with keyed by find_key.
    """

    all_matches = [find_inner(item, find_key) for item in obj]
    final = [item for sublist in all_matches for item in sublist]

    return final


def find_inner(obj, find_key):
    """
    Recursively search through the data structure to find objects
    keyed by find_key.
    """
    results = []

    if not hasattr(obj, '__iter__'):
        # not a sequence type - return nothing
        # this excludes strings
        return results

    if isinstance(obj, dict):
        # a dict - check each key
        for key, prop in obj.iteritems():
            if key == find_key:
                results.extend(prop)
            else:
                results.extend(find_inner(prop, find_key))
    else:
        # a list / tuple - check each item
        for i in obj:
            results.extend(find_inner(i, find_key))

    return results


def make_node_name(state_type, state_label):
    return "{0} - {1}".format(state_type.upper(), state_label)


def find_edges(states, relname):
    """
    Use find() to recursively find objects at keys matching
    relname, yielding a node name for every result.
    """
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
            # TODO - merge these into the main states and remove them
            #sys.stderr.write(
            #        "Removing __extend__ states:\n{0}\n".format(str(props)))
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
