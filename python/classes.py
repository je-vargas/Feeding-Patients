# GLOBALS USED 
DAY = 0
PATIENT = 0
TIME = 1
FEED = 2 
GRV = 3
ISSUES = 4

class Patient:
    
    def __init__(self, row_passed):
        self.__risk = row_passed[1]
        self.__age = row_passed[2]
        self.__current_grv = row_passed[3]
        self.__weight = row_passed[4]
        self.__target_grv = None
        self.__data = list()
        self.__diagosis = list()

    # ------- SETTER 
    def set_target_grv(self, target_grv):
        self.__target_grv = target_grv

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





    

