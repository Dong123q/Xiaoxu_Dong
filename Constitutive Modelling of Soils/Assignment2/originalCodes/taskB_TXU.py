# Exercise 2
# Computation of element tests
# Linear-Elastic Ideal-Plastic constitutive model (liep)

import numpy, sys
# import additional functions
from functions_elementTest import *
from functions_matModels import *
from plotting_routines import *
from dataExperiment import *

#================================
# Input
#================================

# initial state
epor = 0.828    # void ratio
p = 100	        # [kPa]
q = 0.559	    # [kPa]
eps_1 = 0       # [-]
eps_2 = 0	    # [-]
# material models for the elastic and the plastic part
# "linelast" ... linear elasticity
model_el = "linelast"
# "mc"  ... mohr-coulomb
# "dp" ... drucker-prager
model_pl = "mc"
# model_pl = "dp"
model={"model_el":model_el, "model_pl":model_pl}

# material parameters
E = 25647.6   #[kPa] ... Young's modulus
nu = 0.325     # [-] ... Poisson's ratio
phi = 55        # [°] ... friction angle
psi = 16.2    # [°] ... dilatancy angle
modelParam={"E":E, "nu":nu, "phi":phi, "psi":psi}

# test control
# "oed" ... oedometer test
# "txd" ... drained triaxial test
# "txu" ... undrained triaxial test
testType = 'txu'

# stop criteria for calculation
p_max = 1000	# [kPa]
epsq_max = 0.06	# [%]
i_max = 1000	# max iterations

# numerical parameter
dt = 0.001        # time step (numerical integration)

#===============================================================================
# Calculation
#===============================================================================

# inital stress and strain in volumetric and deviatoric invariants
stress = numpy.array([p, q])
strain = eps2pq(eps_1,eps_2)
stateVar = numpy.array([epor,0])
sigma_1 = pq2sigma(stress[0], stress[1])[0]
sigma_2 = pq2sigma(stress[0], stress[1])[1]

# record the state variables in a numpy array in the following order
# column: eps_p, eps_q, p, q, eps_1, eps_2, sigma_1, sigma_2, epor
# every row represents a time step
data = numpy.array([[strain[0], strain[1], stress[0], stress[1], eps_1, eps_2, sigma_1, sigma_2, epor, stateVar[1] ]])

# initialise the loop
step = 1
while (stress[0] < p_max) and (strain[1] < epsq_max) and (step < i_max):
    dstress, dstrain, dStateVar = rates(stress,strain,stateVar,testType,model,modelParam)
    stress, strain, stateVar = integration(stress,strain,dstress,dstrain,stateVar,dStateVar,dt)
    data = recordData(data,stress,strain,stateVar)
    step += 1

# open output file for saving the data and the plot
filename = 'output_' + testType + 'expDataV.S.MC'+'_TMU1'

# save results to a text file
printResults(filename,data)
data2 = expData()[6]

# plot the results
plotting_testData(data, testType='txu', outputName=filename, data2=data2, data3=None)
