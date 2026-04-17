from datetime import datetime

def get_time():
    now = datetime.now()
    return now.minute, now.second