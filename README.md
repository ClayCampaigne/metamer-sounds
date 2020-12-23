# metamer_sounds
This is a hobby project motivated by my dream of "auralizing," or "hearing," the difference between metamers. 
Metamers are different EM (light) spectral power distributions with the same perceived color.
Color space is 3-dimensional, but tone is essentially infinite-dimensional, because of the respective structures of the sensory organs.
That means that there are, like, infinitely times more tones than colors.
(Another notable difference is that there is not really a question of "perfect color" perception, as there is with perfect pitch, except perhaps in philosophy.)

In any case a widget is provided with sliders that independently control the wavelength and amplitude of three pure sinusoidal signals.
The sum(s) of these signals are mapped simultaneously to a visual (color) representation and an aural (tone) representation. 
For the colors, we also show the components and the pairwise sums, using a Venn diagram plotted with `matplotlib-venn`

The nature of interaction is quite janky, but c'est la vie. 
Every slider event makes a static matplotlib-venn plot, together with the fresh creation of an autoplay IPython Display Audio widget whenever you move a slider.
BQPlot would be preferable, but that gets complicated, and in particular one would need to re-implement the matplotlib-venn packge that I rely on for the plots.
And making the sound stuff properly interacive seems at least as complicated.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ClayCampaigne/metamer_sounds/HEAD)

Click the binder link above, wait for the binder site to launch, then open the "metamer_sounds.ipynb" notebook (not sure why I can't get a link directly to the notebook working).
Click the "kernel" menu, and select "restart and run all". Then you can adjust the wavelength and amplitude sliders in the widget at the bottom.
