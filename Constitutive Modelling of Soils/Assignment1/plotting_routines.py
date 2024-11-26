import numpy as np
import matplotlib.pyplot as plt

def plotting_testData(data_iso, testType_iso, data_oed, testType_oed, data_lab, p_type, outputName=None):
    """
    plotting routine for the data produced by the element test script

    Parameters
    ----------
        data_iso : Nx9 array of floats
            data as specified in the print_results() function
            strains, stresses in various invariants for iso test

        testType_iso : string
            type of the element test that is simulated (iso in this case)

        data_oed : Nx9 array of floats
            data as specified in the print_results() function
            strains, stresses in various invariants for oed test

        testType_oed : string
            type of the element test that is simulated (oed in this case)

        outputName : string, optional
            name of the output file if the figure is to be saved
            default is None which will results in an immediate plot

    Returns
    -------
        either an output figure or an immediate plot
    """

    if p_type == "1":
        
        # create the figure and the subplots
        fig, axs = plt.subplots(2, 2, figsize=(12, 5))
        fig.subplots_adjust(hspace=0.4, wspace=0.4)
    
        # Plot for e-sigma_1
        axs[0, 0].plot(data_iso[:, 6], data_iso[:, 8], label=testType_iso)
        axs[0, 0].plot(data_oed[:, 6], data_oed[:, 8], label=testType_oed)
        axs[0, 0].set_xlabel('$\sigma_{1}$ [kPa]')
        axs[0, 0].set_ylabel('e [-]')
        axs[0, 0].grid(which='both')
        axs[0, 0].legend()

        # Plot for eps_1-sigma_1
        axs[0, 1].plot(data_iso[:, 4], data_iso[:, 6], label=testType_iso)
        axs[0, 1].plot(data_oed[:, 4], data_oed[:, 6], label=testType_oed)
        axs[0, 1].set_xlabel('eps_{1} [-]')
        axs[0, 1].set_ylabel('$\sigma_{1}$ [kPa]')
        axs[0, 1].grid(which='both')
        axs[0, 1].legend()

        # plot for sigma_1-sigma_2
        axs[1, 0].plot(data_iso[:, 7], data_iso[:, 6], label=testType_iso)
        axs[1, 0].plot(data_oed[:, 7], data_oed[:, 6], label=testType_oed)
        axs[1, 0].set_xlabel('$\sigma_{2}$ [kPa]')
        axs[1, 0].set_ylabel('$\sigma_{1}$ [kPa]')
        axs[1, 0].grid(which='both')
        axs[1, 0].legend()

        # plot for q-p
        axs[1, 1].plot(data_iso[:, 2], data_iso[:, 3], label=testType_iso)
        axs[1, 1].plot(data_oed[:, 2], data_oed[:, 3], label=testType_oed)
        axs[1, 1].set_xlabel('p [kPa]')
        axs[1, 1].set_ylabel('q [kPa]')
        axs[1, 1].grid(which='both')
        axs[1, 1].legend()
    
        fig.suptitle('Comparison of Iso and Oed Tests on Ohde Model')

    elif p_type == "2":
        # Convert data_lab to a NumPy array if it's not already
        data_lab = np.array(data_lab)

        # create the figure and the subplots
        fig, axs = plt.subplots(1, 2, figsize=(12, 5))
        fig.subplots_adjust(hspace=0.4, wspace=0.4)
    
        # Plot for e-sigma_1
        axs[0].plot(data_oed[:, 6], data_oed[:, 8], label=testType_oed)
        axs[0].scatter(data_lab[0, :], data_lab[2, :], label='labTest_oed', marker='o')
        axs[0].set_xlabel('$\sigma_{1}$ [kPa]')
        axs[0].set_ylabel('e [-]')
        axs[0].grid(which='both')
        axs[0].legend()

        # Plot for eps_1-sigma_1
        axs[1].plot(data_oed[:, 4], data_oed[:, 6], label=testType_oed)
        axs[1].scatter(data_lab[1, :], data_lab[0, :], label='labTest_oed', marker='o')
        axs[1].set_xlabel('eps_{1} [-]')
        axs[1].set_ylabel('$\sigma_{1}$ [kPa]')
        axs[1].grid(which='both')
        axs[1].legend()

        fig.suptitle('Comparison of Oed Tests between labTest and Ohde Model')
    
    else:
        print("No or wrong testType is specified. Aborting...")
        return

    # export figure
    if outputName is not None:
        plt.savefig(outputName + '.pdf', format='pdf', bbox_inches='tight')
    else:
        # show figure
        plt.show()


    

