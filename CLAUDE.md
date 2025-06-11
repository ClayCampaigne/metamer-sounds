# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a research project that "auralizes" color metamers - mapping light wavelengths to sound frequencies to explore perceptual differences between spectral distributions that appear as the same color but would sound different. The project creates interactive widgets that simultaneously display color representations (as Venn diagrams) and generate corresponding audio.

## Architecture

The project consists of two main Jupyter notebooks:

- `metamer_sounds_scientific_scaling.ipynb` - Uses physically-based wavelength-to-frequency conversion mapping light and sound wavelengths proportionally
- `metamer_sounds_simple_scaling.ipynb` - Uses simplified linear scaling between wavelength ranges for more audibly pleasant results

Both notebooks share the same core architecture:
- **Color processing**: Uses `colormath` library to convert spectral power distributions to RGB colors via SpectralColor objects
- **Audio generation**: Maps light wavelengths to audio frequencies and generates sinusoidal tones using numpy
- **Visualization**: Creates interactive Venn diagrams using `matplotlib-venn` to show color combinations
- **Interaction**: Uses `ipywidgets` for real-time wavelength and amplitude control

## Key Functions

- `get_spec_for_cm(wvl, amp)` - Creates pandas Series for colormath spectral color input
- `tritone_metamers_cm()` - Main function that generates both audio and visual output
- Wavelength-to-frequency conversion varies between notebooks (scientific vs simplified scaling)

## Environment Setup

Install dependencies with:
```bash
pip install -r requirements.txt
```

The project is designed to run in Jupyter notebooks, with Binder support for web-based execution.

## Development Notes

- Light wavelengths are in nanometers (381-779 nm visible spectrum)
- Audio frequencies are mapped to audible range (60-4000 Hz)
- Amplitude normalization prevents clipping when multiple signals combine
- Interactive widgets auto-generate matplotlib plots and IPython Audio objects on parameter changes