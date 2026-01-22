# FILE: src/neurotransanalytics/data_adapter/models/response_event.py

class ResponseEvent:
    def __init__(
        self,
        response_event_id,
        stimulus_event_id,
        rt_ms=None,
        validity_flag=None
    ):
        self.response_event_id = response_event_id
        self.stimulus_event_id = stimulus_event_id
        self.rt_ms = rt_ms
        self.validity_flag = validity_flag
