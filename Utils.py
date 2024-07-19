data = {
    'khan academy':(5),
    'reading':(2),
    'break':(15),
    'time':('1:00pm','5:00pm')
    
}

def day_planner(data):
    store_activity = set()
    TIME_SPAN = military_time(data['time']) 
        
def military_time(time):
    result = []
    REMOVE_LENGTH = -2
    TIME = time[0][:REMOVE_LENGTH]
    TIME2 = time[1][:REMOVE_LENGTH]
    if time[0].count('pm') == 1:
       times_split = TIME.split(':')
       
       result.append(time[0][:REMOVE_LENGTH])
    elif time[0].count('am') == 1:
        result.append(time[0][:REMOVE_LENGTH])
    return 0
    
        
        
        

if __name__ == "__main__":
    day_planner(data)

