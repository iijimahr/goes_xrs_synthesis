"""
File downloader with SHA256 verification.
"""

import hashlib
from pathlib import Path

DATA_DIR = Path.home() / ".cache" / "goes_xrs_synthesis"


def _sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    """
    Compute SHA256 hash of a file.
    """
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def _download_file(url: str, dst: Path, timeout: int = 60) -> None:
    import urllib.request

    req = urllib.request.Request(url, headers={"User-Agent": "yourpkg/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r, dst.open("wb") as f:
        f.write(r.read())


def download_file(query: dict) -> Path:
    """
    Download a file from a URL and verify its SHA256 hash.
    """
    file_path = DATA_DIR / Path(query["url"]).name
    if not file_path.exists():
        file_path.parent.mkdir(parents=True, exist_ok=True)
        _download_file(query["url"], file_path)
    got = _sha256_file(file_path)
    if got.lower() != query["sha256"].lower():
        file_path.unlink(missing_ok=True)
        raise ValueError(
            "SHA256 mismatch for downloaded file.\n"
            f"  expected: {query['sha256']}\n"
            f"  got     : {got}\n"
            f"  url     : {query['url']}\n"
            f"  path    : {file_path}"
        )
    return file_path
