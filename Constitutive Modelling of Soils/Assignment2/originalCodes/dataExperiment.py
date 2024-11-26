import numpy as np


# TMD and TMU experimental data loading
def expData():
    expData1 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_2/TMD2_dense.txt")
    expData2 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_2/TMD2_loose.txt")
    expData3 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_2/TMD3_dense.txt")
    expData4 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_2/TMD3_loose.txt")
    expData5 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_2/TMD4_dense.txt")
    expData6 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_2/TMD4_loose.txt")
    expData7 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_2/TMU1.txt")
    expData8 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_2/TMU2.txt")
    expData9 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_2/TMU3.txt")

    return expData1, expData2, expData3, expData4, expData5, expData6, expData7, expData8, expData9