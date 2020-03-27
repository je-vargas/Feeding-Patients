# GLOBALS USED 
DAY_PATIENT = 0
TIME_RISK= 1
FEED_AGE = 2 
GRV = 3
ISSUES_WEIGHT= 4
MAX_FEEDING_OVER_40 = "250"

class Patient:

    def __init__(self):
        self.__age = 0
        self.__weight = 0
        self.__risk = None
        self.__feed = None
        self.__diagosis = None
        self.__current_grv = None
        self.__target_grv = None
        self.__data = list()
        self.__week_diagnosis = list()
        

    # ------- SETTER 
    def set_age(self, row):
        self.__age = row[0]
    def set_weight(self, row):
        self.__weight = row[1]
    def set_risk(self, row):
        self.__risk = row[2]

    def set_feed(self, feed_passed):
        '''
            description: function in intialising variable feed 
            --> to change feed use feed_increment
        '''
        self.__feed = feed_passed

    def set_feed_increment(self):
        if(self.__risk == "LR"):
            if(self.__weight < 40):
                self.__feed = 10
            else:
                self.__feed = 30
            
        else: # this means it's a High Risk patient
            pass

    def set_target_grv(self):
        self.__target_grv = self.__weight * self.__feed

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

    def print_hourly_data(self):
        for row in self.__data:
            print(str(row))

    def get_feed(self):
        return self.__feed

    def get_weight(self):
        return self.__weight

    def __str__(self):
        return "Patient's Info\n" + "current feed: " + str(self.__feed) + ", target grv: " + str(self.__target_grv) + ", current grv: " + str(self.__current_grv) + str(self.print_hourly_data())






    

