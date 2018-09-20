# -*- coding: utf-8 -*-
""" 
Library of common tight binding functions


"""
__author__ = "kha"
__version__ = "0.0.1"



import numpy as np



def e_simple(kx ,ky, kz, t=1, a=1, e0=0):
    """3d, nearest neighbour hopping"""
    res = e0 + 2*t*(np.cos(kx*a) + np.cos(ky*a) + np.cos(kz*a))
    return res

def e_simple_2d(kx, ky, t=1, a=1, e0=0):
    """2d, nearest neighbout hopping"""
    return e_simple(kx, ky, kz=np.pi/(2*a), a=a, e0=e0)



