import csv
from classes import *

def read_file (file_path, patient_class):
    # patient_object = None
    hourly_data = list()
    
    # handles file read
    with open(file_path, 'r') as csv_file:
        line_read = csv.reader(csv_file, delimiter=',')

        for row in line_read: 
            if(row):
                pass
            elif("PATIENT" in row[PATIENT]): # if curent column has patient information we add it to the patients class
                patient_object = patient_class(row) #initialise object as patient
                # print("found it and adding to patient class" + str(row) + "\n")
            else :
                hourly_data.append(row) #adding all row to array 

    patient_object.set_data(hourly_data)
    return patient_object  

if __name__ == "__main__":
    path ="/Users/juanestebanvargassalamanca/Desktop/Desktop – Juan’s MacBook Pro/UNI/Computer_Science /2nd_Year/Algorithm_DataStructures_(Python) /ASSIGNMENT_2/patients_csv/PATIENT DATA - PATIENT B1.csv"
    hourly_data = read_file(path, Patient)
    print(hourly_data.get_data())
    