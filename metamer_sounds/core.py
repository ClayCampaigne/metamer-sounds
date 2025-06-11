"""
Core functions for metamer sound generation and visualization
"""

import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import Audio, display
import numpy as np
from matplotlib_venn import venn3, venn3_circles
from itertools import product

from colormath.color_objects import SpectralColor, sRGBColor
from colormath.color_conversions import convert_color


def get_spec_for_cm(wvl: float, amp: float) -> pd.Series:
    """Get a pandas series with index appropriate to colormath spectral color density with a single nonzero power
    
    Args:
        wvl: Wavelength in nanometers (340-830)
        amp: Amplitude/intensity value
        
    Returns:
        pandas Series with spectral data for colormath
    """
    assert 340 <= wvl <= 830, "we require 340 < wvl < 830"
    spec = pd.Series(index=range(340, 831, 10), data=0.0)
    spec[int(np.round(wvl / 10.) * 10.)] = amp  # round the signals to the nearest 10
    return spec


def get_cm_sc_args(spec: pd.Series) -> dict:
    """Convert pandas series to colormath SpectralColor arguments
    
    Args:
        spec: Spectral power distribution as pandas Series
        
    Returns:
        Dictionary of keyword arguments for SpectralColor constructor
    """
    spec_dict = spec[spec>0].to_dict()
    return {f"spec_{wvl}nm": spec_dict[wvl] for wvl in spec_dict}


def cmsc_from_spec(spec: pd.Series) -> SpectralColor:
    """Create SpectralColor object from spectral power distribution
    
    Args:
        spec: Spectral power distribution as pandas Series
        
    Returns:
        colormath SpectralColor object
    """
    return SpectralColor(**get_cm_sc_args(spec))


# Scientific scaling constants (based on physics)
c_light_mps = 299792458.  # speed of light in meters per second
c_sound_mps = 343.  # speed of sound in meters per second

min_wvl_nM = 381. 
max_wvl_nM = 779. 
min_freq_EM_Hz = c_light_mps / (max_wvl_nM * 1e-9)
max_freq_EM_Hz = c_light_mps / (min_wvl_nM * 1e-9)

min_pitch_hz = 60.
max_wvl_sound_m = c_sound_mps / min_pitch_hz
max_pitch_hz = 4000.
min_wvl_sound_m = c_sound_mps / max_pitch_hz

# Scientific wavelength-to-frequency mapping
m_scientific = (max_wvl_sound_m - min_wvl_sound_m) / (max_wvl_nM - min_wvl_nM)
b_scientific = min_wvl_sound_m - m_scientific * min_wvl_nM


def desired_sound_wvl_from_wvl_light(wvl_light: float, m: float = m_scientific, b: float = b_scientific) -> float:
    """Convert light wavelength to sound wavelength using linear mapping
    
    Args:
        wvl_light: Light wavelength in nanometers
        m: Linear scaling factor
        b: Linear offset
        
    Returns:
        Sound wavelength in meters
    """
    return m * wvl_light + b


def desired_pitch_from_wvl_light(wvl_light: float, m: float = m_scientific, b: float = b_scientific, 
                                c_sound_mps: float = c_sound_mps) -> float:
    """Convert light wavelength to audio frequency
    
    Args:
        wvl_light: Light wavelength in nanometers
        m: Linear scaling factor
        b: Linear offset
        c_sound_mps: Speed of sound in m/s
        
    Returns:
        Audio frequency in Hz
    """
    desired_sound_wvl = desired_sound_wvl_from_wvl_light(wvl_light, m=m, b=b)
    desired_pitch = c_sound_mps / desired_sound_wvl
    return desired_pitch


def tritone_metamers_cm(wvl_1: float = 460, wvl_2: float = 530, wvl_3: float = 610.60, 
                       a1: float = 0.75, a2: float = 0.85, a3: float = 0.85,
                       scaling: str = "scientific", max_time: float = 15, rate: int = 8000) -> None:
    """Generate audio and visual representation of three-wavelength metamer
    
    Args:
        wvl_1, wvl_2, wvl_3: Wavelengths in nanometers
        a1, a2, a3: Amplitudes (normalized if sum > 1.0)
        scaling: "scientific" or "simple" wavelength-to-frequency mapping
        max_time: Audio duration in seconds
        rate: Audio sample rate in Hz
    """
    # Normalize amplitudes if needed
    amp_tot = a1 + a2 + a3
    if amp_tot > 1.0:
        a1 /= amp_tot
        a2 /= amp_tot
        a3 /= amp_tot
    
    # Choose scaling method
    if scaling == "simple":
        # Simple linear mapping for better audio experience
        m = -1.
        b = 1000.
        pitch_1 = m * wvl_1 + b 
        pitch_2 = m * wvl_2 + b
        pitch_3 = m * wvl_3 + b
    else:
        # Scientific scaling based on physics
        pitch_1 = desired_pitch_from_wvl_light(wvl_1)
        pitch_2 = desired_pitch_from_wvl_light(wvl_2)
        pitch_3 = desired_pitch_from_wvl_light(wvl_3)

    print(f"wvl_1 = {wvl_1} nM and pitch_1 = {pitch_1:.2f} Hz")
    print(f"wvl_2 = {wvl_2} nM and pitch_2 = {pitch_2:.2f} Hz")
    print(f"wvl_3 = {wvl_3} nM and pitch_3 = {pitch_3:.2f} Hz")
    
    # Generate audio
    times = np.linspace(0, max_time, int(rate * max_time))
    sig1 = a1 * np.sin(2 * np.pi * pitch_1 * times) 
    sig2 = a2 * np.sin(2 * np.pi * pitch_2 * times)
    sig3 = a3 * np.sin(2 * np.pi * pitch_3 * times)
    sig_tot = sig1 + sig2 + sig3

    display(Audio(data=sig_tot, rate=rate, autoplay=True, normalize=False))
    
    # Generate color visualization
    scale = 15
    spec1 = scale * get_spec_for_cm(wvl_1, a1)
    spec2 = scale * get_spec_for_cm(wvl_2, a2)
    spec3 = scale * get_spec_for_cm(wvl_3, a3)

    plt.figure(figsize=(4, 4), facecolor='k')
    v = venn3(subsets=(1, 1, 1, 1, 1, 1, 1), set_labels = ('', '', ''))

    # Color each patch based on spectral combinations
    for elem in product([0,1], [0,1], [0,1]):
        if elem != (0,0,0):
            this_id = str(elem[0]) + str(elem[1]) + str(elem[2])  # eg '100', '010', etc
            # the color in the patch is the sum of the signal components represented in the patch
            this_spec = elem[0]*spec1 + elem[1]*spec2 + elem[2]*spec3 
            this_cmsc = cmsc_from_spec(this_spec)
            this_rgb = convert_color(this_cmsc, sRGBColor)
            this_clamped_rgb = sRGBColor(this_rgb.clamped_rgb_r,
                                         this_rgb.clamped_rgb_g,
                                         this_rgb.clamped_rgb_b)

            v.get_patch_by_id(this_id).set_color(this_clamped_rgb.get_rgb_hex())
            v.get_patch_by_id(this_id).set_alpha(1.0)
            v.get_label_by_id(this_id).set_text('')

    c = venn3_circles(subsets=(1, 1, 1, 1, 1, 1, 1), linestyle='-')
    plt.show()
    return