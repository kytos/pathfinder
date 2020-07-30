#########
Changelog
#########
All notable changes to the pathfinder NApp will be documented in this file.

[UNRELEASED] - Under development
********************************

Added
=====
- Added support for automated tests and CI with Travis.
- Added unit tests.

Changed
=======

Deprecated
==========

Removed
=======

Fixed
=====
- Fixed package install when creating symlinks.
- Fixed hops addresses in openapi.yml.

Security
========


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
