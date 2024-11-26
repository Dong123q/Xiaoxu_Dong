# plotting routines for the element tests

import numpy, sys
import matplotlib.pyplot as plt


def plotting_testData(data,label,testType=None,outputName=None,data2=None,label2=None):
    
    if testType == 'txd':          
        fig, axs = plt.subplots(2, 2, figsize=(20,13))
        fig.subplots_adjust(hspace=0.4, wspace=0.4)
        fig.suptitle('Experimental data-TMD')
        # fig.suptitle('Comparison of experimental data and MC simulation on txd')

        for idx, (data, label) in enumerate(zip(data, label)):
            eps_1 = data[:, 0]
            q = data[:, 5]
            eps_v = data[:, 1]
            p = data[:, 6]

            axs[0, 0].plot(eps_1, q, label=label)
            axs[0, 1].plot(eps_1, eps_v, label=label)
            axs[1, 0].plot(p, q, label=label)
        if data2 is not None and label2 is not None:
            for idx, (data2, label2) in enumerate(zip(data2, label2)):
                eps_1 = data2[:, 4]
                q = data2[:, 3]
                eps_v = data2[:, 0]
                p = data2[:, 2]
                
                axs[0, 0].plot(eps_1, q, '--', label=label2)
                axs[0, 1].plot(eps_1, eps_v, '--', label=label2)
                axs[1, 0].plot(p, q, '--', label=label2)
        
        # q-eps_1
        axs[0, 0].set_title('q-eps_1')
        axs[0, 0].set_xlabel('$\\epsilon_{1}$ [%]')
        axs[0, 0].set_ylabel('q [kPa]')
        axs[0, 0].legend(loc='upper right', fontsize='small')
        axs[0, 0].grid(which='both')
        
        # eps_v-eps_1
        axs[0, 1].set_title('eps_v-eps_1')
        axs[0, 1].set_xlabel('$\\epsilon_{1}$ [%]')
        axs[0, 1].set_ylabel('$\\epsilon_{v}$ [%]')
        axs[0, 1].legend(loc='upper right', fontsize='small')
        axs[0, 1].grid(which='both')
        
        # q-p
        axs[1, 0].set_title('q-p')
        axs[1, 0].set_xlabel("p [kPa]")
        axs[1, 0].set_ylabel('q [kPa]')
        axs[1, 0].legend(loc='upper right', fontsize='small')
        axs[1, 0].grid(which='both')

        axs[1, 1].set_visible(False)


    elif testType == 'txu':
        fig, axs = plt.subplots(2, 1, figsize=(20, 13))
        fig.subplots_adjust(hspace=0.4, wspace=0.4)
        fig.suptitle('Experimental data-TMU')
        # fig.suptitle('Comparison of experimental data and MC simulation on txu')
        for idx, (data, label) in enumerate(zip(data, label)):
            eps_1 = data[:, 0]
            q = data[:, 7]
            p = data[:, 6]

            axs[0].plot(eps_1, q, label=label)
            axs[1].plot(p, q, label=label)

        if data2 is not None and label2 is not None:
            for idx, (data2, label2) in enumerate(zip(data, label2)):
                eps_1 = data2[:, 4]
                q = data2[:, 3]
                p = data2[:, 6]

                axs[0].plot(eps_1, q, '--', label=label2)
                axs[1].plot(p, q, '--', label=label2)
               
        axs[0].set_title('q-eps_1')
        axs[0].set_xlabel('$\\epsilon_{1}$ [%]')
        axs[0].set_ylabel('q [kPa]')
        axs[0].legend(loc='upper right', fontsize='small')
        axs[0].grid(which='both')

        axs[1].set_title('q-p')
        axs[1].set_xlabel("p [kPa]")
        axs[1].set_ylabel('q [kPa]')
        axs[1].legend(loc='upper right', fontsize='small')
        axs[1].grid(which='both')

    else:
        print("No or wrong testType is specified. Aborting...")
        return
    
    #export figure
    if outputName != None:
        # plt.savefig(outputName+'.png', format='png',bbox_inches='tight')
        plt.savefig(outputName+'.pdf', format='pdf',bbox_inches='tight')
    else:
        #show figure
        plt.show()

