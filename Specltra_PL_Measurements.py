

import numpy as np
import matplotlib.pylab as plt
import os
import scipy.io as sio


class Spectral_PL():
    folder_cal = './CalibratedSpectrums'

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

    def caculate_intensitycalibration(self, fname, defined_SPE):
        """
        Provide a measurements of a known spectrum,
        and calibrates the final intensity.

        the caculated self.correction  can then be multipled against
        a measured spectrum to correct it
        """
        correction = self.load_spectrum(fname)

        def_spec = self.defined_spectrum()

        def_spec = np.interp(
            correction['wavelength'],
            defined_SPE['wavelength'], defined_SPE['spectrum'])
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
            data
        else:
            self.data = data

    def plot_data(self, ax=None,  Raw=False):
        if ax is None:
            _, ax = plt.subplots(1)

        # print self.data.dtype.names
        if Raw:
            ax.plot(self.data['wavelength'], self.data['spectrum'])
        else:
            ax.plot(self.data['wavelength'], self.data['raw_data'])

        ax.set_xlabel('Wavelength (nm)')
        ax.set_ylabel('PL (a.u.)')
        return ax


class Spectral_PL_BWTEC(Spectral_PL):

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


if __name__ == "__main__":

    folder = r'D:\Drive\Temp\Spectral Measurements'
    fname = r'Multi_UNSW_Reference.csv'

    a = Spectral_PL_BWTEC()
    a.defined_spectrum(True)
    # a.load_spectrum(os.path.join(folder, fname), True)
    # ax = a.plot_data()
    # a.plot_data(ax=ax, Raw=True)
    # plt.show()




    plt.show()
