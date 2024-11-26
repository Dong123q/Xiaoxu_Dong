"""
Task A-a: Determination of the Mohr-Coulomb model parameters 
"""
#================================
# Calibration of the parameters
#================================

import numpy as np
import matplotlib.pyplot as plt
from dataExperiment import *
from scipy import optimize
import math


def test_func_linear(x, a, b):
    return a * x + b

# M-fit
M  = 1.44

fig, ax = plt.subplots()
fig.suptitle('M-fit')
ax.plot(expData()[11][:,0],expData()[11][:,1],label='cu_100')
ax.plot(expData()[12][:,0],expData()[12][:,1],label='cu_200')
ax.plot(expData()[13][:,0],expData()[13][:,1],label='cu_400')
ax.plot(np.arange(0,500,10), test_func_linear(np.arange(0,500,10), M, 0), linestyle='--', label='Fit Line')
ax.set_xlabel('p [kPa]')
ax.set_ylabel('q [kPa]')
ax.set_xlim(left=0, right=None)
ax.set_ylim(bottom=0, top=None)
ax.grid(which='both')
plt.legend()
plt.show()
print(f"Material parameter M = {M:.3f}")


# nu-fit
slope  = 0.78

fig, ax = plt.subplots()
fig.suptitle('nu-fit')
ax.plot(expData()[1][:,0],expData()[1][:,1],label='cd_1')
ax.plot(expData()[2][:,0],expData()[2][:,1],label='cd_2')
ax.plot(expData()[3][:,0],expData()[3][:,1],label='cd_4')
ax.plot(expData()[4][:,0],expData()[4][:,1],label='cd_31')
ax.plot(expData()[5][:,0],expData()[5][:,1],label='cd_32')
ax.plot(np.arange(0,0.03,0.001), test_func_linear(np.arange(0,0.03,0.001), slope, 0), linestyle='--', label='Fit Line')
ax.set_xlabel('$\\epsilon_{1}$ [-]')
ax.set_ylabel('$\\epsilon_{v}$ [-]')
ax.set_xlim(left=0, right=None)
ax.set_ylim(bottom=0, top=None)
ax.grid(which='both')
plt.legend()
plt.show()
Nu = 1/2 * (1-slope) 
print(f"Poisson's ratio Nu = {Nu:.3f}")


# lambda-fit
def test_func_ln(x, a, b):
    return a - b * np.log(x)

p0=[1.9, 0.068]  # initial guess
p_fit = expData()[0][:,0]
void_fit = expData()[0][:,1]
params, params_covariance = optimize.curve_fit(test_func_ln, p_fit, void_fit, p0)
print("Paramters for loading. N = %.3f, lambda = %.3f"%(params[0],params[1]))
fig, ax = plt.subplots()
fig.suptitle('lambda-fit')
ax.plot(expData()[0][:,0], expData()[0][:,1])
ax.plot(np.arange(15,1000,10), test_func_ln(np.arange(15,1000,10), params[0], params[1]), '--')
ax.set_xlabel('p [kPa]')
ax.set_ylabel('v [-]')
ax.set_xscale('log')
ax.grid(which='both')
plt.legend()
plt.show()

k_guess = params[1]/10
print(f"Material parameter k = {k_guess:.3f}")

