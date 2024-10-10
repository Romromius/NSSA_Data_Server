import time

from flask import session

from data_base.db_session import create_session, global_init
from data_base.__all_models import *

global_init('test.sqlite')
session = create_session()

user = session.get(CCPlayer, 1)
user.add_coins(1000)
print(user.get_coins())
user.increase_income()
print(user.get_coins())
time.sleep(3)
print(user.get_coins())

