# FILE: src/neurotransanalytics/data_adapter/models/session.py

class TestSession:
    def __init__(
        self,
        session_id,
        subject_id,
        test_type,
        session_datetime=None
    ):
        self.session_id = session_id
        self.subject_id = subject_id
        self.test_type = test_type
        self.session_datetime = session_datetime
