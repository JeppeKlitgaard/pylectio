from lectio.session import Session
from getpass import getpass

s = Session("248")

username = "jepp3467"
password = getpass()

r = s.auth(username, password)
