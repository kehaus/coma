# -*- coding: utf-8 -*-
""" 
Simple usage example of tight binding class


"""
__author__ = "kha"
__version__ = "0.0.1"



import sys
import os
import time
import numpy as np


#import fermi_3d

import tight_binding_model

#from tight_binding_model import TightBindingModel
from tb_functions import e_simple_2d

#print('fermi_3d ', fermi_3d)

# if 'fermi_3d' in sys.modules:
#  	import importlib
#  	importlib.reload(sys.modules['fermi_3d'])
#  	print('fermi_3d.py reloaded')
# else:
#  	import fermi_3d



# from fermi_3d import TightBindingModel


TightBindingModel = tight_binding_model.TightBindingModel


# ==============================================================================
#  kspace settings
# ==============================================================================
kx = np.linspace(-0.5, 0.5, 401)*np.pi
ky = np.linspace(-0.5, 0.5, 401)*np.pi
#kz = np.linspace(-1.5, 1.0, 81)*np.pi
kspace = [kx, ky]


# ==============================================================================
#  tb parameter
# ==============================================================================
simple_prm = { 	# tight-binding parameter
    'a': 3.76,
    't': 1,
    'e0': 0
}


# ==============================================================================
#  dos parameter
# ==============================================================================
E_min = -4; E_max = 4
E_lst = np.linspace(E_min, E_max, 101)


# ==============================================================================
#  tb object
# ==============================================================================
tb = TightBindingModel(simple_prm, kspace, tb_func=e_simple_2d, verbose=True)
tb.calculate_dos(E_lst)
#tb._plot_dos()

tb.plot_BS(tb.kspace, tb.E)


# from mayavi import mlab

# mlab.mesh(*tb.kspace, tb.E)
