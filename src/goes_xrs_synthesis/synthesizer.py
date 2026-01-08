"""
Synthesizing GOES XRS fluxes from (differential) emission measure (DEM).
"""

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from astropy.io import fits
from numpy.typing import ArrayLike, NDArray

from .downloader import download_file


def get_goes_xrs_response_table() -> Path:
    """
    Get the path to the GOES XRS response FITS file.
    Downloads it if not already cached.
    """
    query = {
        "url": "https://sohoftp.nascom.nasa.gov/solarsoft/gen/idl/synoptic/goes/goes_chianti_response_latest.fits",
        "sha256": "cb00c05850e3dc3bbd856eb07c1a372758d689d0845ee591d6e2531afeab0382",
    }
    return download_file(query)


def define_satellite_index(goes_num) -> int:
    """
    Define the satellite index used in the response table
    based on GOES satellite number.
    """
    #  following supy.sunkit-instruments
    if goes_num <= 15:
        return goes_num - 1
    else:
        secondary = 0
        return 15 + 4 * (goes_num - 16) + secondary


def load_goes_xrs_response_table() -> fits.fitsrec.FITS_rec:
    """
    Load the GOES XRS response table from the FITS file.
    """
    path = get_goes_xrs_response_table()
    with fits.open(path) as hdul:
        return hdul[1].data.copy()


@dataclass(frozen=True, slots=True)
class GOESXRSResponse:
    """GOES XRS temperature response functions.

    Attributes
    ----------
    temp : NDArray[np.float64]
        Temperature grid [MK].
    long : NDArray[np.float64]
        Long-channel response [(W m^-2) / (1e49 cm^-3)].
    short : NDArray[np.float64]
        Short-channel response [(W m^-2) / (1e49 cm^-3)].
    """

    temp: NDArray[np.float64]
    long: NDArray[np.float64]
    short: NDArray[np.float64]


def get_response_function(goes_num: int = 17) -> GOESXRSResponse:
    """
    Get the GOES XRS response functions.

    Parameters
    ----------
    goes_num : int, optional
        GOES satellite number (default: 17).

    Returns
    -------
    GOESXRSResponse
        Temperature grid [MK] and channel response functions
        [(W m^-2) / (1e49 cm^-3)].
    """
    tab = load_goes_xrs_response_table()
    sat = define_satellite_index(goes_num)

    # Temperature grid (MK)
    temp = np.asanyarray(tab["TEMP_MK"][sat], dtype=np.float64)

    # Compute response function and scale (W m^-2) / (1e49 cm^-3)
    scale = 10.0 ** (49.0 - tab["ALOG10EM"][sat])  # -> per 1e49

    # Use response functions for coronal abundance
    resp_long = np.asarray(tab["FLONG_COR"][sat], dtype=np.float64) * scale
    resp_short = np.asarray(tab["FSHORT_COR"][sat], dtype=np.float64) * scale

    return GOESXRSResponse(
        temp=temp,
        long=resp_long,
        short=resp_short,
    )


def synth_isothermal(
    temp: ArrayLike, em: ArrayLike, goes_num: int = 17
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """
    Synthesize GOES XRS flux from isothermal emission measure.

    Parameters
    ----------
    temp : ArrayLike
        Temperature [K].
        Will be converted to float64.
    em : ArrayLike
        Emission measure [cm^-3].
        Will be converted to float64.
    goes_num : int, optional
        GOES satellite number, by default 17.

    Returns
    -------
    tuple[NDArray[np.float64], NDArray[np.float64]]
        Synthesized fluxes in the long and short channels [W m^-2].
    """
    temp = np.asarray(temp, dtype=np.float64)
    em = np.asarray(em, dtype=np.float64)
    assert temp.shape == em.shape

    r = get_response_function(goes_num)

    temp_mk = temp.flatten() / 1.0e6
    shape = em.shape
    em49 = em / 1e49

    flux_long = np.interp(temp_mk, r.temp, r.long).reshape(shape) * (em49)
    flux_short = np.interp(temp_mk, r.temp, r.short).reshape(shape) * (em49)
    return flux_long, flux_short


def synth_dem(
    temp: ArrayLike,
    dem: ArrayLike,
    axis: int = -1,
    goes_num: int = 17,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """
    Synthesize GOES XRS flux from differential emission measure (DEM).

    Parameters
    ----------
    temp : ArrayLike
        Temperature [K].
        Will be converted to float64.
    dem : ArrayLike
        Differential emission measure [cm^-3 K^-1].
        Will be converted to float64.
    axis : int, optional
        Temperature axis in `dem`, by default -1.
    goes_num : int, optional
        GOES satellite number, by default 17 (GOES-17).

    Returns
    -------
    tuple[NDArray[np.float64], NDArray[np.float64]]
        Synthesized fluxes in the long and short channels [W m^-2].
    """
    temp = np.asarray(temp, dtype=np.float64)
    assert temp.ndim == 1
    assert np.all(np.diff(temp) > 0)
    assert temp.min() > 0

    dem = np.asarray(dem, dtype=np.float64)
    assert dem.ndim >= 1
    assert dem.shape[axis] == temp.shape[0]

    # Interpolate response function
    # * left/right=0.0: zero response outside tabulated range
    r = get_response_function(goes_num)
    r_long = np.interp(temp / 1.0e6, r.temp, r.long, left=0.0, right=0.0)
    r_short = np.interp(temp / 1.0e6, r.temp, r.short, left=0.0, right=0.0)

    # Integrate DEM * response over temperature
    dem_Tlast = np.moveaxis(dem, axis, -1)  # for broadcasting
    logT = np.log10(temp)
    dT_dlogT = temp * np.log(10.0)
    dEM49_dlogT = dem_Tlast * dT_dlogT / 1e49
    flux_long = np.trapezoid(r_long * dEM49_dlogT, x=logT, axis=-1)
    flux_short = np.trapezoid(r_short * dEM49_dlogT, x=logT, axis=-1)
    return flux_long, flux_short
