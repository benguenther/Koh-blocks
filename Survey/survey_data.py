import csv, sys, string

class SurveyData:
    def __init__(self, id):
        self.__id = id
        self.__data = self.load_data()
        self.__data["calc_hand"] = self.calculated_handedness()
        self.__data["gen"] = self.proccess_gender_response()

    def load_data(self):
        try:
            with open(f"info_{self.__id}.csv", mode = "r", newline = '') as survey:
                reader = csv.DictReader(survey)
                data = next(reader)
                survey.close()
                return data
        except FileNotFoundError:
            #print()
            sys.exit(f"survey data for participant# {self.__id} not found")

    
    def proccess_gender_response(self):
        if self.__data["gender"].isnull():
            self.__data["gender"] = self.__data["sex"].str.lower()
        
        if self.__data["gender"].lower().strip() in ["man", "male", "boy", "guy"]:
            return "man"
        elif self.__data["gender"].lower().strip() in ["woman", "female", "girl", "gal", "lady"]:
            return "woman"
        elif self.__data["gender"].lower().strip() == "prefer not to say":
            return "null"
        else:
            return "".join([letter.lower() for letter in self.__data["gender"] if letter in string.ascii_letters])
        
    
    def calculated_handedness(self):
        return (
            int(self.__data["q1"]) + int(self.__data["q2"]) + int(self.__data["q3"]) + int(self.__data["q4"]) + int(self.__data["q5"]) + int(self.__data["q6"]) + 
            int(self.__data["q7"]) + int(self.__data["q8"]) + int(self.__data["q9"]) + int(self.__data["q10"]) + int(self.__data["q11"]) + int(self.__data["q12"])
            )
        
    @property
    def data(self):
        return self.__data
    

if __name__ in "__main__":
    survey_data = SurveyData("64387")
    print(survey_data.data)





