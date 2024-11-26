"""
Task A : Compression behaviour of soil
"""
import numpy as np
import matplotlib.pyplot as plt

#================================
# Task A
#================================

# Experimental data from the odemetric test
sig_ax = [100, 200, 300, 500, 600]
settlement = [0.55, 0.95, 1.20, 1.50, 1.60]
density_s = 2.65
h0 = 20.0
d = 50.7
m_d = 55.6

# Calculation data recording
def recordData(sig_ax, settlement):
    eps_ax = [s / h0 for s in settlement]    # eps_ax
    
    sig_m = [0.5 * (sig_ax[i+1] + sig_ax[i]) for i in range(0, len(sig_ax)-1)]  
    sig_m.insert(0, 0.5 * (sig_ax[0] + 0))
    Es = [(sig_ax[i+1] - sig_ax[i]) / (eps_ax[i+1] - eps_ax[i]) for i in range(0, len(sig_ax)-1)]  
    Es.insert(0, (sig_ax[0] + 0) / (eps_ax[0] - 0))   # odemetric modulus
    log_Es = np.log10(Es)
    log_sig_ax = np.log10(sig_ax)

    V_solid = m_d / density_s
    V_total = [np.pi * ((d * 0.1 / 2) ** 2) * (h0 * 0.1 - s * 0.1) for s in settlement]
    V_void = [V_t - V_solid for V_t in V_total]
    e = [-1 * V_v / V_solid for V_v in V_void]   # void ratio

    data = np.array([sig_ax, settlement, eps_ax, Es, log_Es, log_sig_ax, e, sig_m]).T

    return data

# output to a text file
def printResults(data):
    with open('recordData.txt', 'w') as outputfile:
        outputfile.write('{:<17} {:<17} {:<17} {:<17} {:<17} {:<17} {:<17} {:<17}\n'.format(
            'sig_ax[kPa]', 'settlement[mm]', 'eps_ax[-]', 'Es[kPa]', 'log_Es[kPa]', 'log_sig_ax[kPa]', 'e', 'sig_m[kPa]'))
        for row in data:
            sig_ax, settlement, eps_ax, Es, log_Es, log_sig_ax, e, sig_m = row
            outputfile.write('{:<17.5f} {:<17.5f} {:<17.5f} {:<17.5f} {:<17.5f} {:<17.5f} {:<17.5f} {:<17.5f}\n'.format(
                sig_ax, settlement, eps_ax, Es, log_Es, log_sig_ax, e, sig_m))

def data_plot(data):
    # create the figure and the subplots
    fig, axs = plt.subplots(3, 2, figsize=(17, 8))
    fig.subplots_adjust(hspace=0.4, wspace=0.4)
    
    # Plot for sigma_ax-s
    axs[0, 0].scatter(data[:, 0], data[:, 1], label='Data')
    axs[0, 0].set_xlabel('$\sigma_{ax}$ [kPa]')
    axs[0, 0].set_ylabel('s [mm]')
    axs[0, 0].grid(which='both')
    axs[0, 0].legend()
    axs[0, 0].invert_yaxis()

    # Plot for sigma_ax-eps_ax
    axs[0, 1].scatter(data[:, 0], data[:, 2], label='Data')
    axs[0, 1].set_xlabel('$\sigma_{ax}$ [kPa]')
    axs[0, 1].set_ylabel('$\epsilon_{ax}$ [-]')
    axs[0, 1].grid(which='both')
    axs[0, 1].legend()
    axs[0, 1].invert_yaxis()

    # Plot for sigma_m-Es
    axs[1, 0].scatter(data[:, 7], data[:, 3], label='Data')
    axs[1, 0].set_xlabel('$\sigma_{m}$ [kPa]')
    axs[1, 0].set_ylabel('$E_s$ [kPa]')
    axs[1, 0].grid(which='both')
    axs[1, 0].legend()

    # Plot for sigma_ax-e
    axs[1, 1].scatter(data[:, 0], data[:, 6], label='Data')
    axs[1, 1].set_xlabel('$\sigma_{ax}$ [kPa]')
    axs[1, 1].set_ylabel('e')
    axs[1, 1].grid(which='both')
    axs[1, 1].legend()
    axs[1, 1].invert_yaxis()

    # Plot and linear regression for log_sig_ax-log_Es
    axs[2, 0].scatter(data[:, 5], data[:, 4], label='Data')
    axs[2, 0].set_xlabel('$\log_{10}(\sigma_{ax})$ [kPa]')
    axs[2, 0].set_ylabel('$\log_{10}(E_s)$ [kPa]')
    axs[2, 0].grid(which='both')
    axs[2, 0].legend()

    # Perform linear regression
    slope, intercept = np.polyfit(data[:, 5], data[:, 4], 1)
    fit_x = np.array([min(data[:, 5]), max(data[:, 5])])
    fit_y = slope * fit_x + intercept
    axs[2, 0].plot(fit_x, fit_y, color='red', label=f'Linear Fit: y = {slope:.2f}x + {intercept:.2f}')
    axs[2, 0].legend()

    # Plot and linear regression for log_sig_ax-e
    axs[2, 1].scatter(data[:, 5], data[:, 6], label='Data')
    axs[2, 1].set_xlabel('$\log_{10}(\sigma_{ax})$ [kPa]')
    axs[2, 1].set_ylabel('e')
    axs[2, 1].grid(which='both')
    axs[2, 1].legend()
    axs[2, 1].invert_yaxis()

    # Perform linear regression
    slope, intercept = np.polyfit(data[:, 5], data[:, 6], 1)
    fit_x = np.array([min(data[:, 5]), max(data[:, 5])])
    fit_y = slope * fit_x + intercept
    axs[2, 1].plot(fit_x, fit_y, color='red', label=f'Linear Fit: y = {slope:.2f}x + {intercept:.2f}')
    axs[2, 1].legend()

    fig.suptitle('TaskA Plot')
    
    # show figure
    plt.show()

data = recordData(sig_ax, settlement)
printResults(data)
data_plot(data)



