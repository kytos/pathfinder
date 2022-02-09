|Stable| |Tag| |License| |Build| |Coverage| |Quality|

.. raw:: html

  <div align="center">
    <h1><code>kytos/pathfinder</code></h1>

    <strong>NApp that finds network paths</strong>

    <h3><a href="https://kytos-ng.github.io/api/pathfinder.html">OpenAPI Docs</a></h3>
  </div>

Overview
========

``pathfinder`` is responsible for creating a graph with
the latest network topology and providing rest endpoint to calculate the best
path between two devices. In the network, each device is a host or a switch and
each link is a connection between two devices. In the graph, each device
represents a node and each link represents an edge between two nodes.

The NApp learns custom properties from the topology, being able to define the
best paths based on a weighted parameter. Please see the Rest API documentation
for details.

Features
========
- REST API to find constrained network paths
- Keep track of the current network graph to find constrained paths
- Web UI

Installing
==========

To install this NApp, first, make sure to have the same venv activated as you have ``kytos`` installed on:

.. code:: shell

   $ git clone https://github.com/kytos-ng/pathfinder.git
   $ cd pathfinder
   $ python setup.py develop

Requirements
============

- `kytos/topology <https://github.com/kytos-ng/topology.git>`_

Events
======

Subscribed
----------

- ``kytos/topology.updated``
- ``kytos/topology.links.metadata.(added|removed)``

.. TAGs

.. |License| image:: https://img.shields.io/github/license/kytos-ng/kytos.svg
   :target: https://github.com/kytos-ng/ /blob/master/LICENSE
.. |Build| image:: https://scrutinizer-ci.com/g/kytos-ng/pathfinder/badges/build.png?b=master
  :alt: Build status
  :target: https://scrutinizer-ci.com/g/kytos-ng/pathfinder/?branch=master
.. |Coverage| image:: https://scrutinizer-ci.com/g/kytos-ng/pathfinder/badges/coverage.png?b=master
  :alt: Code coverage
  :target: https://scrutinizer-ci.com/g/kytos-ng/pathfinder/?branch=master
.. |Quality| image:: https://scrutinizer-ci.com/g/kytos-ng/pathfinder/badges/quality-score.png?b=master
  :alt: Code-quality score
  :target: https://scrutinizer-ci.com/g/kytos-ng/pathfinder/?branch=master
.. |Stable| image:: https://img.shields.io/badge/stability-stable-green.svg
   :target: https://github.com/kytos-ng/pathfinder
.. |Tag| image:: https://img.shields.io/github/tag/kytos-ng/pathfinder.svg
   :target: https://github.com/kytos-ng/pathfinder/tags
