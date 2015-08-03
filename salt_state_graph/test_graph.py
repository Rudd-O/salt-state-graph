import os
import salt_state_graph

test_folder = os.path.join(os.path.dirname(__file__), "testdata")


def test_graph():
    """
    Use our example data to see that the dot output produced matches what we
    expect.
    """
    examples = set([
        os.path.join(test_folder, f.split(".")[0])
        for f in os.listdir(test_folder)
    ])

    # The examples won't be byte-for-byte identical with what we produce unless
    # we sort the lines
    for e in examples:
        with open(e + ".dot") as f:
            expect = "".join(sorted([l.strip() for l in f.readlines()]))
        with open(e + ".json") as f:
            g = salt_state_graph.Graph(f)
            got = "".join(sorted(g.render('dot').splitlines()))
            assert got.strip() == expect.strip()
