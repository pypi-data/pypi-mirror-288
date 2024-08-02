"""
Computational Hypergraph Discovery Package


This is the main module for the Computational Hypergraph Discovery package.
This package provides functionality for discovering hypergraphs from data.

Classes:
    GraphDiscovery: A class for discovering hypergraphs from data. This class
        is the main class for the package.

Modules:
    Modes: A module containing different modes for hypergraph discovery.
    decision: A module containing decision functions for hypergraph discovery.
    util: A module containing utility functions for hypergraph discovery.
"""

import jax

try:
    jax.config.update("jax_enable_x64", True)
except:
    print(
        "CHD needs JAX in 64 bits precision. Please run `jax.config.update('jax_enable_x64', True)` after initializing jax, or import CHD first"
    )
from ._GraphDiscoveryMain import GraphDiscovery
from . import Modes
from . import decision
from . import util
