def day_planner(data):
    easy = []
    medium = []
    hard = []
    for activity, details in data.items():
        time, difficulty, break_time = details
        if activity == "break":
            continue
        if difficulty == "h":
            hard.append((activity, time, difficulty, break_time))
        elif difficulty == "m":
            medium.append((activity, time, difficulty, break_time))
        else:
            easy.append((activity, time, difficulty, break_time))
    
    return sort_activities(easy, medium, hard)

def sort_activities(easy, medium, hard):
    result = {}
    break_counter = 0
    
    for activities in [hard, medium, easy]:
        for activity in sorted(activities, reverse=True):
            result[activity[0]] = (activity[1], activity[2], activity[3])
            break_counter += 1
            result[f'break_{break_counter}'] = activity[3]
    
    return result


def display_schedule(schedule):
    SPACE = 8
    lines = []
    for items, value in schedule.items():
        length = len(items) + SPACE + len(str(value)) + len(' minutes')
        line = '-' * length + '\n'
        line += f'| {items} for {value} minutes|\n'
        line += '-' * length
        lines.append(line)
    return lines
