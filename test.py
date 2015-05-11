from lectio import get_periods

school_id = "248"
student_id = "9232029391"
week = 6
year = 2015

periods = get_periods(school_id, student_id, week, year)

for period in periods:
    print(period)
