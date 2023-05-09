#########
Changelog
#########
All notable changes to the pathfinder NApp will be documented in this file.

[UNRELEASED] - Under development
********************************

Added
=====
- ``POST /v3/`` has replaced ``POST /v2/``
- ``POST /v3/`` now validates its OpenAPI spec

Fixed
=====

- ``undesired_links`` links now filter upfront as a subgraph to still efficiently allow a lazy computation of k shortest (constrained) paths.

Removed
=======
- ``desired_links`` is no longer supported. If used to use ``desired_links`` you can try to parametrize it with a different constraint for instance ``undesired_links`` or with ``mandatory_metrics``.
- ``POST /v2/`` has been removed

[2022.3.0] - 2022-12-15
***********************

Added
=====
- Subscribed to ``kytos/topology.topology_loaded`` to be more promptly responsive
- Subscribed to ``kytos/topology.current``
- Updated ``on_links_metadata_changed`` to also try to reconciliate the topology

Fixed
=====
- Fixed ``undesired_links`` (logical OR) and ``desired_links`` (logical AND) filters.
- Safe guards to discard graph topology older (out of order) events

General Information
===================
- ``@rest`` endpoints are now run by ``starlette/uvicorn`` instead of ``flask/werkzeug``.


[2022.1.1] - 2022-02-02
***********************

Changed
=======
- Changed UI ``k-select`` links items description to try to use ``link.metadata.link_name``


[2022.1.0] - 2022-01-25
***********************

Changed
=======
- Adapted ``update_nodes`` to only add if node.status is ``EntityStatus.UP``
- Adapted ``update_links`` to only add if link.status is ``EntityStatus.UP``


[2.4.1] - 2022-01-21
********************

Changed
=======
- Upgraded requirements
- Updated README to refer to Kytos NG


[2.4.0] - 2021-12-20
********************

Added
=====
- Subscribed to to `kytos/topology.links.metadata.(added|removed)` events to update the graph when computing the CSPF accordingly.


[2.3.0] - 2021-10-19
********************

Changed
=======
- Changed ``setup.py`` run both unit and integration tests.
- Bumped ``networkx to 2.5.1`` to support ``spf_attribute``.
- Augmented shortest paths to compute lazily what is needed.
- Updated ``openapi.yml`` spec accordingly to EP23-2
- ``POST v2/`` JSON response now includes both ``cost`` and ``metrics`` attributes, in addition to the ``hops`` attribute.
- Added a basic validation support for the API until full spec validation is implemented.
- Formatted changing files with ``black -l 79``

Added
=====
- Implemented support for EP23-2, without breaking changes in the ``v2`` API.
- Added support for both ``mandatory_metrics`` and ``flexible_metrics`` to find constrained best paths based on user-specified network metric constraints.
- Added support for ``spf_attribute`` in the API .
- Added support for ``spf_max_paths`` in the API.
- Added support for ``spf_max_path_cost`` in the API.
- Added new UI filtering components accordingly.
- Updated the UI to also support listing multiple best paths in the accordion list.


[2.2.4] - 2021-05-27
********************

Changed
=======
- Changed ``setup.py`` to alert when a test fails on Travis.
- Updated ``requirements/dev.txt`` file.

Fixed
=====
- Fixed a bug in parsing metadata of links (fix #64).


[2.2.3] - 2020-07-24
********************

Added
=====
- Added support for automated tests and CI with Travis.
- Added tags decorator to run tests by type and size.
- Added unit tests, increasing coverage to 90%.

Changed
=======
- Improved documentation about NApp dependencies.
- Changed tests structure to separate unit and integration tests.

Fixed
=====
- Fixed package install when creating symlinks.
- Fixed hops addresses in openapi.yml.
- Updated ``run.in`` to include ``networkx`` dependency


[2.2.2] - 2020-03-11
********************
Added
=====
- Log error message when networkx package isn't installed.
- Updated __init__.py file in tests folder to solve bug when running tests.

Fixed
=====
- Fixed Scrutinizer coverage error.
- Fixed some linter issues.


[2.2.1] - 2019-03-15
********************
Changed
=======
- Continuous integration enabled at scrutinizer.

Fixed
=====
- Improve code organization and fix some linter issues.


[2.2.0] - 2018-12-14
********************
Fixed
=====
- Link status (active/inactive) now considered when creating the graph.


[2.1.1] - 2018-06-15
********************
Fixed
=====
- Fixed pathfinder component to use `k-toolbar-item`.


[2.1.0] - 2018-04-20
********************
Added
=====
- Implements Pathfinder ui.

Fixed
=====
- Fix optional parameters (api/kytos/pathfinder/v2):
  - parameter, undesired_links and desired_links must be optional.

[2.0.0] - 2018-03-09
********************
Added
=====
- Support for filters in the output path list:
  - Desired links, which are required in the paths;
  - Undesired links, which cannot be in any path.

Changed
=======
- Code adapted to work with the new topology NApp output.
