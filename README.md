# metamer_sounds
This project is a hobby project to "auralize," or "hear," the difference between metamers. 
Metamers are different EM (light) spectral power distributions with the same perceived color.
Color space is 3-dimensional, but tone is essentially infinite-dimensional because of the respective structures of the sensory organs.
(Another notable difference is that there is not really a question of "perfect color" perception, as there is with perfect pitch, except perhaps in philosophy.)
So I want to make an app with sliders that independently control the wavelength and amplitude of several pure sinusoidal signals,
and map the sum(s) of these signals simultaneously to a visual (color) representation and an aural (tone) representation.

I ripped off https://scipython.com/blog/converting-a-spectrum-to-a-colour/ for the color part, and I ripped off https://ipywidgets.readthedocs.io/en/stable/examples/Beat%20Frequencies.html for the sound (and widget).

The second draft of the interactive widget in the notebook uses `python-colormath` to get dark colors, which
I couldn't figure out with `colour-science`. This seems to work well enough, although
I still need to do some calibration. The major problem to be addressed here is that is that the 
"clamping" of RGB values to project onto the RGB gamut seems to make it hard to get 
everything bright at the same time. E.g., getting one display with the three primary colors, including
a bright yellow in the red-green intersection. Or just a nice white.


Note: the color is in wavelength (nM), while the sound is in Herz, slightly scaled. 
This is dumb because wavelength is proportional to the inverse of frequency. 

The other major problem is that it is not truly interactive. It creates a static autoplay sound and a static matplotlib plot, 
so the interaction is extremely janky. But updating to bqplot would take a lot of work, and for the audio portion, that
seems even more complicated. I have been unable to install pyaudio because of OSX C++ compiler issues, I guess.

Click this link, wait for the binder site to launch, then open the "tricolor_venn_colormath.ipynb" notebook (not sure why I can't get a link directly to the notebook working. Click the "kernel" menu, and select "restart and run all". Then you can adjust the frequency/wavelength and amplitude sliders in the widget at the bottom.
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ClayCampaigne/metamer_sounds/HEAD)
