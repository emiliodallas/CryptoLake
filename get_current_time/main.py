from datetime import datetime

def get_current_time():
   current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
   return current_datetime