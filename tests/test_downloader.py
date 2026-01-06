"""
Tests for the downloader module.
"""

from goes_xrs_synthesis.downloader import download_file

query_goes_chianti_response = {
    "url": "https://sohoftp.nascom.nasa.gov/solarsoft/gen/idl/synoptic/goes/goes_chianti_response_latest.fits",
    "sha256": "cb00c05850e3dc3bbd856eb07c1a372758d689d0845ee591d6e2531afeab0382",
}


def test_download_file():
    file_path = download_file(query_goes_chianti_response)
    assert file_path.exists()
    assert file_path.name == "goes_chianti_response_latest.fits"
    file_path.unlink()
