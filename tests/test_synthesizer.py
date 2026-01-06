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
    synthesize_isothermal,
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

    for idx in range(0, 2001, 500):
        # Observed flux from the *same* truncated series and same idx
        obs_short = float(obs_flux.quantity("xrsa")[idx].to_value(u.W / u.m**2))
        obs_long = float(obs_flux.quantity("xrsb")[idx].to_value(u.W / u.m**2))

        T_est = float(obs_em.quantity("temperature")[idx].to_value(u.K))
        EM_est = float(
            obs_em.quantity("emission_measure")[idx].to_value(u.cm**-3)
        )

        inv_long, inv_short = synthesize_isothermal(
            temp=T_est, em=EM_est, goes_num=goes_num
        )

        # Scale for SDAC/GSFC data if needed
        if "SDAC/GSFC" == obs_flux.meta.metas[0].get("Origin"):
            obs_long /= 0.7
            obs_short /= 0.85

        rtol = 0.1
        assert np.isclose(inv_long, obs_long, rtol=rtol)
        assert np.isclose(inv_short, obs_short, rtol=rtol)


if __name__ == "__main__":
    test_get_goes_xrs_response_table()
    test_synthesize_isothermal()
