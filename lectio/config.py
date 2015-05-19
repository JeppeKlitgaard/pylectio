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

EVENTVALIDATION = ("NqCgrFleahJiNLJy+ZoeITtYXPBOrIlZbkBmxzdK2iM8ZsXaYo9U+ZYX2Z"
                   "2aVk3YQt5MN2YwIyQ6H/Dq2tXyLfV2B6rl8ACZE0GXZIFValsuI+aSxHnV"
                   "ha9386obrX776gSnN3yFTdqUpw090gvAEnQmb5AQj6CN7+HTO5PcMS3ROu"
                   "3qJQA+4G+HLeIGOy/ShHXl9+TCTijqBRTAseOm/c0R37BoFdZxM1QU9nGj"
                   "YTnwt3QEDnkx99nG0wmNw3LIgmyyIpVru6DH5rVWejugtIYCfK/sMcWdE1"
                   "VVbKmi0jEfBWEwWeqTAfD5MDntWpqlABfnXcDGJXHMzvfZ8L6iyZTQ36Oy"
                   "BBQ+Eb5qdyN1frKh4zgcfjJmVXj2xoXIsPg21xINNmKJ/TkO6VWvxlPxqJ"
                   "KRFSgkK9jpSPCjDAB1zmiv3Qf3z1HKHUqhPnF1zi0W")
