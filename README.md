# metamer_sounds
This project is a hobby project motivated by my dream of "auralizing," or "hearing," the difference between metamers. 
Metamers are different EM (light) spectral power distributions with the same perceived color.
Color space is 3-dimensional, but tone is essentially infinite-dimensional, because of the respective structures of the sensory organs.
(Another notable difference is that there is not really a question of "perfect color" perception, as there is with perfect pitch, except perhaps in philosophy.)

In any case this is a widget with sliders that independently control the wavelength and amplitude of several pure sinusoidal signals,
and map the sum(s) of these signals simultaneously to a visual (color) representation and an aural (tone) representation.

The nature of interaction is quite janky, but c'est la vie. 
(Static matplotlib, together with the fresh creation of an autoplay IPython Display Audio widget whenever you move a slider.
BQPlot would be preferable, but that gets complicated, 
and in particular one would need to re-implement the matplotlib-venn packge that I rely on for the plots.

Click this link, wait for the binder site to launch, then open the "metamer_sounds.ipynb" notebook (not sure why I can't get a link directly to the notebook working). Click the "kernel" menu, and select "restart and run all". Then you can adjust the wavelength and amplitude sliders in the widget at the bottom.
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ClayCampaigne/metamer_sounds/HEAD)
