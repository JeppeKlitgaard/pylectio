# pylectio
Super simple quick'n'dirty Lectio timetable parser
Note that this is a very quick and hacky project. If you're going to use it, expect to read through the (ugly) source code.

Probably only works on Python 3.4.

Usage
===
First you need to find the school in question's `school_id` and the student in question's `student_id`. This is done by inspecting the URL of the students timetable. It will look something like this: `https://www.lectio.dk/lectio/{school_id}/SkemaNy.aspx?type=elev&elevid={student_id}`.

Next up, you need to figure out what year and week you'd like to retrieve.

Finally you pass this information to `get_periods(school_id, student_id, week, year)` which should return a list of `Period` objects.

Period object
---
A `Period` object has the following attributes:
* `status`
* `starttime` - datetime object
* `endtime` - datetime object
* `topic`
* `groups`
* `teachers`
* `rooms`
* `resources`
* `links`
* `homework`
* `note`

Contact
===
Email: jeppe@dapj.dk
