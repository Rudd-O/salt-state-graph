import os
import pip.req
import uuid
import setuptools


VERSION = '0.0.1'

#reqs = pip.req.parse_requirements(
#        os.path.join(os.path.dirname(__file__),
#            "requirements.txt"), session=uuid.uuid1())

test_requirements = ['pytest==2.7.2', 'flake8']

setup = dict(
    author='Cera Davies',
    author_email='ceralena.davies@learnosity.com',
    url='https://github.com/ceralena/salt-state-graph',
    version=VERSION,
    name='salt_state_graph',
    description='a tool to represent salt states and their dependencies as an acyclic graph',
    packages=[
        'salt_state_graph',
    ],

    scripts=[
        'bin/salt_state_graph'
    ],

    tests_require=test_requirements,

    install_requires=[]+test_requirements,

    include_package_data=True,
)

setuptools.setup(**setup)
