# -*- coding: utf-8 -*-
import collections
import json
import sys

import pydot


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

    if not hasattr(obj, "__iter__"):
        # not a sequence type - return nothing
        # this excludes strings
        return results

    if isinstance(obj, dict):
        # a dict - check each key
        for key, prop in obj.items():
            if key == find_key:
                results.extend(prop)
            elif isinstance(prop, dict):
                results.extend(find_inner(prop, find_key))
    elif isinstance(obj, list):
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
    try:
        deps = find(states, relname)
        for dep in deps:
            for dep_type, dep_name in dep.items():
                yield make_node_name(dep_type, dep_name)
    except AttributeError as e:
        sys.stderr.write("Bad state: {0}\n".format(str(states)))
        raise e


class Graph(object):
    def __init__(self, input):
        state_obj = json.load(input, object_pairs_hook=collections.OrderedDict)
        self.graph = pydot.Dot("states", graph_type="digraph")

        rules = {
            "require": {"color": "blue"},
            "require_in": {"color": "blue", "reverse": True},
            "watch": {"color": "red"},
            "watch_in": {"color": "red", "reverse": True},
            "onchanges": {"color": "green"},
            "onchanges_in": {"color": "green", "reverse": True},
        }

        if len(state_obj.keys()) > 1:
            raise Exception(
                "Unsupported: graph for multiple minions: {}".format(
                    ",".join(state_obj)
                )
            )

        minion_obj = list(state_obj.values())[0]

        if "__extend__" in minion_obj:
            for extend_element in minion_obj["__extend__"]:
                for state_name, extend_block in extend_element.items():
                    for extend_type, extend_value in extend_block.items():
                        if extend_type[:2] == "__":
                            continue
                        if state_name not in minion_obj:
                            minion_obj[state_name] = collections.OrderedDict()
                        if extend_type not in minion_obj[state_name]:
                            minion_obj[state_name][extend_type] = []
                        extended_state = minion_obj[state_name][extend_type]

                        def get_subprop(s, n):
                            for x in s:
                                if hasattr(x, "items") and n in x:
                                    return x[n]

                        for rule in rules:
                            extend_state_req = get_subprop(extend_value, rule)
                            extended_state_req = get_subprop(extended_state, rule)
                            if extend_state_req:
                                if extended_state_req:
                                    extended_state_req.extend(extend_state_req)
                                else:
                                    extended_state.append(
                                        [
                                            collections.OrderedDict(
                                                {rule: extend_state_req}
                                            )
                                        ]
                                    )
            del minion_obj["__extend__"]

        for top_key, props in minion_obj.items():
            # Add a node for each state type embedded in this state
            # keys starting with underscores are not candidates

            for top_key_type, states in list(props.items()):
                if top_key_type[:2] == "__":
                    continue

                node_name = make_node_name(top_key_type, top_key)
                self.graph.add_node(pydot.Node(node_name))

                for edge_type, ruleset in list(rules.items()):
                    for relname in find_edges(states, edge_type):
                        if "reverse" in ruleset and ruleset["reverse"]:
                            self.graph.add_edge(
                                pydot.Edge(node_name, relname, color=ruleset["color"])
                            )
                        else:
                            self.graph.add_edge(
                                pydot.Edge(relname, node_name, color=ruleset["color"])
                            )

    def render(self, fmt):
        if fmt == "dot":
            return self.graph.to_string()
        else:
            pass
