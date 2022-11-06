# -*- coding: utf-8 -*-
""" 
Simple usage example of tight binding class with 3d next nearst neighbor hopping


"""
__author__ = "kha"
__version__ = "0.0.1"



import sys
import os
import time
import numpy as np


#import fermi_3d

import tight_binding_model


from tb_functions import e_simple

TightBindingModel = tight_binding_model.TightBindingModel


# ==============================================================================
#  kspace settings
# ==============================================================================
kx = np.linspace(-0.3, 0.3, 101)*np.pi
ky = np.linspace(-0.3, 0.3, 101)*np.pi
kz = np.linspace(-0.3, 0.3, 101)*np.pi
kspace = [kx, ky, kz]


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
tb = TightBindingModel(simple_prm, kspace, tb_func=e_simple, verbose=True)
tb.calculate_dos(E_lst)


tb.plot_iso_surface()

from mayavi import mlab



