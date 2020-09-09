import numpy as np
import scipy
import scipy.signal
import scipy.optimize
import scipy.special
from scipy.special import factorial


class Morlet:
    def __init__(self, c=None, w0=None):
        """ Describe c!
        """
        if (c is None) and (w0 is None):
            print("No resolution factor given. Setting c=0.0125")
            self.c = 0.0125
            # Omega0 as defined in Torrence and Compo
            self.w0 = 1/np.sqrt(2*c)
        elif (c is not None) and (w0 is None):
            self.c = c
            self.w0 = 1/np.sqrt(2*c)
        elif (c is None) and (w0 is not None):
            self.w0 = w0
            self.c = 1/(2*w0**2)
        else:
            sys.exit("Either c or w0 needs to be defined, but not both!")

    def __call__(self, *args, **kwargs):
        return self.construct_wavelet(*args, **kwargs)

    def construct_wavelet(self, t, tau=1.0, s=1.0, use_scale=False, time=True):
        """
        Docstrings!
        """
        if time:
            return self.construct_wavelet_time(t, tau, s, use_scale)
        else:
            return self.construct_wavelet_freq(t, tau, s, use_scale)

    def weights(self, t, s=1.0, tau=1.0, use_scale=False):
        # If use_scale is set then s is taken to be the scale rather than dilation
        if use_scale:
            eta = 2*np.pi*(t - tau)/s
        else:
            eta = s * (t - tau)
        return np.exp(-self.c*eta**2)

    def compute_fourier_wavelength(self, s):
        """
        Compute the Fourier wavelength of Morlet wavelet
        Table 1 of Torrence and Compo (1998)
        """
        return 4 * np.pi * s / (self.w0 + (2 + self.w0 ** 2) ** .5)

    def scale_from_period(self, period):
        """
        Returns the scale from a given Fourier period.

        #from aarens wavelet package
        """
        coeff = np.sqrt(self.w0 * self.w0 + 2)
        return (period * (coeff + self.w0)) / (4. * np.pi)

    def construct_wavelet_time(self, t, s=1.0, tau=1.0, use_scale=False):

        # If use_scale is set then s is taken to be the scale rather than dilation
        if use_scale:
            eta = 2*np.pi*(t - tau)/s
        else:
            eta = s * (t - tau)

        output = np.exp(1j*eta) * np.exp(-self.c * eta**2)
        
        return output

    def construct_wavelet_freq(self, omega, s=1.0, use_scale=False):
        """
        Need to add docstrings!
        """
        if use_scale:
            x = omega * s
        else:
            # TODO: Need to check that conversion from s -> omega is correct
            # and that 2pi factor is needed.
            x = omega * (2*np.pi)/s
        # Heaviside mock
        Hw = np.zeros_like(omega)
        Hw[w > 0] = 1
        # Need to check normalisation is consistent with our formulation
        return Hw * np.exp((-(x - self.w0) ** 2) / 2)