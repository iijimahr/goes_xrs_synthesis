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


Examples
========

Define a logarithmic temperature grid:

.. doctest::

   >>> import numpy as np
   >>> from goes_xrs_synthesis import synth_dem
   >>> temp = np.logspace(6.0, 7.2, 200)

Define a Gaussian DEM in log10(T):

.. doctest::

   >>> logT0 = 6.5
   >>> sigma = 0.15
   >>> dem = 1e22 * np.exp(-0.5 * ((np.log10(temp) - logT0) / sigma) ** 2)

Synthesize GOES XRS fluxes:

.. doctest::

   >>> flux_long, flux_short = synth_dem(temp, dem)

The output is a pair of scalars or arrays:

.. doctest::
   :options: +ELLIPSIS

   >>> flux_long.shape
   ()
   >>> flux_short.shape
   ()
   >>> flux_long, flux_short
   (np.float64(6.7...e-27), np.float64(1.7...e-28))

Data
====

GOES XRS response functions are based on precomputed,
CHIANTI-based temperature response tables
provided by `SolarSoftWare <https://www.lmsal.com/solarsoft/>`_.

Units
=====

- Temperature: :math:`\mathrm{K}`
- Emission measure: :math:`\mathrm{cm^{-3}}`
- Differential emission measure: :math:`\mathrm{cm^{-3}\, K^{-1}}`
- GOES XRS fluxes: :math:`\mathrm{W\,m^{-2}}`
- GOES XRS response function: :math:`\mathrm{W\,m^{-2}\, (10^{49}\, cm^{-3})^{-1}}`

License
=======

This project is licensed under the BSD-3-Clause License.

API Reference
=============

.. automodule:: goes_xrs_synthesis
   :members:
