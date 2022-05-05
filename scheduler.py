#scheduler.py
from moment import utilities as mu

class chart():
    def __init__(self):
        self.mat = []
class task:
    types = ["Homework", "Task", "Event", "Exam", "Reminder"]
    def __init__(self):
        self.type = None
        self.start_time = None
        self.created = dateLib.getNow()
        self.end_time = None
        self.title = None
        self.description = None
        self.completion_percentage = 0.0
        self.tte = 100000000000
    def fuzzy_init(self, numbers, days, context):
        potential_hours = []
        potential_days = []
        potential_days = days
        potential_minutes = []
        for x in range(0, len(numbers)):
            if(int(numbers[x])>12):
                potential_minutes.append(numbers[x])
                potential_days.append(numbers[x])

    def to_dict(self):
        data = {}
        data['type']=self.type
        data['start_time']=self.start_time
        data['created']=self.created
        data['end_time']=self.end_time
        data['title']=self.title
        data['description']=self.description
        data['completion_percentage']=self.completion_percentage
        data['tte']=self.tte
        return(data)
    def from_dict(self, data):
        self.type=data['type']
        self.start_time=data['start_time']
        self.created=data['created']
        self.end_time=data['end_time']
        self.title=data['title']
        self.description=data['description']
        self.completion_percentage=data['completion_percentage']
        self.tte=data['tte']
    #def
q = task()
