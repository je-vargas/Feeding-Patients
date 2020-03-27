import csv
from classes import *

def read_file (file_path, patient_object):
    '''
        returns : the object where all data read from csv is saved
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
    day_data = patient_passed.get_data() #returns the array with hourly data
    feeding_stopped = 0
    grv_is_over = False
    target_grv = str(patient_passed.get_target_grv()) #use target_grv as a measure to either increase feed or stop feeding
    terminate = False
    
    for current_row in day_data:

        hour = int(current_row[TIME_RISK][:2]) # this returns hour in format 0-23

        # feed every 2 hours
        if(hour % 2 == 0 and not terminate): # here we are feeding every 2 hours as per flowchart

            if (feeding_stopped == 2):
                # print(current_row)
                terminate = True

            if (terminate):
                current_row[FEED_AGE] = None
                current_row[ISSUES_WEIGHT] = "Refer to Dietician "
                grv_is_over = False
            elif(grv_is_over and current_row[GRV] > target_grv): #check used to stop adding feeds when patient has been refered to dietician
                feeding_stopped += 1
                current_row[FEED_AGE] = "No Feeding"
                current_row[ISSUES_WEIGHT] = "Feeding Stopped"
            else:
                update_feeding_diagnosis(current_row, patient_passed)

            

            # check every four hours and adjust GRV
            if (hour % 4 == 0 and not grv_is_over ):

                patient_passed.set_current_grv(current_row[GRV]) # set current grv from file
                            
                if(patient_passed.get_weight() < 40 ): #patient weight is under 40

                    #current target is less so increment feed and the grv is present
                    if(current_row[GRV] <= target_grv and current_row[GRV] != ""): 
                        
                        if(patient_passed.get_feed() == 5 ):
                            patient_passed.set_feed(10)
                            update_feeding_diagnosis(current_row, patient_passed)
                        else:
                            patient_passed.set_feed_increment()
                            update_feeding_diagnosis(current_row, patient_passed)
                    
                    elif(current_row[GRV] > target_grv and current_row[GRV] != "" and not terminate): 
                    # current target is more that target stop feeding check every 2 hours now

                        grv_is_over = True
                        feeding_stopped += 1
                        current_row[FEED_AGE] = "No Feeding"
                        current_row[ISSUES_WEIGHT] = "Feeding Stopped"
                        # print(current_row)
                
                else: #patient weight is over 40
                    if(current_row[GRV] < MAX_FEEDING_OVER_40 and current_row[GRV] != ""): #less so increment feed
                        
                        if(patient_passed.get_feed() == 20):
                            patient_passed.set_feed(30)
                            update_feeding_diagnosis(current_row, patient_passed)
                            # print(current_row)
                        else:
                            patient_passed.set_feed_increment()
                            update_feeding_diagnosis(current_row, patient_passed)

                    elif(current_row[GRV] > target_grv and current_row != ""):# current target is more that target stop feeding
                        grv_is_over = True
                        feeding_stopped += 1
                        current_row[FEED_AGE] = "No Feeding"
                        current_row[ISSUES_WEIGHT] = "Feeding Stopped"
                        
    end_of_day_diagnosis(day_data, patient_passed)
    patient_passed.set_data(day_data)


# def refer_to_dietician(grv_is_over, current_row, target_grv, feed):
    

def end_of_day_diagnosis(day_data, current_paitient):
    day = 0
    weekly_diagnosis = [None] * 5
    
    for current_row in day_data:
        if (current_row[DAY_PATIENT] != "" ):
            day = int(current_row[DAY_PATIENT])
            print(day)

        if("Refer" in current_row[ISSUES_WEIGHT]):
            weekly_diagnosis[day] = (current_row[ISSUES_WEIGHT])
        elif("Feeding" in current_row[ISSUES_WEIGHT] and "22" in current_row[TIME_RISK]):
            weekly_diagnosis[day] = (current_row[ISSUES_WEIGHT])
        elif("22" in current_row[TIME_RISK] and current_row[ISSUES_WEIGHT] != ""):
            weekly_diagnosis[day] = (current_row[ISSUES_WEIGHT])

    current_paitient.set_week_diagnosis(weekly_diagnosis)

def update_feeding_diagnosis(current_row, patient_passed):
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
        

if __name__ == "__main__":

    # current low risk ar (b1 b3 b5 b7)
    patient_b2 = Patient()
    # path = "/Users/juanestebanvargassalamanca/Desktop/Desktop – Juan’s MacBook Pro/UNI/Computer_Science /2nd_Year/Algorithm_DataStructures_(Python) /ASSIGNMENT_2/patients_csv/PATIENT DATA - PATIENT B3.csv"
    path  = "/Users/juanestebanvargassalamanca/Desktop/Desktop – Juan’s MacBook Pro/UNI/Computer_Science /2nd_Year/Algorithm_DataStructures_(Python) /ASSIGNMENT_2/patients_csv/PATIENT DATA - PATIENT B1.csv"
    read_file(path, patient_b2)
    print("\n\nAfter going through low risk function")
    low_risk_blanks(patient_b2)
    print(patient_b2.get_week_diagnosis())
    # print(patient_b2)
    

