# SSRF 
Impact: 
- make the server do request for us.

possible attack: 
- access local infrastructure
- access third party application in order to leak credentials
- RCE in some cases

 
# SSRF access admin panel of the application

If the application try to communicate with a specific API , try to replace this address with 

```
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
...
```


In some cases the admin panel can be accessible only from localhost , in this context we can use a vulnerability like SSRF in order to access it.
<br>
worst case: access as an admin for user from localhost

(sometimes the application can use an other port than 80 or 443 , in this case you need to bruteforce it)

# SSRF access other application :

There are cases where a database like redis or MongoDb is present on different port , different ip address than "127.0.0.1"<br>
In this case you need to bruteforce the following private ip address.

- 10.0.0.0 — 10.255.255.255; 
- 172.16.0.0 — 172.31.255.255; 
- 192.168.0.0 — 192.168.255.255

Once you found the ip , you can bruteforce the port number or use well-known port
 

# weak protection against SSRF: 

if the server or the reverse proxy blocks the following payload: localhost, 127.0.0.1, ..<br>
you can try to bypass with these payloads : 


    ```
    2130706433 which is 127.0.0.1 in decimal
    127.0.0.1
    0177.0.0.1
    0x7f.0.0.1
    127.0.1
    127.1
    2130706433
    017700000001
    0x7f000001
    ```

 
# orange tsai make SSRF great again :


play with the strange  behaviour of url parser.

https://www.blackhat.com/docs/us-17/thursday/us-17-Tsai-A-New-Era-Of-SSRF-Exploiting-URL-Parser-In-Trending-Programming-Languages.pdf

# ssrf via open redirect 

If the application is using a whitelist based approach, and you find a link using a redirect you can use it to exploit the ssrf


# other ressources on ssrf: 

https://www.dailysecurity.fr/server-side-request-forgery/ (in french)