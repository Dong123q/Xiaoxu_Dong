"""
This file is used to load the experimental data for the assignment 3.
"""

import numpy as np


# TMD and TMU experimental data loading
def expData():
    expData1 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_3/isoCompression.txt")
    expData2 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_3/cd_ev-1.txt")
    expData3 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_3/cd_ev-2.txt")
    expData4 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_3/cd_ev-4.txt")
    expData5 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_3/cd_ev-31.txt")
    expData6 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_3/cd_ev-32.txt")
    expData7 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_3/cd_q-1.txt")
    expData8 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_3/cd_q-2.txt")
    expData9 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_3/cd_q-4.txt")
    expData10 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_3/cd_q-31.txt")
    expData11 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_3/cd_q-32.txt")
    expData12 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_3/cu_100.txt")
    expData13 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_3/cu_200.txt")
    expData14 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_3/cu_400.txt")

    return expData1, expData2, expData3, expData4, expData5, expData6, expData7, expData8, expData9, expData10, expData11, expData12, expData13, expData14

def cd():
    expData2 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_3/cd_ev-1.txt")
    expData3 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_3/cd_ev-2.txt")
    expData4 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_3/cd_ev-4.txt")
    expData5 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_3/cd_ev-31.txt")
    expData6 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_3/cd_ev-32.txt")
    expData7 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_3/cd_q-1.txt")
    expData8 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_3/cd_q-2.txt")
    expData9 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_3/cd_q-4.txt")
    expData10 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_3/cd_q-31.txt")
    expData11 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_3/cd_q-32.txt")

    return expData2, expData3, expData4, expData5, expData6, expData7, expData8, expData9, expData10, expData11

def cu():
    expData12 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_3/cu_100.txt")
    expData13 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_3/cu_200.txt")
    expData14 = np.loadtxt("D:/selfLearning_programming/constitutive_modeling_soils/assignment/assignment_3/cu_400.txt")

    return expData12, expData13, expData14