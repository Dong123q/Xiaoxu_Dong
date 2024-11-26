# plotting routines for the element tests

import numpy, sys
import matplotlib.pyplot as plt

def log_model(x, a, b):
    return a * numpy.log(x) + b

def plotting_testData(data,testType=None,outputName=None,data2=None,data3=None):
    """
    plotting routine for the data produced by the element test script

    Parameters
    ----------
        data : Nx9 array of floats
            data as specified in the print_results() function
            strains, stresses in various invariants
            #eps_p #eps_q #p #q #eps_1 #eps_2 #sigma_1 #sigma_2 #epor

        testType : string
            type of the element test that is simulated
            the options are: txd, txu, oed

        outputName : string, optional
            name of the output file if the figure is to be saved
            default is None which will results in an immediate plot

    Returns
    -------
        either an output figure or an immediate plot
    """

    # create the figure and the subplots
    # option that might be useful: sharex='col', sharey='row'
    if testType == 'txd':
        fig, axs = plt.subplots(1, 2, figsize=(8,6))
        fig.subplots_adjust(hspace=0.4, wspace=0.4)
        fig.suptitle('Drained triaxial test')
        # eps_1-eps_v
        axs[0].plot(data[:,4],data[:,0], '-', label='mcc_simulation_data')
        if data2 is not None:
            axs[0].plot(data2[4][:,0],data2[4][:,1], '-', label='experimental_data')
        if data3 is not None:
            axs[0].plot(data3[:,1],data3[:,3], '-')
        axs[0].set_xlabel('$\epsilon_{1}$ [-]')
        axs[0].set_ylabel('$\epsilon_{v}$ [-]')
        axs[0].set_xlim(left=0, right=None)
        axs[0].set_ylim(bottom=0, top=None)
        axs[0].grid(which='both')
        axs[0].legend(loc='upper right', fontsize='small')

        # eps_1-q
        axs[1].plot(data[:,4],data[:,3], '-', label='mcc_simulation_data')
        if data2 is not None:
            axs[1].plot(data2[9][:,0],data2[9][:,1], '-', label='experiment_data')
        if data3 is not None:
            axs[1].plot(data3[:,2],data3[:,3], '-')
        axs[1].set_xlabel('$\epsilon_{1}$ [-]')
        axs[1].set_ylabel('q [kPa]')
        axs[1].set_xlim(left=0, right=None)
        axs[1].set_ylim(bottom=0, top=None)
        axs[1].grid(which='both')
        axs[1].legend(loc='upper right', fontsize='small')

    elif testType == 'txu':
        fig, ax = plt.subplots(1, 1, figsize=(8,6))
        fig.subplots_adjust(hspace=0.4, wspace=0.4)
        fig.suptitle('Undrained triaxial test')
       
        # q-p
        ax.plot(data[:,2]+(data[0,7]-data[:,7]), data[:,3], '-', label='mcc_simulation_data')
        if data2 is not None:
            ax.plot(data2[0][:,0],data2[0][:,1], '-', label='experimental_data')
        if data3 is not None:
            ax.plot(data3[:,2],data3[:,3], '-')
        ax.set_xlabel("$p'$ [kPa]")
        ax.set_ylabel("$q$ [kPa]")
        ax.set_xlim(left=0, right=None)
        ax.set_ylim(bottom=0, top=None)
        ax.grid(which='both')
        ax.legend(loc='upper right', fontsize='small')


    else:
        print("No or wrong testType is specified. Aborting...")
        return
    
    #export figure
    if outputName != None:
        plt.savefig(outputName+'.png', format='png',bbox_inches='tight')

    else:
        #show figure
        plt.show()


