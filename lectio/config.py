"""
Contains configuration values used by pylectio.
"""

import pytz

LECTIO_URL = (u"https://www.lectio.dk/lectio/{SCHOOL_ID}/SkemaNy.aspx"
              u"?type=elev&elevid={STUDENT_ID}&week={WEEK_ID}")
DEFAULT_TZ = pytz.timezone("Europe/Copenhagen")
