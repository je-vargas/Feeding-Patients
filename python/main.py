'''
File: DADSA Coursework_B
Author: Juan Esteban Vargas Salamanca
Date: 22/04/2020
Description: ALl Code is run from here
'''


from functions import *
from classes import *

patient1_path = "/Users/juanestebanvargassalamanca/Desktop/Desktop – Juan’s MacBook Pro/UNI/Computer_Science /2nd_Year/Algorithm_DataStructures_(Python) /ASSIGNMENT_2/patients_csv/PATIENT DATA - PATIENT B1.csv"


if __name__ == "__main__":

    patient_objects = [Patient() for i in range(len(CSV_PATHS))]
    order_patient_files = ["Patient A1", "Patient A2", "Patient A3", "Patient B1", "Patient B2", "Patient B3", "Patient B4", "Patient B5", "Patient B6", "Patient B7"]
    end_day_diagnosis = list()
   
    for i in range(len(CSV_PATHS)):
        start_of_patient_diagnosis(CSV_PATHS[i], patient_objects[i])
        end_day_diagnosis.append(patient_objects[i].get_week_diagnosis())

    day_to_day_diagnosis_print(patient_objects, order_patient_files) # prints all patiets end of day diagnosis sequencially as required
    complete_sort(order_patient_files, end_day_diagnosis)   
    
    