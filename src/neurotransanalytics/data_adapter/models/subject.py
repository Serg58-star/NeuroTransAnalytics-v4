# FILE: src/neurotransanalytics/data_adapter/models/subject.py

class Subject:
    def __init__(self, subject_id, sex=None, birth_date=None):
        self.subject_id = subject_id
        self.sex = sex
        self.birth_date = birth_date
