"""
Task B: Extend the Python routines and run simulations
"""

import numpy
# import additional functions
from functions_elementTest import *
from functions_matModels import *
from plotting_routines import *

#================================
# Task B
#================================

# initial state
def ini_state(testType):
    if testType == 'oed':
        epor = 0.924  # void ratio
        sigma_1 = 100  # [kPa]
        sigma_2 = 0  # [kPa]
        eps_1 = 0  # [-]
        eps_2 = 0  # [-]
    elif testType == 'iso':
        epor = 0.924  # void ratio
        sigma_1 = 100  # [kPa]
        sigma_2 = 100  # [kPa]
        eps_1 = 0  # [-]
        eps_2 = 0  # [-]
    else:
        return

    return epor, sigma_1, sigma_2, eps_1, eps_2

# material models for the elastic part
# "linelast" ... linear elasticity
# "hyperb"   ... non-linear elasticity (strain-dependent hyperbolic stiffness)
model_el = 'ohde'

# define the parameters for the material models
alpha = 0.937     # soil parameter    
nu = 0.3          # poisson ratio
# save them to a dictionary
modelParam={"alpha":alpha, "nu":nu}

#  stop criterion for calculation
p_max = 1000     # [kPa]
epsq_max = 0.2  # [-]
i_max = 1000

# numerical parameter
dt = 0.001              # time step (numerical integration)

# Function to run the test
def run_test(testType):
    # inital stress and strain in volumetric and deviatoric invariants
    epor = ini_state(testType)[0]
    sigma_1 = ini_state(testType)[1]
    sigma_2 = ini_state(testType)[2]
    eps_1 = ini_state(testType)[3]
    eps_2 = ini_state(testType)[4]
    stress = sigma2pq(sigma_1, sigma_2)
    strain = eps2pq(eps_1, eps_2)

    # these arrays are only for later use with more complex constitutive models
    stateVar = numpy.array([epor, 0])
    dStateVar = numpy.array([0, 0])
    
    # record the state variables in a numpy array in the following order
    # column: eps_p, eps_q, p, q, eps_1, eps_2, sigma_1, sigma_2, epor
    # every row represents a time step
    data = numpy.array([[strain[0], strain[1], stress[0], stress[1], eps_1, eps_2, sigma_1, sigma_2, epor, stateVar[1]]])

    # initialise the loop
    step = 1
    while (stress[0] < p_max) and (strain[1] < epsq_max) and (step < i_max):
        M = matModel(stress, strain, stateVar, model_el, modelParam)
        dstress, dstrain = testControl(M, testType)
        stress, strain, epor = integration(stress, strain, dstress, dstrain, stateVar, dStateVar, dt)
        data = recordData(data, stress, strain, stateVar)
        step += 1

    # open output file for saving the data and the plot
    filename = 'output_' + testType + '_' + model_el
    # save results to a text file
    printResults(filename, data)
    
    return data

# Run the tests
data_iso = run_test('iso')
data_oed = run_test('oed')
data_lab = [[100, 200, 300, 500, 600], [0.0275, 0.0475, 0.06, 0.075, 0.08], [0.872, 0.833, 0.81, 0.78, 0.77]]
 
# Plot the results
print("The plot type you want to realize:\n"
      "1:Comparison of Iso and Oed Tests on Ohde Model\n"  
      "2:Comparison of Oed Tests between labTest and Ohde Model"
    )
p_type = input("which kind of plot you want to realize: ")
if p_type == "1":
    plotting_testData(data_iso, 'iso', data_oed, 'oed', data_lab, "1")
elif p_type == "2":
    plotting_testData(data_iso, 'iso', data_oed, 'oed', data_lab, "2")
