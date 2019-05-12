from datetime import datetime, date, timedelta


def hour_generator(start, end, step=10):
    while start < end:
        yield start
        start = start + timedelta(minutes=step)


def create_hour(hour, date=None):
    if not date:
        return datetime.strptime(hour, '%H:%M')
    h = datetime.strptime(hour, '%H:%M')
    return datetime(year=date.year, month=date.month, day=date.day, hour=h.hour, minute=h.minute)


def right_intervals(hours):
    duration = 40
    #bar = Barber.query.get(2)
    #hours = bar.get_hours(date.today(), duration)
    intervals = int(duration / 10)
    for i in range(len(hours)):
        works = True
        for j in range(intervals):
            if hours[i + j] != hours[i] + timedelta(minutes=10 * j):
                works = False
            break
        if works:
            print(hours[i])
