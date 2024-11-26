# functions for the element test programme
# especially for the material models

import numpy, math
from functions_elementTest import *

   
def matModel(stress,strain,stateVar,model,modelParam):
    """
    Calculates the stiffness matrix for a given material model
    This function only deals with elastic models

    Parameters
    ----------
        stress : 2x1 array
            stress in volumetric and deviatoric invariants (p, q)

        strain : 2x1 array
            strain in volumetric and deviatoric invariants (deps_p, deps_q)

        stateVar : 2x1 array
            actual state variables, stateVar[0] is usually void ratio

        model : string
            type of the material model
            'linelast' for a linear elastic model,
            'hyperb' for a strain dependent hyperbolic model

        modelParam : dictionary
            parameters for the material models
            such as: E, nu, G0, phi, psi, ...

    Returns
    -------
        M : 2x2 array of floats
            stiffness matrix
    """

    p, q = stress
    eps_p, eps_q = strain
    # linear elasticity
    if model=='linelast':
        E  = modelParam["E"]
        nu = modelParam["nu"]
        K = E/3/(1-2*nu)  # bulk modulus
        G = E/2/(1+nu)    # shear modulus
    # non-linear elasticity (strain-dependent hyperbolic stiffness)
    elif model=='hyperb':
        G0   = modelParam["G0"]
        nu   = modelParam["nu"]
        qmax = modelParam["qmax"]
        bhyp = 1/G0
        ahyp = 1/qmax
        G = 1/(bhyp+ahyp*eps_q)  #tangent stiffness
        E = 2*G*(1+nu)
        K = E/3/(1-2*nu)
    elif model=='mcc':
        kappa = modelParam["kappa"]
        nu    = modelParam["nu"]
        K = (1 + stateVar[0])*p/kappa
        G = 3*(1-2*nu)/(2*(1+nu))*K
    elif model=='ohde':
        alpha = modelParam["alpha"]
        nu = modelParam["nu"]
        E = ohde_Es(stress,3636.364,100,alpha)*(1+nu)*(1-2*nu)/(1-nu)
        K = E/3/(1-2*nu)  # bulk modulus
        G = E/2/(1+nu)    # shear modulus
    else:
        return
    M_pp, M_qq = K, 3*G
    M_pq, M_qp = 0, 0
    M = numpy.array([[M_pp,M_pq],[M_qp,M_qq]])
    return M

# define odemetric modulus
def ohde_Es(stress,Es0,sigma0,alpha):
    p,q = stress
    Es = Es0 * math.pow(pq2sigma(p,q)[0]/sigma0, alpha)
    return Es
