|Release| |test|

.. |Release| image:: https://github.com/canonical/craft-artifacts/actions/workflows/release-publish.yaml/badge.svg?branch=main&event=push
   :target: https://github.com/canonical/craft-artifacts/actions/workflows/release-publish.yaml
.. |test| image:: https://github.com/canonical/craft-artifacts/actions/workflows/qa.yaml/badge.svg?branch=main&event=push
   :target: https://github.com/canonical/craft-artifacts/actions/workflows/qa.yaml

***************
Craft Artifacts
***************

Craft Artifacts is a Python package to manage artifacts packing on behalf of tools
relying on the Craft framework.

Craft Artifacts provides:

* a set of common interfaces to define the desired artifacts and their dependencies.
* a set of common packers to produce artifacts under various formats.
* an interface to add custom packers.
