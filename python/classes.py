# GLOBALS USED 
DAY_PATIENT = 0
TIME_RISK= 1
FEED_AGE = 2 
GRV = 3
ISSUES_WEIGHT= 4

class Patient:

    def __init__(self):
        self.__age = 0
        self.__weight = 0
        self.__risk = None
        self.__diagosis = None
        self.__current_grv = None
        self.__target_grv = None
        self.__data = list()
        self.__week_diagnosis = list()

        # --- LR ---
        self.__feed = None
        self.__feed_stop_counter = 0
        self.__feed_increment_bool= False
        self.__feed_stop_bool= False
        self.__dietician_referal= False
        self.__reset_counter = False

        # --- HR --
        self.__change_feed_bool = False
        self.__low_risk_transfer_bool = False

        # -- NO MORE DATA --
        self.__stop_printing_feed_data = False

    # ------- SETTER 
    def set_age(self, row):
        self.__age = row[0]
    
    def set_weight(self, row):
        self.__weight = row[1]
    
    def set_risk(self, row):
        self.__risk = row[2]
        
    def set_target_grv(self):
        if(self.__risk == "LR"):
            if(self.__weight > 40):
                self.__target_grv = self.__weight * 5
            else:
                self.__target_grv = self.__weight * self.__feed
        else:
            self.__target_grv = self.__weight * 5

    def set_current_grv(self, current_grv):
        self.__current_grv = current_grv

    def set_daily_diagnosis(self, end_of_day_diagnosis):
       self.__diagosis.append(end_of_day_diagnosis)

    def set_data(self, data_array):
        self.__data = data_array

    def set_diagnosis(self, diagnosis):
        self.__issues = diagnosis
    
    def set_week_diagnosis(self, end_day_diagnosis):
        self.__week_diagnosis = end_day_diagnosis

    ''' -------- LOW RISK SETTER METHODS --------'''
    def set_feed(self, feed_passed):
        '''
            description: function in intialising variable feed 
            --> to change feed use feed_increment
        '''
        self.__feed = feed_passed

        if(self.__weight > 40):
            if(self.__feed < 20):
                self.__feed = 20

    def set_feed_increment_boolean(self, true_false):
        '''
            description: 
        '''
        self.__feed_increment_bool = true_false

    def set_feed_stopped_boolean(self, true_false):
        '''
            description: 
        '''
        self.__feed_stop_bool = true_false

    def set_feed_stop_counter(self, number_of_pauses=0):
        '''
            description: keeps track of number of feedings stopped when grv is over target 
                        - incrementing to refer to dietician
        '''
        self.__feed_stop_counter += 1
        
        if(self.__feed_stop_counter == 3):
            self.__dietician_referal = True
        
        if(self.__reset_counter):
            self.__feed_stop_counter = number_of_pauses

        if(self.__feed_stop_counter > 3):
            print("feed counter has not been reset")

    def set_dietician_referal_bool(self, true_false):
        '''
            description: 
        '''
        self.__dietician_referal = true_false

    def set_reset_counter_bool(self, true_false):
        '''
            description: set counter boolean value
        '''
        self.__reset_counter = true_false
        
    ''' -------- HIGH RISK SETTER METHODS --------'''
    def set_change_feed_bool(self, true_false):
        self.__change_feed_bool = true_false

    def set_low_risk_transfer_bool(self, true_false):
        self.__low_risk_transfer_bool = true_false

    ''' -------- NO MORE DATA STOP PRINTING GETTER--------'''
    def set_stop_printing_feed_data(self, true_false):
        self.__stop_printing_feed_data = true_false
    
    # ------- GETTER
    def get_week_diagnosis(self):
        for day in range(5):
            if(day == ""):
                self.__week_diagnosis.append("None")
        return self.__week_diagnosis

    def get_diagnosis(self):
        return self.__issues
    
    def get_daily_assessment(self):
        return self.__diagosis

    def get_target_grv(self):
        return self.__target_grv

    def get_current_grv(self):
        return self.__current_grv
    
    def get_risk(self):
        return self.__risk

    def get_data(self):
        return self.__data

    def get_weight(self):
        return self.__weight

    def print_hourly_data(self):
        for row in self.__data:
            print(row)

    def get_age(self):
        return self.__age
    ''' -------- LOW RISK GETTER METHODS --------'''
    def get_feed(self):
        return self.__feed

    def get_feed_stopped(self):
        return self.__feed_stop_counter

    def get_feed_increment_boolean(self):
        '''
            description: 
        '''
        return self.__feed_increment_bool

    def get_feed_stopped_boolean(self):
        '''
            description: becomes true when feeding stops
        '''
        return self.__feed_stop_bool

    def get_dietician_referal_bool(self):
        '''
            description: 
        '''
        return self.__dietician_referal

    def get_reset_counter_bool(self):
        '''
            description: 
        '''
        return self.__reset_counter

    ''' -------- HIGH RISK GETTER METHODS --------'''
    def get_change_feed_bool(self):
        return self.__change_feed_bool

    def get_low_risk_transfer_bool(self):
        return self.__low_risk_transfer_bool

    ''' -------- NO MORE DATA STOP PRINTING GETTER--------'''
    def get_stop_printing_feed_data(self):
        return self.__stop_printing_feed_data

    def __str__(self):
        return "\n------------- Patient's Info:\n" + "age: " + str(self.__age) + "\nweight: " + str(self.__weight) + "\nrisk: " + str(self.__risk) + "\ntarget grv: " + str(self.__target_grv) + "\ncurrent grv: " + str(self.__current_grv) + "\ncurrent feed: " + str(self.__feed) +  "\nweek diagnosis: " + str(self.get_week_diagnosis()) + "\n"



    

