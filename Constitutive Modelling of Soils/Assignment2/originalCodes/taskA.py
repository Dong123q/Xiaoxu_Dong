"""
Task A: Determination of the Mohr-Coulomb model parameters 
"""

#================================
# Plot the experimental data
#================================
import numpy as np
import matplotlib.pyplot as plt
from plottingTaskA import plotting_testData
from dataExperiment import *
from scipy.optimize import curve_fit
import math

# Data group
expData_TMD = [expData()[0],expData()[1],expData()[2],expData()[3],expData()[4],expData()[5]]
labels_TMD = ('TMD2_dense', 'TMD2_loose', 'TMD3_dense', 'TMD3_loose', 'TMD4_dense', 'TMD4_loose')
expData_TMU = [expData()[6],expData()[7],expData()[8]]
labels_TMU = ('TMU1', 'TMU2', 'TMU3')

# Emperimental data plotting
print("The experimental data you want to plot: ",
      "1: txd, 2: txu"
     )
testType = input("which kind of plot you want to realize: ")
if testType == '1':
    plotting_testData(expData_TMD,labels_TMD,'txd',None,None,None)
elif testType == '2':
    plotting_testData(expData_TMU,labels_TMU,'txu',None,None,None)

#================================
# Calibration of the parameters
#================================

def test_func_linear(x, a, b):
    return a * x + b

# Data group 
TMD = [expData()[0],expData()[1],expData()[2],expData()[3],expData()[4],expData()[5]]
labels1 = ['TMD2_dense', 'TMD2_loose', 'TMD3_dense', 'TMD3_loose', 'TMD4_dense', 'TMD4_loose']
TMU = [expData()[6],expData()[7],expData()[8]]
labels2 = ['TMU1', 'TMU2', 'TMU3']

# Fit parameters
def plot_phi_fit(ax, phi, p, q, line_style):
    M = 6 * math.sin(math.radians(phi)) / (3 - math.sin(math.radians(phi)))
    ax.plot(np.arange(100, 800, 10), test_func_linear(np.arange(100, 800, 10), M, 0), line_style)
    return phi

def fit_params(data_type, labels):
    if data_type == 'TMD':
        fig, axs = plt.subplots(2, 2, figsize=(13, 9))
        for idx, (data, label) in enumerate(zip(TMD, labels)):
            eps_1 = data[:, 0]/100
            q = data[:, 5]
            eps_v = data[:, 1]/100
            p = data[:, 6]
            
            # E-fit
            indices = np.where(eps_1 < 0.01)
            eps_1_fit = eps_1[indices]
            q_fit = q[indices]
            p0 = [10000, 0]
            params, params_covariance = curve_fit(test_func_linear, eps_1_fit, q_fit, p0)

            # nu-fit
            indices_nu = np.where(eps_1 < 0.005)
            eps_1_fitNu = eps_1[indices_nu]
            eps_v_fitNu = eps_v[indices_nu]
            p1 = [0.5, 0]
            paramsNu, paramsNu_covariance = curve_fit(test_func_linear, eps_1_fitNu, eps_v_fitNu, p1)
            paramsNu = [1/2 * (1-i) for i in paramsNu]

            # Psi-fit
            eps_1_fitPsi = eps_1[np.where((eps_1 > 0.025) & (eps_1 < 0.1))]
            eps_vPsi = eps_v[np.where((eps_1 > 0.025) & (eps_1 < 0.1))]
            p2 = [1, -1]
            paramsPsi, paramsPsi_covariance = curve_fit(test_func_linear, eps_1_fitPsi, eps_vPsi, p2)
            sin_Psi = paramsPsi[0] / (paramsPsi[0] - 2)
            Psi_deg = math.degrees(math.asin(sin_Psi))

            # Fitting and Plotting
            axs[0, 0].plot(eps_1, q, label=label)
            axs[0, 0].plot(eps_1_fit, test_func_linear(eps_1_fit, *params), '--', label=f'{label} - Fitted function')
            axs[0, 1].plot(eps_1, eps_v, label=label)
            axs[0, 1].plot(eps_1_fitNu, test_func_linear(eps_1_fitNu, *paramsNu), '--', label=f'{label} - Fitted function')
            axs[1, 0].plot(eps_1, eps_v, label=label)
            axs[1, 0].plot(np.arange(0.01, 0.13, 0.001), test_func_linear(np.arange(0.01, 0.13, 0.001), paramsPsi[0], paramsPsi[1]),'--',
                           label='Fitted function')
            # Phi-fit
            axs[1,1].plot(p, q, label=label)
            phi_loose = plot_phi_fit(axs[1, 1], 34, p, q, '--')
            phi_dense = plot_phi_fit(axs[1, 1], 42, p, q, ':')

            print(f"Optimized parameters for {label} (E, C):", params)
            print(f"Young's modulus E = {params[0]:.1f} kPa")
            print(f"Optimized parameters for {label} (Nu, C):", paramsNu)
            print(f"Poisson's ratio Nu = {paramsNu[0]:.3f}")
            print(f"Optimized parameters for {label} (Psi, C):", paramsPsi)
            print(f"Dilatancy angle Psi = {Psi_deg:.1f} degrees")
            print(f"Phi for loose sample = {phi_loose} degrees")
            print(f"Phi for dense sample = {phi_dense} degrees")

        axs[0, 0].set_title('TXD Calibration (Young\'s Modulus)', fontsize='small')
        axs[0, 0].set_xlabel('$\\epsilon_{1}$', fontsize='x-small')
        axs[0, 0].set_ylabel('q [kPa]', fontsize='x-small')
        axs[0, 0].legend(loc='upper right', fontsize='x-small')
        axs[0, 0].grid(which='both')

        axs[0, 1].set_title('TXD Calibration (Poisson\'s Ratio)', fontsize='small')
        axs[0, 1].set_xlabel('$\\epsilon_{1}$', fontsize='x-small')
        axs[0, 1].set_ylabel('$\\epsilon_{v}$', fontsize='x-small')
        axs[0, 1].legend(loc='upper right', fontsize='x-small')
        axs[0, 1].grid(which='both')

        axs[1, 0].set_title('TXD Calibration (Psi)', fontsize='small')
        axs[1, 0].set_xlabel('$\\epsilon_{1}$', fontsize='x-small')
        axs[1, 0].set_ylabel('$\\epsilon_{v}$', fontsize='x-small')
        axs[1, 0].legend(loc='upper right', fontsize='x-small')
        axs[1, 0].grid(which='both')

        axs[1, 1].set_title('TXD Calibration (Phi)', fontsize='small')
        axs[1, 1].set_xlabel("p [kPa]", fontsize='x-small')
        axs[1, 1].set_ylabel('q [kPa]', fontsize='x-small')
        axs[1, 1].legend(loc='upper left', fontsize='x-small')
        axs[1, 1].grid(which='both')
   
    elif data_type == 'TMU':
        fig, axs = plt.subplots(1, 1, figsize=(10, 7))
        for idx, (data, label) in enumerate(zip(TMU, labels)):
            q = data[:, 7]
            p = data[:, 6]
            
            # Phi-fit
            phi = 35
            M  = 6*math.sin(math.radians(phi))/(3-math.sin(math.radians(phi)))

            # Fitting and Plotting
            axs.plot(p, q, label=label)
            axs.plot(np.arange(0,1000,10), test_func_linear(np.arange(0,1000,10), M, 0),'--', label='Fitted function')
            
        axs.set_title('TXU Calibration (Phi)')
        axs.set_xlabel(r"$p'$ [kPa]")
        axs.set_ylabel('q [kPa]')
        axs.legend(loc='upper right', fontsize='medium')
        axs.grid(which='both')
        print(f"Friction angle Phi = {phi:.1f} degrees")

    plt.subplots_adjust(hspace=0.6, wspace=0.4)
    plt.tight_layout()
    plt.show()

fit_params('TMD', labels1)
fit_params('TMU', labels2)
