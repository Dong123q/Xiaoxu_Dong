"""
Part A:
1. Importance sampling in underline pdf(x1, x2), surface_function: linear/non-linear(sin/cos)
2. Direct Monte Carlo simulation
3. Compare 1 & 2 in x-axis: number of sampling points, y-axis: failure probability
Part B:
parameter study: weights, box(standard deviation), sampling function distribution, starting point
such as epsilon see P119
if did not meet the formula listed in P119, then change the step again use method 1 and get the new pf until meet the formula.
tips: According to the formula to fint out the input and output!
"""
import function
import plot_function
import matplotlib.pyplot as plt
import numpy as np
import time

plt.ion()   # Enable interactive mode in matplotlib

def Impor_sampl(num_steps):
    fig, ax = plt.subplots()

    # plot_function.twoD_plot(mean_point=[20, 10])
    plot_function.twoD_plot(mean_point=function.ini_data()['mean_value'])

    input("Press Enter to continue...")  # Pause for interactive viewing
    f = []
    I = []
    h = []
    step = 1

    # Initial data generation and plotting
    # starting_point = [30, 0]
    data = function.sample_generation(x1_axis=[], x2_axis=[], distribution1=function.ini_data()['distribution1'], 
                                      distribution2=function.ini_data()['distribution2'], n=function.ini_data()['num_samples'], 
                                      max_point=function.ini_data()['starting_point'])
    max_point_in = function.find_max_joint_pdf1(data)[0]
    max_joint_pdf_in = function.find_max_joint_pdf1(data)[1]
    f_value = function.find_max_joint_pdf1(data)[2]
    f.append(f_value) 
    I_value = function.indicator_function(data)
    I.append(I_value)
    h_value = f_value
    h.append(h_value)

    # Plot initial box and samples
    # max_point_out = plot_function.box(1, 1, data[0], data[1], mean_point=[30, 0], max_point=max_point_in)[0]
    max_point_out = plot_function.box(function.ini_data()['sigma_1'], function.ini_data()['sigma_2'], data[0], data[1], 
                                      mean_point=function.ini_data()['starting_point'], max_point=max_point_in)[0]
    
    start_time = time.time()  # Start time

    while step <= function.ini_data()['num_steps']:
        # Generate and plot samples with constraints for each iteration
        gener_sampl_with_constraints = plot_function.generate_samples_with_constraintsion(max_point_in, max_point_out)
        max_point_in = gener_sampl_with_constraints[0]
        max_point_out = gener_sampl_with_constraints[1]  
        data = gener_sampl_with_constraints[2]  
        f_value = data
        f.append(f_value)
        I_value = gener_sampl_with_constraints[4]
        I.append(I_value)
        h_value = gener_sampl_with_constraints[3]
        h.append(h_value)
       
        # Increment step
        step += 1

        # Update plot
        plt.draw()
        plt.pause(0.1)

    end_time = time.time()  # End time
    cpu_time_is = end_time - start_time
    print(f"IS Method CPU Time: {cpu_time_is} seconds")

    # Turn off interactive mode after plotting
    plt.ioff()
    plt.legend(loc='upper right', fontsize='small')

    hx = function.importance_sampling_pdf(f, step)
    I_f = function.I_mult_f(I, f)
    If_x = function.I_f_accum(I_f, step)
    pf_values = function.failure_probability(step, If_x, hx)

    return step, pf_values

######## Monto Carlo simulation ########

plt.ion()  # Enable interactive mode in matplotlib

def MC(ini_data):
    fig, ax = plt.subplots()

    # plot_function.twoD_plot(mean_point=[20, 10])
    plot_function.twoD_plot(mean_point = function.ini_data()['mean_value'])

    input("Press Enter to continue...")  # Pause for interactive viewing
    step = 0

    # Initial data generation and plotting
    # mean_point = [20, 10]
    mean_point = function.ini_data()['mean_value']

    # Accumulate statistics
    total_points = 0
    total_I = 0
    Pf_values = []

    start_time = time.time()  # Start time
    
    while step < function.ini_data()['num_steps']:
        step += 1
        
        # Generate new data based on previous data
        new_data_x, new_data_y, _ = function.sample_generation(x1_axis=[], x2_axis=[], distribution1=function.ini_data()['distribution1'], 
                                      distribution2=function.ini_data()['distribution2'], n=function.ini_data()['num_samples'], max_point=mean_point)

        # Use indicator_function to determine if new data points are in g < 0 region
        I = function.indicator_function((new_data_x, new_data_y))
        num_g_less_than_0 = sum(I)
        num_g_greater_than_0 = len(I) - num_g_less_than_0

        # Accumulate total indicator function value and total number of sample points
        total_I += num_g_less_than_0
        total_points += len(I)

        # Calculate values failure probability Pf
        Pf_value = total_I / total_points
        Pf_values.append(Pf_value)

        # Update scatter plot data
        ax.scatter(new_data_x, new_data_y, s=10)

        # Set plot title to show current step
        ax.set_title(f"Step {step}/{function.ini_data()['num_steps']}")

        # Update plot
        plt.draw()
        plt.pause(0.1)

    end_time = time.time()  # End time
    cpu_time_mc = end_time - start_time
    print(f"MC Method CPU Time: {cpu_time_mc} seconds")

    # Turn off interactive mode after plotting
    plt.ioff()
    return step, Pf_values

######## code execution ########
# Load initial parameters
ini_params = function.ini_data()
# Perform the Importance Sampling and obtain results
step_IS, pf_values_IS = Impor_sampl(ini_params)
# Perform the Monte Carlo simulation and obtain results
step_MC, pf_values_MC = MC(ini_params)
# Plot the results
plot_function.pf_plot(step_IS, step_MC, pf_values_IS, pf_values_MC)
