from datetime import datetime

def getCurrTerm():
    '''Select fall or spring depending on current date'''
    right_now = datetime.now()

    if datetime(right_now.year, 3, 1) < right_now < datetime(right_now.year, 10, 1):
        return 'Fall ' + right_now.year
    else :
        return f'Spring {right_now.year + 1}' if right_now.month > 9 else f'Spring {right_now.year}'

    raise Exception("something has gone terribly wrong")