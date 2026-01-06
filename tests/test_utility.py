"""
Tests for utility functions.
"""

import numpy as np

from goes_xrs_synthesis.utility import flare_class_to_flux, flux_to_flare_class


def test_flare_class_to_flux():
    assert np.isclose(flare_class_to_flux("A1.0"), 1e-8)
    assert np.isclose(flare_class_to_flux("B2.5"), 2.5e-7)
    assert np.isclose(flare_class_to_flux("C3.2"), 3.2e-6)
    assert np.isclose(flare_class_to_flux("M5.0"), 5e-5)
    assert np.isclose(flare_class_to_flux("X3.0"), 3.0e-4)
    assert np.isclose(flare_class_to_flux("X15.0"), 1.5e-3)


def test_flux_to_flare_class():
    assert flux_to_flare_class(5e-8) == "A5.0"
    assert flux_to_flare_class(2.5e-7) == "B2.5"
    assert flux_to_flare_class(3.2e-6) == "C3.2"
    assert flux_to_flare_class(5e-5) == "M5.0"
    assert flux_to_flare_class(3e-4) == "X3.0"
    assert flux_to_flare_class(1.5e-3) == "X15.0"
