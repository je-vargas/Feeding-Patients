import csv
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
                # print(patient_object.get_weight())
            else: # gets all the hourly current_rows
                if(current_row[DAY_PATIENT]== "1" and "00:00" in current_row[TIME_RISK]): #gets only days 1 as this holds patient feeding info
                    patient_object.set_feed(clean_up_feed(current_row)) # us this to set the feeding attribute in patient object
                    # print("feed after cleaning " + str(patient_object.get_feed()))
                    patient_object.set_target_grv()
                    current_row[FEED_AGE] = patient_object.get_feed()
                    patient_object.set_diagnosis(current_row[ISSUES_WEIGHT])
                    # print(patient_object.get_target_grv())

                hourly_data.append(current_row) #adding all current_row to array 
    
    patient_object.set_data(hourly_data) #save hourly data inside the object

def low_risk_blanks(patient_passed):
    '''
        DESCRIPTION: Follows low risk patient flowchart, populating patient feeds 
    '''
    # ------------- function variables declaration
    day_data = patient_passed.get_data() #returns the array with hourly data
    target_grv = int(patient_passed.get_target_grv()) #use target_grv as a measure to either increase feed or stop feeding
    
    feeding_stopped = 0
    grv_is_over_target = False
    refer_to_dietician = False
    # -------------

    # ------------- Loop over passed patient data
    for current_row in day_data:

        hour = int(current_row[TIME_RISK][:2]) # this returns hour in format 0-23
        current_grv = current_grv_integer_cleaned(current_row) # returns the current grv as an integer
        
        if(hour % 2 == 0 and not refer_to_dietician): # !!!!!!!!! this needs to change to finish populating until there is no more grv to check

            # ------------- handles dietician referal
            if (feeding_stopped == 2):
                refer_to_dietician = True
                # print(current_row)

            if (refer_to_dietician):
                current_row[FEED_AGE] = None
                current_row[ISSUES_WEIGHT] = "Refer to Dietician "
                grv_is_over_target = False
            elif(grv_is_over_target and current_grv > target_grv): #check used to stop adding feeds when patient has been refered to dietician
                feeding_stopped += 1
                current_row[FEED_AGE] = "No Feeding"
                current_row[ISSUES_WEIGHT] = "Feeding Stopped"
            else:
                update_feeding_diagnosis(current_row, patient_passed)
            # -------------
            

            # check every four hours and adjust GRV
            if (hour % 4 == 0 and not grv_is_over_target ):

                patient_passed.set_current_grv(current_row[GRV]) # current grv is set as each row is read
                            
                if(patient_passed.get_weight() < 40 ): #patient weight is under 40

                    if(current_grv <= target_grv and current_row[GRV] != ""):  #current target is less so increment feed and the grv is present
                     
                        set_feed(patient_passed, current_row)
                    
                    elif(current_grv > target_grv and current_row[GRV] != "" and not refer_to_dietician): # current target is more that target stop feeding check every 2 hours now
                
                        grv_is_over_target = True
                        feeding_stopped += 1
                        current_row[FEED_AGE] = "No Feeding"
                        current_row[ISSUES_WEIGHT] = "Feeding Stopped"
                        # print(current_row)
                
                else: #patient weight is over 40
                    if(current_grv < target_grv and current_grv != ""): #less so increment feed
                        
                        if(patient_passed.get_feed() == 20):
                            patient_passed.set_feed(30)
                            update_feeding_diagnosis(current_row, patient_passed)
                            # print(current_row)
                        else:
                            patient_passed.set_feed_increment()
                            update_feeding_diagnosis(current_row, patient_passed)

                    elif(current_grv > target_grv and current_row[GRV] != "" and not refer_to_dietician):# current target is more that target stop feeding
                        grv_is_over_target = True
                        feeding_stopped += 1
                        current_row[FEED_AGE] = "No Feeding"
                        current_row[ISSUES_WEIGHT] = "Feeding Stopped"
                    
                        
    end_of_day_diagnosis(day_data, patient_passed) # this needs to be fixed

    patient_passed.set_data(day_data)    

def end_of_day_diagnosis(day_data, current_paitient):
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

def update_feeding_diagnosis(current_row, patient_passed):
    '''
        DESCRITPTION: this function is updating the feed and issue from the patient which is the most upto date information
                        as each row is read 
                        
    '''
    current_row[FEED_AGE] = patient_passed.get_feed()
    current_row[ISSUES_WEIGHT] = patient_passed.get_diagnosis()

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

def clean_up_feed(feed_current_row):
    feed_joined = ''.join(filter(lambda i: i.isdigit(), feed_current_row[FEED_AGE]))
    feed_length = len(feed_joined) - 1
    feed_to_return = feed_joined[0:feed_length]
    return int(feed_to_return)
        
def current_grv_integer_cleaned(row):
    current_grv = 0
    if (row[GRV] != "GRV" and row[GRV] != ""):
            current_grv = int(float(row[GRV]))
    return current_grv

def set_feed(patient_passed, row_passed):
    if(patient_passed.get_feed() == 5 ):
        patient_passed.set_feed(10)
        update_feeding_diagnosis(row_passed, patient_passed)
    else:
        patient_passed.set_feed_increment()
        update_feeding_diagnosis(row_passed, patient_passed)

    # if(patient_passed.get_feed() == 5 ):
    #     patient_passed.set_feed(10)
    #     update_feeding_diagnosis(current_row, patient_passed)
    # else:
    #     patient_passed.set_feed_increment()
    #     update_feeding_diagnosis(current_row, patient_passed)

if __name__ == "__main__":

    # current low risk under 40 (b1 b3 b5 b7)
    
    path  = "/Users/juanestebanvargassalamanca/Desktop/Desktop – Juan’s MacBook Pro/UNI/Computer_Science /2nd_Year/Algorithm_DataStructures_(Python) /ASSIGNMENT_2/patients_csv/PATIENT DATA - PATIENT B1.csv"
    # path = "/Users/juanestebanvargassalamanca/Desktop/Desktop – Juan’s MacBook Pro/UNI/Computer_Science /2nd_Year/Algorithm_DataStructures_(Python) /ASSIGNMENT_2/patients_csv/PATIENT DATA - PATIENT B3.csv"
    # path = "/Users/juanestebanvargassalamanca/Desktop/Desktop – Juan’s MacBook Pro/UNI/Computer_Science /2nd_Year/Algorithm_DataStructures_(Python) /ASSIGNMENT_2/patients_csv/PATIENT DATA - PATIENT B5.csv"
    # path = "/Users/juanestebanvargassalamanca/Desktop/Desktop – Juan’s MacBook Pro/UNI/Computer_Science /2nd_Year/Algorithm_DataStructures_(Python) /ASSIGNMENT_2/patients_csv/PATIENT DATA - PATIENT B7.csv"
    
    patient= Patient()
    read_file(path, patient)
    low_risk_blanks(patient)
    
    print("------------- PATIENT B1 -------------")
    print(patient)
    print("\n------------- HOURLY DATA:")
    print(patient.print_hourly_data())