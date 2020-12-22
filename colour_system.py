
# ripped off from:
# https://scipython.com/blog/converting-a-spectrum-to-a-colour/

# also see here:
# https://mathematica.stackexchange.com/questions/57389/convert-spectral-distribution-to-rgb-color
import numpy as np
import pandas as pd


def xyz_from_xy(x, y):
    """Return the vector (x, y, 1-x-y)."""
    return np.array((x, y, 1-x-y))


class ColourSystem:
    """A class representing a colour system.

    A colour system defined by the CIE x, y and z=1-x-y coordinates of
    its three primary illuminants and its "white point".

    TODO: Implement gamma correction

    """

    # The CIE colour matching function for 380 - 780 nm in 5 nm intervals
    cmf = np.loadtxt('cie-cmf.txt', usecols=(1,2,3))

    def __init__(self, red, green, blue, white):
        """Initialise the ColourSystem object.

        Pass vectors (ie NumPy arrays of shape (3,)) for each of the
        red, green, blue  chromaticities and the white illuminant
        defining the colour system.

        """

        # Chromaticities
        self.red, self.green, self.blue = red, green, blue
        self.white = white
        # The chromaticity matrix (rgb -> xyz) and its inverse
        self.M = np.vstack((self.red, self.green, self.blue)).T
        self.MI = np.linalg.inv(self.M)
        # White scaling array
        self.wscale = self.MI.dot(self.white)
        # xyz -> rgb transformation matrix
        self.T = self.MI / self.wscale[:, np.newaxis]

    def xyz_to_rgb(self, xyz, out_fmt=None, normalize=True):
        """Transform from xyz to rgb representation of colour.

        The output rgb components are normalized on their maximum
        value. If xyz is out the rgb gamut, it is desaturated until it
        comes into gamut.

        By default, fractional rgb components are returned; if
        out_fmt='html', the HTML hex string '#rrggbb' is returned.

        """

        rgb = self.T.dot(xyz)
        if np.any(rgb < 0):
            # We're not in the RGB gamut: approximate by desaturating
            # CWC: should I instead project onto the Gamut coordinatewise?
            w = - np.min(rgb)
            rgb += w
        if not np.all(rgb==0) or normalize:
            # Normalize the rgb vector
            rgb /= np.max(rgb)

        if out_fmt == 'html':
            return self.rgb_to_hex(rgb)
        return rgb

    def rgb_to_hex(self, rgb):
        """Convert from fractional rgb values to HTML-style hex string."""

        hex_rgb = (255 * rgb).astype(int)
        return '#{:02x}{:02x}{:02x}'.format(*hex_rgb)

    def spec_to_xyz(self, spec, normalize=True):
        """Convert a spectrum to an xyz point.
        # removing normalization is not working
        The spectrum must be on the same grid of points as the colour-matching
        function, self.cmf: 380-780 nm in 5 nm steps.

        """

        XYZ = np.sum(spec[:, np.newaxis] * self.cmf, axis=0)
        den = np.sum(XYZ)
        if den == 0. or not normalize:
            return XYZ
        return XYZ / den

    def spec_to_rgb(self, spec, out_fmt=None, normalize=False):
        """Convert a spectrum to an rgb value."""
        # removing normalization is not working
        xyz = self.spec_to_xyz(spec, normalize=normalize)
        return self.xyz_to_rgb(xyz, out_fmt, normalize=normalize)


illuminant_D65 = xyz_from_xy(0.3127, 0.3291)
cs_hdtv = ColourSystem(red=xyz_from_xy(0.67, 0.33),
                       green=xyz_from_xy(0.21, 0.71),
                       blue=xyz_from_xy(0.15, 0.06),
                       white=illuminant_D65)

cs_smpte = ColourSystem(red=xyz_from_xy(0.63, 0.34),
                        green=xyz_from_xy(0.31, 0.595),
                        blue=xyz_from_xy(0.155, 0.070),
                        white=illuminant_D65)

cs_srgb = ColourSystem(red=xyz_from_xy(0.64, 0.33),
                       green=xyz_from_xy(0.30, 0.60),
                       blue=xyz_from_xy(0.15, 0.06),
                       white=illuminant_D65)


# Clay's code:
def get_spec(wvl, amp):
    """Clay gets a color spectrum for a single wavelength, amplitude pair"""
    # the color frequencies are represented on a grid of 380-780 nm in 5 nm steps
    # if the result is not the right length, you probably gave a bad input
    #  which required adding a new index entry
    # not sure why the following assertion doesn't prevent that:
    assert 380 < wvl < 780, "we require 380 < wvl < 780"
    spec = pd.Series(index=np.arange(380., 781., 5), data=0.0)
    spec[np.ceil(wvl/5.)*5.] = amp  # round the signals to the nearest 5.0
    return spec