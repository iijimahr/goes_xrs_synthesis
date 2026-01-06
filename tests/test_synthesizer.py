"""
Tests for the synthesizer module.
"""

import astropy.units as u
import numpy as np
import sunpy.data.sample
from astropy.io import fits
from sunkit_instruments import goes_xrs
from sunpy import timeseries as ts

from goes_xrs_synthesis.synthesizer import (
    load_goes_xrs_response_table,
    synth_dem,
    synth_isothermal,
)


def test_get_goes_xrs_response_table():
    tab = load_goes_xrs_response_table()
    assert isinstance(tab, fits.fitsrec.FITS_rec)
    for key in ["TEMP_MK", "ALOG10EM", "FLONG_COR", "FSHORT_COR"]:
        assert key in tab.names


def test_synthesize_isothermal():
    obs_ts = ts.TimeSeries(sunpy.data.sample.GOES_XRS_TIMESERIES)
    obs_flux = obs_ts.truncate("2011-06-07 06:20", "2011-06-07 07:30")
    assert obs_flux.shape == (2051, 2)

    # Derive GOES number from metadata
    goes_num = int(obs_flux.observatory.split("-")[-1])
    assert goes_num == 15

    # temperature/em from the *same* truncated series
    obs_em = goes_xrs.calculate_temperature_em(obs_flux, abundance="coronal")

    idx = range(0, 2001, 500)

    obs_short = obs_flux.quantity("xrsa")[idx].to_value(u.W / u.m**2)
    obs_long = obs_flux.quantity("xrsb")[idx].to_value(u.W / u.m**2)
    temp = obs_em.quantity("temperature")[idx].to_value(u.K)
    em = obs_em.quantity("emission_measure")[idx].to_value(u.cm**-3)

    inv_long, inv_short = synth_isothermal(temp=temp, em=em, goes_num=goes_num)

    # Scale for SDAC/GSFC data if needed
    if "SDAC/GSFC" == obs_flux.meta.metas[0].get("Origin"):
        if 8 <= goes_num <= 16:
            obs_long /= 0.7
            obs_short /= 0.85

    rtol = 0.01
    np.testing.assert_allclose(inv_long, obs_long, rtol=rtol)
    np.testing.assert_allclose(inv_short, obs_short, rtol=rtol)


def test_synthesize_dem_compare_isothermal():
    temp = np.logspace(6.0, 7.3, 200)
    i0 = 123
    em = 3e48

    dem = np.zeros_like(temp)
    dT = np.gradient(temp)  # (nT,)
    dem[i0] = em / dT[i0]  # cm^-3 K^-1

    fl_dem_L, fl_dem_S = synth_dem(temp, dem, axis=-1, goes_num=17)
    fl_iso_L, fl_iso_S = synth_isothermal(temp[i0], em, goes_num=17)

    np.testing.assert_allclose(fl_dem_L, fl_iso_L, rtol=5e-3, atol=0.0)
    np.testing.assert_allclose(fl_dem_S, fl_iso_S, rtol=5e-3, atol=0.0)


def test_synth_dem_axis_argument():
    temp = np.logspace(6.0, 7.0, 200)
    n = 5
    dem = np.abs(np.random.default_rng(0).normal(size=(n, temp.size))) * 1e45

    fL1, fS1 = synth_dem(temp, dem, axis=-1, goes_num=17)
    assert fL1.shape == (n,)
    assert fS1.shape == (n,)

    dem2 = dem.T  # (nT, n)
    fL2, fS2 = synth_dem(temp, dem2, axis=0, goes_num=17)
    assert fL2.shape == (n,)
    assert fS2.shape == (n,)

    np.testing.assert_allclose(fL1, fL2, rtol=1e-12, atol=0.0)
    np.testing.assert_allclose(fS1, fS2, rtol=1e-12, atol=0.0)


def test_synth_dem_integration_invariance():
    rng = np.random.default_rng(1234)
    temp = np.logspace(6.0, 7.3, 400)
    dem = np.abs(rng.normal(size=temp.size)) * 1e45

    fL_log, fS_log = synth_dem(temp, dem, axis=-1, goes_num=17)

    temp_lin = np.linspace(temp.min(), temp.max(), temp.size)
    dem_lin = np.interp(temp_lin, temp, dem)
    fL_T, fS_T = synth_dem(temp_lin, dem_lin, axis=-1, goes_num=17)

    np.testing.assert_allclose(fL_log, fL_T, rtol=1e-2, atol=0.0)
    np.testing.assert_allclose(fS_log, fS_T, rtol=1e-2, atol=0.0)


if __name__ == "__main__":
    test_get_goes_xrs_response_table()
    test_synthesize_isothermal()
    test_synthesize_dem_compare_isothermal()
    test_synth_dem_axis_argument()
    test_synth_dem_integration_invariance()
