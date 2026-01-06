"""
Synthesizing GOES XRS fluxes from (differential) emission measure (DEM).
"""

import numpy as np
from astropy.io import fits

from .downloader import download_file


def get_goes_xrs_response_table() -> str:
    """
    Get the path to the GOES XRS response FITS file.
    Downloads it if not already cached.
    """
    query = {
        "url": "https://sohoftp.nascom.nasa.gov/solarsoft/gen/idl/synoptic/goes/goes_chianti_response_latest.fits",
        "sha256": "cb00c05850e3dc3bbd856eb07c1a372758d689d0845ee591d6e2531afeab0382",
    }
    return download_file(query)


def define_satellite_index(goes_num: int = 17) -> int:
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


def synthesize_isothermal(
    temp: float = 1.0e6, em: float = 1e49, goes_num: int = 17
) -> tuple[float, float]:
    """
    Synthesize GOES XRS fluxes from DEM.
    """
    tab = load_goes_xrs_response_table()
    sat = define_satellite_index(goes_num)

    # Temperature grid (MK)
    tab_temp = tab["TEMP_MK"][sat]

    # Compute response function and scale (W/m^2) / (1e49 cm^-3)
    scale = 10.0 ** (49.0 - tab["ALOG10EM"][sat])  # -> per 1e49

    # Use response functions for coronal abundance
    resp_long = tab["FLONG_COR"][sat] * scale
    resp_short = tab["FSHORT_COR"][sat] * scale

    # Synthesized flux (W/m^2)
    flux_long = np.interp(temp / 1.0e6, tab_temp, resp_long) * (em / 1e49)
    flux_short = np.interp(temp / 1.0e6, tab_temp, resp_short) * (em / 1e49)

    return flux_long, flux_short
