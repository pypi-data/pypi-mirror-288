"""
#############################################################################

Copyright (C) 2024, Michele Cappellari
E-mail: michele.cappellari_at_physics.ox.ac.uk

Updated versions of the software are available from my web page
http://purl.org/cappellari/software

If you have found this software useful for your research,
I would appreciate an acknowledgement to the use of the
"JAM modelling package of Cappellari (2008)".

https://ui.adsabs.harvard.edu/abs/2008MNRAS.390...71C

This software is provided as is without any warranty whatsoever.
Permission to use, for non-commercial purposes is granted.
Permission to modify for personal or internal use is granted,
provided this copyright and disclaimer are included unchanged
at the beginning of the file. All other rights are reserved.
In particular, redistribution of the code is not allowed.

#############################################################################

MODIFICATION HISTORY:
    V1.0.0: Written and tested. Michele Cappellari, Oxford, 4 February 2016
    V1.0.1: Written documentation. MC, Oxford, 4 April 2024

"""
import numpy as np
from scipy import special

from jampy.quad1d import quad1d

###################################################################################

def mge_cylindrical_mass(surf, sigma, qobs, rad, distance=1e-5):
    """
    Calculates the mass of a projected axisymmetric MGE enclosed inside a
    cylinder of radius R with symmetry axis along the line-of-sight.

    Parameters
    ----------    
    surf: array_like with shape (n,)
        Peak value of every Gaussian in the `Multi-Gaussian Expansion
        <https://pypi.org/project/mgefit/>`_ (MGE) describing the surface
        brightness in units of ``Lsun/pc^2`` (solar luminosities per
        ``parsec^2``).
    sigma: array_like with shape (n,)
        Dispersion (sigma) in arcsec of the MGE Gaussians.
    qobs: array_like with shape (n,)
        Observed axial ratio (q') of the MGE Gaussians.
    rad: array_like with shape (m,)
        Radii in arcsec at which one wants to compute the enclosed mass.    
    distance: float, optional
        distance in Mpc (default distance = 10pc = 1e-5Mpc)

    Returns
    -------
    mass_r: array_like with shape (m,)
        Projected mass in solar masses enclosed within the m radii.
    """
    rad = np.atleast_1d(rad)
    pc = distance*np.pi/0.648  # Constant factor to convert arcsec --> pc
    lum = 2*np.pi*surf*qobs*(sigma*pc)**2  # total luminosity each Gaussian

    # If the MGE is circular, use analytic eq.(11) of Cappellari et al (2013) 
    # https://ui.adsabs.harvard.edu/abs/2013MNRAS.432.1709C
    if np.all(np.abs(qobs - 1) < 0.01):
        mass_r = (lum*(1 - np.exp(-0.5*(rad[:, None]/sigma)**2))).sum(1)
    else:
        def integrand(rad):
            h = rad[:, None]/(2*qobs*sigma)
            mass_R = 2*lum*h*np.exp(-2*(h*qobs)**2)*special.i0e(h**2*(qobs**2 - 1))/sigma
            return mass_R.sum(1)
        mass_r = [quad1d(integrand, [0, r], singular=True).integ for r in rad]

    return mass_r

###################################################################################
