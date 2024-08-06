import numpy as np
import matplotlib.pyplot as plt
from .histogram import Histogram
from iminuit import Minuit
from iminuit.cost import LeastSquares
from ..utils.unit import unit, unit_uncertainty
from .histogram import bisection
from scipy.interpolate import PchipInterpolator
from tqdm import tqdm
from numba import njit
import concurrent.futures

def decay(x, tau):
    return tau * (1 - np.exp(-x / tau))

@njit
def signal(t, risetime, decaytime, lightyield):
    return (np.exp(-t/decaytime) - np.exp(-t/risetime)) / (decaytime - risetime) * lightyield

@njit
def signal_int(t, risetime, decaytime, lightyield):
    x = np.arange(0, t, 2E-12)
    y = 1 - np.trapz(signal(x, risetime, decaytime, lightyield), x)
    return np.exp(y)

@njit
def sCTR(t, risetime, decaytime, lightyield):
    return signal(t, risetime, decaytime, lightyield) * signal_int(t, risetime, decaytime, lightyield)

def model(x, dt, risetime, decaytime, lightyield):
    t = np.linspace(0, np.amax(x) - np.amin(x), 100)
    sctr = np.array([sCTR(i, risetime, decaytime, lightyield) for i in t])
    ctr = np.convolve(sctr, np.flip(sctr), "full")
    ct = np.linspace(-np.amax(t), np.amax(t), len(ctr))
    area = np.trapz(ctr, ct)
    ctr = PchipInterpolator(ct, ctr / area)(x - dt)
    return ctr

# def model(x, dt, risetime, decaytime, lightyield):
#
#     diff = risetime / decaytime
#
#     risetime *= diff
#     decaytime /= diff
#
#     ctr = np.exp(
#         - (lightyield / (decaytime - risetime)) * (decay(np.abs(x - dt), decaytime) - decay(np.abs(x - dt), risetime)))
#     area = np.trapz(ctr, x)
#
#     return ctr / area


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

    def fit_worker(self):
        lsq = LeastSquares(self.x, self.y, 0.1 * np.amax(self.y), model)
        m = Minuit(lsq,
                   dt=self.x[np.argmax(self.y)] * np.random.uniform(0.9, 1.1),
                   risetime=self.risetime * np.random.uniform(0.99, 1.01),
                   decaytime=self.decaytime * np.random.uniform(0.99, 1.01),
                   lightyield=self.lightyield * np.random.uniform(0.5, 1.5))

        # m.fixed['dt'] = True
        m.fixed['risetime'] = True
        m.fixed['decaytime'] = True
        # m.limits['risetime'] = (0, risetime * 1.1)
        # m.limits['decaytime'] = (decaytime * 0.9 , decaytime * 1.1)
        m.limits['lightyield'] = (0, 30000)
        m.migrad()
        m.hesse()

        return m

    def fit(self, risetime, decaytime, lightyield):
        self.risetime = risetime
        self.decaytime = decaytime
        self.lightyield = lightyield

        num_tasks = 1000

        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = []
            futures = [executor.submit(self.fit_worker) for _ in range(num_tasks)]

            for future in tqdm(concurrent.futures.as_completed(futures), total=num_tasks):
                results.append(future.result())

        chi2 = [m.fval / (len(self.x) - len(m.values)) for m in results]

        m = results[np.argmin(chi2)]

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

        m.fixed['dt'] = True
        m.fixed['risetime'] = True
        m.fixed['decaytime'] = True
        m.fixed['lightyield'] = True
        
        m.migrad()
        m.hesse()

        self.dt = m.values['dt']
        self.risetime = m.values['risetime']
        self.decaytime = m.values['decaytime']
        self.lightyield = m.values['lightyield']
        self.dt_error = m.errors['dt']
        self.risetime_error = m.errors['risetime']
        self.decaytime_error = m.errors['decaytime']
        self.lightyield_error = m.errors['lightyield']
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
            f'Sample Size \t{int(self.sample_size)} $[Events]$',
            f"Bin Width \t{unit(self.bin_size, 's')}\n"
        ]

        plt.errorbar(self.x, self.y, yerr=self.e, fmt='o', label='Data', zorder=1, color='black')
        x = np.linspace(np.amin(self.x), np.amax(self.x), 1000)
        plt.plot(x, model(x, self.dt, self.risetime, self.decaytime, self.lightyield), label='Fit', zorder=2, color='black', linestyle='--',
                 linewidth=2)


        plt.legend(title='\n'.join(fit_info), bbox_to_anchor=(1.11, 1.14), loc='upper right', borderaxespad=0.)
        plt.xlabel('Time Difference [s]')
        plt.ylabel('Probability Density')
        plt.grid(True)





