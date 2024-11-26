"""
This file is for functions calculation
"""

import math
import random


def uniform_cdf(x, a, b):
    """
    function: Calculate the cumulative distribution function of the uniform distribution
    :param x: The value of a random variable
    :param a: The lower limit of the uniform distribution interval
    :param b: The upper limit of the uniform distribution interval
    :return:  The probability of the random variable
    """
    if b <= a:
        raise ValueError("Upper limit(b) must be greater than lower limit(a)")
    if x < a:
        return 0.0
    elif x > b:
        return 1.0
    else:
        q = (x - a) / (b - a)
    return q


def uniform_cdf_inv(q, a, b):
    """
    function: Calculate the inverse of cumulative distribution function of the uniform distribution
    :param q: The probability of the random variable
    :param a: The lower limit of the uniform distribution interval
    :param b: The upper limit of the uniform distribution interval
    :return: The corresponding random variable
    """
    if b <= a:
        raise ValueError("Upper limit(b) must be greater than lower limit(a)")
    if q < 0 or q > 1:
        raise ValueError("Probability q must be between 0 and 1")

    x = a + q * (b - a)
    return x


def st_nor_cdf(x):
    """
    function: Calculate the approximation of the cumulative distribution function of the standard normal distribution
    :param x: The value of random variable
    :return:  The probability of the random variable
    """
    b = [0.319381530, -0.356563782, 1.781477937, -1.821255978, 1.330274429]
    p = 0.2316419

    if x > 0:
        sign = 1
    else:
        sign = -1
    t = 1 / (1 + p * sign * x)
    bt = (b[0] * t + b[1] * t ** 2 + b[2] * t ** 3 + b[3] * t ** 4 + b[4] * t ** 5)

    if x > 0:
        q = 1 - (1 / math.sqrt(2 * math.pi) * math.exp(-x ** 2 / 2)) * bt
    else:
        q = 1 / math.sqrt(2 * math.pi) * math.exp(-x ** 2 / 2) * bt

    return q


def st_nor_cdf_inv(q):
    """
    function: Calculate the inverse of cumulative distribution function of the uniform distribution
    :param q: The probability of the random variable
    :return:  The corresponding random variable
    """

    if q < 0 or q > 1:
        raise ValueError("Probability q must be between 0 and 1")

    c = [2.515517, 0.802853, 0.010328]
    d = [1.432788, 0.189269, 0.001308]

    x = None

    if 0 < q <= 0.5:
        u = math.sqrt(math.log(1/(q ** 2)))
        x = -u + (c[0] + c[1] * u + c[2] * u ** 2)/(1 + d[0] * u + d[1] * u ** 2 + d[2] * u ** 3)
    elif 0.5 < q <= 1:
        u = math.sqrt(math.log(1/((1-q) ** 2)))
        x = u - (c[0] + c[1] * u + c[2] * u ** 2)/(1 + d[0] * u + d[1] * u ** 2 + d[2] * u ** 3)

    return x


def nor_cdf(x, mx, sig):
    """
    function: Calculate the cumulative distribution function of the normal distribution
    :param x: The value of random variable
    :param mx: The mean value of the normal distribution
    :param sig: The standard deviation of the normal distribution
    :return: The probability of the random variable
    """
    y = (x - mx) / sig
    q = st_nor_cdf(y)
    return q


def nor_cdf_inv(q, mx, sig):
    """
    function: Calculate the inverse of cumulative distribution function of the normal distribution
    :param q: The probability of the random variable
    :param mx: The mean value of the normal distribution
    :param sig: The standard deviation of the normal distribution
    :return: The corresponding random variable
    """
    y = st_nor_cdf_inv(q)
    x = y * sig + mx
    return x


def log_nor_cdf(x, x_0, mx, sig_x):
    """
    function: Calculate the cumulative distribution function of the log-normal distribution
    :param x: The value of the random variable
    :param x_0: The offset parameter, x > x_0
    :param mx: The mean value of the log-normal distribution, mx > x_0
    :param sig_x: The standard deviation of the log-normal distribution
    :return: The probability of the random variable, The mean value of the corresponding normal distribution,
            The standard deviation of the corresponding normal distribution
    """
    x = math.log(x - x_0)
    mu = math.log(mx - x_0) - 0.5 * math.log(1 + (sig_x / (mx - x_0)) ** 2)
    sig_u = math.sqrt(math.log(1 + (sig_x / (mx - x_0)) ** 2))
    q = nor_cdf(x, mu, sig_u)
    return q, mu, sig_u


def log_nor_cdf_inv(x_0, q, mu, sig_u):
    """
    function: Calculate the inverse of cumulative distribution function of the log-normal distribution
    :param x_0: The offset parameter, x > x_0
    :param q: The probability of the random variable
    :param mu: The mean value of the corresponding normal distribution
    :param sig_u: The standard deviation of the corresponding normal distribution
    :return: The corresponding random variable
    """
    x = st_nor_cdf_inv(q)
    x = x_0 + math.exp(mu + sig_u * x)
    return x


def exp_cdf(x, mx, sig_x):
    """
    function: Calculate the cumulative distribution function of the exponential distribution
    :param x: The value of the random variable, x >= x_0
    :param mx: The mean value of the exponential distribution
    :param sig_x: The standard deviation of the exponential distribution
    :return: The probability of the random variable, The rate parameter(b > 0),
            The offset parameter also location parameter(x > x_0)
    """
    b = 1 / sig_x
    x0 = mx - 1 / b
    q = 1 - math.exp(-b * (x - x0))
    return q, b, x0


def exp_cdf_inv(q, b, x0):
    """
    function: Calculate the inverse of cumulative distribution function of the exponential distribution
    :param q: The probability of the random variable
    :param b: The rate parameter(b > 0)
    :param x_0: The offset parameter also location parameter(x >= x_0)
    :return: The corresponding random variable           
    """
    x = x0 - 1 / b * math.log(1 - q)
    return x


def uni_pdf(x, a, b):
    """
    function: Calculate the cumulative distribution function of the uniform distribution
    :param x: The value of a random variable
    :param a: The lower limit of the uniform distribution interval
    :param b: The upper limit of the uniform distribution interval
    :return:  The pdf of the random variable
    """
    if b <= a:
        raise ValueError("Upper limit(b) must be greater than lower limit(a)")
    if x < a or x > b:
        return 0.0
    else:
        pdf = 1 / (b - a)
    return pdf


def st_n_pdf(x):
    """
    function: Calculate the approximation of the pdf of the standard normal distribution
    :param x: The value of random variable
    :return:  The pdf of the random variable
    """
    pdf = 1 / math.sqrt(2 * math.pi) * math.exp(-1 * (x ** 2) / 2)
    return pdf


def n_pdf(x, mx, sig):
    """
    function: Calculate the pdf of the normal distribution
    :param x: The value of random variable
    :param mx: The mean value of the normal distribution
    :param sig: The standard deviation of the normal distribution
    :return: The pdf of the random variable
    """
    pdf = (1 / sig * math.sqrt(2 * math.pi)) * math.exp(-1 / 2 * ((x - mx)/ sig) ** 2)
    return pdf

def log_n_pdf(x, x_0, mx, sig_x):
    """
    function: Calculate the pdf of the log-normal distribution
    :param x: The value of the random variable
    :param x_0: The offset parameter
    :param mx: The mean value of the log-normal distribution
    :param sig_x: The standard deviation of the log-normal distribution
    :return: The pdf of the random variable
    """
    mu = math.log(mx - x_0) - 0.5 * math.log(1 + (sig_x / (mx - x_0)) ** 2)
    sig_u = math.sqrt(math.log(1 + (sig_x / (mx - x_0)) ** 2))
    x = (math.log(x - x_0) - mu) / sig_u
    pdf = st_n_pdf(x)
    return pdf


def e_pdf(x, mx, sig_x):
    """
    function: Calculate the pdf of the exponential distribution
    :param x: The value of the random variable, x >= x_0
    :param mx: The mean value of the exponential distribution
    :param sig_x: The standard deviation of the exponential distribution
    :return: The pdf of the random variable
    """
    b = 1 / sig_x
    x0 = mx - 1 / b
    pdf = b * math.exp(-b * (x - x0))
    return pdf


def main():

    print("The description of the following number:\n"
        "1:Uniform , 2:Standard Normal, 3:Normal, 4:Log-Normal, 5:Exponential"
    )
    number = input("Which distrubution you want to realize: ")
    if number == "1":
        x = float(input("The value of a random variable(x): "))
        a = float(input("The lower limit of the uniform distribution interval(a): "))
        b = float(input("The upper limit of the uniform distribution interval(b): "))
        pdf = uni_pdf(x, a, b)
        q = uniform_cdf(x, a, b)
        x = uniform_cdf_inv(q, a, b)
        print(f"uniform_cdf: {q}")
        print(f"uniform_cdf_inv: {x}")
        print(f"uni_pdf: {pdf}")
    elif number == "2":
        x = float(input("The value of a random variable(x): "))
        pdf = st_n_pdf(x)
        q = st_nor_cdf(x)
        x = st_nor_cdf_inv(q)
        print(f"st_nor_cdf: {q}")
        print(f"st_nor_cdf_inv: {x}")
        print(f"st_n_pdf: {pdf}")
    elif number == '3':
        x = float(input("The value of a random variable(x): "))
        mx = float(input("The mean value of the normal distribution(mx): "))
        sig = float(input("The standard deviation of the normal distribution(sig): "))
        pdf = n_pdf(x, mx, sig)
        q = nor_cdf(x, mx, sig)
        x = nor_cdf_inv(q, mx, sig)
        print(f"nor_cdf: {q}")
        print(f"nor_cdf_inv: {x}")
        print(f"n_pdf: {pdf}")
    elif number == '4':
        x = float(input("The value of a random variable(x): "))
        x_0 = float(input("The offset parameter(x_0, x > x_0): "))
        mx = float(input("The mean value of the log-normal distribution(mx, mx > x_0): "))
        sig_x = float(input("The standard deviation of the log-normal distribution(sig_x): "))
        pdf = log_n_pdf(x, x_0, mx, sig_x)
        q, mu, sig_u = log_nor_cdf(x, x_0, mx, sig_x)
        x = log_nor_cdf_inv(x_0, q, mu, sig_u)
        print(f"log_nor_cdf: {q, mu, sig_u}")
        print(f"log_nor_cdf_inv: {x}")
        print(f"log_n_pdf: {pdf}")
    elif number == '5':
        x = float(input("The value of a random variable(x): "))
        mx = float(input("The mean value of the exponential distribution(mx): "))
        sig_x = float(input("The standard deviation of the exponential distribution(sig_x): "))
        pdf = e_pdf(x, mx, sig_x)
        q, b, x0 = exp_cdf(x, mx, sig_x)
        x = exp_cdf_inv(q, b, x0)
        print(f"exp_cdf: {q}")
        print(f"exp_cdf_inv: {x}")
        print(f"e_pdf: {pdf}")


def ini_data():
    data = {
        "limit_state_function": lambda x1, x2: x2 - x1,  # Linear limit state function: X2 - X1 = 0
        "mean_value": [288, 288],  # Underling distribution mean value
        "sigma_1": 26.4,  # Standard deviation for underlying pdf and box size
        "sigma_2": 26.4,  # Standard deviation for underlying pdf and box size
        "starting_point": [540, 100], # Starting point for the simulation
        "distribution1": "3",  # Sampling distribution for x1
        "distribution2": "3",  # Sampling distribution for x2
        "num_samples": 100,  # Number of samples per step
        "num_steps": 100, # Number of steps in the simulation
        "num_box_sample": 50  # Number of samples insider or outside the box
    }
    return data


def limit_state_function(x1, x2):
    g = x2 - x1
    return g
#     g = x2 - 1/3 * x1


def indicator_function(data):
    x1, x2 = data[0], data[1]
    I = []
    for x1, x2 in zip(x1, x2):
        if limit_state_function(x1, x2) < 0:
            I_value = 1
            I.append(I_value)
        else:
            I_value = 0
            I.append(I_value)
    return I

    
def joint_pdf(pdf1, pdf2):
    f = pdf1 * pdf2
    return f


def importance_sampling_pdf(h, step):
    hx = []    
    cumulative_h = [0] * len(h[0]) 
    for i in range(step):
        cumulative_h = [cumulative_h[j] + h[i][j] for j in range(len(h[i]))] 
        hx.append(cumulative_h[:]) 
    return hx


def I_mult_f(f, I):
    I_f = [[(i * fj) for i, fj in zip(I_sublist, f_sublist)]
              for I_sublist, f_sublist in zip(I, f)]
    return I_f


def I_f_accum(I_f,step):
    If_x = []    
    cumulative_If = [0] * len(I_f[0]) 
    for i in range(step):
        cumulative_If = [cumulative_If[j] + I_f[i][j] for j in range(len(I_f[i]))] 
        If_x.append(cumulative_If[:])  
    return If_x


def failure_probability(step, If_x, hx):
    pf_values = []
    for i in range(step):
        pf = 0
        n_all = 100 * (i+1)
        for j in range(100):
            pf += (If_x[i][j]/(1/(i + 1) * hx[i][j]))
        pf = pf/n_all
        pf_values.append(pf)
    return pf_values


def sample_generation(x1_axis, x2_axis, distribution1, distribution2, n, max_point=None):

    n = int(n)
    rand = [random.random() for _ in range(n)]

    pdf1 = []
    pdf2 = []

    if distribution1 == "2":
        distribution1 = "Standard Normal"
        for element in rand:
            q = float(element)
            x1 = st_nor_cdf_inv(q)
            x1_axis.append(x1)
            pdf1.append(st_n_pdf(x1))

    elif distribution1 == "3":
        distribution1 = "Normal"
        mx = max_point[0]
        # sig = 3
        sig = ini_data()['sigma_1']
        for element in rand:
            q = float(element)
            x1 = nor_cdf_inv(q, mx, sig)
            x1_axis.append(x1)
            # pdf1.append(n_pdf(x1, 20, 3))
            pdf1.append(n_pdf(x1, ini_data()['mean_value'][0], ini_data()['sigma_1']))

    elif distribution1 == "4":
        distribution1 = "Log Normal"
        x_0 = float(input("The offset parameter(x_0, x > x_0): "))
        mu = float(input("The mean value of the log-normal distribution(mu): "))
        sig_u = float(input("The standard deviation of the log-normal distribution(sig_u): "))
        for element in rand:
            q = float(element)
            x1 = log_nor_cdf_inv(x_0, q, mu, sig_u)
            x1_axis.append(x1)
            pdf1.append(log_n_pdf(x1, x_0, mu, sig_u))

    elif distribution1 == "5":
        distribution1 = "Exponential"
        b = float(input("The rate parameter(b > 0): "))
        x_0 = float(input("The offset parameter also location parameter(x > x_0): "))
        for element in rand:
            q = float(element)
            x1 = exp_cdf_inv(q, b, x_0)
            x1_axis.append(x1)
            pdf1.append(e_pdf(x1, b, x_0))

    rand = [random.random() for _ in range(n)]

    if distribution2 == "2":
        distribution2 = "Standard Normal"
        for element in rand:
            q = float(element)
            x2 = st_nor_cdf_inv(q)
            x2_axis.append(x2)
            pdf2.append(st_n_pdf(x2))

    elif distribution2 == "3":
        distribution2 = "Normal"
        mx = max_point[1]
        # sig = 3
        sig = ini_data()['sigma_2']
        for element in rand:
            q = float(element)
            x2 = nor_cdf_inv(q, mx, sig)
            x2_axis.append(x2)
            # pdf2.append(n_pdf(x2, 10, 3))
            pdf2.append(n_pdf(x2, ini_data()['mean_value'][1], ini_data()['sigma_2']))

    elif distribution2 == "4":
        distribution2 = "Log Normal"
        x_0 = float(input("The offset parameter(x_0, x > x_0): "))
        mu = float(input("The mean value of the log-normal distribution(mu): "))
        sig_u = float(input("The standard deviation of the log-normal distribution(sig_u): "))
        for element in rand:
            q = float(element)
            x2 = log_nor_cdf_inv(x_0, q, mu, sig_u)
            x2_axis.append(x2)
            pdf2.append(log_n_pdf(x2, x_0, mu, sig_u))

    elif distribution2 == "5":
        distribution2 = "Exponential"
        b = float(input("The rate parameter(b > 0): "))
        x_0 = float(input("The offset parameter also location parameter(x > x_0): "))
        for element in rand:
            q = float(element)
            x2 = exp_cdf_inv(q, b, x_0)
            x2_axis.append(x2)
            pdf2.append(e_pdf(x2, b, x_0))
    
    # Calculate joint pdf values
    f = [joint_pdf(p1, p2) for p1, p2 in zip(pdf1, pdf2)]

    return x1_axis, x2_axis, f


def find_max_joint_pdf1(data):
    x2, y2 = data[0], data[1]
    joint_pdf_value = data[2]
    max_joint_pdf = max(joint_pdf_value)
    max_point = (x2[joint_pdf_value.index(max_joint_pdf)], y2[joint_pdf_value.index(max_joint_pdf)])
    return max_point, max_joint_pdf, joint_pdf_value


def find_max_joint_pdf2(data, distribution1, distribution2):
    x1, y1 = data[0], data[1]
    pdf1 = []
    pdf2 = []
    if distribution1 == "3":
        distribution1 = "Normal"
        for xi in x1:
            # pdf1.append(n_pdf(xi, 20, 3))
            pdf1.append(n_pdf(xi, ini_data()['mean_value'][0], ini_data()['sigma_2']))
    if distribution2 == "3":
        distribution2 = "Normal"
        for yi in y1:
            # pdf2.append(n_pdf(yi, 10, 3))
            pdf2.append(n_pdf(yi, ini_data()['mean_value'][0], ini_data()['sigma_2']))
    joint_pdf_value = [joint_pdf(p1, p2) for p1, p2 in zip(pdf1, pdf2)]
    max_joint_pdf = max(joint_pdf_value)
    max_point = (x1[joint_pdf_value.index(max_joint_pdf)], y1[joint_pdf_value.index(max_joint_pdf)])
    return max_point, max_joint_pdf, joint_pdf_value



