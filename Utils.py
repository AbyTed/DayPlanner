data = {
    'khan academy':(60, 'h'),
    'reading':(60, 'e'),
    'break':(15),
    
}

def day_planner(data):
    easy = []
    medium = []
    hard = []
    for activity in data:
        difficulty = data[activity][1]
        PAYLOAD = (activity, data[activity][0]) 
        if difficulty == 'h':
            hard.append(PAYLOAD)
        elif difficulty == 'm':
            medium.append(PAYLOAD)
        else:
            easy.append(PAYLOAD)
    
def sort_activity(easy, medium, hard):
    
    pass

def assembler(result):
    pass

def display_schedule(schedule):
    pass
        
        
        
        
        
        

    
        
        
        

if __name__ == "__main__":
    day_planner(data)

