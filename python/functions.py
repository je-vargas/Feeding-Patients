'''
File: DADSA Coursework_B
Author: Juan Esteban Vargas Salamanca
Date: 22/04/2020
Description: Function used in Sysem
'''

import csv
import re
from classes import *

CSV_PATHS = [
    "/Users/juanestebanvargassalamanca/Desktop/Desktop – Juan’s MacBook Pro/UNI/Computer_Science /2nd_Year/Algorithm_DataStructures_(Python) /ASSIGNMENT_2/patients_csv/PATIENT DATA - PATIENT A1.csv",
    "/Users/juanestebanvargassalamanca/Desktop/Desktop – Juan’s MacBook Pro/UNI/Computer_Science /2nd_Year/Algorithm_DataStructures_(Python) /ASSIGNMENT_2/patients_csv/PATIENT DATA - PATIENT A2.csv",
    "/Users/juanestebanvargassalamanca/Desktop/Desktop – Juan’s MacBook Pro/UNI/Computer_Science /2nd_Year/Algorithm_DataStructures_(Python) /ASSIGNMENT_2/patients_csv/PATIENT DATA - PATIENT A3.csv",
    "/Users/juanestebanvargassalamanca/Desktop/Desktop – Juan’s MacBook Pro/UNI/Computer_Science /2nd_Year/Algorithm_DataStructures_(Python) /ASSIGNMENT_2/patients_csv/PATIENT DATA - PATIENT B1.csv",
    "/Users/juanestebanvargassalamanca/Desktop/Desktop – Juan’s MacBook Pro/UNI/Computer_Science /2nd_Year/Algorithm_DataStructures_(Python) /ASSIGNMENT_2/patients_csv/PATIENT DATA - PATIENT B2 (2).csv",
    "/Users/juanestebanvargassalamanca/Desktop/Desktop – Juan’s MacBook Pro/UNI/Computer_Science /2nd_Year/Algorithm_DataStructures_(Python) /ASSIGNMENT_2/patients_csv/PATIENT DATA - PATIENT B3.csv",
    "/Users/juanestebanvargassalamanca/Desktop/Desktop – Juan’s MacBook Pro/UNI/Computer_Science /2nd_Year/Algorithm_DataStructures_(Python) /ASSIGNMENT_2/patients_csv/PATIENT DATA - PATIENT B4.csv",
    "/Users/juanestebanvargassalamanca/Desktop/Desktop – Juan’s MacBook Pro/UNI/Computer_Science /2nd_Year/Algorithm_DataStructures_(Python) /ASSIGNMENT_2/patients_csv/PATIENT DATA - PATIENT B5.csv",
    "/Users/juanestebanvargassalamanca/Desktop/Desktop – Juan’s MacBook Pro/UNI/Computer_Science /2nd_Year/Algorithm_DataStructures_(Python) /ASSIGNMENT_2/patients_csv/PATIENT DATA - PATIENT B6.csv",
    "/Users/juanestebanvargassalamanca/Desktop/Desktop – Juan’s MacBook Pro/UNI/Computer_Science /2nd_Year/Algorithm_DataStructures_(Python) /ASSIGNMENT_2/patients_csv/PATIENT DATA - PATIENT B7.csv"
]

def read_file(file_path, patient_object):
    '''
        DESCRIPTION: populates age, weight, risk, target_grv and diagnosies found from file
        INPUT: takes csv file path and patient object -> saves to object
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
        INPUT: Patient object passed 
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

                ''' ----- USED BY HIGH RISK ONLY ------ '''
                # patient_passed.get_risk() == "HR" and
                if(not patient_passed.get_feed_stopped_boolean()):
                    if(patient_passed.get_weight() > 40 and patient_passed.get_risk() == "LR"):
                        patient_passed.set_current_grv(current_grv) # set new grv read from the data as you read each hour
                        current_vs_target_grv_checker(patient_passed, current_row, current_grv, target_grv, 30)
                    else:
                        patient_passed.set_current_grv(current_grv) # set new grv read from the data as you read each hour
                        current_vs_target_grv_checker(patient_passed, current_row, current_grv, target_grv, 10)
                ''' ----- USED BY HIGH RISK ONLY ------ '''
                
                if(hour % 4 == 0 and not patient_passed.get_feed_stopped_boolean()): # check every four hours and adjust GRV

                    patient_passed.set_current_grv(current_grv) # set new grv read from the data as you read each hour

                    if(patient_passed.get_weight() < 40 ): #patient weight is under 40

                        current_vs_target_grv_checker(patient_passed, current_row, current_grv, target_grv, 10)

                    else: #patient weight is over 40
                        current_vs_target_grv_checker(patient_passed, current_row, current_grv, target_grv, 30)
 
    weekly_diagnosis(day_data, patient_passed) # this needs to be fixed

    patient_passed.set_data(day_data)    

def high_risk_patients(patient_object):
    '''
        DESCRIPTION: Follows High risk patient flowchart, populating patient feeds , 
                    also transfer patient over to low risk when necessary to do so as per flowchart
        INPUT: Patient object passed 
    '''

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
        patient_object.set_feed(10)
        low_risk_patients(patient_object)

def adjust_new_feed_high_risk(patient_passed, row_passed):

    '''
        DESCRIPTION: fills high risk feed of patient 
        INPUT: patient object and the current row looked at in the data --> (this one hour (row))
    '''

    if(patient_passed.get_change_feed_bool()):
        patient_passed.set_feed(clean_up_string_to_number(row_passed))
        row_passed[FEED_AGE] = patient_passed.get_feed()
    elif(row_passed[ISSUES_WEIGHT] == 'NONE'):
        row_passed[FEED_AGE] = patient_passed.get_feed()

def adjust_new_feed_low_risk(patient_passed, row_passed):
    '''
        DESCRIPTION: set feed increments, pauses and normal feeds of patient from original value giving in the CSV file for LOW RISK patients
        INPUT: patient object and the current row looked at in the data --> (this one hour (row))
    '''
    
    stop_feeding = patient_passed.get_feed_stopped_boolean()

    if(stop_feeding):
        #current grv higher than target, therefore stop feeding
        stop_printing_feed(patient_passed)

        if(patient_passed.get_dietician_referal_bool() and row_passed[GRV] != ""):
            row_passed[FEED_AGE] = "No Update in the Feed "
            row_passed[ISSUES_WEIGHT] = "Refer to Dietician"
                         
        elif(row_passed[GRV] != ""):
            row_passed[FEED_AGE] = "No Feeding"
            row_passed[ISSUES_WEIGHT] = "Feeding Stopped"
        
    elif(not patient_passed.get_stop_printing_feed_data()):
        row_passed[FEED_AGE] = patient_passed.get_feed()
        row_passed[ISSUES_WEIGHT] = patient_passed.get_diagnosis()

def reset_counter_after_referal(patient_passed):
    '''
        DESCRIPTION: allows referal to dietician once counter is 3 and resets counter to 0
        INPUT: Patient object

    '''
    patient_passed.set_reset_counter_bool(True)
    patient_passed.set_feed_stop_counter(0)
    patient_passed.set_dietician_referal_bool(False)
    patient_passed.set_reset_counter_bool(False)

def weekly_diagnosis(day_data, current_patient):

    '''
        DESCRIPTION: saves 5 day week diagnosis of the patient to the patients object 
        INPUT: patient object, and array contatining all the day feeds
    '''
    array_index = 0
    weekly_diagnosis = ["Populate"] * 5
    current_diagnosis = "change"

    if(current_patient.get_risk() == "LR"):
        
        for current_row in day_data:

            hour = int(current_row[TIME_RISK][:2]) # this returns hour in format 0-23
            
            if(current_row[ISSUES_WEIGHT] != ""):
                current_diagnosis = current_row[ISSUES_WEIGHT]
            
            if(current_row[DAY_PATIENT] == "5" and current_row[ISSUES_WEIGHT] == ""):
                current_diagnosis = "NONE"

            if(hour == 22):
                weekly_diagnosis[array_index] = current_diagnosis
                array_index += 1

    else:
        for current_row in day_data:

            hour = int(current_row[TIME_RISK][:2]) # this returns hour in format 0-23
            
            if(current_row[ISSUES_WEIGHT] != ""):
                current_diagnosis = current_row[ISSUES_WEIGHT]

            if(hour == 23):
                weekly_diagnosis[array_index] = current_diagnosis
                array_index += 1


    current_patient.set_week_diagnosis(weekly_diagnosis)

def clean_up_string(patient_info):

    '''
        DESCRIPTION: used when reading the file to save patient weight, age, and risk in a cleaned format
        INPUT: patient object
        OUTPUT: array containing cleaned data
    '''

    cleaned_data = list()
    risk = patient_info[TIME_RISK]
    age = clean_up_string_to_number(patient_info[FEED_AGE])
    weight = clean_up_string_to_number(patient_info[ISSUES_WEIGHT])


    cleaned_data.append(age)
    cleaned_data.append(weight)
    cleaned_data.append(risk)


    # print("cleaned data is: " + str(cleaned_data))
    return cleaned_data

def clean_up_string_to_number(string_passed):

    '''
        DESCRIPTION: Feed is integer with quantity in ml, this function cleans and returns the number only
        INPUT: String to be cleaned passed
        OUTPUT: return array contatining the cleaned data
    '''
    feed_into_array = re.findall(r"[-+]?\d*\.\d+|\d+", str(string_passed))

    if feed_into_array[0].isdigit():
        feed_to_return = int(feed_into_array[0])
    else:
        feed_to_return = float(feed_into_array[0])

    return feed_to_return
        
def current_grv_integer_cleaned(row):
    '''
        DESCRIPTION: makes the grv an integer to sav
        INPUT: row read in loop as you itereate over hourly data
        OUTPUT: the GRV returned as an integer

    '''
    current_grv = 0
    if (row[GRV] != "GRV" and row[GRV] != ""):
            current_grv = int(float(row[GRV]))
    return current_grv

def set_feed_HR_LR(patient_object, row_read):
    '''
        DESCRIPTION: used in reading file function to direct object to be processed by high risk algorithm or low risk algorithm
        INPUT: patient object and row read in loop 
    '''
    
    if(patient_object.get_risk() == "HR"):
        patient_object.set_feed(clean_up_string_to_number(row_read[FEED_AGE]))
    else:
        patient_object.set_feed(clean_up_string_to_number(row_read[FEED_AGE])) # this to set the feeding attribute in patient object

def feeding_stopped_low_risk(patient_passed, current_row,current_grv, target_grv):
    '''
        DESCRIPTION: handles all the event when the feeding is stoped for a patients
        INPUT:  patient object, row read in loop, grv and target grv to 
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

    '''
        DESCRIPTION: handles  event when grv is less than target or vice versa 
        INPUT:  patient object, row read in loop, grv,  target grv and new feed to set the increment to
    '''

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

def assign_patient_based_on_risk(patient_object):
    '''
        DESCRIPTION: controlls whether a patient is passed into the high risk or low risk algorithm 
        INPUT:  patient object
    '''
    if(patient_object.get_risk() == "HR"):
        high_risk_patients(patient_object)
    else:
        low_risk_patients(patient_object)

def start_of_patient_diagnosis(path, patient):
    '''
        Description: entry point of system
    '''
    read_file(path, patient)
    assign_patient_based_on_risk(patient)

def stop_printing_feed(patient_passed):
    '''
        DESCRIPTION: checks for a specific condition were printing must stop as no more data is present
        INPUT:  patient object
    '''

    if(patient_passed.get_weight() == 38 and patient_passed.get_age() == 10):
        patient_passed.set_stop_printing_feed_data(True)

def day_to_day_diagnosis_print(patient_list, patient_file__order):
    '''
        DESCRIPTION: prints day by day diagnosis of all patients
        INPUT: Patient list that holds end of day diagnosis and and patient list to match diagnosis with patient
    '''
    for day in range(1,6):
        print("Day " + str(day))
        for i in range(len(patient_list)):
            day_diagnosis = patient_list[i].get_week_diagnosis()
            print(str(patient_file__order[i]) + " = " + str(day_diagnosis[:day]))
        print("")


''' ---------- SORTING ------------'''

def partition(patient_list_tracker, list_to_sort, first_index_in_list, last_index_in_list): 

    i = (first_index_in_list - 1)         # index of smaller element 
    pivot = list_to_sort[last_index_in_list]     # pivot 
  
    for j in range(first_index_in_list , last_index_in_list): 
  
        # If current element is smaller than or 
        # equal to pivot 
        if (list_to_sort[j] <= pivot): 
            # print(str(list_to_sort[j]) + " pivot: " + str(pivot))
          
            # increment index of smaller element 
            i = i+1 

            patient_list_tracker[i],patient_list_tracker[j] = patient_list_tracker[j],patient_list_tracker[i] 
            list_to_sort[i],list_to_sort[j] = list_to_sort[j],list_to_sort[i] 
  
    patient_list_tracker[i+1],patient_list_tracker[last_index_in_list] = patient_list_tracker[last_index_in_list],patient_list_tracker[i+1] 
    list_to_sort[i+1],list_to_sort[last_index_in_list] = list_to_sort[last_index_in_list],list_to_sort[i+1] 
    
    return (i + 1) 
  
# Function to do Quick sort 
def quickSort(patient_list_tracker, list_to_sort, first_index_in_list, last_index_in_list): 
    if first_index_in_list < last_index_in_list: 
  
        # pi is partitioning index, arr[p] is now 
        # at right place 
        pi = partition(patient_list_tracker, list_to_sort, first_index_in_list, last_index_in_list) 
  
        # Separately sort elements before 
        # partition and after partition 
        quickSort(patient_list_tracker, list_to_sort, first_index_in_list, pi - 1) 
        quickSort(patient_list_tracker, list_to_sort, pi + 1, last_index_in_list) 

def transform_list_to_sort(change_list):
    '''
        DESCRIPTION: takes list to sort and changes the values to make it easier to sort
        INPUT:  takes list to be sorted
    '''
    for i in range(len(change_list)):
        for day in range(5):
            if(change_list[i][day] == "NONE"):
                change_list[i][day] = 0
            
            elif(change_list[i][day] == "Feeding Stopped"):
                change_list[i][day] = 1
            
            elif(change_list[i][day] == "Refer to Dietician"):
                change_list[i][day] = 2
    return change_list

def revert_list_to_original_state(change_list):
    '''
        DESCRIPTION: list sorted is then reverted back to it's original state 
        INPUT: list sorted of end day diagnosis
    '''
    for i in range(len(change_list)):
        for day in range(5):
            if(change_list[i][day] == 0):
                change_list[i][day] = "NONE"
            elif(change_list[i][day] == 1):
                change_list[i][day] = "Feeding Stopped"
            elif(change_list[i][day] == 2):
                change_list[i][day] = "Refer to Dietician"
    return change_list

def ammend_sort(array_to_sort, sort_patient_list):

    '''
        DESCRIPTION: ammends the sorted list
        INPUT:  list to the sorted and list of patient to match the diagnosis to 
    '''
    size = len(array_to_sort) - 1 
    for i in range(size, -1, -1):
        if(i - 1 < 0):
            i = 0
            break

        if(array_to_sort[i][3] < array_to_sort[i-1][3]):
            swap_up = array_to_sort[i]
            swap_down = array_to_sort[i-1]
            array_to_sort[i] = swap_down
            array_to_sort[i-1] = swap_up

            swap_up_patient = sort_patient_list[i]
            swap_down_patient = sort_patient_list[i-1]
            sort_patient_list[i] = swap_down_patient
            sort_patient_list[i-1] = swap_up_patient

def complete_sort(patient_lists, array_to_sort):

    '''
        DESCRIPTION: handles all the sorting of the list calling all the necessary functions
        INPUT: list to the sorted and list of patient to match the diagnosis to 
    '''
    size_of_list = len(array_to_sort)

    quickSort(patient_lists, transform_list_to_sort(array_to_sort), 0, size_of_list - 1)

    ammend_sort(array_to_sort, patient_lists)

    revert_list_to_original_state(array_to_sort)
    print("------ Patient's Sorted by Progress Made ------\n")
    for i in range(len(array_to_sort)):
       print(str(patient_lists[i]) + " = " + str(array_to_sort[i]))
    

if __name__ == "__main__":

    patient_objects = [Patient() for i in range(len(CSV_PATHS))]
    order_patient_files = ["Patient A1", "Patient A2", "Patient A3", "Patient B1", "Patient B2", "Patient B3", "Patient B4", "Patient B5", "Patient B6", "Patient B7"]
    end_day_diagnosis = list()

    # loop takes all the patients objects with csv to populate data
    for i in range(len(CSV_PATHS)):
        start_of_patient_diagnosis(CSV_PATHS[i], patient_objects[i])
        end_day_diagnosis.append(patient_objects[i].get_week_diagnosis())

    day_to_day_diagnosis_print(patient_objects, order_patient_files) # prints all patiets end of day diagnosis sequencially as required
    complete_sort(order_patient_files, end_day_diagnosis)    
    
    
    
