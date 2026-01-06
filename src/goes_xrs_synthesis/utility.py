"""
Utility functions for GOES XRS data.
"""


def flare_class_to_flux(flare_class: str) -> float:
    """
    Convert GOES XRS flare class string (e.g. 'C3.2') to flux in W/m^2.

    Parameters
    ----------
    flare_class : str
        Flare class string.

    Returns
    -------
    float
        Peak flux in W/m^2.
    """
    class_map = {"A": 1e-8, "B": 1e-7, "C": 1e-6, "M": 1e-5, "X": 1e-4}
    try:
        letter = flare_class[0].upper()
        scale = float(flare_class[1:]) if len(flare_class) > 1 else 1.0
        return class_map[letter] * scale
    except (KeyError, ValueError, IndexError, TypeError):
        raise ValueError(f"Invalid flare class: {flare_class}")


def flux_to_flare_class(peak_flux: float) -> str:
    """
    Convert peak GOES XRS long-channel flux [W/m^2] to flare class string.

    Parameters
    ----------
    peak_flux : float
        Peak flux in W/m^2.

    Returns
    -------
    str
        Flare class string.
    """
    if peak_flux < 1e-7:
        base, letter = 1e-8, "A"
    elif peak_flux < 1e-6:
        base, letter = 1e-7, "B"
    elif peak_flux < 1e-5:
        base, letter = 1e-6, "C"
    elif peak_flux < 1e-4:
        base, letter = 1e-5, "M"
    else:
        base, letter = 1e-4, "X"
    mult = peak_flux / base
    return f"{letter}{mult:.1f}"
