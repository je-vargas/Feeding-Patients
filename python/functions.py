import csv
from classes import *

def read_file (file_path, patient_class):
    '''
        returns : the object where all data read from csv is saved
    '''
    # patient_object = None
    hourly_data = list()
    
    # handles file read
    with open(file_path, 'r') as csv_file:
        line_read = csv.reader(csv_file, delimiter=',')

        for row in line_read: 
            if("DAY" in row or row[TIME_RISK] == "" ):
                pass # pass rows with no data
            elif("PATIENT" in row[DAY_PATIENT]): # if curent column has patient information we add it to the patients class
                patient_object = patient_class(clean_up_string(row)) #initialise object as patient
                # print("found it and adding to patient class" + str(row) + "\n")
                # print(clean_up_string(row)

            else: # gets all the hourly rows
                hourly_data.append(row) #adding all row to array 
                if(row[DAY_PATIENT]== "1" and "00:00" in row[TIME_RISK]): #gets only days that contain a day
                    print(row)
                    print("this value is being passed: " + str(clean_up_feed(row)))
                    patient_class.set_feed(patient_class, clean_up_feed(row))
               

    patient_object.set_data(hourly_data) #save hourly data inside the object
    return patient_object

def low_risk_blanks(patient_passed):
    day_data = patient_passed.get_data() #returns the array with hourly data
    
    for row in day_data:
        hour = int(row[TIME_RISK][:2]) # this returns hour in format 0-23

        # feed every 2 hours
        if(hour % 2 == 0 and row[FEED_AGE] == ""): # here we are feeding every 2 hours as per flowchart
            row[FEED_AGE] = patient_passed.get_feed()

            # check every four house and adjust GRV
            if (hour % 4 == 0 and hour != 00):
                target_grv = str(patient_passed.get_target_grv())

                if(patient_passed.get_weight() < 40 and row[GRV] < target_grv):
                    if(patient_passed.get_feed() == 5 or patient_passed.get_feed == 20):
                        
                        patient_passed.set_feed_increment()
                    
                else:
                     pass 
                 

    patient_passed.set_data(day_data)


def clean_up_string(patient_info):
    cleaned_data = list()
    risk = patient_info[TIME_RISK]
    age = [int(i) for i in patient_info[FEED_AGE].split() if i.isdigit()]
    weight = [int(i) for i in patient_info[ISSUES_WEIGHT].split() if i.isdigit()]

    cleaned_data.append(age[0])
    cleaned_data.append(weight[0])
    cleaned_data.append(risk)

    print("cleaned data is: " + str(cleaned_data))
    return cleaned_data

def clean_up_feed(feed_row):
    feed_joined = ''.join(filter(lambda i: i.isdigit(), feed_row[FEED_AGE]))
    feed_length = len(feed_joined) - 1
    feed_to_return = feed_joined[0:feed_length]
    return feed_to_return
        

if __name__ == "__main__":
    path ="/Users/juanestebanvargassalamanca/Desktop/Desktop – Juan’s MacBook Pro/UNI/Computer_Science /2nd_Year/Algorithm_DataStructures_(Python) /ASSIGNMENT_2/patients_csv/PATIENT DATA - PATIENT B1.csv"
    object_returned = read_file(path, Patient)
    low_risk_blanks(object_returned)
    print(object_returned.get_data())

    print(object_returned.get_feed())
