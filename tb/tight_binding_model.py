# -*- coding: utf-8 -*-
""" 
Tight binding calculations for *d Fermi surface of LSCO

follows the caluclations presented in *Three-Dimensional Fermi Surface of Overdoped 
La-base Cuprates

DOI:  https://doi.org/10.1103/PhysRevLett.121.077004



TODO:
    * kx,ky,kz input variables are neglected if one of those is None in __init__(). 
    change this implementation to a more accurate bahavoir
    * implement test which check if prm kwargs match to kwargs of tb_func in __init__()
    * include functionality to plot multiple dos-datasets in the same figure/axes


"""
__author__ = "kha"
__version__ = "0.0.1"



import time


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import cmocean
from mayavi import mlab


print('################ tight_binding_model loaded ############')

# =====================================
# Plot settings
# =====================================
AX_DCT = {
    'xlabel':   r'$ k_x\ [\pi/a] $',
    'ylabel':   r'$ k_y\ [\pi/b] $',
    'zlabel':   r'$ E(k_x, k_y)\ [eV] $',
}

AX_DCT_DOS = {
    'xlabel':   r'$ E\ [eV] $',
    'ylabel':   r'$ DOS $',
}

LN_DCT_DOS = {   # matplotlib.lines.Line2D
#    'color':        'r',
    'linewidth':    1.5,
}

SURF_DCT = {
	'colormap':	'viridis'

}


# ==============================================================================
# Tight Binding Error
# ==============================================================================
class TightBindingError(Exception):
    """ """
    pass


# ==============================================================================
# Tight Binding class
# ==============================================================================
class DensityOfStates(object):
	""" """

	def __init__(self, E_lst, dos_val):
		""" """
		super().__init__()
		self.E = E_lst
		self.val = dos_val


class TightBindingBase(object):
    """ """

    def __init__(self, prm, kspace, tb_func=None, verbose=False):
        """contain functions to initialize kspace and energy dataset

        TODO: implement test which check if prm kwargs match to kwargs of tb_func

         """
        super().__init__()

        self.type = 'tb'
        self.verbose = verbose
        self.has_tb_func = False
        self.E_calculated = False

        self._init_kspace(prm, kspace)
        self.prm = prm

        if tb_func != None:
            self.set_tb_model(tb_func)

    def _init_kspace(self, prm, kspace):
        """initialize kspace parameter"""
        self.kspace = kspace
        self.dim = len(self.kspace)
        self.kspace = np.meshgrid(*self.kspace)


    def _wrapp_tb_func(self, tb_func, **prm):
    	"""return ŵrapped *tb_func* where *kwargs* are set by *prm* """
    	def tb_wrapper(*args):
    	    return tb_func(*args, **prm)
    	return tb_wrapper


    def set_tb_model(self, tb_func):
        """set *tb_model* and call *calc_tb* if *E_calculated* flag is *False* """
#        self.tb_model = tb_func

        self.tb_model = self._wrapp_tb_func(tb_func, **self.prm)
        self.has_tb_func = True
        if self.E_calculated == False:
            self.calc_E(verbose=self.verbose)

    # calc energy
    def _calc_E(self):
        """private method to calc E by calling the tight-binding function"""
        return self.tb_model(*self.kspace)


    def calc_E(self, verbose=False):
        """calculates tight binding Energy with self.tb_model"""

        if self.has_tb_func == False:
            raise TightBindingError(
                'No tb_func defined yet. ' +
                'Use set_tb_func(..) to set it first'
            )

        if verbose: 
            print('calculate tight binding dset ...')
            print('kspace dimension: ', self.kspace[0].shape)

        self.E = self._calc_E()
        self.E_calculated = True
        if verbose: print('tight binding dset calculated.')



class TightBindingDOSCalc(TightBindingBase):
    """contains functions necessary to calculate density of states"""

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)

        self.dos_calculated = False


    def calculate_dos(self, E_lst):
    	""" """

    	if self.E_calculated == False:
    		raise TightBindingError(
    			'self.E not calculated yet. ' +
    			'Use self.calc_E() to calculate it first'
    		)

    	dos_val = TightBindingDOSCalc.calc_dos(self.E, E_lst, verbose=False)
    	self.dos = DensityOfStates(E_lst, dos_val)
    	self.dos_calculated = True


    @staticmethod
    def calc_dos(E_dset, E_lst, verbose=False):
        """calculates normalized DOS by using ``np.histogram`` """
        E_step = E_lst[1] - E_lst[0]
        dset_ = E_dset.reshape(1, E_dset.size)
        E_bin = np.concatenate((np.array([E_lst[0]]),
                                np.array(E_lst)+E_step/2.), axis=0)
        dos, b = np.histogram(dset_, bins=E_bin)
        return dos/np.sum(dos)

    @staticmethod
    def calc_dos_kz_average(E_dset, E_lst, verbose=False):
        """calc DOS by averaging over kz and summing over 2D iso-energy surface"""
        if len(E_dset.shape) != 3:
            raise TightBindingError("E_dset dimension need to be 3!")
        
        dos_lst = []       # fill with DOS for every kz value
        for idx in range(E_dset.shape[2]):
            if verbose: print('    ', end='')
            dos = TightBindingBS.calc_dos(E_dset[:,:,idx], E_lst, verbose=verbose)
            dos_lst.append(dos)
        if verbose: print('idx: {:d}'.format(idx))
        return np.mean(dos_lst, axis=0)



class TightBindingDOSPlot(TightBindingDOSCalc):
    """ """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def _plot_dos(self):
    	""" """
    	if self.dos_calculated == False:
    		raise TightBindingError(
    			'self.dos not calculated yet. ' +
    			'Use self.calculate_dos() to calculate it first'
    		)
    	fig, ax, ln = TightBindingDOSPlot.plot_dos(self.dos.E, self.dos.val)


    @staticmethod
    def plot_dos(E_lst, dos, num=1, figsize=(8,6), ax_dct=None, line_dct=None):
        """ """
        if ax_dct == None:
            ax_dct = AX_DCT_DOS

        if line_dct == None:
            line_dct = LN_DCT_DOS

        fig = plt.figure(num=num, figsize=figsize)
        ax = fig.add_axes([0.1, 0.1, 0.85, 0.85], **ax_dct)
        ln = ax.plot(E_lst, dos, **line_dct)
        ax.grid()
        return fig, ax, ln


class TightBindingEnergyPlot(TightBindingBase):
    """ """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def plot_BS(kspace, E_dset, num=2, figsize=(8,6), ax_dct=None, surf_dct=None, 
    				verbose=False):
    	""" """

    	if surf_dct == None:
    		surf_dct = SURF_DCT

    	s = mlab.surf(kspace[0].T, kspace[1].T, E_dset, **surf_dct)
    	mlab.show()

    	return


class TightBindingModel(TightBindingDOSPlot, TightBindingEnergyPlot):
    """represents a tight Binding model"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)






