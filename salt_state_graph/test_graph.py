import os
import pytest

import salt_state_graph


test_folder = os.path.join(os.path.dirname(__file__), "testdata")
examples = set(
    [os.path.join(test_folder, f.split(".")[0]) for f in os.listdir(test_folder)]
)


@pytest.mark.parametrize("example", examples)
def test_graph(example):
    """
    Use our example data to see that the dot output produced matches what we
    expect.
    """
    # The examples won't be byte-for-byte identical with what we produce unless
    # we sort the lines
    with open(example + ".dot") as f:
        expect = "".join([l.strip() for l in f.readlines()])
    with open(example + ".json") as f:
        g = salt_state_graph.Graph(f)
        got = "".join(g.render("dot").splitlines())
        assert got.strip() == expect.strip()
