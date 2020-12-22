# metamer_sounds
This project is a hobby project to "auralize," or "hear," the difference between metamers. 
Metamers are different EM (light) spectral power distributions with the same perceived color.
Color space is 3-dimensional, but tone is essentially infinite-dimensional because of the respective structures of the sensory organs.
(Another notable difference is that there is not really a question of "perfect color" perception, as there is with perfect pitch, except perhaps in philosophy.)
So I want to make an app with sliders that independently control the wavelength and amplitude of several pure sinusoidal signals,
and map the sum(s) of these signals simultaneously to a visual (color) representation and an aural (tone) representation.

I ripped off https://scipython.com/blog/converting-a-spectrum-to-a-colour/ for the color part, and I ripped off https://ipywidgets.readthedocs.io/en/stable/examples/Beat%20Frequencies.html for the sound (and widget).

I'm currently stuck, trying to undo normalization of total intensity for the colors. Help!

Note: the color is in wavelength (nM), while the sound is in Herz, slightly scaled. 
This is dumb because wavelength is proportional to the inverse of frequency. 

The other major problem is that it is not truly interactive. It creates a static autoplay sound and a static matplotlib plot, 
so the interaction is extremely janky. But updating to bqplot would take a lot of work, and for the audio portion, that
seems even more complicated. I have been unable to install pyaudio because of OSX C++ compiler issues, I guess.

Try running the notebook. Install packages until it works :)
