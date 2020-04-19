import csv
import re
from classes import *

def read_file(file_path, patient_object):
    '''
        DESCRIPTION: populates age, weight, risk, target_grv and diagnosies found from file
        Additioanl info: calls clean_up_string function to clean the data saved into the object

    '''
    hourly_data = list()
    
    # handles file read
    with open(file_path, 'r') as csv_file:
        line_read = csv.reader(csv_file, delimiter=',')

        for current_row in line_read: 
            if("DAY" in current_row or current_row[TIME_RISK] == "" ):
                pass # pass current_rows with no data
            elif("PATIENT" in current_row[DAY_PATIENT]): # if curent column has patient information we add it to the patients class
                patient_object.set_age(clean_up_string(current_row)) #initialise object as patient
                patient_object.set_weight(clean_up_string(current_row)) #initialise object as patient
                patient_object.set_risk(clean_up_string(current_row)) #initialise object as patient
            else: # gets all the hourly current_rows
                if(current_row[DAY_PATIENT]== "1" and "00:00" in current_row[TIME_RISK]): #gets only days 1 as this holds patient feeding info
                    set_feed_HR_LR(patient_object, current_row)
                    patient_object.set_diagnosis(current_row[ISSUES_WEIGHT])
                    patient_object.set_target_grv()
                    current_row[FEED_AGE] = patient_object.get_feed()

                    adjust_new_feed_low_risk(patient_object, current_row)

                hourly_data.append(current_row) #adding all current_row to array 
    
    patient_object.set_data(hourly_data) #save hourly data inside the object

def low_risk_patients(patient_passed):
    '''
        DESCRIPTION: Follows low risk patient flowchart, populating patient feeds 
    '''
    # ------------- function variables declaration
    day_data = patient_passed.get_data() #returns the array with hourly data
    target_grv = int(patient_passed.get_target_grv()) #use target_grv as a measure to either increase feed or stop feeding
    # ------------- Loop over passed patient data
   
    for current_row in day_data:

        if (str(patient_passed.get_risk()) == "HR" and current_row[GRV] == ""):
            #ignoers rows where there is not grv for HR patients!
           pass
    
        else:
            hour = int(current_row[TIME_RISK][:2]) # this returns hour in format 0-23
            current_grv = current_grv_integer_cleaned(current_row) # returns the current grv as an integer
            
            if(hour % 2 == 0 or (hour % 2 == 1 and current_row[GRV] != "")): # this is using the hours to check either every 2 or 4 hours to populate

                if(patient_passed.get_feed_stopped_boolean()):
                    feeding_stopped_low_risk(patient_passed, current_row, current_grv, target_grv) # called only when feeding is stopped
                else:
                    adjust_new_feed_low_risk(patient_passed, current_row) #need to feed every 2 hour or check depeding on flowchart and patient

                if(patient_passed.get_risk() == "HR" and not patient_passed.get_feed_stopped_boolean()):
                    patient_passed.set_current_grv(current_grv) # set new grv read from the data as you read each hour
                    current_vs_target_grv_checker(patient_passed, current_row, current_grv, target_grv, 10)
                
                if(hour % 4 == 0 and not patient_passed.get_feed_stopped_boolean()): # check every four hours and adjust GRV

                    patient_passed.set_current_grv(current_grv) # set new grv read from the data as you read each hour
                                
                    if(patient_passed.get_weight() < 40 ): #patient weight is under 40

                        current_vs_target_grv_checker(patient_passed, current_row, current_grv, target_grv, 10)

                    else: #patient weight is over 40
                        current_vs_target_grv_checker(patient_passed, current_row, current_grv, target_grv, 30)
 
    weekly_diagnosis(day_data, patient_passed) # this needs to be fixed

    patient_passed.set_data(day_data)    

def high_risk_patients(patient_object):

    day_data = patient_object.get_data()
    
    for current_row in day_data:

        if(current_row[GRV] == "" and not patient_object.get_low_risk_transfer_bool()): #checks to see if there's a grv value -> in which case transfer to low risk 
            # continue with high risk flowchart rules
            if(str(current_row[FEED_AGE]) != str(patient_object.get_feed()) and current_row[FEED_AGE] != ""):
                #check if feeding has changed -> if so set new feed in object with function call
                patient_object.set_change_feed_bool(True)
                adjust_new_feed_high_risk(patient_object, current_row)
            else: #otherwise keep feeding hourly feeds
                patient_object.set_change_feed_bool(False)
                adjust_new_feed_high_risk(patient_object, current_row)
        else:
            # passed to become low risks
            patient_object.set_low_risk_transfer_bool(True)
            break

    if(patient_object.get_low_risk_transfer_bool()):
        print(current_row)
        patient_object.set_feed(10)
        low_risk_patients(patient_object)


def adjust_new_feed_high_risk(patient_passed, row_passed):

    # new_feed_found = patient_passed.get_feed()

    if(patient_passed.get_change_feed_bool()):
        patient_passed.set_feed(clean_up_feed_high_risk(row_passed))
        row_passed[FEED_AGE] = patient_passed.get_feed()
    elif(row_passed[ISSUES_WEIGHT] == 'NONE'):
        row_passed[FEED_AGE] = patient_passed.get_feed()



def adjust_new_feed_low_risk(patient_passed, row_passed):
    '''
        Description: set feed increments, pauses and normal feeds of patient from original value giving in the CSV file for LOW RISK patients
    '''

    stop_feeding = patient_passed.get_feed_stopped_boolean()
             
    if(stop_feeding):
        #current grv higher than target, therefore stop feeding

        if(patient_passed.get_dietician_referal_bool() and row_passed[GRV] != ""):
            row_passed[FEED_AGE] = "No Update in the Feed "
            row_passed[ISSUES_WEIGHT] = "Refer to Dietician"
            # patient_passed.set_dietician_referal_bool(False)
            # print(str(patient_passed.get_feed_stopped()))
                         
        elif(row_passed[GRV] != ""):
            row_passed[FEED_AGE] = "No Feeding"
            row_passed[ISSUES_WEIGHT] = "Feeding Stopped"
        
    else:
        row_passed[FEED_AGE] = patient_passed.get_feed()
        row_passed[ISSUES_WEIGHT] = patient_passed.get_diagnosis()

def reset_counter_after_referal(patient_passed):
    '''
        Description: allows referal to dietician once counter is 3 and resets counter to 0
    '''
    patient_passed.set_reset_counter_bool(True)
    patient_passed.set_feed_stop_counter(0)
    patient_passed.set_dietician_referal_bool(False)
    patient_passed.set_reset_counter_bool(False)

def weekly_diagnosis(day_data, current_paitient):

    '''
        Descritpion: saves 5 day week diagnosis of the patient to the patients object 
    '''
    day = 0
    weekly_diagnosis = ["None"] * 5
    
    for current_row in day_data:
        if (current_row[DAY_PATIENT] != "" ):
            day = int(current_row[DAY_PATIENT]) - 1

        if("Refer" in current_row[ISSUES_WEIGHT]):
            weekly_diagnosis[day] = (current_row[ISSUES_WEIGHT])
        elif("Feeding" in current_row[ISSUES_WEIGHT] and "22" in current_row[TIME_RISK]):
            weekly_diagnosis[day] = (current_row[ISSUES_WEIGHT])
        elif("22" in current_row[TIME_RISK] and current_row[ISSUES_WEIGHT] != ""):
            weekly_diagnosis[day] = (current_row[ISSUES_WEIGHT])

    current_paitient.set_week_diagnosis(weekly_diagnosis)

def clean_up_string(patient_info):
    cleaned_data = list()
    risk = patient_info[TIME_RISK]
    age = [int(i) for i in patient_info[FEED_AGE].split() if i.isdigit()]
    weight = [int(i) for i in patient_info[ISSUES_WEIGHT].split() if i.isdigit()]

    cleaned_data.append(age[0])
    cleaned_data.append(weight[0])
    cleaned_data.append(risk)

    # print("cleaned data is: " + str(cleaned_data))
    return cleaned_data

def clean_up_feed_low_risk(feed_current_row):

    '''
        Description: Feed is integer with quantity in ml, this function cleans and returns the number only
    '''

    feed_joined = ''.join(filter(lambda i: i.isdigit(), feed_current_row[FEED_AGE]))
    feed_length = len(feed_joined) - 1
    feed_to_return = int(feed_joined[0:feed_length])
    return feed_to_return

def clean_up_feed_high_risk(feed_current_row):

    '''
        Description: Feed is integer with quantity in ml, this function cleans and returns the number only
    '''
    feed_into_array = re.findall(r"[-+]?\d*\.\d+|\d+", feed_current_row[FEED_AGE])
    if feed_into_array[0].isdigit():
        feed_to_return = int(feed_into_array[0])
    else:
        feed_to_return = float(feed_into_array[0])
    return feed_to_return
        
def current_grv_integer_cleaned(row):
    current_grv = 0
    if (row[GRV] != "GRV" and row[GRV] != ""):
            current_grv = int(float(row[GRV]))
    return current_grv

def set_feed_HR_LR(patient_object, row_read):
    if(patient_object.get_risk() == "HR"):
        patient_object.set_feed(clean_up_feed_high_risk(row_read))
        # patient_object.set_feed(row_read[FEED_AGE])
    else:
        patient_object.set_feed(clean_up_feed_low_risk(row_read)) # this to set the feeding attribute in patient object

def feeding_stopped_low_risk(patient_passed, current_row,current_grv, target_grv):
    '''
        Description: handles all the event when the feeding is stoped for a patients
    '''
    patient_passed.set_current_grv(current_grv)

    if(patient_passed.get_dietician_referal_bool()):
        reset_counter_after_referal(patient_passed)

    if(current_grv > target_grv and current_row[GRV] != ""): 
        patient_passed.set_feed_stop_counter()
        adjust_new_feed_low_risk(patient_passed, current_row)
        
    elif(patient_passed.get_weight() < 40): #current target is less so increment feed and the grv is present
        patient_passed.set_feed_increment_boolean(True)
        patient_passed.set_feed_stopped_boolean(False)
        patient_passed.set_feed(10)
        adjust_new_feed_low_risk(patient_passed, current_row)
        reset_counter_after_referal(patient_passed)
    else:
        patient_passed.set_feed_increment_boolean(True)
        patient_passed.set_feed_stopped_boolean(False)
        patient_passed.set_feed(30)
        adjust_new_feed_low_risk(patient_passed, current_row)
        reset_counter_after_referal(patient_passed)

def current_vs_target_grv_checker(patient_passed, current_row, current_grv, target_grv, new_feed):

    if(current_grv <= target_grv and current_row[GRV] != "" ):  #current target is less so increment feed and the grv is present
        patient_passed.set_feed_increment_boolean(True)
        patient_passed.set_feed_stopped_boolean(False)
        patient_passed.set_feed(new_feed)
        adjust_new_feed_low_risk(patient_passed, current_row) #keeps icrementing feed until grv is over
    
    elif(current_grv > target_grv): # current target is more that target stop feeding check every 2 hours now
        patient_passed.set_feed_increment_boolean(False)
        patient_passed.set_feed_stopped_boolean(True)
        patient_passed.set_feed_stop_counter()
        adjust_new_feed_low_risk(patient_passed, current_row)

def low_risk_complete(path, patient):
    read_file(path, patient)
    low_risk_patients(patient)


if __name__ == "__main__":

    print("Low Risk")

    paths = [
        "/Users/juanestebanvargassalamanca/Desktop/Desktop – Juan’s MacBook Pro/UNI/Computer_Science /2nd_Year/Algorithm_DataStructures_(Python) /ASSIGNMENT_2/patients_csv/PATIENT DATA - PATIENT B1.csv", 
        "/Users/juanestebanvargassalamanca/Desktop/Desktop – Juan’s MacBook Pro/UNI/Computer_Science /2nd_Year/Algorithm_DataStructures_(Python) /ASSIGNMENT_2/patients_csv/PATIENT DATA - PATIENT B3.csv", 
        "/Users/juanestebanvargassalamanca/Desktop/Desktop – Juan’s MacBook Pro/UNI/Computer_Science /2nd_Year/Algorithm_DataStructures_(Python) /ASSIGNMENT_2/patients_csv/PATIENT DATA - PATIENT B5.csv", 
        "/Users/juanestebanvargassalamanca/Desktop/Desktop – Juan’s MacBook Pro/UNI/Computer_Science /2nd_Year/Algorithm_DataStructures_(Python) /ASSIGNMENT_2/patients_csv/PATIENT DATA - PATIENT B7.csv", 
        "/Users/juanestebanvargassalamanca/Desktop/Desktop – Juan’s MacBook Pro/UNI/Computer_Science /2nd_Year/Algorithm_DataStructures_(Python) /ASSIGNMENT_2/patients_csv/PATIENT DATA - PATIENT B2 (2).csv",
        "/Users/juanestebanvargassalamanca/Desktop/Desktop – Juan’s MacBook Pro/UNI/Computer_Science /2nd_Year/Algorithm_DataStructures_(Python) /ASSIGNMENT_2/patients_csv/PATIENT DATA - PATIENT B4.csv",
        "/Users/juanestebanvargassalamanca/Desktop/Desktop – Juan’s MacBook Pro/UNI/Computer_Science /2nd_Year/Algorithm_DataStructures_(Python) /ASSIGNMENT_2/patients_csv/PATIENT DATA - PATIENT B6.csv", 
        "/Users/juanestebanvargassalamanca/Desktop/Desktop – Juan’s MacBook Pro/UNI/Computer_Science /2nd_Year/Algorithm_DataStructures_(Python) /ASSIGNMENT_2/patients_csv/PATIENT DATA - PATIENT A1.csv",
        "/Users/juanestebanvargassalamanca/Desktop/Desktop – Juan’s MacBook Pro/UNI/Computer_Science /2nd_Year/Algorithm_DataStructures_(Python) /ASSIGNMENT_2/patients_csv/PATIENT DATA - PATIENT A2.csv",
        "/Users/juanestebanvargassalamanca/Desktop/Desktop – Juan’s MacBook Pro/UNI/Computer_Science /2nd_Year/Algorithm_DataStructures_(Python) /ASSIGNMENT_2/patients_csv/PATIENT DATA - PATIENT A3.csv"
    ]
    
    # path_hr = [
    #     "/Users/juanestebanvargassalamanca/Desktop/Desktop – Juan’s MacBook Pro/UNI/Computer_Science /2nd_Year/Algorithm_DataStructures_(Python) /ASSIGNMENT_2/patients_csv/PATIENT DATA - PATIENT A1.csv",
    #     "/Users/juanestebanvargassalamanca/Desktop/Desktop – Juan’s MacBook Pro/UNI/Computer_Science /2nd_Year/Algorithm_DataStructures_(Python) /ASSIGNMENT_2/patients_csv/PATIENT DATA - PATIENT A2.csv",
    #     "/Users/juanestebanvargassalamanca/Desktop/Desktop – Juan’s MacBook Pro/UNI/Computer_Science /2nd_Year/Algorithm_DataStructures_(Python) /ASSIGNMENT_2/patients_csv/PATIENT DATA - PATIENT A3.csv"
    # ]
        
    obj = [Patient() for i in range(len(paths))]

    for i in range(len(obj)):
        low_risk_complete(paths[i], obj[i])
    
        
    # patient= Patient()
    # read_file(path_, patient)
    # low_risk_patients(patient)   
    # print(patient)

    # read_file(path_, patient)
    # low_risk_patients(patient)   
    # print(patient)
    # print("\n------------- PATIENT B2 -------------")
    # print("------------- HOURLY DATA:")
    # print(patient.print_hourly_data())
    
    ''' ----------- HIGH RISK ----------- '''
    
    # patient = Patient()
    
    # print("High Risk --> A2")
    # read_file(path_, patient)
    # high_risk_patients(patient)
    # # low_risk_patients(patient)
    # print(patient)
    # print(patient.print_hourly_data())