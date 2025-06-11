"""
Metamer Sounds: Converting light wavelengths to audio frequencies
"""

from .core import (
    get_spec_for_cm,
    get_cm_sc_args,
    cmsc_from_spec,
    desired_pitch_from_wvl_light,
    tritone_metamers_cm
)

__version__ = "0.1.0"
__all__ = [
    "get_spec_for_cm",
    "get_cm_sc_args", 
    "cmsc_from_spec",
    "desired_pitch_from_wvl_light",
    "tritone_metamers_cm"
]