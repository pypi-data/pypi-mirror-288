import numpy as np
import matplotlib.pyplot as plt 
from .histogram import Histogram
from iminuit import Minuit
from iminuit.cost import LeastSquares
from ..utils.unit import unit, unit_uncertainty
from .histogram import bisection
from scipy.interpolate import PchipInterpolator
import numpy as np
import scipy.special as sp



def landau_pdf(x, loc, scale):
    """
    Calculate the Landau distribution's PDF at a given point using numerical approximation.

    Parameters:
    - x (float or array-like): The value(s) at which to evaluate the PDF.
    - loc (float): The location parameter (default is 0).
    - scale (float): The scale parameter (default is 1).

    Returns:
    - pdf (float or array-like): The value of the PDF at x.
    """
    # Constants for the numerical approximation
    pi_inv_sqrt = 1 / np.sqrt(np.pi)
    
    # Transform x with location and scale
    z = (x - loc) / scale

    # Calculation using the real part of the complex error function
    # The use of sp.wofz corresponds to Faddeeva function w(z)
    pdf = pi_inv_sqrt * np.exp(-0.5 * (z + np.exp(-z))) * sp.wofz(z * 1j).real
    
    area = np.trapz(pdf, x)
    
    return pdf / area


def model(x, loc, scale):
    return landau_pdf(x, loc, scale)
    


class Landau(Histogram):
    def __init__(self, sample, bin_size, confidence_level=0.95, bin_count=None):
        super().__init__(sample, bin_size, confidence_level, bin_count)
        self.sample_size = len(self.sample)
        
    def fit(self):
        min_fval = None
        m_min = None
        for _ in range(1000):
            lsq = LeastSquares(self.x, self.y, self.e, model)
            m = Minuit(lsq,
                       loc=np.random.normal(np.mean(self.sample), np.std(self.sample)),
                       scale=np.random.normal(np.std(self.sample)))
            
            m.migrad()
            m.hesse()

            if min_fval is None or m.fval < min_fval:
                min_fval = m.fval
                m_min = m
        m = m_min
        
        self.loc = m.values['loc']
        self.scale = m.values['scale']
        self.loc_error = m.errors['loc']
        self.scale_error = m.errors['scale']
        self.chi2 = m.fval / (len(self.x) - len(m.values))
        self.ndof = len(self.x) - len(m.values)

        self.y_fit = model(self.x, self.loc, self.scale)
        
    def fit_plot(self, units=""):
        plt.rcParams["font.family"] = "monospace"
        fit_info = [
            f'$\chi^2$\t      ${self.chi2:.3f}$\n',
            f'Location \t{unit_uncertainty(self.loc, self.loc_error, units)}',
            f'Scale \t\t{unit_uncertainty(self.scale, self.scale_error, units)}\n',
            f'FWHM \t\t{unit(self.fit_FWHM(1E-12), units)}',
            f'Sample Size \t{int(self.sample_size)} $[Events]$\n',
        ]
        
        plt.errorbar(self.x, self.y, yerr=self.e, fmt='o', label='Data', zorder=1, color='black')
        x = np.linspace(np.amin(self.x), np.amax(self.x), 1000)
        plt.plot(x, model(x, self.loc, self.scale), label='Fit', zorder=2, color='black', linestyle='--', linewidth=2)
        
        plt.legend(title='\n'.join(fit_info))
        plt.grid(True)


    def fit_FWHM(self, resolution):
        y = PchipInterpolator(self.x, self.y_fit)

        max_value = np.amax(self.y)
        half_max = max_value / 2

        peak_x = self.x[np.argmax(self.y)]

        min_x = np.amin(self.x)
        max_x = np.amax(self.x)

        left = bisection(self.x, y, half_max, resolution, min_x, peak_x)
        right = bisection(self.x, y, half_max, resolution, peak_x, max_x)

        return np.abs(right - left)
   

