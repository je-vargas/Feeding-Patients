# GLOBALS USED 
DAY_PATIENT = 0
TIME_RISK= 1
FEED_AGE = 2 
GRV = 3
ISSUES_WEIGHT= 4

class Patient:
    
    def __init__(self, row_passed):
        self.__age = row_passed[0]
        self.__weight = row_passed[1]
        self.__risk = row_passed[2]
        self.__feed = None
        self.__current_grv = None
        self.__target_grv = None
        self.__data = list()
        self.__diagosis = list()

    # ------- SETTER 
    def set_feed(self, feed_passed):
        '''
            description: function in intialising variable feed 
            --> to change feed use feed_increment
        '''
        self.__feed = feed_passed

    def set_feed_increment(self):
        if(self.__risk == "LR"):
            if (self.__feed == 5):
                self.__feed = 10

            
        else:
            pass
        # high risk

    def set_target_grv(self):
        self.__target_grv = self.__weight * self.__feed

    def set_current_grv(self, current_grv):
        self.__current_grv = current_grv

    def set_daily_diagnosis(self, end_of_day_diagnosis):
       self.__diagosis.append(end_of_day_diagnosis)

    def set_data(self, data_array):
        self.__data = data_array
        
    def set_risk(self, risk):
        self.__risk = risk

    
        
    # ------- GETTER
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

    def get_feed(self):
        return self.__feed

    def get_weight(self):
        return self.__weight






    

