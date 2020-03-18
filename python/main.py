from functions import read_file
from classes import Patient

patient1_path = "/Users/juanestebanvargassalamanca/Desktop/Desktop – Juan’s MacBook Pro/UNI/Computer_Science /2nd_Year/Algorithm_DataStructures_(Python) /ASSIGNMENT_2/patients_csv/PATIENT DATA - PATIENT B1.csv"


if __name__ == "__main__":
    print ("reading patient row")
    read_file(patient1_path, Patient)
    