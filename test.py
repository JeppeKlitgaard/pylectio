from lectio.session import Session

school_id = "163"
student_id = "16571398735"
week = 17
year = 2019

s = Session(school_id)

periods = s.get_periods(week, year, student_id=student_id)

for period in periods:
    print(period)
