import numpy as np
import matplotlib.pyplot as plt
from .histogram import Histogram
from iminuit import Minuit
from iminuit.cost import LeastSquares
from ..utils.unit import unit, unit_uncertainty
from .histogram import bisection
from scipy.interpolate import PchipInterpolator
from tqdm import tqdm


def decay(x, tau):
    return tau * (1 - np.exp(-x / tau))

def signal(t, dt, risetime, decaytime, lightyield):
    return (np.exp(-(t - dt)/decaytime) - np.exp(-(t - dt)/risetime)) / (decaytime - risetime) * lightyield

def model(x, dt, risetime, decaytime, lightyield):
    ctr = np.exp(
        - (lightyield / (decaytime - risetime)) * (decay(np.abs(x - dt), decaytime) - decay(np.abs(x - dt), risetime)))
    area = np.trapz(ctr, x)

    return ctr / area


class CTR(Histogram):
    def __init__(self, sample, bin_size, confidence_level=0.95, offset=True, bin_count=None):
        super().__init__(sample, bin_size, confidence_level, bin_count)
        self.sample_size = len(self.sample)

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

    def fit(self, risetime, decaytime, lightyield):
        min_fval = None
        m_min = None

        for _ in tqdm(range(1000)):
            lsq = LeastSquares(self.x, self.y, 1E7, model)
            m = Minuit(lsq,
                       dt= np.random.normal(np.mean(self.sample), np.std(self.sample)),
                       risetime=risetime,
                       decaytime=decaytime,
                       lightyield=lightyield * np.random.uniform(0,1))


            m.fixed['risetime'] = True
            m.fixed['decaytime'] = True
            m.limits['risetime'] = (0, risetime)
            m.limits['decaytime'] = (0, decaytime)
            m.migrad()
            m.hesse()

            if min_fval is None or m.fval < min_fval:
                min_fval = m.fval
                m_min = m

        m = m_min
        m.minos()

        self.dt = m.values['dt']
        self.risetime = m.values['risetime']
        self.decaytime = m.values['decaytime']
        self.lightyield = m.values['lightyield']
        self.dt_error = m.errors['dt']
        self.risetime_error = m.errors['risetime']
        self.decaytime_error = m.errors['decaytime']
        self.lightyield_error = m.errors['lightyield']

        lsq = LeastSquares(self.x, self.y, self.e, model)
        m = Minuit(lsq, dt=self.dt, risetime=self.risetime, decaytime=self.decaytime, lightyield=self.lightyield)
        m.hesse()

        self.chi2 = m.fval / (len(self.x) - len(m.values))
        self.ndof = len(self.x) - len(m.values)

        self.y_fit = model(self.x, self.dt, self.risetime, self.decaytime, self.lightyield)

    def fit_plot(self):
        plt.rcParams["font.family"] = "monospace"
        # plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Liberation Sans"]

        fit_info = [
            f'$\chi^2$\t      ${self.chi2:.3f}$\n',
            f'$\Delta t$ \t\t{unit_uncertainty(self.dt, self.dt_error, "s")}',
            f'Rise Time \t{unit_uncertainty(self.risetime, self.risetime_error, "s")}',
            f'Decay Time \t{unit_uncertainty(self.decaytime, self.decaytime_error, "s")}',
            f'Light Yield \t{unit_uncertainty(self.lightyield, self.lightyield_error, "ph")}\n',
            f'FWHM \t\t{unit(self.fit_FWHM(1E-12), "s")}',
            f'Sample Size \t{int(self.sample_size)} $[Events]$\n',
        ]

        plt.errorbar(self.x, self.y, yerr=self.e, fmt='o', label='Data', zorder=1, color='black')
        x = np.linspace(np.amin(self.x), np.amax(self.x), 1000)
        plt.plot(x, model(x, self.dt, self.risetime, self.decaytime, self.lightyield), label='Fit', zorder=2, color='black', linestyle='--',
                 linewidth=2)


        plt.legend(title='\n'.join(fit_info), bbox_to_anchor=(1.11, 1.14), loc='upper right', borderaxespad=0.)
        plt.xlabel('Time Difference [s]')
        plt.ylabel('Probability Density')
        plt.grid(True)





