GOES XRS Flux Synthesis from Emission Measure
=============================================

This package provides forward modeling of GOES XRS long and short
channel fluxes from emission measure (EM) or differential emission
measure (DEM).

Status
======

This package is provided primarily for personal and research use.
No guarantees are made regarding correctness, stability, or
long-term maintenance.

Installation
============

To install the package, use pip:

.. code-block:: bash
   pip install git+https://github.com/iijimahr/goes_xrs_synthesis.git

Data
====

GOES XRS response functions are based on precomputed,
CHIANTI-based temperature response tables
provided by `SolarSoftWare <https://www.lmsal.com/solarsoft/>`_.

Units
=====

- Temperature is given in megakelvin (MK).
- Emission measure is normalized to :math:`10^{49}\,\mathrm{cm^{-3}}`.
- GOES XRS fluxes are returned in :math:`\mathrm{W\,m^{-2}}`.

License
=======

This project is licensed under the BSD-3-Clause License.

API Reference
=============

.. automodule:: goes_xrs_synthesis
   :members:
