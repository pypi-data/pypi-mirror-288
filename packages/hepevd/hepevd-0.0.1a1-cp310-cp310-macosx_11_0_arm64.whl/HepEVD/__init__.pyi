from collections.abc import Collection
import enum
from typing import Dict, Union


class HitDimension(enum.IntEnum):
    """Enum to distinguish between 3D and 2D hits."""

    _member_names_: list = ['TWO_D', 'THREE_D']

    _member_map_: dict = ...

    _value2member_map_: dict = ...

    TWO_D = 1
    """A 2D hit"""

    THREE_D = 0
    """A 3D hit"""

class HitType(enum.IntEnum):
    """
    Enum for various possible hit types. This is mostly useful for LArTPC view data.
    """

    _member_names_: list = ['GENERAL', 'TWO_D_U', 'TWO_D_V', 'TWO_D_W']

    _member_map_: dict = ...

    _value2member_map_: dict = ...

    GENERAL = 0
    """General hit type"""

    TWO_D_U = 1
    """A 2D U View hit, from a LArTPC"""

    TWO_D_V = 2
    """A 2D V View hit, from a LArTPC"""

    TWO_D_W = 3
    """A 2D W View hit, from a LArTPC"""

def add_hit_properties(hit: Collection[float | int], properties: Dict[float | int]) -> None:
    """
    Add custom properties to a hit, via a string / double dictionary.
    The hit must be passed as a (x, y, z, energy) list or array.
    """

def add_hits(hits: Collection[Collection[float | int | HitType | HitDimension]], label: str = '') -> None:
    """
    Adds hits to the current event state.
    Hits must be passed as an (NHits, Y) list or array, with the columns being (x, y, z, energy) and two optional columns (view, dimension) for the hit type and dimension.
    The view and dimension values must be from the HepEVD.HitType and HepEVD.HitDimension enums respectively.
    """

def add_mc(hits: Collection[Collection[float | int | HitType | HitDimension]], label: str = '') -> None:
    """
    Adds MC hits to the current event state.
    Hits must be passed as an (NHits, Y) list or array, with the columns being (x, y, z, energy, PDG) and two optional columns (view, dimension) for the hit type and dimension.
    The view and dimension values must be from the HepEVD.HitType and HepEVD.HitDimension enums respectively.
    """

def is_initialised() -> bool:
    """
    Checks if the server is initialised - i.e. does a server exists, with the geometry set?
    """

def reset_server(reset_geo: bool = False) -> None:
    """Resets the server"""

def save_state(state_name: str, min_size: int = -1, clear_on_show: bool = True) -> None:
    """Saves the current state"""

def set_geometry(geometry: Union[str, Collection[Collection[float | int]]]) -> None:
    """Sets the geometry of the server"""

def set_verbose(verbose: bool) -> None:
    """Sets the verbosity of the HepEVD server"""

def start_server(start_state: int = -1, clear_on_show: bool = True) -> None:
    """Starts the HepEVD server"""
