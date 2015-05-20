from lectio.session import Session

school_id = "248"
student_id = "9232029391"
week = 6
year = 2015

s = Session(school_id)

periods = s.get_periods(week, year, student_id=student_id)

for period in periods:
    print(period)
