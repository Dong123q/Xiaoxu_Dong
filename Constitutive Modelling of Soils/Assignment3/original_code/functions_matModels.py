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
        alpha  = modelParam["alpha"]
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

# yield surface and plastic potential
def surfaces(stress,dstress,stateVar,model_pl,modelParam):
    """
    Calculates the yield function, the gradients of yield surface and
    plastic potential and the loading direction

    Parameters
    ----------
        stress, dstress : 2x1 array
            stress and stress increment in volumetric and
            deviatoric invariants (p, q)

        stateVar : 2x1 array
            actual state variables, stateVar[0] is usually void ratio

        model_pl : string
            name of the plastic model

        modelParam : dictionary
            parameters for the material models
            such as: E, nu, G0, phi, psi, ...

    Returns
    -------
        f : float
            value of the yield function

        df_dsig : float
            gradient of the yield surface in volumetric, deviatoric notation

        dg_dsig : float
            gradient of the plastic potential in volumetric, deviatoric
            notation

        H : 2x1 array
            hardening modulus in volumetric and
            deviatoric invariants (p, q)

        Hp : float
            hardening function

        loading : float
            direction of the stress increment with respect to the yield
            function
    """

    p, q = stress
    dp, dq = dstress

    if model_pl=="mc":
        # converting friction and dilatancy angles from [°] to [rad]
        phi = math.radians(modelParam["phi"])
        psi = math.radians(modelParam["psi"])

        sigma_1, sigma_2 = pq2sigma(p,q)
        sigma_max = max(sigma_1, sigma_2)
        sigma_min = min(sigma_1, sigma_2)

        # Mohr-Coulomb failure criterion
        f = (sigma_max - sigma_min) - (sigma_max + sigma_min) * math.sin(phi)

        # gradient of yield surface
        df_dp = -2 * math.sin(phi)
        df_dq = 1 - math.sin(phi) / 3.
        # gradient of plastic potential
        dg_dp = -2 * math.sin(psi)
        dg_dq = 1 -  math.sin(psi) / 3.
        # gradient of the additional state variables
        df_dchi = 0
        dchi_depsp = 0
        dchi_depsq = 0
    
    elif model_pl == "dp":
        # converting friction and dilatancy angles from [°] to [rad]
        phi = math.radians(modelParam["phi"])
        psi = math.radians(modelParam["psi"])
        p = stress[0]
        q = stress[1]

        # Drucker-Prager failure criterion
        f = q - (6 * math.sin(phi) / (3 - math.sin(phi))) * p

        # gradient of yield surface
        df_dp = -(6 * math.sin(phi) / (3 - math.sin(phi)))
        df_dq = 1
        # gradient of plastic potential
        dg_dp = -(6 * math.sin(psi) / (3 - math.sin(psi)))
        dg_dq = 1
        # gradient of the additional state variables
        df_dchi = 0
        dchi_depsp = 0
        dchi_depsq = 0
        
    elif model_pl=='edp':
        # model parameters
        etaP = modelParam["etaP"]
        a    = modelParam["a"]
        # state variable
        etaY = stateVar[1]

        f = q - etaY*p
        # gradient of yield surface
        df_dp = - etaY
        df_dq = 1
        # gradient of plastic potential
        dg_dp = - etaY
        dg_dq = 1
        # gradient of the additional state variables
        df_dchi = -p
        dchi_depsp = 0
        dchi_depsq = ((etaP - etaY)**2) / (a * etaP)

    elif model_pl=='mcc':
        # model parameters
        M      = modelParam["M"]
        Lambda = modelParam["Lambda"]
        kappa  = modelParam["kappa"]
        # state variables
        epor = stateVar[0]
        pC   = stateVar[1]

        f = (q/M)**2 + p*(p - pC)
        # gradient of yield surface
        df_dp = 2 * p - pC
        df_dq = 2 * q / (M**2)
        # gradient of plastic potential (associated)
        dg_dp = df_dp
        dg_dq = df_dq
        # gradient of the additional state variables
        df_dchi = -p
        dchi_depsp = (1 + epor)*pC / (Lambda - kappa)
        dchi_depsq = 0

    df_dsig = numpy.array([df_dp,df_dq])
    dg_dsig = numpy.array([dg_dp,dg_dq])
    # hardening modulus
    H = numpy.array([dchi_depsp,dchi_depsq])
    # hardening function
    Hp = df_dchi * numpy.dot(H,dg_dsig)
    # loading direction
    loading = numpy.dot(df_dsig,dstress)

    return f, df_dsig, dg_dsig, H, Hp, loading

# update the state variable controlling the plastic part
def stateVarRate(stress,dstress,dstrainP,H,model_pl,modelParam):
    """
    Calculates stress and strain rates based on the testType and the
    material model

    Parameters
    ----------
        stress, dstress : 2x1 array
            stress and stress increment in volumetric and
            deviatoric invariants (p, q)

        dstrainP : 2x1 array
            plastic strain increment in volumetric and
            deviatoric invariants (depsP_p, depsP_q)

        H : 2x1 array
            hardening modulus in volumetric and
            deviatoric invariants (p, q)

        model_pl : string
            name for the plastic model

        modelParam : dictionary
            parameters for the material models
            such as: E, nu, G0, phi, psi, ...

    Returns
    -------
        dStateVar : 2x1 array
            increment of the additional state variables.
            usually only the second element is updated via this array
    """
    # important for the next model
    p, q = stress
    dp, dq = dstress
    dStateVar = numpy.zeros(2)
    if model_pl=='edp':
        dEtaY = H[1] * dstrainP[1]
        dStateVar[1] = dEtaY

    elif model_pl=='mcc':
        # dpC = nu/(lambda-kappa)*pC*dstrainP_p
        dStateVar[1] = H[0]*dstrainP[0]

    return dStateVar

# stress, strain and void ratio rates according to type of loading
def rates(stress,strain,stateVar,testType,model,modelParam):
    """
    Calculates stress and strain rates based on the testType and the
    material model

    Parameters
    ----------
        stress : 2x1 array
            stress in volumetric and deviatoric invariants (p, q)

        strain : 2x1 array
            strain in volumetric and deviatoric invariants (deps_p, deps_q)

        stateVar : 2x1 array
            actual state variables, stateVar[0] is usually void ratio

        testType : string
            type of the element test, the options are
            'oed' for oedometric compression,
            'txd' for drained triaxial compression,
            'txu' for undrained triaxial compression

        modelParam : dictionary
            name for the elastic and plastic models, i.e.
            "model_el" and "model_pl"

        modelParam : dictionary
            parameters for the material models
            such as: E, nu, G0, phi, psi, ...

    Returns
    -------
        dstress : 2x1 array
            stress increment in volumetric and deviatoric invariants
            order: dp, dq

        dstrain : 2x1 array
            strain increment in volumetric and deviatoric invariants
            order: deps_p, deps_q

        dStateVar : 2x1 array
            increment of the additional state variables.
            usually only the second element is updated via this array
    """

    # elastic stiffness matrix
    Me = matModel(stress,strain,stateVar,model["model_el"],modelParam)

    # elastic stress and strain rates
    dstress, dstrain = testControl(Me,testType)

    # yield function, gradients and loading direction
    f, n, m, H, Hp, loading = surfaces(stress,dstress,stateVar,model["model_pl"],modelParam)

    tol = 0.001  # tolerance
    # elasto-plastic stress and strain rates for plastic loading steps
    if (f >= 0) and (loading >= -tol):
        # Calculating parts of the plastic stiffness matrix
        # Me m nT Me
        Numerator = numpy.matmul(Me,numpy.outer(m,numpy.dot(n,Me)))
        # nT Me m (- Hp)
        Denominator = numpy.dot(n,numpy.dot(Me,m)) - Hp

        # assembling the plastic stiffness matrix
        Mp = Numerator/Denominator
        # elasto-plastic stiffness matrix
        Mep = Me - Mp
        # elasto-plastic rates
        dstress, dstrain = testControl(Mep,testType)
        # plastic strain rate
        dstrainP = dstrain - numpy.dot(numpy.linalg.inv(Me),dstress)
        # state variable rate
        dStateVar = stateVarRate(stress,dstress,dstrainP,H,model["model_pl"],modelParam)
    else:
        dStateVar = numpy.zeros(2)

    return dstress, dstrain, dStateVar
