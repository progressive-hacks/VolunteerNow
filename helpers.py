from datetime import datetime
from datetime import timedelta

def _dow(m, d, y):
    # offset for each month
    t = (0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4)
    
    # check if the year is a leap year
    y -= m < 3
    
    # find the day of week
    return (y + y // 4 - y // 100 + y // 400 + t[m - 1] + d) % 7


def get_this_week():
    offset = _dow(
        datetime.today().month, 
        datetime.today().day,
        datetime.today().year
    )

    dates = []

    t = datetime.today() - timedelta(days = offset)
    for _ in range(7):
        dates.append((t.month, t.day))
        t += timedelta(days = 1) 

    return dates

def create_datetime(string):
    return datetime.strptime(string, '%Y/%m/%d/%H/%M')


if __name__ == '__main__':
    print(get_this_week())
