

import numpy as np
import matplotlib.pylab as plt
import os
import scipy.io as sio


class Spectral_PL():

    folder_cal = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'CalibratedSpectrums')

    def CalibratedSpectrum(self, data):
        """
        attempts to calibrate the data
        if it fails it prints a warning
        """
        try:
            for names in ['raw_data', 'spectrum']:
                data[names] *= self.correction
        except:
            print 'Correction not installed'

        return data

    def defined_spectrum(self, Plot=False):
        """
        Gets the defined spectums from a file
        can pass Plot as a flag to plot the spectrum
        """

        def_spec = np.genfromtxt(
            os.path.join(self.folder_cal, self.calibration_source),
            names=['wavelength', 'spectrum'],
            delimiter=',')
        if Plot:
            plt.plot(def_spec['wavelength'], def_spec['spectrum'])
            plt.show

        return def_spec

    def caculate_intensitycalibration(self, fname):
        """
        Provide a measurements of a known spectrum,
        and calibrates the final intensity.

        the caculated self.correction  can then be multipled against
        a measured spectrum to correct it
        """
        correction = self.load_spectrum(fname, Return=True)
        print correction.dtype.names

        def_spec = self.defined_spectrum()

        def_spec = np.interp(
            correction['wavelength'],
            def_spec['wavelength'], def_spec['spectrum'])
        self.correction = def_spec / correction['spectrum']

    def load_spectrum(self, fname, correct=False, Return=False):
        """
        load data file with colums for:
        pixel
        wavelength
        raw-data
        spectrum
        """
        # print kwargs
        data = self._load_spectrum(fname)

        if correct:
            data = self.CalibratedSpectrum(data)

        if Return:
            return data
        else:
            self.data = data
            pass

    def plot_data(self, ax=None,  Raw=False, norm=False):
        if ax is None:
            _, ax = plt.subplots(1)

        if Raw:
            data2plot = self.data['raw_data']
        else:
            data2plot = self.data['spectrum']

        if norm:
            print np.nanmax(data2plot)
            data2plot /= np.nanmax(data2plot)

        ax.plot(self.data['wavelength'], data2plot, '.-')

        ax.set_xlabel('Wavelength (nm)')
        ax.set_ylabel('PL (a.u.)')
        return ax

    def bin_data(self, data, binAmount):
        """ A function to perform binning on the measurement"""
        if len(data.dtype.names) != 1:
            data2 = np.copy(data)[::binAmount]

        for i in data.dtype.names:
            for j in range(data.shape[0] // binAmount):

                data2[i][j] = np.mean(
                    data[i][j * binAmount:(j + 1) * binAmount], axis=0)

        return data2


class Spectral_PL_Sol17_BWTEC(Spectral_PL):

    """ This class if for the Sol17"""

    def __init__(self):
        self.ymax = 60000
        self.calibration_source = r'Sol17__SLS201+M28L01-400umfibre+mini-isphere-w-4mm-aperture.csv'
        pass

    def _load_spectrum(self, fname):
        # print fname
        data = np.genfromtxt(
            fname, skip_header=79,
            usecols=(0, 1, 6, 7),
            names=['pixel', 'wavelength', 'raw_data', 'spectrum'],
            # names = True,
            delimiter=',',
            comments='!')

        return data


class Spectral_PL_GlacierX_BWTEC(Spectral_PL):

    """ This class if for the GlacierX from BWTEC"""

    def __init__(self):
        self.ymax = 60000
        self.calibration_source = r'GlacierX__SLS201+M28L01-400umfibre+mini-isphere-w-4mm-aperture.csv'
        pass

    def _load_spectrum(self, fname):
        """
        loads the particulars of the glaxcierx
        Havn't checked this works
        """
        # print fname
        data = np.genfromtxt(
            fname, skip_header=79,
            usecols=(0, 1, 6, 7),
            names=['pixel', 'wavelength', 'raw_data', 'spectrum'],
            # names = True,
            delimiter=',',
            comments='!')

        return data


if __name__ == "__main__":

    folder = r'R:\1stGenPhotonics\- Mattias Juhl\Calibration'
    cal = r'Reference_Hal+1mfibre+smallInt_100.csv'
    fname = r'2V_Nostage_875LP+850LP.csv'

    a = Spectral_PL_Sol17_BWTEC()

    a.caculate_intensitycalibration(os.path.join(folder, cal))
    Corrected_data = a.load_spectrum(os.path.join(folder, fname), correct=True)
    ax = a.plot_data(norm=True)

    data = a.load_spectrum(os.path.join(folder, fname), correct=False)
    a.plot_data(ax=ax, norm=True)

    ax.semilogy()

    plt.show()
