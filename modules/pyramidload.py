# modules/pyramid_loader.py
"""
Module for loading and using pre-computed pyramids.
Supports both local files and remote GitHub-hosted pyramid files.
"""

import pickle
import io
from pathlib import Path
from urllib.parse import urljoin
import requests
import xarray as xr
import shared


def is_remote_url(path):
    """Check if path is a remote URL"""
    return isinstance(path, str) and path.startswith(('http://', 'https://'))


class PyramidCache:
    """Cache for loaded pyramids from local or remote sources"""

    def __init__(self, pyramid_dir=shared.PYRAMID_DIR):
        self.pyramid_dir = pyramid_dir
        self.is_remote = is_remote_url(pyramid_dir)
        if not self.is_remote:
            self.pyramid_dir = Path(pyramid_dir)
        self.cache = {}

    def _build_pyramid_path(self, variable, profile):
        """Build the full path/URL for a pyramid file"""
        filename = f"prob_2024_dec_tercile_probability_max_{variable}_lvl_{profile}_subsampled.pkl"

        if self.is_remote:
            # Ensure base URL ends with /
            base_url = self.pyramid_dir.rstrip('/') + '/'
            # Append the pyramids subfolder and filename
            return urljoin(base_url, f"refs/heads/main/get_ldas_probabilistic_output/subsampled/{filename}")
        else:
            return self.pyramid_dir / filename

    def _load_from_remote(self, url):
        """Load pickle file from remote GitHub URL"""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return pickle.load(io.BytesIO(response.content))
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise FileNotFoundError(
                    f"Pyramid not found at remote URL: {url}\n"
                    f"Ensure pyramid files are uploaded to the GitHub repository"
                )
            raise RuntimeError(f"Failed to fetch pyramid from {url}: {e}")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Network error fetching pyramid from {url}: {e}")

    def _load_from_disk(self, filepath):
        """Load pickle file from local disk"""
        if not filepath.exists():
            raise FileNotFoundError(
                f"Pyramid not found: {filepath}\n"
                f"Run scripts/create_all_pyramids.py to generate pyramids"
            )

        with open(filepath, 'rb') as f:
            return pickle.load(f)

    def get_pyramid(self, variable, profile=0):
        """
        Load pyramid from cache, remote URL, or local disk

        Parameters
        ----------
        variable : str
            Variable name
        profile : int
            Profile/depth index

        Returns
        -------
        dict : Pyramid data with 'pyramid' and 'grain_map' keys
        """
        cache_key = f"{variable}_lvl_{profile}"

        # Check cache first
        if cache_key in self.cache:
            return self.cache[cache_key]

        # Build path/URL
        pyramid_path = self._build_pyramid_path(variable, profile)

        # Load from appropriate source
        if self.is_remote:
            pyramid_data = self._load_from_remote(pyramid_path)
        else:
            pyramid_data = self._load_from_disk(pyramid_path)

        # Cache it
        self.cache[cache_key] = pyramid_data

        return pyramid_data
    
    def get_data_at_zoom(self, variable, profile, zoom_level):
        """
        Get data at specific zoom level
        
        Parameters
        ----------
        variable : str
            Variable name
        profile : int
            Profile/depth index
        zoom_level : int
            Zoom level (0-5)
            
        Returns
        -------
        xr.DataArray : Data at requested zoom level
        """
        pyramid_data = self.get_pyramid(variable, profile)
        pyramid = pyramid_data['pyramid']
        
        if zoom_level not in pyramid:
            # Use nearest available zoom
            available_zooms = sorted(pyramid.keys())
            zoom_level = min(available_zooms, key=lambda k: abs(k - zoom_level))
        
        return pyramid[zoom_level]


# Global pyramid cache
_pyramid_cache = PyramidCache()


def get_pyramid_data(variable, profile=0, zoom_level=None):
    """
    Convenience function to get pyramid data
    
    Parameters
    ----------
    variable : str
        Variable name
    profile : int
        Profile/depth index
    zoom_level : int, optional
        Specific zoom level to retrieve (default: use shared.PYRAMID_ZOOM_LEVEL)
        
    Returns
    -------
    xr.DataArray : Data at requested resolution
    lon, lat, time : Coordinate arrays
    """
    if zoom_level is None:
        zoom_level = shared.PYRAMID_ZOOM_LEVEL
    
    data = _pyramid_cache.get_data_at_zoom(variable, profile, zoom_level)
    
    # Extract coordinates
    lon = data.lon.values
    lat = data.lat.values
    time = data.time.values if 'time' in data.dims else None
    
    return data, lon, lat, time