# plotting routines for the element tests

import numpy, sys
import matplotlib.pyplot as plt

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
    fig, axs = plt.subplots(2, 2, figsize=(8,6))
    fig.subplots_adjust(hspace=0.4, wspace=0.4)

    if testType == 'txd':
        fig.suptitle('Drained triaxial test')
        # q-eps_q
        axs[0,0].plot(data[:,1],data[:,3], '-', label='MC_simulation_data')
        # axs[0,0].plot(data[:,1],data[:,3], '-', label='DP_simulation_data')
        if data2 is not None:
            axs[0,0].plot(data2[:,3]/100,data2[:,5], '-', label='experimental_data')
        if data3 is not None:
            axs[0,0].plot(data3[:,1],data3[:,3], '-')
        axs[0,0].set_xlabel('$\epsilon_{q}$ [-]')
        axs[0,0].set_ylabel('q [kPa]')
        axs[0,0].set_xlim(left=0, right=None)
        axs[0,0].set_ylim(bottom=0, top=None)
        axs[0,0].grid(which='both')
        axs[0, 0].legend(loc='upper right', fontsize='small')

        # q-p
        axs[0,1].plot(data[:,2],data[:,3], '-', label='MC_simulation_data')
        # axs[0,1].plot(data[:,2],data[:,3], '-', label='DP_simulation_data')
        if data2 is not None:
            axs[0,1].plot(data2[:,6],data2[:,5], '-', label='experiment_data')
        if data3 is not None:
            axs[0,1].plot(data3[:,2],data3[:,3], '-')
        axs[0,1].set_xlabel('p [kPa]')
        axs[0,1].set_ylabel('q [kPa]')
        axs[0,1].set_xlim(left=0, right=None)
        axs[0,1].set_ylim(bottom=0, top=None)
        axs[0,1].grid(which='both')
        axs[0, 1].legend(loc='upper right', fontsize='small')

        # e-eps_q
        axs[1,0].plot(data[:,1], data[:,8], '-', label='MC_simulation_data')
        # axs[1,0].plot(data[:,1], data[:,8], '-', label='DP_simulation_data')
        if data2 is not None:
            axs[1,0].plot( data2[:,3]/100,data2[:,4], '-', label='experiment_data')
        if data3 is not None:
            axs[1,0].plot(data3[:,1],data3[:,8], '-')
        axs[1,0].set_xlabel('$\epsilon_{q}$ [-]')
        axs[1,0].set_ylabel('e [-]')
        axs[1,0].set_xlim(left=0, right=None)
        axs[1,0].grid(which='both')
        axs[1, 0].legend(loc='upper right', fontsize='small')

        # e-p
        axs[1,1].plot(data[:,2], data[:,8], '-', label='MC_simulation_data')
        # axs[1,1].plot(data[:,2], data[:,8], '-', label='DP_simulation_data')
        if data2 is not None:
            axs[1,1].plot(data2[:,6],data2[:,4], '-', label='experiment_data')
        if data3 is not None:
            axs[1,1].plot(data3[:,2],data3[:,8], '-')
        axs[1,1].set_xlabel('p [kPa]')
        axs[1,1].set_ylabel('e [-]')
        axs[1,1].set_xlim(left=0, right=None)
        axs[1,1].grid(which='both')
        axs[1, 1].legend(loc='upper right', fontsize='small')

    elif testType == 'txu':
        fig.suptitle('Undrained triaxial test')
        # q-eps_q
        axs[0,0].plot(data[:,1],data[:,3]-(data[0,7]-data[:,7]), '-', label='MC_simulation_data')
        # axs[0,0].plot(data[:,1],data[:,3]-(data[0,7]-data[:,7]), '-', label='DP_simulation_data')
        if data2 is not None:
            axs[0,0].plot((2/3*data2[:,0])/100,data2[:,7], '-', label='experimental_data')
        if data3 is not None:
            axs[0,0].plot(data3[:,1],data3[:,3], '-')
        axs[0,0].set_xlabel('$\epsilon_{q}$ [-]')
        axs[0,0].set_ylabel("$q'$ [kPa]")
        axs[0,0].set_xlim(left=0, right=None)
        axs[0,0].set_ylim(bottom=0, top=None)
        axs[0,0].grid(which='both')
        axs[0, 0].legend(loc='upper right', fontsize='small')  

        # q-p
        axs[0,1].plot(data[:,2]-(data[0,7]-data[:,7]),data[:,3]-(data[0,7]-data[:,7]), '-', label='MC_simulation_data')
        # axs[0,1].plot(data[:,2]-(data[0,7]-data[:,7]),data[:,3]-(data[0,7]-data[:,7]), '-', label='DP_simulation_data')
        if data2 is not None:
            axs[0,1].plot(data2[:,6],data2[:,7], '-', label='experimental_data')
        if data3 is not None:
            axs[0,1].plot(data3[:,2],data3[:,3], '-')
        axs[0,1].set_xlabel("$p'$ [kPa]")
        axs[0,1].set_ylabel("$q'$ [kPa]")
        axs[0,1].set_xlim(left=0, right=None)
        axs[0,1].set_ylim(bottom=0, top=None)
        axs[0,1].grid(which='both')
        axs[0, 1].legend(loc='upper right', fontsize='small')

        # u-eps_q
        axs[1,0].plot(data[:,1],199.51+data[0,7]-data[:,7], '-', label='MC_simulation_data')
        # axs[1,0].plot(data[:,1],199.51+data[0,7]-data[:,7], '-', label='DP_simulation_data')
        if data2 is not None:
            axs[1,0].plot((2/3*data2[:,0])/100,data2[:,1], '-', label='experimental_data')
        if data3 is not None:
            axs[1,0].plot(data3[:,1],data3[0,7]-data3[:,7], '-')
        axs[1,0].set_xlabel('$\epsilon_{q}$ [-]')
        axs[1,0].set_ylabel('u [kPa]')
        axs[1,0].set_xlim(left=0, right=None)
        axs[1,0].set_ylim(bottom=0, top=None)
        axs[1,0].grid(which='both')
        axs[1, 0].legend(loc='upper right', fontsize='small')

        axs[1,1].set_visible(False)

    elif testType == 'oed':
        fig.suptitle('Oedometric test')
        # sigma_1-e
        axs[0,0].plot(data[:,6],data[:,8], '-')
        if data2 is not None:
            axs[0,0].plot(data2[:,6],data2[:,8], '-')
        if data3 is not None:
            axs[0,0].plot(data3[:,6],data3[:,8], '-')
        axs[0,0].set_xlabel('$\sigma_{1}$ [kPa]')
        axs[0,0].set_ylabel('e [-]')
        axs[0,0].set_xlim(left=0, right=None)
        axs[0,0].grid(which='both')

        # eps_1-sigma_1
        axs[0,1].plot(data[:,4],data[:,6], '-')
        if data2 is not None:
            axs[0,1].plot(data2[:,4],data2[:,6], '-')
        if data3 is not None:
            axs[0,1].plot(data3[:,4],data3[:,6], '-')
        axs[0,1].set_xlabel('eps_1 [-]')
        axs[0,1].set_ylabel('$\sigma_{1}$ [kPa]')
        axs[0,1].set_xlim(left=0, right=None)
        axs[0,1].grid(which='both')

        axs[1,0].set_visible(False)
        axs[1,1].set_visible(False)
   
    elif testType == 'iso':
        fig.suptitle('Isotropic test')
        # sigma_1-e
        axs[0,0].plot(data[:,6],data[:,8], '-')
        if data2 is not None:
            axs[0,0].plot(data2[:,6],data2[:,8], '-')
        if data3 is not None:
            axs[0,0].plot(data3[:,6],data3[:,8], '-')
        axs[0,0].set_xlabel('$\sigma_{1}$ [kPa]')
        axs[0,0].set_ylabel('e [-]')
        axs[0,0].set_xlim(left=0, right=None)
        axs[0,0].grid(which='both')

        # eps_1-sigma_1
        axs[0,1].plot(data[:,4],data[:,6], '-')
        if data2 is not None:
            axs[0,1].plot(data2[:,4],data2[:,6], '-')
        if data3 is not None:
            axs[0,1].plot(data3[:,4],data3[:,6], '-')
        axs[0,1].set_xlabel('eps_1 [-]')
        axs[0,1].set_ylabel('$\sigma_{1}$ [kPa]')
        axs[0,1].set_xlim(left=0, right=None)
        axs[0,1].grid(which='both')

        axs[1,0].set_visible(False)
        axs[1,1].set_visible(False)
   
    else:
        print("No or wrong testType is specified. Aborting...")
        return
    
    #export figure
    if outputName != None:
        plt.savefig(outputName+'.png', format='png',bbox_inches='tight')
        # plt.savefig(outputName+'.pdf', format='pdf',bbox_inches='tight')
    else:
        #show figure
        plt.show()


