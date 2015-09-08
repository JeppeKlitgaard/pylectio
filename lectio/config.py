"""
Contains configuration values used by pylectio.
"""

import pytz

DEFAULT_TZ = pytz.timezone("Europe/Copenhagen")

BASE_URL = u"https://www.lectio.dk/lectio/"

# Session authentication constants
VIEW_STATEX = ("igAAAGlpZQotNzc3Mjg0NjU3aWwCawCBbAJoaWRsAmcCaWwCawFlA29mZmwCZw"
               "NpZGwCZwVpZGwCZwVpZGwGgWlsAmsCZRNTaWxrZWJvcmcgR3ltbmFzaXVtZGcF"
               "aWRsAoFpZGwCgWlsAmsDZQI1MGRnB2lkbAKBaWRsAoFpamlsAmsEcGRkZGRkBQ"
               "AAABNWYWxpZGF0ZVJlcXVlc3RNb2RlDGF1dG9jb21wbGV0ZQlpbm5lcmh0bWwJ"
               "bWF4bGVuZ3RoB0NoZWNrZWQAQ7qEXX4YWB6lvoORqK0bTe3OSHA=")

EVENTVALIDATION = ("zbZWcFhVBVWLCO5zNUuI2PsDDTTPi/fDOgr5LlIPP5+vaoQWV/XhZWruNb"
                   "yoqOsT2KQ8iSaFNAdaWkYkmeQWVNO249jAesebDvHhP+otIz6Mxzl9WHk4"
                   "99pw99GsAPWFq/YKI4kE4+QVVjG96bF90POwmkY3UUcpgvElhP9RNN5HIx"
                   "A065DD4q9vZ5JLb62cewnzhhnkBbnzrKrX68yXt5xSYyzRRflUs+18qdcT"
                   "njDztyNaWc5EihgQPIn+5LzmW5d9xQZlU6hQc7iEiW89zxqXCrOhGBSJnn"
                   "YRhWGkMGnvLoJHQRZ3jl+oA2utm5iYq66AzBbqBYR82MBhXbxHu3Hhk4NV"
                   "bLnhad5lf3cnPtXcDmMJdNBigXH8eAPFoCb5sR7inOMjs7mdJAGLL0Hk2h"
                   "z0swGb3quXC8HWOog3ivHYXKY0yOUJrpWKbhugUtOYXyOEfkzAkZ+lOLCI"
                   "1qxHww==")

DECIMAL_SEPARATOR = ","
