#!/usr/bin/env python

from distutils.core import setup
from lectio import __version__ as version

<<<<<<< HEAD
setup(name="lectio",
=======
setup(name="Lectio",
>>>>>>> 85672063c1c4a7bedaccd6eb21430dd0dad94a2d
      version=".".join([str(x) for x in version]),
      description="Quick'n'dirty Lectio timetable scraper.",
      author="Jeppe Klitgaard",
      author_email="jeppe@dapj.dk",
      url="https://github.com/dkkline/pylectio",
      packages=["lectio"])
