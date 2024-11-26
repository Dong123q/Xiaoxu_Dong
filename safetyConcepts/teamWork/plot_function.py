"""
This file is for plotting functions
"""

import matplotlib.pyplot as plt
import numpy as np
import function


def plot_cdf(x_axis, y_axis, title):
    x_sorted = sorted(x_axis)
    y_sorted = [(i + 1) / len(x_sorted) for i in range(len(x_sorted))]
    plt.scatter(x_axis, y_axis, label='Analytical CDF')
    plt.scatter(x_sorted, y_sorted, label='Empirical CDF')
    plt.title(title)
    plt.xlabel('x')
    plt.ylabel('F(x)')
    plt.legend()
    plt.show()


def plot_pdf(x_axis, z_axis, title):
# Divide observation data into 20 equal-width levels
    bin_width = (max(x_axis) - min(x_axis)) / 20
    bins = [min(x_axis) + i * bin_width for i in range(21)]
# Calculate the number of data in each level that falls within it
    histogram = [0] * 20
    for data_point in x_axis:
        for i in range(len(bins) - 1):
            if bins[i] <= data_point < bins[i + 1]:
                histogram[i] += 1
                break
# Normalized the historgram
    total_count = sum(histogram)
    normalized_histogram = [count / (total_count * bin_width) for count in histogram]
# Plot
    plt.scatter(x_axis, z_axis, label='PDF')
    plt.bar(bins[:-1], normalized_histogram, width=bin_width, alpha=0.7, color='g', edgecolor='black', label='Histogram')
    plt.title(title)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend()
    plt.show()


def plot_choose(x_axis, y_axis, z_axis, dist_name):
    print("The plot type you want to realize:"
          "1: plot_cdf, 2: plot_pdf")
    plot = input("Which plot you want to realize: ")
    if plot == "1":
        plot_cdf(x_axis, y_axis, f'{dist_name} Distribution')
    elif plot == "2":
        plot_pdf(x_axis, z_axis,f'{dist_name} Distribution')


def twoD_plot(mean_point):
    if not plt.gca().has_data():
        plt.grid(True, linewidth=0.5)
        x_values = np.linspace(0, 1000, 100)
        y_values = x_values 
        plt.plot(x_values, y_values, color='red', label='Limit state function: X2 - X1 = 0')
        plt.scatter(*mean_point, color='red', marker='x', s=100, label='Mean Point')

    plt.draw()
    plt.pause(0.1)  


def box(sigma_1, sigma_2, x2, y2, mean_point=None, max_point=None):

    box_len = 0.1 * sigma_1
    box_width = 0.1 * sigma_2
    
    # Initialize a list to store points outside the box
    outside_points = []

    plt.scatter(x2, y2, label='Sample around start point', s=10)
    
    if mean_point:
        plt.scatter(*mean_point, color='red', marker='x', s=100, label='Starting point')
    
    if max_point:
        rect_x = max_point[0] - box_len / 2
        rect_y = max_point[1] - box_width / 2
        rectangle = plt.Rectangle((rect_x, rect_y), box_len, box_width, color='red', fill=False)
        plt.gca().add_patch(rectangle)
        plt.scatter(*max_point, color='blue', marker='x', s=100, label='Max Joint PDF Point')
        
        # Identify points outside the box
        outside_points = [(x, y) for x, y in zip(x2, y2)
                          if not (rect_x <= x <= rect_x + box_len and rect_y <= y <= rect_y + box_width)]
    # Find the max joint PDF value among the points outside the box
    if outside_points and function.find_max_joint_pdf2:
        outside_data = list(zip(*outside_points))
        max_point_outside = function.find_max_joint_pdf2(outside_data, distribution1=function.ini_data()['distribution1'], 
                                      distribution2=function.ini_data()['distribution2'])[0]
        max_joint_pdf_outside = function.find_max_joint_pdf2(outside_data, distribution1=function.ini_data()['distribution1'], 
                                      distribution2=function.ini_data()['distribution2'])[1]
        plt.scatter(*max_point_outside, color='green', marker='x', s=100, label='Max Outside Joint PDF Point')
    else:
        max_point_outside = None
        max_joint_pdf_outside = None
        print("No points outside the box.")
    
    plt.gca().set_aspect('equal', adjustable='box')
    plt.legend(loc='upper right', fontsize='small')
    plt.show()
    
    return max_point_outside, max_joint_pdf_outside


def generate_samples_with_constraintsion(max_point_in=None, max_point_out=None):

    # Generate samples around the maximum point inside the box
    data = function.sample_generation(x1_axis=[], x2_axis=[], distribution1=function.ini_data()['distribution1'], 
                                      distribution2=function.ini_data()['distribution2'], n=function.ini_data()['num_box_sample'], 
                                      max_point=max_point_in)
    x1_samples_in = data[0]
    x2_samples_in = data[1]
    # Plot the samples
    plt.scatter(x1_samples_in, x2_samples_in, s=10)

    # Generate samples around the maximum point outside the box
    data = function.sample_generation(x1_axis=[], x2_axis=[], distribution1=function.ini_data()['distribution1'], 
                                      distribution2=function.ini_data()['distribution2'], n=function.ini_data()['num_box_sample'],
                                      max_point=max_point_out)
    x1_samples_out = data[0]
    x2_samples_out = data[1]
    plt.scatter(x1_samples_out, x2_samples_out, s=10)

    # Convert samples to list 
    data_samples_in = [x1_samples_in, x2_samples_in]
    data_samples_out = [x1_samples_out, x2_samples_out]
    
    # Find the maximum joint PDF point inside the box
    max_point_in = function.find_max_joint_pdf2(data_samples_in, distribution1=function.ini_data()['distribution1'], 
                                      distribution2=function.ini_data()['distribution2'])[0]
    max_joint_pdf_in = function.find_max_joint_pdf2(data_samples_in, distribution1=function.ini_data()['distribution1'], 
                                      distribution2=function.ini_data()['distribution2'])[1]
    joint_pdf_in = function.find_max_joint_pdf2(data_samples_in, distribution1=function.ini_data()['distribution1'], 
                                      distribution2=function.ini_data()['distribution2'])[2]
    I_in = function.indicator_function(data_samples_in)
    plt.scatter(*max_point_in, color='red', marker='x', s=100)

    # Find the maximum joint PDF point outside the box
    max_point_out = function.find_max_joint_pdf2(data_samples_out, distribution1=function.ini_data()['distribution1'], 
                                      distribution2=function.ini_data()['distribution2'])[0]
    max_joint_pdf_out = function.find_max_joint_pdf2(data_samples_out, distribution1=function.ini_data()['distribution1'], 
                                      distribution2=function.ini_data()['distribution2'])[1]
    joint_pdf_out = function.find_max_joint_pdf2(data_samples_out, distribution1=function.ini_data()['distribution1'], 
                                      distribution2=function.ini_data()['distribution2'])[2]
    I_out = function.indicator_function(data_samples_out)
    plt.scatter(*max_point_out, color='pink', marker='x', s=100)

    joint_pdf_combined = joint_pdf_in + joint_pdf_out
    I = I_in + I_out
    h = [0.5 * val for val in joint_pdf_in] + [0.5 * val for val in joint_pdf_out]

    return max_point_in, max_point_out, joint_pdf_combined, h, I


def pf_plot(step_IS, step_MC, pf_values_IS,  pf_values_MC):

    plt.figure(figsize=(10, 6))
    steps_IS = list(range(1, step_IS + 1))
    steps_MC = list(range(1, step_MC + 1))

    plt.plot(steps_IS, pf_values_IS, label='Importance Sampling', marker='o')
    plt.plot(steps_MC, pf_values_MC, label='Monte Carlo Simulation', marker='x')

    plt.xlabel('Steps')
    plt.ylabel('Failure Probability')
    plt.title('Failure Probability vs Steps')
    plt.legend()
    plt.grid(True)
    plt.show()
