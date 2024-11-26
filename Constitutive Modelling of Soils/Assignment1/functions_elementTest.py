# functions for the element test programme

import numpy

# transformation of principal stresses into invariants
def sigma2pq(sigma_1,sigma_2):
    p = (sigma_1+2*sigma_2)/3
    q = sigma_1-sigma_2
    stresspq = numpy.array([p,q])
    return stresspq

# transformation of invariants into principal stresses
def pq2sigma(p,q):
    sigma_1 = p+2*q/3
    sigma_2 = p-q/3
    stress12 = numpy.array([sigma_1,sigma_2])
    return stress12

# transformation of principal strains into invariants
def eps2pq(eps_1,eps_2):
    eps_p = eps_1+2*eps_2
    eps_q = 2*(eps_1-eps_2)/3
    strainpq = numpy.array([eps_p,eps_q])
    return strainpq

# transformation of invariants into principal strains
def pq2eps(eps_p,eps_q):
    eps_1 = eps_p/3+eps_q
    eps_2 = eps_p/3-eps_q/2
    strain12 = numpy.array([eps_1,eps_2])
    return strain12

def testControl(M,testType):
    """
    Calculates the strain and strain increments for a given testType

    Parameters
    ----------
        M : 2x2 array of floats
            stiffness matrix

        testtype : string
            type of the element test, the options are
            'oed' for oedometric compression,
            'txd' for drained triaxial compression,
            'txu' for undrained triaxial compression

    Returns
    -------
        dstress : 2x1 array
            stress increment in volumetric and deviatoric invariants
            order: dp, dq

        dstrain : 2x1 array
            strain increment in volumetric and deviatoric invariants
            order: deps_p, deps_q
    """

    M_pp = M[0,0]; M_pq = M[0,1]
    M_qp = M[1,0]; M_qq = M[1,1]

    #strain increment according to test type
    if testType=='oed':
        deps_1 = 1
        deps_2 = 0
        deps_p, deps_q = eps2pq(deps_1,deps_2)
    elif testType=='txd':
        deps_q = 1
        deps_p = (M_qq-3*M_pq)*deps_q/(3*M_pp-M_qp)
    elif testType=='txu':
        deps_1 = 1
        deps_2 = -0.5
        deps_p, deps_q = eps2pq(deps_1,deps_2)
    elif testType == 'iso':
        deps_1 = 1
        deps_2 = 1
        deps_p, deps_q = eps2pq(deps_1,deps_2)
    else:
        return
    dstrain=numpy.array([deps_p,deps_q])
    # stress increment
    dstress=numpy.dot(M,dstrain)
    
    return dstress, dstrain

def integration(stress,strain,dstress,dstrain,stateVar,dStateVar,dt):
    """
    Explicit numerical integration of the state variables

    Parameters
    ----------
        stress, dstress : 2x1 array
            actual stress and stress increment in volumetric and
            deviatoric invariants (p, q)

        strain, dstrain : 2x1 array
            actual strain and strain increment in volumetric and
            deviatoric invariants (eps_p, eps_q)

        stateVar, dStateVar : 2x1 array
            actual state variables additional to stress and strain
            and their increments

        dt : float
            time step

    Returns
    -------
        stress : 2x1 array
            updated stress in volumetric and deviatoric invariants (p, q)

        strain : 2x1 array
            updated strain in volumetric and deviatoric invariants (eps_p, eps_q)

        stateVar : 2x1 array
            updated additional state variables
    """

    stress = stress+dstress*dt
    strain = strain+dstrain*dt
    deps_p, deps_q = dstrain
    stateVar[0] = stateVar[0]-deps_p*(1+stateVar[0])*dt
    stateVar[1] = stateVar[1]+dStateVar[1]*dt

    return stress, strain, stateVar

#================================
# output
#================================

# save state variables to a numpy array
def recordData(data,stress,strain,stateVar):
    """
    Records the state variables in a numpy array

    Parameters
    ----------
        data : Nx10 array of floats
            array for saving the state variables in the following order
            #eps_p #eps_q #p #q #eps_1 #eps_2 #sigma_1 #sigma_2 #epor #stateVar2

        stress : 2x1 array
            volumetric and deviatoric stress invariants
            order: p, q

        strain : 2x1 array
            volumetric and deviatoric strain invariants
            order: eps_p, eps_q

        stateVar : 2x1 array
            actual state variables, stateVar[0] is usually void ratio

    Returns
    -------
        a textfile with the output stored in the same order as written in the data array
    """

    p, q = stress
    eps_p, eps_q = strain
    sigma_1, sigma_2 = pq2sigma(p,q)
    eps_1, eps_2 = pq2eps(eps_p,eps_q)
    data = numpy.append(data,[[eps_p, eps_q, p, q, eps_1, eps_2, sigma_1, sigma_2, stateVar[0], stateVar[1] ]], axis=0)
 
    return data

# output to a text file
def printResults(filename,data):
    """
    Records the state variables in a text file

    Parameters
    ----------
        filename : string
            Name of the outputfile

        data : Nx10 array of floats
            data as specified in the print_results() function
            strains, stresses in various invariants
            #eps_p #eps_q #p #q #eps_1 #eps_2 #sigma_1 #sigma_2 #epor #stateVar2

    Returns
    -------
        a textfile with the output stored in the same order as written in the data array
    """

    outputfile = open(filename+'.txt','w')
    outputfile.write('{:<8} {:<8} {:<8} {:<8} {:<8} {:<8} {:<8} {:<8} {:<8} {:<8}\n'.format(
        'eps_p', 'eps_q', 'p', 'q', 'eps_1', 'eps_2', 'sigma_1', 'sigma_2', 'epor', 'stateVar2'))
    for i in range(numpy.shape(data)[0]):
        outputfile.write('{:<8.5f} {:<8.5f} {:<8.1f} {:<8.1f} {:<8.5f} {:<8.5f} {:<8.1f} {:<8.1f} {:<8.5f} {:<8.5f}\n'.format(
            data[i,0], data[i,1], data[i,2], data[i,3], data[i,4], data[i,5], data[i,6], data[i,7], data[i,8], data[i,9]))
    outputfile.close()

    return
