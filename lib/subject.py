import json

class Subject:
    def __init__(self, subject_id: str):
        self.subject_id = subject_id
        self.age = None
        self.height = None
        self.weight = None
        self.gender = None

    def load_data(self):
        with open("data/subject_data.json", "r") as f:
            data = json.load(f)

        self.age = data[self.subject_id]["Age"]
        self.height = data[self.subject_id]["Height"]
        self.weight = data[self.subject_id]["Weight"]
        self.gender = data[self.subject_id]["Gender"]
    
    def tokenize_age(self):
        if self.gender == "M":
            self.gender = 1
        elif self.gender == "F":
            self.gender = 0
        else:
            raise ValueError("Gender must be either M or F")
        